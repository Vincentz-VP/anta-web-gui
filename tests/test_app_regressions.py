"""UI regressions for deployment credentials and invalid custom catalogs."""

import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import PropertyMock, patch

import streamlit as st
from streamlit.testing.v1 import AppTest


APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT))


class AppRegressionTests(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.data_dir = Path(directory)
        env = dict(os.environ, ANTA_DATA_DIR=directory)
        for key in ("ANTA_USERNAME", "ANTA_PASSWORD", "ANTA_DEVICE_CATALOGS_DIR", "AVD_CATALOGS_DIR"):
            env.pop(key, None)
        self.enterContext(patch.dict(os.environ, env, clear=True))
        self.enterContext(patch.object(
            type(st.context), "cookies", new_callable=PropertyMock,
            return_value={"anta_client_id": "regression-browser"},
        ))

    def app(self):
        at = AppTest.from_file(str(APP_ROOT / "app.py"), default_timeout=45).run()
        self.assertFalse(at.exception, [e.message for e in at.exception])
        return at

    def test_default_credentials(self):
        at = self.app()
        self.assertEqual(at.session_state["anta_user"], "admin")
        self.assertEqual(at.session_state["anta_pass"], "admin")

    def test_environment_credentials(self):
        os.environ.update(ANTA_USERNAME="env-user", ANTA_PASSWORD="env-password")
        at = self.app()
        self.assertEqual(at.session_state["anta_user"], "env-user")
        self.assertEqual(at.session_state["anta_pass"], "env-password")

    def test_saved_credentials_take_precedence(self):
        os.environ.update(ANTA_USERNAME="env-user", ANTA_PASSWORD="env-password")
        settings = self.data_dir / "users" / "regression-browser" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({"anta_user": "saved-user", "anta_pass": "saved-password"}))
        at = self.app()
        self.assertEqual(at.session_state["anta_user"], "saved-user")
        self.assertEqual(at.session_state["anta_pass"], "saved-password")

    def test_empty_custom_test_shows_validation_error(self):
        at = self.app()
        custom = next(r for r in at.radio if r.label == "**🧩 Custom**")
        custom.set_value("🧩 Custom YAML").run()
        at.text_area(key="param_custom_yaml").set_value("anta.tests.system:\n  - {}\n").run()
        self.assertFalse(at.exception, [e.message for e in at.exception])
        errors = at.session_state["invalid_config_results"]
        self.assertTrue(any(
            row["result"] == "error" and row["description"] == "{} (Invalid Config/Missing Parameters)"
            for row in errors
        ))
        self.assertNotIn({}, at.session_state["session_valid_catalog_dict"].get("anta.tests.system", []))


if __name__ == "__main__":
    unittest.main()
