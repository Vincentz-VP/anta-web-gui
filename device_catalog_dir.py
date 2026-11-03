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
from concurrent.futures import ThreadPoolExecutor, as_completed
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


def _env_int(name: str, default: int, minimum: int = 1) -> int:
    try:
        return max(minimum, int(os.environ.get(name, default)))
    except (TypeError, ValueError):
        return default


def _error_row(device: str, category: str, description: str, message: str) -> dict[str, Any]:
    return {
        "name": device,
        "categories": [category],
        "description": description,
        "result": "error",
        "messages": [message],
    }


def _read_text(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def _run_one_device(
    *,
    device: str,
    catalog_path: str,
    inventory_payload: dict[str, Any],
    run_env: dict[str, str],
    run_id: str,
    timeout: int,
) -> tuple[list[dict[str, Any]], str]:
    """Run ``anta nrfu`` for a single device catalog. Returns (result rows, console log)."""
    out_file = f"temp_dcat_results_{run_id}_{device}.json"
    stdout_file = f"temp_dcat_stdout_{run_id}_{device}.log"
    stderr_file = f"temp_dcat_stderr_{run_id}_{device}.log"
    inv_file = f"temp_dcat_inventory_{run_id}_{device}.yml"

    try:
        with open(inv_file, "w", encoding="utf-8") as handle:
            yaml.safe_dump(inventory_payload, handle, sort_keys=False)

        cmd = ["anta", "nrfu"]
        # Same as the standard run: no --enable unless the operator opts in.
        if os.environ.get("ANTA_DEVICE_CATALOG_ENABLE", "").strip().lower() in ("1", "true", "yes"):
            cmd.append("--enable")
        cmd += [
            "-i", inv_file,
            "-c", catalog_path,
            "--catalog-format", _catalog_format(catalog_path),
            "-d", device,
            "--ignore-status",
            "json",
            "-o", out_file,
        ]

        start = time.time()
        timed_out = False
        with open(stdout_file, "w", encoding="utf-8") as out_f, open(
            stderr_file, "w", encoding="utf-8"
        ) as err_f:
            proc = subprocess.Popen(cmd, stdout=out_f, stderr=err_f, text=True, env=run_env)
            while proc.poll() is None:
                if time.time() - start > timeout:
                    proc.kill()
                    proc.wait()
                    timed_out = True
                    break
                time.sleep(0.2)

        stdout = _read_text(stdout_file)
        stderr = _read_text(stderr_file)
        log = f"=== {device} ===\n{stdout}\n{stderr}"

        if timed_out:
            return [
                _error_row(
                    device,
                    "timeout",
                    "Device catalog run timed out",
                    f"No result from {device} after {timeout}s - the device may be unreachable.",
                )
            ], log

        if os.path.exists(out_file):
            try:
                with open(out_file, encoding="utf-8") as handle:
                    chunk = json.load(handle)
            except (json.JSONDecodeError, OSError) as exc:
                return [_error_row(device, "parse", "Could not read ANTA JSON output", str(exc))], log
            rows = chunk if isinstance(chunk, list) else [chunk]
            if not rows:
                # ANTA exits cleanly with an empty result list when it cannot reach the
                # device ("No reachable devices found"), so without this row the switch
                # would silently vanish from the table.
                return [
                    _error_row(
                        device,
                        "unreachable",
                        "No test results returned",
                        f"{device} returned no results - it is probably unreachable. "
                        "See the ANTA console output below.",
                    )
                ], log
            return rows, log

        return [
            _error_row(device, "anta", "ANTA produced no JSON output", stderr or stdout or "Unknown error")
        ], log
    finally:
        for path in (out_file, inv_file, stdout_file, stderr_file):
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass


def run_device_catalog_suite(
    *,
    catalogs_dir: str,
    inventory_payload: dict[str, Any],
    run_env: dict[str, str],
    nrfu_timeout: int,
    run_id: str | None = None,
    status_callback: Callable[[str], None] | None = None,
) -> tuple[list[dict[str, Any]], str]:
    """Execute ``anta nrfu json`` once per ``<device>.json`` (or .yaml) catalog.

    Devices run in parallel (``ANTA_DEVICE_CATALOG_WORKERS``, default 4). Each device
    gets its own timeout (``ANTA_DEVICE_CATALOG_TIMEOUT`` seconds, default 300, never
    more than ``nrfu_timeout``) so one unreachable switch cannot hold up the others.
    Results are returned in catalog (alphabetical) order. ``status_callback`` is only
    ever called from the calling thread.
    """
    device_names = list_device_catalogs(catalogs_dir)
    if not device_names:
        return [], ""

    inv_hosts = {
        h.get("name")
        for h in inventory_payload.get("anta_inventory", {}).get("hosts", [])
        if h.get("name")
    }
    run_id = run_id or uuid.uuid4().hex[:8]
    timeout = min(nrfu_timeout, _env_int("ANTA_DEVICE_CATALOG_TIMEOUT", 300))
    workers = _env_int("ANTA_DEVICE_CATALOG_WORKERS", 4)

    per_device: dict[str, list[dict[str, Any]]] = {}
    logs: dict[str, str] = {}
    to_run: list[tuple[str, str]] = []

    for device in device_names:
        catalog_path = None
        for ext in (".json", ".yaml", ".yml"):
            candidate = os.path.join(catalogs_dir, f"{device}{ext}")
            if os.path.isfile(candidate):
                catalog_path = candidate
                break
        if not catalog_path:
            continue
        if device not in inv_hosts:
            per_device[device] = [
                _error_row(
                    device,
                    "inventory",
                    "Catalog file has no matching inventory host name",
                    f"No inventory host named '{device}'. Add it under Manage Inventory "
                    "(the host name must match the catalog filename without its extension). "
                    f"Inventory host names: {', '.join(sorted(inv_hosts)) or 'none'}.",
                )
            ]
            continue
        to_run.append((device, catalog_path))

    done = 0
    if to_run:
        with ThreadPoolExecutor(max_workers=min(workers, len(to_run))) as pool:
            futures = {
                pool.submit(
                    _run_one_device,
                    device=device,
                    catalog_path=catalog_path,
                    inventory_payload=inventory_payload,
                    run_env=run_env,
                    run_id=run_id,
                    timeout=timeout,
                ): device
                for device, catalog_path in to_run
            }
            if status_callback:
                status_callback(f"Running catalogs for {len(to_run)} device(s)...")
            for future in as_completed(futures):
                device = futures[future]
                done += 1
                try:
                    per_device[device], logs[device] = future.result()
                except Exception as exc:  # keep one bad device from killing the run
                    per_device[device] = [_error_row(device, "anta", "Device catalog run failed", str(exc))]
                    logs[device] = f"=== {device} ===\n{exc}"
                if status_callback:
                    status_callback(f"Finished {device} ({done}/{len(to_run)})")

    merged: list[dict[str, Any]] = []
    for device in device_names:
        merged.extend(per_device.get(device, []))
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    full_log = "\n".join(logs[d] for d in device_names if d in logs)
    return merged, ansi_escape.sub("", full_log)


def display_nrfu_results(st, results: list[dict[str, Any]], full_log: str = "", run_id: str = "") -> None:
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

    from results_export import results_export_buttons

    results_export_buttons(st, df, run_id)
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
