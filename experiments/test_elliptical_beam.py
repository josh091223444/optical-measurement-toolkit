import cv2
import numpy as np
import matplotlib.pyplot as plt

from src.beam_simulator import generate_elliptical_beam

from src.beam_fitting import (
    fit_gaussian_2d,
    sigma_to_beam_radii
)

from src.metrics import percentage_error


PIXEL_SCALE = 0.05

# Known beam parameters
TRUE_WX = 1.20
TRUE_WY = 0.90


# Generate synthetic elliptical beam
image = generate_elliptical_beam(
    wx=TRUE_WX,
    wy=TRUE_WY,
    pixel_scale=PIXEL_SCALE
)


# Fit the entire 2D image
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


# Convert sigma to 1/e² beam radii
measured_wx_pixels, measured_wy_pixels = (
    sigma_to_beam_radii(
        sigma_x,
        sigma_y
    )
)


measured_wx = (
    measured_wx_pixels * PIXEL_SCALE
)

measured_wy = (
    measured_wy_pixels * PIXEL_SCALE
)


# Calculate errors
error_x = percentage_error(
    measured_wx,
    TRUE_WX
)

error_y = percentage_error(
    measured_wy,
    TRUE_WY
)


# Calculate ellipticity
measured_ellipticity = (
    measured_wx / measured_wy
)

true_ellipticity = (
    TRUE_WX / TRUE_WY
)


ellipticity_error = percentage_error(
    measured_ellipticity,
    true_ellipticity
)


print("Elliptical Beam Validation")
print("-" * 35)

print(
    f"True wx:       {TRUE_WX:.4f} mm"
)

print(
    f"Measured wx:   {measured_wx:.4f} mm"
)

print(
    f"wx error:      {error_x:.2f}%"
)

print()

print(
    f"True wy:       {TRUE_WY:.4f} mm"
)

print(
    f"Measured wy:   {measured_wy:.4f} mm"
)

print(
    f"wy error:      {error_y:.2f}%"
)

print()

print(
    f"True ellipticity:     "
    f"{true_ellipticity:.4f}"
)

print(
    f"Measured ellipticity: "
    f"{measured_ellipticity:.4f}"
)

print(
    f"Ellipticity error:    "
    f"{ellipticity_error:.2f}%"
)


# Create visualisation
x_values = np.arange(image.shape[1])
y_values = np.arange(image.shape[0])

X, Y = np.meshgrid(
    x_values,
    y_values
)


fitted_image = (
    amplitude
    * np.exp(
        -(
            (X - x_centre) ** 2
            / (2 * sigma_x ** 2)
            +
            (Y - y_centre) ** 2
            / (2 * sigma_y ** 2)
        )
    )
    + offset
)


plt.figure(figsize=(7, 6))

plt.imshow(
    image,
    cmap="gray"
)

plt.contour(
    fitted_image,
    levels=6
)

plt.xlabel("X (pixels)")
plt.ylabel("Y (pixels)")

plt.title(
    "Elliptical Beam with 2D Gaussian Fit"
)

plt.tight_layout()

plt.savefig(
    "results/elliptical_beam_fit.png",
    dpi=150
)

plt.close()


# Residual
residual = (
    image.astype(float)
    - fitted_image
)


plt.figure(figsize=(7, 6))

plt.imshow(
    residual,
    cmap="seismic"
)

plt.colorbar(
    label="Intensity Residual"
)

plt.xlabel("X (pixels)")
plt.ylabel("Y (pixels)")

plt.title(
    "Elliptical Beam Fit Residual"
)

plt.tight_layout()

plt.savefig(
    "results/elliptical_beam_residual.png",
    dpi=150
)

plt.close()