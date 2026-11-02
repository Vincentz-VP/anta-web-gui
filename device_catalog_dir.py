"""Run ANTA NRFU using one JSON/YAML catalog file per device in a directory.

Typical layout: ``<catalogs_dir>/<inventory_hostname>.json`` — the same pattern
produced by Arista AVD ``anta_runner`` (``avd/anta/avd_catalogs/``).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
import uuid
from typing import Any, Callable

import pandas as pd
import yaml

DEFAULT_CATALOGS_DIR = os.environ.get(
    "ANTA_DEVICE_CATALOGS_DIR",
    os.environ.get("AVD_CATALOGS_DIR", ""),
)

RUN_MODE_DEVICE_CATALOG = "device_catalog_dir"
AVD_PROFILE_NAME = os.environ.get(
    "ANTA_CATALOG_PROFILE_NAME",
    "📐 AVD design catalogs",
)


def resolve_catalogs_dir(override: str | None = None) -> str:
    path = (override or "").strip() or DEFAULT_CATALOGS_DIR.strip()
    return path


def catalog_profile_description(catalogs_dir: str) -> str:
    custom = os.environ.get("ANTA_CATALOG_PROFILE_DESCRIPTION", "").strip()
    if custom:
        return custom
    source = os.environ.get("ANTA_CATALOG_SOURCE_LABEL", "AVD `anta_runner`").strip()
    return (
        f"Tests are loaded from **pre-generated per-device catalog files** in `{catalogs_dir}` "
        f"(one `<inventory_name>.json` per switch). Catalogs are produced by {source} from the "
        "fabric structured configuration—not from the Manage Tests checkboxes."
    )


def device_catalog_profile_entry() -> dict[str, Any] | None:
    """Built-in sidebar profile when a catalog directory is configured (e.g. avd-demo lab)."""
    catalogs_dir = resolve_catalogs_dir()
    if not catalogs_dir:
        return None
    return {
        "run_mode": RUN_MODE_DEVICE_CATALOG,
        "catalogs_dir": catalogs_dir,
        "description": catalog_profile_description(catalogs_dir),
        "keys": [],
        "cfg_rules": [],
        "builtin": True,
    }


def merge_device_catalog_profile(profiles: dict[str, Any]) -> dict[str, Any]:
    merged = dict(profiles)
    entry = device_catalog_profile_entry()
    if entry:
        merged[AVD_PROFILE_NAME] = entry
    elif AVD_PROFILE_NAME in merged and merged[AVD_PROFILE_NAME].get("builtin"):
        del merged[AVD_PROFILE_NAME]
    return merged


def list_device_catalogs(catalogs_dir: str) -> list[str]:
    if not catalogs_dir or not os.path.isdir(catalogs_dir):
        return []
    names: list[str] = []
    for entry in sorted(os.listdir(catalogs_dir)):
        if entry.endswith((".json", ".yaml", ".yml")):
            for suffix in (".json", ".yaml", ".yml"):
                if entry.endswith(suffix):
                    names.append(entry[: -len(suffix)])
                    break
    return names


def _catalog_format(path: str) -> str:
    if path.endswith(".json"):
        return "json"
    return "yaml"


def run_device_catalog_suite(
    *,
    catalogs_dir: str,
    inventory_payload: dict[str, Any],
    run_env: dict[str, str],
    nrfu_timeout: int,
    status_callback: Callable[[str], None] | None = None,
) -> tuple[list[dict[str, Any]], str]:
    """Execute ``anta nrfu json`` once per ``<device>.json`` (or .yaml) catalog."""
    device_names = list_device_catalogs(catalogs_dir)
    if not device_names:
        return [], ""

    inv_hosts = {
        h.get("name"): h
        for h in inventory_payload.get("anta_inventory", {}).get("hosts", [])
        if h.get("name")
    }

    merged: list[dict[str, Any]] = []
    logs: list[str] = []
    run_id = uuid.uuid4().hex[:8]

    for idx, device in enumerate(device_names, start=1):
        catalog_path = None
        for ext in (".json", ".yaml", ".yml"):
            candidate = os.path.join(catalogs_dir, f"{device}{ext}")
            if os.path.isfile(candidate):
                catalog_path = candidate
                break
        if not catalog_path:
            continue

        if device not in inv_hosts:
            merged.append(
                {
                    "name": device,
                    "categories": ["inventory"],
                    "description": "Catalog file has no matching inventory host name",
                    "result": "error",
                    "messages": [
                        f"No inventory host named '{device}'. Add it under Manage Inventory "
                        "(host **name** must match the catalog filename stem)."
                    ],
                }
            )
            continue

        out_file = f"temp_dcat_results_{run_id}_{device}.json"
        stdout_file = f"temp_dcat_stdout_{run_id}_{device}.log"
        stderr_file = f"temp_dcat_stderr_{run_id}_{device}.log"
        inv_file = f"temp_dcat_inventory_{run_id}_{device}.yml"

        try:
            with open(inv_file, "w", encoding="utf-8") as handle:
                yaml.safe_dump(inventory_payload, handle, sort_keys=False)

            cmd = [
                "anta",
                "nrfu",
                "--enable",
                "-i",
                inv_file,
                "-c",
                catalog_path,
                "--catalog-format",
                _catalog_format(catalog_path),
                "-d",
                device,
                "--ignore-status",
                "json",
                "-o",
                out_file,
            ]
            if status_callback:
                status_callback(f"Running catalog for **{device}** ({idx}/{len(device_names)})…")

            start = time.time()
            with open(stdout_file, "w", encoding="utf-8") as out_f, open(
                stderr_file, "w", encoding="utf-8"
            ) as err_f:
                proc = subprocess.Popen(cmd, stdout=out_f, stderr=err_f, text=True, env=run_env)
                timed_out = False
                while proc.poll() is None:
                    if time.time() - start > nrfu_timeout:
                        proc.kill()
                        proc.wait()
                        timed_out = True
                        break
                    time.sleep(0.5)
                if timed_out:
                    merged.append(
                        {
                            "name": device,
                            "categories": ["timeout"],
                            "description": "Device catalog run timed out",
                            "result": "error",
                            "messages": [f"Exceeded {nrfu_timeout}s for {device}."],
                        }
                    )
                    continue

            stdout = open(stdout_file, encoding="utf-8").read() if os.path.exists(stdout_file) else ""
            stderr = open(stderr_file, encoding="utf-8").read() if os.path.exists(stderr_file) else ""
            logs.append(stdout + "\n" + stderr)

            if os.path.exists(out_file):
                try:
                    with open(out_file, encoding="utf-8") as handle:
                        chunk = json.load(handle)
                    if isinstance(chunk, list):
                        merged.extend(chunk)
                    else:
                        merged.append(chunk)
                except (json.JSONDecodeError, OSError) as exc:
                    merged.append(
                        {
                            "name": device,
                            "categories": ["parse"],
                            "description": "Could not read ANTA JSON output",
                            "result": "error",
                            "messages": [str(exc)],
                        }
                    )
            else:
                merged.append(
                    {
                        "name": device,
                        "categories": ["anta"],
                        "description": "ANTA produced no JSON output",
                        "result": "error",
                        "messages": [stderr or stdout or "Unknown error"],
                    }
                )
        finally:
            for path in (out_file, inv_file, stdout_file, stderr_file):
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return merged, ansi_escape.sub("", "\n".join(logs))


def display_nrfu_results(st, results: list[dict[str, Any]], full_log: str = "") -> None:
    """Shared summary table for NRFU JSON result lists."""
    if not results:
        st.error("No test results returned.")
        if full_log:
            with st.expander("ANTA console output"):
                st.code(full_log, language=None)
        return

    df = pd.DataFrame(results)
    if "messages" in df.columns:
        df["messages"] = df["messages"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else x
        )

    total_tests = len(df)
    passed = len(df[df["result"] == "success"]) if "result" in df.columns else 0
    failed = len(df[df["result"] == "failure"]) if "result" in df.columns else 0
    error = len(df[df["result"] == "error"]) if "result" in df.columns else 0
    skipped = len(df[df["result"] == "skipped"]) if "result" in df.columns else 0

    st.subheader("📊 Test Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Tests", total_tests)
    col2.metric("✅ Passed", passed)
    col3.metric("❌ Failed", failed)
    col4.metric("🚨 Error / Exception", error)
    col5.metric("⏭️ Skipped", skipped)

    st.divider()
    display_cols = ["name", "categories", "description", "result", "messages"]
    df_display = df[[col for col in display_cols if col in df.columns]].copy()
    df_display["full_message"] = df_display["messages"]

    def color_result(val: str) -> str:
        if val == "success":
            return "color: #28a745; font-weight: bold"
        if val in ("failure", "error"):
            return "color: #dc3545; font-weight: bold"
        return "color: #ffc107; font-weight: bold"

    styled = df_display.drop(columns=["full_message"]).style.map(color_result, subset=["result"])
    st.dataframe(
        styled,
        use_container_width=True,
        column_config={"messages": st.column_config.TextColumn("messages", width="large")},
    )

    failed_df = df_display[df_display["result"].isin(["failure", "error"])].copy()
    if not failed_df.empty:
        st.divider()
        st.subheader("🔍 Failed Tests Details (Grouped by Switch)")
        failed_df["name"] = failed_df["name"].fillna("(unknown device)")
        for device_name, device_failures in failed_df.groupby("name"):
            count = len(device_failures)
            with st.expander(f"❌ **{device_name}** ({count} failed test{'s' if count != 1 else ''})"):
                for _, row in device_failures.iterrows():
                    st.markdown(f"**{row.get('description', 'Test')}** — `{row.get('result')}`")
                    st.code(row.get("full_message") or "", language=None)

    if full_log:
        with st.expander("ANTA console output"):
            st.code(full_log, language=None)


def inventory_catalog_warnings(
    catalog_devices: list[str], inventory_payload: dict[str, Any]
) -> list[str]:
    host_names = [
        h.get("name")
        for h in inventory_payload.get("anta_inventory", {}).get("hosts", [])
        if h.get("name")
    ]
    return [d for d in catalog_devices if d not in host_names]
