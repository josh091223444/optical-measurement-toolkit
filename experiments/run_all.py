import subprocess
import sys


EXPERIMENTS = [
    "experiments.compare_measured_vs_theory",
    "experiments.uncertainty_analysis",
    "experiments.test_2d_fitting",
    "experiments.test_elliptical_beam",
    "experiments.noise_sensitivity",
]


def run_experiment(module_name):
    print("\n" + "=" * 60)
    print(f"Running: {module_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        check=False
    )

    if result.returncode != 0:
        print(f"\nERROR: {module_name} failed.")
        return False

    print(f"\nCompleted: {module_name}")
    return True


def generate_report():
    print("\n" + "=" * 60)
    print("Generating measurement report")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "experiments.generate_report"],
        check=False
    )

    if result.returncode != 0:
        print("\nERROR: Measurement report generation failed.")
        return False

    print("\nCompleted: measurement report")
    return True


def main():
    print("Optical Measurement Toolkit")
    print("Running validation experiments...")

    all_passed = True

    for experiment in EXPERIMENTS:
        success = run_experiment(experiment)

        if not success:
            all_passed = False

    print("\n" + "=" * 60)

    if all_passed:
        print("All experiments completed successfully.")

        report_success = generate_report()

        if not report_success:
            all_passed = False

    else:
        print("One or more experiments failed.")

    print("=" * 60)

    if all_passed:
        print("Validation pipeline completed successfully.")
    else:
        print("Validation pipeline completed with errors.")

    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())