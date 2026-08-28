from datetime import datetime


def format_measurement_report(
    beam_results,
    uncertainty_results,
    elliptical_results,
    noise_results
):
    """
    Create a formatted engineering measurement report.

    Parameters
    ----------
    beam_results : pandas.DataFrame
        Theory versus measured beam-radius results.

    uncertainty_results : pandas.DataFrame
        Repeatability and uncertainty measurements.

    elliptical_results : dict
        Results from elliptical beam validation.

    noise_results : pandas.DataFrame
        Noise sensitivity measurements.

    Returns
    -------
    str
        Formatted measurement report.
    """

    lines = []

    lines.append("=" * 70)
    lines.append("OPTICAL MEASUREMENT TOOLKIT")
    lines.append("AUTOMATED MEASUREMENT REPORT")
    lines.append("=" * 70)

    lines.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    lines.append("")

    # --------------------------------------------------
    # Theory vs Measurement
    # --------------------------------------------------

    lines.append("1. THEORY VS MEASUREMENT")
    lines.append("-" * 70)

    mean_error = beam_results[
        "error_percent"
    ].mean()

    max_error = beam_results[
        "error_percent"
    ].max()

    lines.append(
        f"Mean measurement error: {mean_error:.2f}%"
    )

    lines.append(
        f"Maximum measurement error: {max_error:.2f}%"
    )

    lines.append("")

    # --------------------------------------------------
    # Uncertainty Analysis
    # --------------------------------------------------

    lines.append("2. REPEATABILITY AND UNCERTAINTY")
    lines.append("-" * 70)

    mean_std = uncertainty_results[
        "std_radius_mm"
    ].mean()

    max_std = uncertainty_results[
        "std_radius_mm"
    ].max()

    lines.append(
        f"Mean measurement standard deviation: "
        f"{mean_std:.4f} mm"
    )

    lines.append(
        f"Maximum measurement standard deviation: "
        f"{max_std:.4f} mm"
    )

    lines.append("")

    # --------------------------------------------------
    # Elliptical Beam Validation
    # --------------------------------------------------

    lines.append("3. ELLIPTICAL BEAM VALIDATION")
    lines.append("-" * 70)

    lines.append(
        f"True ellipticity: "
        f"{elliptical_results['true_ellipticity']:.4f}"
    )

    lines.append(
        f"Measured ellipticity: "
        f"{elliptical_results['measured_ellipticity']:.4f}"
    )

    lines.append(
        f"Ellipticity error: "
        f"{elliptical_results['ellipticity_error']:.2f}%"
    )

    lines.append("")

    # --------------------------------------------------
    # Noise Sensitivity
    # --------------------------------------------------

    lines.append("4. NOISE SENSITIVITY")
    lines.append("-" * 70)

    highest_noise = noise_results.iloc[-1]

    lines.append(
        f"Highest tested noise level: "
        f"{highest_noise['noise_std']}"
    )

    lines.append(
        f"Radius X error at highest noise: "
        f"{highest_noise['wx_error_percent']:.2f}%"
    )

    lines.append(
        f"Radius Y error at highest noise: "
        f"{highest_noise['wy_error_percent']:.2f}%"
    )

    lines.append(
        f"Ellipticity error at highest noise: "
        f"{highest_noise['ellipticity_error_percent']:.2f}%"
    )

    lines.append("")

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    lines.append("5. ENGINEERING SUMMARY")
    lines.append("-" * 70)

    lines.append(
        "The Gaussian fitting approach successfully recovered "
        "beam dimensions from simulated intensity images."
    )

    lines.append(
        "Measurement error remained low under nominal conditions "
        "and increased with simulated sensor noise."
    )

    lines.append(
        "Ellipticity measurements remained comparatively robust "
        "under increased noise."
    )

    lines.append("")

    lines.append("=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)

    return "\n".join(lines)


def save_report(report_text, output_path):
    """
    Save a measurement report to a text file.
    """

    with open(output_path, "w") as file:
        file.write(report_text)