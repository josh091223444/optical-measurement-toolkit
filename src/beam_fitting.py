import numpy as np 
import cv2
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def gaussian_1d(x, amplitude, centre, sigma, offset):
    """Standard 1D Gaussian function for curve fitting."""
    return amplitude * np.exp(-((x - centre)**2)/ (2 * sigma ** 2)) + offset

def extract_horizontal_profile(gray_image, y_row=None):
    """
    Extract a horizontal intensity slice through the beam.
    If y_row is not given, use the row with the brightest pixel.
   """
    if y_row is None: 
        y_row = np.unravel_index(np.argmax(gray_image), gray_image.shape)[0]

    profile = gray_image[y_row, :].astype(np.float64)
    x_values = np.arange(len(profile))

    return x_values, profile, y_row

def fit_gaussian_profile(x_values, profile):
    """
    Fit a 1D Gaussina to the intensity profile.
    Returns fitted parameters and covariance maxtrix
    """

    amplitude_guess = np.max(profile ) - np.min(profile)
    centre_guess = x_values[np.argmax(profile)]
    sigma_guess = 20
    offset_guess = np.min(profile)

    initial_guess = [amplitude_guess, centre_guess, sigma_guess, offset_guess]

    params, covariance = curve_fit(
        gaussian_1d, x_values, profile, p0=initial_guess
    )

    return params, covariance

def sigma_to_beam_radius(sigma):
    """
    Convert Gaussian standard deviation to the
    1/e^2 intensity beam radius.

    For a Gaussian intensity profile:

        I(x) = I0 * exp(-2 * (x-x0)^2 / w^2)

    the relationship between sigma and the 1/e^2
    beam radius is:

        w = 2 * sigma
    """
    return 2 * sigma

def gaussian_2d(
    coordinates,
    amplitude, 
    x_centre, 
    y_centre,
    sigma_x, 
    sigma_y, 
    offset
):

    """
    Axis-aligned 2D Gaussian function.
    
    Parameters are fitted using the standard Gaussian form:

         I(x, y) = A * exp(
            -((x - x0)^2 / (2 * sigma_x^2)
            - ((y - y0)^2 / (2 * sigma_y^2))
        ) + offset

    Returns a flattened array for scipy.optimize.curve_fit.
"""

    x, y = coordinates

    exponent = (
        ((x - x_centre) ** 2) / (2 * sigma_x ** 2) 
        + (( y - y_centre) ** 2) / (2 * sigma_y ** 2)
    )
    
    gaussian = (

        amplitude * np.exp(-exponent)
          + offset
)

    return gaussian.ravel()


def fit_gaussian_2d(gray_image):
    """
    Fit an axis-aligned 2D Gaussian to a grayscale beam image.

    Returns
    -------
    params : array
        Fitted parameters:
        amplitude, x_centre, y_centre,
        sigma_x, sigma_y, offset

    covariance : array
        Covariance matrix returned by curve_fit.
    """

    image = gray_image.astype(np.float64)

    height, width = image.shape

    y_values, x_values = np.indices(image.shape)

    amplitude_guess = np.max(image) - np.min(image)

    max_y, max_x = np.unravel_index(
        np.argmax(image),
        image.shape
    )

    x_centre_guess = max_x
    y_centre_guess = max_y

    sigma_x_guess = width / 10
    sigma_y_guess = height / 10

    offset_guess = np.min(image)

    initial_guess = [
        amplitude_guess,
        x_centre_guess,
        y_centre_guess,
        sigma_x_guess,
        sigma_y_guess,
        offset_guess
    ]

    lower_bounds = [
        0,
        0,
        0,
        0.1,
        0.1,
        0
    ]

    upper_bounds = [
        255,
        width,
        height,
        width,
        height,
        255
    ]

    params, covariance = curve_fit(
        gaussian_2d,
        (x_values, y_values),
        image.ravel(),
        p0=initial_guess,
        bounds=(lower_bounds, upper_bounds),
        maxfev=20000
    )

    return params, covariance

def sigma_to_beam_radii(sigma_x, sigma_y):
    """
    Convert fitted Gaussian standard deviations to 
    1/e² beam radii
   
    Returns 
    -------

    radius_x, radius_y 
        Horizontal and vertical 1/e² beam radii.

    """
    radius_x = 2 * sigma_x
    radius_y = 2 * sigma_y

    return radius_x, radius_y
    

def main():
    image_path = "data/raw/simulated/beam_300mm.png"

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    x_values, profile, y_row = extract_horizontal_profile(gray_image)

    params, covariance = fit_gaussian_profile(x_values, profile)
    amplitude, centre, sigma, offset = params

    beam_width_pixels = sigma_to_beam_radius(sigma)

    print(f"Row used for profile: {y_row}")
    print(f"Fitted centre: {centre:.2f} pixels")
    print(f"Fitted sigma: {sigma:.2f} pixels")
    print(f"Measured beam width (1/e^2 radius): {beam_width_pixels:.2f} pixels")

    fitted_curve = gaussian_1d(x_values, *params)

    plt.figure(figsize=(8, 5))
    plt.plot(x_values, profile, label="Measured profile", alpha=0.6)
    plt.plot(x_values, fitted_curve, label="Gaussian fit", linewidth=2)
    plt.xlabel("Pixel position")
    plt.ylabel("Intensity")
    plt.title("Beam Intensity Profile with Gaussian Fit")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()


