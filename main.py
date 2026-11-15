from pathlib import Path
from contextlib import redirect_stdout
from call_inputs import call
from Nitrogen_Script import bottle_sizing
from Nitrous_Tank import nitrous_tank_sizing
from Total_System_Dimensions import total_system_dimensions
from reporting import report, next_results_file

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

def main():
    nitrous = call(nitrous_tank_sizing)
    bottle  = call(bottle_sizing)

    system = call(total_system_dimensions,
                  nitrous_tank_length     = nitrous["tank_length"],
                  bottle_length           = bottle["tank_length"],
                  nitrous_liner_thickness = nitrous["liner_thickness"],
                  bottle_liner_thickness  = bottle["liner_thickness"])

    out = next_results_file(RESULTS_DIR)
    with open(out, "w", encoding="utf-8") as f, redirect_stdout(f):
        report(nitrous, bottle, system)
    print(f"Results saved to: {out}")

if __name__ == "__main__":
    main()