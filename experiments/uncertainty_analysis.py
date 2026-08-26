import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from src.beam_simulator import (
    gaussian_beam_radius,
    generate_simulated_beam
)

from src.beam_fitting import (
    extract_horizontal_profile,
    fit_gaussian_profile,
    sigma_to_beam_radius
)

from src.metrics import percentage_error


PIXEL_SCALE = 0.05
W0 = 0.05
WAVELENGTH = 0.00065

distances_mm = [100, 200, 300, 400, 500]
n_repeats = 20

mean_radii_mm = []
std_radii_mm = []
theoretical_radii_mm = []

results = []

# Fixed seed makes the experiment reproducible
rng = np.random.default_rng(42)


for distance in distances_mm:

    measured_radii_this_distance = []

    for repeat in range(n_repeats):

        image, _ = generate_simulated_beam(
            distance=distance,
            w0=W0,
            wavelength=WAVELENGTH,
            pixel_scale=PIXEL_SCALE,
            rng=rng
        )

        x_values, profile, y_row = extract_horizontal_profile(
            image
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

        measured_radii_this_distance.append(
            measured_radius_mm
        )

    mean_radius = np.mean(
        measured_radii_this_distance
    )

    std_radius = np.std(
        measured_radii_this_distance
    )

    theoretical_radius = gaussian_beam_radius(
        distance,
        W0,
        WAVELENGTH
    )

    error_percent = percentage_error(
        mean_radius,
        theoretical_radius
    )

    mean_radii_mm.append(mean_radius)
    std_radii_mm.append(std_radius)
    theoretical_radii_mm.append(theoretical_radius)

    results.append({
        "distance_mm": distance,
        "theoretical_radius_mm": theoretical_radius,
        "mean_measured_radius_mm": mean_radius,
        "std_radius_mm": std_radius,
        "error_percent": error_percent
    })

    print(
        f"Distance: {distance} mm | "
        f"Mean measured radius: {mean_radius:.4f} mm ± "
        f"{std_radius:.4f} mm | "
        f"Theoretical radius: {theoretical_radius:.4f} mm | "
        f"Error: {error_percent:.2f}%"
    )


results_df = pd.DataFrame(results)

results_df.to_csv(
    "results/uncertainty_measurements.csv",
    index=False
)


plt.figure(figsize=(8, 6))

plt.errorbar(
    distances_mm,
    mean_radii_mm,
    yerr=std_radii_mm,
    fmt="o-",
    capsize=4,
    label="Measured (mean ± std, n=20)"
)

plt.plot(
    distances_mm,
    theoretical_radii_mm,
    "s--",
    label="Theoretical (Gaussian beam model)"
)

plt.xlabel("Propagation distance (mm)")
plt.ylabel("1/e² Beam Radius (mm)")

plt.title(
    "Measured vs Theoretical 1/e² Beam Radius "
    "with Uncertainty"
)

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "results/uncertainty_analysis.png",
    dpi=150
)

plt.show()