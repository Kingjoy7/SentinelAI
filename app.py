from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parent
DASHBOARD_APP = ROOT / "backend" / "dashboard" / "app.py"

if not DASHBOARD_APP.exists():
    raise FileNotFoundError(f"Dashboard entrypoint not found: {DASHBOARD_APP}")

runpy.run_path(str(DASHBOARD_APP), run_name="__main__")
