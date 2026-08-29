import sys
import cv2

from src.beam_fitting import (
    extract_horizontal_profile,
    fit_gaussian_profile,
    sigma_to_beam_radius,
)

from src.calibration import PixelCalibration
from src.metrics import percentage_error


CALIBRATION = PixelCalibration(
    mm_per_pixel=0.05
)


def analyse_image(image_path):
    """
    Analyse a grayscale or colour beam image.

    Parameters
    ----------
    image_path : str
        Path to the image to analyse.

    Returns
    -------
    dict
        Beam measurement results.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    # Convert colour images to grayscale.
    if len(image.shape) == 3:
        gray_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )
    else:
        gray_image = image

    x_values, profile, y_row = (
        extract_horizontal_profile(gray_image)
    )

    params, covariance = fit_gaussian_profile(
        x_values,
        profile
    )

    amplitude, centre, sigma, offset = params

    radius_pixels = sigma_to_beam_radius(
        sigma
    )

    radius_mm = CALIBRATION.pixels_to_mm(
        radius_pixels
    )

    return {
        "image_path": image_path,
        "beam_radius_mm": radius_mm,
        "beam_radius_pixels": radius_pixels,
        "centre_pixels": centre,
        "profile_row": y_row,
        "sigma_pixels": sigma,
        "amplitude": amplitude,
        "offset": offset,
        "covariance": covariance,
    }


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python -m experiments.analyse_image "
            "<image_path>"
        )
        raise SystemExit(1)

    image_path = sys.argv[1]

    result = analyse_image(image_path)

    print()
    print("OPTICAL BEAM IMAGE ANALYSIS")
    print("=" * 40)

    print(
        f"Image: {result['image_path']}"
    )

    print(
        f"Profile row: "
        f"{result['profile_row']}"
    )

    print(
        f"Beam centre: "
        f"{result['centre_pixels']:.2f} pixels"
    )

    print(
        f"Sigma: "
        f"{result['sigma_pixels']:.2f} pixels"
    )

    print(
        f"1/e² beam radius: "
        f"{result['beam_radius_pixels']:.2f} pixels"
    )

    print(
        f"1/e² beam radius: "
        f"{result['beam_radius_mm']:.4f} mm"
    )

    print("=" * 40)


if __name__ == "__main__":
    main()