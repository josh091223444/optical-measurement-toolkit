import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(image_path):
    image = cv2.imread(image_path)

    if image is None: 
        raise FileNotFoundError(f"Could not load image: {image_path}")

    return image 

def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def calculate_beam_centroid(gray_image):
    intensity = gray_image.astype(np.float64)

    total_intensity = np.sum(intensity)
    if total_intensity == 0:
        raise ValueError("Image contains no measurable intensity.")

    height, width = intensity.shape

    x_coordinates = np.arange(width)
    y_coordinates = np.arange(height)


    x_grid, y_grid = np.meshgrid(x_coordinates, y_coordinates)

    x_centroid = np.sum(x_grid * intensity) / total_intensity
    y_centroid = np.sum(y_grid * intensity) / total_intensity

    return x_centroid, y_centroid

def display_beam_image(gray_image, x_centroid, y_centroid):
    plt.figure(figsize=(8,6))
    plt.imshow(gray_image, cmap="gray")
    plt.scatter(x_centroid, y_centroid, marker="+", s=200)

    plt.title("Laser Beam Intensity Distribution")
    plt.xlabel("Pixel X")
    plt.ylabel("Pixel Y")

    plt.tight_layout()
    plt.show()

def main():
    image_path = "data/raw/simulated/beam_100mm.png"
    image = load_image(image_path)
    gray_image = convert_to_grayscale(image)
    x_centroid, y_centroid = calculate_beam_centroid(gray_image)

    print(f"Beam centre X: {x_centroid: .2f} pixels")
    print(f"Beam centre Y: {y_centroid: .2f} pixels")

    display_beam_image(gray_image, x_centroid, y_centroid)

if __name__ == "__main__":
    main()