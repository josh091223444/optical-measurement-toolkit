import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from src.beam_simulator import generate_elliptical_beam

from src.beam_fitting import (
    fit_gaussian_2d,
    sigma_to_beam_radii
)

from src.metrics import percentage_error


# -----------------------------
# Experimental parameters
# -----------------------------

PIXEL_SCALE = 0.05

TRUE_WX = 1.20
TRUE_WY = 0.90

TRUE_ELLIPTICITY = TRUE_WX / TRUE_WY

NOISE_LEVELS = [
    0,
    1,
    2,
    5,
    10,
    15,
    20
]

N_REPEATS = 20


# -----------------------------
# Storage
# -----------------------------

results = []


# -----------------------------
# Run noise experiment
# -----------------------------

for noise_std in NOISE_LEVELS:

    measured_wx_values = []
    measured_wy_values = []
    measured_ellipticity_values = []

    for repeat in range(N_REPEATS):

        # Reproducible random number generator
        rng = np.random.default_rng(
            seed=1000 + noise_std * 100 + repeat
        )

        image = generate_elliptical_beam(
            wx=TRUE_WX,
            wy=TRUE_WY,
            noise_std=noise_std,
            pixel_scale=PIXEL_SCALE,
            rng=rng
        )

        params, covariance = fit_gaussian_2d(
            image
        )

        (
            amplitude,
            x_centre,
            y_centre,
            sigma_x,
            sigma_y,
            offset
        ) = params

        wx_pixels, wy_pixels = (
            sigma_to_beam_radii(
                sigma_x,
                sigma_y
            )
        )

        wx_mm = (
            wx_pixels * PIXEL_SCALE
        )

        wy_mm = (
            wy_pixels * PIXEL_SCALE
        )

        ellipticity = (
            wx_mm / wy_mm
        )

        measured_wx_values.append(wx_mm)
        measured_wy_values.append(wy_mm)
        measured_ellipticity_values.append(
            ellipticity
        )

    # -----------------------------
    # Calculate statistics
    # -----------------------------

    mean_wx = np.mean(
        measured_wx_values
    )

    std_wx = np.std(
        measured_wx_values
    )

    mean_wy = np.mean(
        measured_wy_values
    )

    std_wy = np.std(
        measured_wy_values
    )

    mean_ellipticity = np.mean(
        measured_ellipticity_values
    )

    std_ellipticity = np.std(
        measured_ellipticity_values
    )

    wx_error = percentage_error(
        mean_wx,
        TRUE_WX
    )

    wy_error = percentage_error(
        mean_wy,
        TRUE_WY
    )

    ellipticity_error = percentage_error(
        mean_ellipticity,
        TRUE_ELLIPTICITY
    )

    results.append({
        "noise_std": noise_std,
        "mean_wx_mm": mean_wx,
        "std_wx_mm": std_wx,
        "wx_error_percent": wx_error,
        "mean_wy_mm": mean_wy,
        "std_wy_mm": std_wy,
        "wy_error_percent": wy_error,
        "mean_ellipticity": mean_ellipticity,
        "std_ellipticity": std_ellipticity,
        "ellipticity_error_percent": (
            ellipticity_error
        )
    })

    print(
        f"Noise: {noise_std:>2} | "
        f"wx: {mean_wx:.4f} ± {std_wx:.4f} mm "
        f"({wx_error:.2f}% error) | "
        f"wy: {mean_wy:.4f} ± {std_wy:.4f} mm "
        f"({wy_error:.2f}% error) | "
        f"Ellipticity: {mean_ellipticity:.4f} "
        f"({ellipticity_error:.2f}% error)"
    )


# -----------------------------
# Save results
# -----------------------------

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    "results/noise_sensitivity.csv",
    index=False
)


# -----------------------------
# Plot radius error
# -----------------------------

plt.figure(figsize=(8, 6))

plt.plot(
    NOISE_LEVELS,
    results_df["wx_error_percent"],
    "o-",
    label="wx error"
)

plt.plot(
    NOISE_LEVELS,
    results_df["wy_error_percent"],
    "s-",
    label="wy error"
)

plt.xlabel(
    "Noise standard deviation"
)

plt.ylabel(
    "Mean measurement error (%)"
)

plt.title(
    "Beam Radius Measurement Error vs Sensor Noise"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "results/noise_radius_error.png",
    dpi=150
)

plt.close()


# -----------------------------
# Plot ellipticity error
# -----------------------------

plt.figure(figsize=(8, 6))

plt.plot(
    NOISE_LEVELS,
    results_df["ellipticity_error_percent"],
    "o-",
    label="Ellipticity error"
)

plt.xlabel(
    "Noise standard deviation"
)

plt.ylabel(
    "Mean ellipticity error (%)"
)

plt.title(
    "Ellipticity Measurement Error vs Sensor Noise"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "results/noise_ellipticity_error.png",
    dpi=150
)

plt.close()