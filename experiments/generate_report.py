import pandas as pd

from src.reporting import (
    format_measurement_report,
    save_report
)


# --------------------------------------------------
# Load measurement results
# --------------------------------------------------

beam_results = pd.read_csv(
    "results/beam_measurements.csv"
)

uncertainty_results = pd.read_csv(
    "results/uncertainty_measurements.csv"
)

noise_results = pd.read_csv(
    "results/noise_sensitivity.csv"
)


# --------------------------------------------------
# Elliptical beam validation results
# --------------------------------------------------

elliptical_results = {

    "true_ellipticity": 1.20 / 0.90,

    "measured_ellipticity": 1.3336,

    "ellipticity_error": 0.02

}


# --------------------------------------------------
# Generate report
# --------------------------------------------------

report = format_measurement_report(
    beam_results,
    uncertainty_results,
    elliptical_results,
    noise_results
)


# --------------------------------------------------
# Save report
# --------------------------------------------------

output_path = "results/measurement_report.txt"

save_report(
    report,
    output_path
)


print(
    f"Measurement report saved to: {output_path}"
)

print()

print(report)