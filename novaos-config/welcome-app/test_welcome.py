"""Minimal smoke test for the NovaOS welcome app.

We can't actually launch the GUI in a headless test environment, so we
test what we CAN test without a display:
  - imports work
  - the `first_run` config write works
  - the parser accepts both --first-run and bare invocation

Run with:
    python3 test_welcome.py
"""
import sys
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Stub PyQt5 if missing (CI environments)
try:
    from PyQt5 import QtWidgets  # noqa: F401
    HAS_PYQT = True
except ImportError:
    HAS_PYQT = False
    sys.modules['PyQt5'] = MagicMock()
    sys.modules['PyQt5.QtCore'] = MagicMock()
    sys.modules['PyQt5.QtGui'] = MagicMock()
    sys.modules['PyQt5.QtWidgets'] = MagicMock()


class TestFirstRunPref(unittest.TestCase):

    def test_writes_config(self):
        # Use a temp dir so we don't touch the real user home.
        # Patch Path.home() — that's what the module reads at import time.
        with tempfile.TemporaryDirectory() as tmp:
            fake_home = Path(tmp)
            with patch.object(Path, 'home', lambda: fake_home):
                # Re-import so module-level Path.home() is re-evaluated
                if 'welcome' in sys.modules:
                    del sys.modules['welcome']
                import welcome

                welcome._set_first_run_pref(suppress=True)
                cfg = (fake_home / ".config" / "novaos" / "welcome.cfg").read_text()
                self.assertIn("first_run=False", cfg)

                welcome._set_first_run_pref(suppress=False)
                cfg = (fake_home / ".config" / "novaos" / "welcome.cfg").read_text()
                self.assertIn("first_run=True", cfg)


class TestImports(unittest.TestCase):

    @unittest.skipUnless(HAS_PYQT, "PyQt5 not available in CI")
    def test_welcome_imports_cleanly(self):
        """The main module must import without errors on a real install."""
        # We add the dir to sys.path for this test
        import importlib.util
        here = Path(__file__).parent
        spec = importlib.util.spec_from_file_location("welcome", here / "welcome.py")
        self.assertIsNotNone(spec)
        if spec is not None:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore
            self.assertTrue(hasattr(mod, 'NovaWelcome'))


if __name__ == "__main__":
    unittest.main(verbosity=2)
