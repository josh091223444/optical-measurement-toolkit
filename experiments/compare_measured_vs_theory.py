import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from src.beam_fitting import (
    extract_horizontal_profile,
    fit_gaussian_profile,
    sigma_to_beam_radius
)

from src.beam_simulator import gaussian_beam_radius
from src.metrics import percentage_error


PIXEL_SCALE = 0.05
W0 = 0.05
WAVELENGTH = 0.00065

distances_mm = [100, 200, 300, 400, 500]

measured_radii_mm = []
theoretical_radii_mm = []

results = []


for distance in distances_mm:

    image_path = f"data/raw/simulated/beam_{distance}mm.png"

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    gray_image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    x_values, profile, y_row = extract_horizontal_profile(
        gray_image
    )

    params, covariance = fit_gaussian_profile(
        x_values,
        profile
    )

    amplitude, centre, sigma, offset = params

    measured_radius_pixels = sigma_to_beam_radius(
        sigma
    )

    measured_radius_mm = (
        measured_radius_pixels * PIXEL_SCALE
    )

    theoretical_radius_mm = gaussian_beam_radius(
        distance,
        W0,
        WAVELENGTH
    )

    error_percent = percentage_error(
        measured_radius_mm,
        theoretical_radius_mm
    )

    measured_radii_mm.append(
        measured_radius_mm
    )

    theoretical_radii_mm.append(
        theoretical_radius_mm
    )

    results.append({
        "distance_mm": distance,
        "theoretical_radius_mm": theoretical_radius_mm,
        "measured_radius_mm": measured_radius_mm,
        "error_percent": error_percent
    })

    print(
        f"Distance: {distance} mm | "
        f"Measured radius: {measured_radius_mm:.4f} mm | "
        f"Theoretical radius: {theoretical_radius_mm:.4f} mm | "
        f"Error: {error_percent:.2f}%"
    )



results_df = pd.DataFrame(results)


results_df.to_csv(
    "results/beam_measurements.csv",
    index=False
)



plt.figure(figsize=(8, 6))

plt.plot(
    distances_mm,
    measured_radii_mm,
    "o-",
    label="Measured (fitted)"
)

plt.plot(
    distances_mm,
    theoretical_radii_mm,
    "s--",
    label="Theoretical (Gaussian beam model)"
)

plt.xlabel("Propagation distance (mm)")
plt.ylabel("1/e² Beam Radius (mm)")
plt.title("Measured vs Theoretical 1/e² Beam Radius")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "results/measured_vs_theoretical.png",
    dpi=150
)

plt.show()