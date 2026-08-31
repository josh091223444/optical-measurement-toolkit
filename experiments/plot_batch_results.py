import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "results/batch_analysis.csv"
OUTPUT_FILE = "results/batch_analysis_plot.png"


def main():

    results = pd.read_csv(INPUT_FILE)

    print("Columns found:")
    print(list(results.columns))

    distance = results["distance_mm"]
    measured = results["radius_mm"]
    theoretical = results["theoretical_radius_mm"]
    plt.figure(figsize=(8, 6))

    plt.plot(
        distance,
        measured,
        "o-",
        label="Measured"
    )

    plt.plot(
        distance,
        theoretical,
        "s--",
        label="Theoretical"
    )

    plt.xlabel("Propagation distance (mm)")
    plt.ylabel("1/e² Beam Radius (mm)")

    plt.title(
        "Batch Beam Analysis: Measured vs Theoretical Radius"
    )

    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FILE,
        dpi=150
    )

    plt.close()

    print("=" * 60)
    print("BATCH VISUALISATION")
    print("=" * 60)
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print("Plot generated successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()