import cv2
import re
import glob
import pandas as pd

from src.beam_fitting import (
    extract_horizontal_profile,
    fit_gaussian_profile,
    sigma_to_beam_radius
)

from src.calibration import PixelCalibration
from src.beam_simulator import gaussian_beam_radius
from src.metrics import percentage_error


IMAGE_PATTERN = "data/raw/simulated/beam_*mm.png"

W0 = 0.05
WAVELENGTH = 0.00065


def extract_distance(image_path):
    """
    Extract propagation distance from filename.

    Example:
        beam_300mm.png -> 300 mm
    """

    match = re.search(r"beam_(\d+)mm\.png", image_path)

    if match is None:
        raise ValueError(
            f"Could not determine distance from filename: {image_path}"
        )

    return float(match.group(1))


def analyse_image(image_path, calibration):
    """
    Analyse one beam image and return measurement results.
    """

    distance = extract_distance(image_path)

    image = cv2.imread(
        image_path,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    x_values, profile, y_row = extract_horizontal_profile(
        image
    )

    params, covariance = fit_gaussian_profile(
        x_values,
        profile
    )

    amplitude, centre, sigma, offset = params

    radius_pixels = sigma_to_beam_radius(
        sigma
    )

    radius_mm = calibration.pixels_to_mm(
        radius_pixels
    )

    theoretical_radius = gaussian_beam_radius(
        distance,
        W0,
        WAVELENGTH
    )

    error_percent = percentage_error(
        radius_mm,
        theoretical_radius
    )

    return {
        "distance_mm": distance,
        "beam_centre_pixels": centre,
        "sigma_pixels": sigma,
        "radius_pixels": radius_pixels,
        "radius_mm": radius_mm,
        "theoretical_radius_mm": theoretical_radius,
        "error_percent": error_percent
    }


def main():

    calibration = PixelCalibration(
        mm_per_pixel=0.05
    )

    image_paths = sorted(
        glob.glob(IMAGE_PATTERN)
    )

    if not image_paths:
        raise FileNotFoundError(
            f"No images found matching: {IMAGE_PATTERN}"
        )

    results = []

    print()
    print("BATCH BEAM ANALYSIS")
    print("=" * 60)

    for image_path in image_paths:

        result = analyse_image(
            image_path,
            calibration
        )

        results.append(result)

        print(
            f"Distance: {result['distance_mm']:.0f} mm | "
            f"Measured: {result['radius_mm']:.4f} mm | "
            f"Theory: {result['theoretical_radius_mm']:.4f} mm | "
            f"Error: {result['error_percent']:.2f}%"
        )

    results_df = pd.DataFrame(results)

    output_path = "results/batch_analysis.csv"

    results_df.to_csv(
        output_path,
        index=False
    )

    print()
    print("=" * 60)
    print("Batch analysis complete.")
    print(f"Results saved to: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()