"""Download buttons for NRFU results (shared by the standard and device-catalog runs)."""
from __future__ import annotations

import time
from typing import Any

import pandas as pd


def results_export_buttons(st, df: pd.DataFrame, run_id: str = "") -> None:
    """Offer the full result table as CSV and JSON.

    ``on_click="ignore"`` keeps Streamlit from rerunning the script when a file is
    downloaded; otherwise the results (rendered only right after the Execute click)
    would disappear the moment the user downloads them.
    """
    if df is None or df.empty:
        return
    export_df = df.copy()
    for col in export_df.columns:
        export_df[col] = export_df[col].apply(
            lambda v: ", ".join(map(str, v)) if isinstance(v, (list, tuple)) else v
        )
    stamp = time.strftime("%Y%m%d-%H%M%S")
    base = f"anta_results_{run_id + '_' if run_id else ''}{stamp}"
    c1, c2, _ = st.columns([1, 1, 3])
    with c1:
        st.download_button(
            "⬇️ Download CSV",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name=f"{base}.csv",
            mime="text/csv",
            on_click="ignore",
            key=f"dl_csv_{base}",
        )
    with c2:
        st.download_button(
            "⬇️ Download JSON",
            data=export_df.to_json(orient="records", indent=2).encode("utf-8"),
            file_name=f"{base}.json",
            mime="application/json",
            on_click="ignore",
            key=f"dl_json_{base}",
        )


def parse_custom_yaml(text: str) -> tuple[dict[str, list[Any]], str | None]:
    """Parse the Custom YAML box (ANTA catalog format). Returns (catalog_dict, error)."""
    import yaml

    if not text or not text.strip():
        return {}, None
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return {}, f"Invalid YAML: {exc}"
    if data is None:  # only comments
        return {}, None
    if not isinstance(data, dict):
        return {}, "Custom YAML must be a mapping of ANTA modules, e.g. 'anta.tests.system:' followed by a list of tests."
    out: dict[str, list[Any]] = {}
    for module, tests in data.items():
        if not isinstance(tests, list):
            return {}, f"'{module}' must contain a list of tests (each line starting with '- ')."
        out[str(module)] = tests
    return out, None
