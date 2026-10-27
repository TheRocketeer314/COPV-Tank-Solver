import runpy
from pathlib import Path
from contextlib import redirect_stdout

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

i = 1
while True:
    OUTPUT_FILE = RESULTS_DIR / f"results_{i:03d}.txt"
    if not OUTPUT_FILE.exists():
        break
    i += 1

modules = [
    "COPV Netting Analysis.py",
    "Nitrous_Tank_Length.py",
    "Geodesic_Dome.py"
]

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    with redirect_stdout(file):
        for module in modules:
            print(f"\n{'=' * 50}")
            print(f"Running {module}")
            print(f"{'=' * 50}\n")

            runpy.run_path(str(BASE_DIR / module))

print(f"Results saved to: {OUTPUT_FILE}")
