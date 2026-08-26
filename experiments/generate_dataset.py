import cv2
import os
from src.beam_simulator import generate_simulated_beam

distances_mm = [100, 200, 300, 400, 500]  # 10cm to 50cm

output_dir = "data/raw/simulated"
os.makedirs(output_dir, exist_ok=True)

results = []

for distance in distances_mm:
    image, w_z = generate_simulated_beam(distance=distance)
    filename = f"{output_dir}/beam_{distance}mm.png"
    cv2.imwrite(filename, image)
    results.append((distance, w_z))
    print(f"Saved {filename} — theoretical width: {w_z:.4f} mm")