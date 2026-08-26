import numpy as np


def gaussian_beam_radius(z, w0, wavelength):
    """
    Calculate the 1/e² beam radius w(z) at propagation
    distance z using the standard Gaussian beam equation.

    Parameters
    ----------
    z : float
        Propagation distance in mm.
    w0 : float
        Beam waist (minimum 1/e² radius) in mm.
    wavelength : float
        Wavelength in mm.
        Example: 650 nm = 0.00065 mm.

    Returns
    -------
    float
        Theoretical 1/e² beam radius at distance z, in mm.
    """

    z_R = (np.pi * w0**2) / wavelength

    w_z = w0 * np.sqrt(
        1 + (z / z_R)**2
    )

    return w_z


def generate_simulated_beam(
    image_size=500,
    w0=0.05,
    wavelength=0.00065,
    distance=0.0,
    peak_intensity=255,
    noise_std=5,
    pixel_scale=0.05,
    rng=None
):



    """
    Generate a synthetic 2D Gaussian laser beam image.

    Parameters
    ----------
    image_size : int
        Image width and height in pixels.
    w0 : float
        Beam waist in mm.
    wavelength : float
        Wavelength in mm.
    distance : float
        Propagation distance in mm.
    peak_intensity : float
        Peak simulated intensity, from 0 to 255.
    noise_std : float
        Standard deviation of Gaussian sensor noise.
    pixel_scale : float
        Physical size represented by each pixel, in mm/pixel.
    rng : numpy.random.Generator, optional
        Random number generator used for reproducible noise.

    Returns
    -------
    image : numpy.ndarray
        Synthetic 8-bit grayscale beam image.
    w_z : float
        Theoretical 1/e² beam radius in mm.
    """

    if rng is None:
        rng = np.random.default_rng()

    w_z = gaussian_beam_radius(
        distance,
        w0,
        wavelength
    )

    w_z_pixels = w_z / pixel_scale

    x = np.arange(image_size)
    y = np.arange(image_size)

    x_grid, y_grid = np.meshgrid(x, y)

    x_centre = image_size / 2
    y_centre = image_size / 2

    r_squared = (
        (x_grid - x_centre)**2
        + (y_grid - y_centre)**2
    )

    intensity = (
        peak_intensity
        * np.exp(-2 * r_squared / w_z_pixels**2)
    )

    noise = rng.normal(
        0,
        noise_std,
        size=intensity.shape
    )

    noisy_intensity = intensity + noise

    image = np.clip(
        noisy_intensity,
        0,
        255
    ).astype(np.uint8)

    return image, w_z

def generate_elliptical_beam(
    image_size=500,
    wx=0.05,
    wy=0.04,
    peak_intensity=255,
    noise_std=5,
    pixel_scale=0.05,
    rng=None
):
    """
    Generate a synthetic elliptical 2D Gaussian beam.

    Parameters
    ----------
    image_size : int
        Image width and height in pixels.

    wx : float
        Horizontal 1/e² beam radius in mm.

    wy : float
        Vertical 1/e² beam radius in mm.

    peak_intensity : float
        Peak simulated intensity, from 0 to 255.

    noise_std : float
        Standard deviation of Gaussian sensor noise.

    pixel_scale : float
        Physical size represented by each pixel, in mm/pixel.

    rng : numpy.random.Generator, optional
        Random number generator used for reproducible noise.

    Returns
    -------
    image : numpy.ndarray
        Synthetic 8-bit grayscale elliptical beam image.
    """

    if rng is None:
        rng = np.random.default_rng()

    wx_pixels = wx / pixel_scale
    wy_pixels = wy / pixel_scale

    x = np.arange(image_size)
    y = np.arange(image_size)

    x_grid, y_grid = np.meshgrid(x, y)

    x_centre = image_size / 2
    y_centre = image_size / 2

    x_squared = (
        x_grid - x_centre
    ) ** 2

    y_squared = (
        y_grid - y_centre
    ) ** 2

    intensity = (
        peak_intensity
        * np.exp(
            -2 * (
                x_squared / wx_pixels**2
                + y_squared / wy_pixels**2
            )
        )
    )

    noise = rng.normal(
        0,
        noise_std,
        size=intensity.shape
    )

    noisy_intensity = (
        intensity + noise
    )

    image = np.clip(
        noisy_intensity,
        0,
        255
    ).astype(np.uint8)

    return image


def main():
    image, w_z = generate_simulated_beam(
        distance=100
    )

    print(
        f"Theoretical 1/e² beam radius at 100 mm: "
        f"{w_z:.4f} mm"
    )


if __name__ == "__main__":
    main()