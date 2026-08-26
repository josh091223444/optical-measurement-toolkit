import cv2
import numpy as np
import matplotlib.pyplot as plt

from src.beam_fitting import (
    gaussian_2d,
    fit_gaussian_2d,
    sigma_to_beam_radii
)


IMAGE_PATH = "data/raw/simulated/beam_300mm.png"
PIXEL_SCALE = 0.05


image = cv2.imread(
    IMAGE_PATH,
    cv2.IMREAD_GRAYSCALE
)

if image is None:
    raise FileNotFoundError(
        f"Could not load image: {IMAGE_PATH}"
    )


params, covariance = fit_gaussian_2d(image)

(
    amplitude,
    x_centre,
    y_centre,
    sigma_x,
    sigma_y,
    offset
) = params


radius_x_pixels, radius_y_pixels = (
    sigma_to_beam_radii(
        sigma_x,
        sigma_y
    )
)

radius_x_mm = radius_x_pixels * PIXEL_SCALE
radius_y_mm = radius_y_pixels * PIXEL_SCALE

ellipticity = radius_x_mm / radius_y_mm


print("2D Gaussian Fit Results")
print("-" * 30)

print(f"Amplitude: {amplitude:.2f}")
print(
    f"Centre: ({x_centre:.2f}, "
    f"{y_centre:.2f}) pixels"
)

print(
    f"Sigma X: {sigma_x:.2f} pixels"
)

print(
    f"Sigma Y: {sigma_y:.2f} pixels"
)

print(
    f"1/e² Radius X: {radius_x_mm:.4f} mm"
)

print(
    f"1/e² Radius Y: {radius_y_mm:.4f} mm"
)

print(
    f"Ellipticity: {ellipticity:.4f}"
)


fitted_image = gaussian_2d(
    np.indices(image.shape)[::-1],
    *params
).reshape(image.shape)


residual = (
    image.astype(float)
    - fitted_image
)


plt.figure(figsize=(7, 6))

plt.imshow(image, cmap="gray")

plt.contour(
    fitted_image,
    levels=6
)

plt.title(
    "Simulated Beam with 2D Gaussian Fit"
)

plt.xlabel("X (pixels)")
plt.ylabel("Y (pixels)")

plt.tight_layout()

plt.savefig(
    "results/2d_gaussian_fit.png",
    dpi=150
)

plt.close()


plt.figure(figsize=(7, 6))

plt.imshow(
    residual,
    cmap="seismic"
)

plt.colorbar(
    label="Intensity Residual"
)

plt.title(
    "2D Gaussian Fit Residual"
)

plt.xlabel("X (pixels)")
plt.ylabel("Y (pixels)")

plt.tight_layout()

plt.savefig(
    "results/2d_gaussian_residual.png",
    dpi=150
)

plt.close()