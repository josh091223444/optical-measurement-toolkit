Laser Beam Characterisation & Optical Measurement Toolkit 

Joshua Ojo  23/08/26

1.Summary 


I built a an optical measurment toolkit which analyses a laser beam image, measure its intesity profile and beam width, and compare measurements  across diffrent distances. Due to hardware constraints, beam images were gennerated syntheitcally using physics of Gaussian beam propagation, allowing the analysis pipeline to be validated against a known ground truth. The measured beam width agreed with theoretical predictions to within approximately 1%, demonstrating that the toolkit accurately recovers physical beam parameters from noisy image data.


2.Introduction 

A Gaussian laser beam is a beam of light whose intensity distribution follows a bell-shaped curve across its width, being brightest at the centre and falling off smoothly towards the edges. Accurately measuring beam width and how it changes with propagation distance is a fundamental part of characterising laser performance  a step required when developing and testing prototype laser systems, verifying they meet design specifications, and diagnosing issues during assembly. This is particularly relevant to applications such as coupling laser light into photonic crystal fibres, where precise beam size and divergence directly affect coupling efficiency. This project aimed to build a software toolkit capable of measuring beam width from an image and tracking its change across distance, with the analysis pipeline validated against the known physics of Gaussian beam propagation.


3.Methodology

3.1 Software Pipeline 

The toolkit processes each beam image through the following stages: 

1. Image loading and grayscale conversion: 

The image is loaded and converted to a single channel grayscale array, where pixel value represents light intensisty. 

2. Beam centroid calculation: 

the intensity weighted centre of the beam is calculated across the full 2D image, giving the beam's (x,y) position.


3. Horizontal intensity profile extraction:

a 1D slice of pixel intensity is taken through the row containing the brightest point, giving an intensity vs position profile across the beam.

4. Gaussian curve fitting: 

this profile is fitted to a 1D Gaussian function using scipy.optimize.curve_fit, returing the beams fitted centre, width(sigma), amplitude and background offset.

5. Pixel to millimetere calibration:

the fittted width measured in pixels is converted to physical unites using a known pixel scales

6. Repeated measurment for uncertainty estimation: 

for each propagation distance, the measurments was repeated 20 times with independent noise realisations, and the mean and standard deviation of the measured width were caculcated to quantify repeatability. 

This pipeline was designed to mirror what would be applied to a real photographed laser beam the only difference for this project was the source of the input image (see Section 3.2).

Image → Grayscale → Centroid → 1D Profile → Gaussian Fit → mm Calibration → Repeated Measurement → Statistics

3.2 Note on Data Source 

Due to hardware constraints, a physical laser was not available during this project. To validate the analysis software, beam images were instead generated synthetically using the standard Gaussian beam propagation equation:
w(z) = w0 · √(1 + (z/z_R)²)

where z_R = π·w0²/λ is the Rayleigh range. Realistic sensor noise was added to each simulated image to approximate the noise present in a real camera measurement.

This approach allowed the analysis pipeline — grayscale conversion, centroid calculation, Gaussian fitting, and calibration — to be tested against a known ground truth, since the true beam width at each distance was defined by the simulation parameters rather than measured independently. This is a standard validation technique in optical and measurement engineering: confirming an analysis method correctly recovers known inputs before applying it to real, uncontrolled data. The natural next step, given access to a laser, would be to apply this same pipeline directly to photographed beam images.


3.3 Parameters Used

Parameter	Value
Beam waist (w0)	0.05 mm
Wavelength	0.00065 mm (650 nm)
Pixel scale	0.05 mm/pixel
Noise standard deviation	5 (8-bit intensity units)
Distances tested	100, 200, 300, 400, 500 mm
Repeats per distance	20


4. Results 

4.1 Measured vs Theoretical Beam Width 

Distance (mm)	Mean Measured Width (mm)	Std Dev (mm)	Theoretical Width (mm)	Difference (%)
100	0.4126	0.0034	0.4168	1.0%
200	0.8185	0.0048	0.8291	1.3%
300	1.2280	0.0065	1.2424	1.2%
400	1.6399	0.0087	1.6560	1.0%
500	2.0474	0.0113	2.0696	

4.2 Example Fitted Profile 

5. Discussion 

Overall agreement 

Across all five propagation distances, measured beam widths agreed with theoretical predictions to within approximately 1%. This level of agreement indicates that the analysis pipeline from image loading through Gaussian fitting to physical calibration correctly recovers known beam parameters from noisy image data. Since the simulated images included realistic sensor noise, this result validates not just the underlying mathematics but the robustness of the fitting process under imperfect measurement conditions, which is a reasonable proxy for how the pipeline would perform on real photographed data.

Systematic bias 

Interestingly, the measured width consistently underestimated the theoretical value by a small, fairly constant margin (approximately 1.0–1.3%) at every distance tested, rather than the discrepancy growing as the beam became larger. This suggests the source of the bias is not distance-dependent but instead relates to the fitting method itself. A likely explanation is that beam width was estimated from a single 1D horizontal slice through the beam's brightest row, rather than from a fit across the full 2D intensity distribution — a single-row profile is more sensitive to local noise near the peak and may slightly underrepresent the true Gaussian width compared to a full 2D fit. It's also possible that the background offset term in the fit, which absorbs some of the noise floor, interacts with how tightly curve_fit weights the beam's outer edges, where intensity is lowest and most affected by noise. Because the bias was small and consistent rather than distance-dependent, it is best interpreted as a limitation of the specific fitting method used, rather than an error in the underlying physical model.

Limitations 

This project has several limitations that should be addressed before applying the pipeline to real laser measurements. Most significantly, all data used was generated synthetically rather than measured from a physical laser, due to hardware constraints during the project timeframe; while this allowed rigorous validation against known physics, it does not capture real-world effects such as camera lens distortion, sensor non-linearity, ambient light contamination, or beam profile asymmetries that a genuine physical setup would introduce. Additionally, beam width was measured using a single horizontal intensity profile rather than a full 2D Gaussian fit, which — as discussed above — likely contributes to the small systematic bias observed; a full 2D fit would be a natural improvement. Finally, the noise model used (independent Gaussian noise per pixel) is a simplification of real camera noise, which often includes structured components such as fixed-pattern noise or shot noise that scales with signal intensity.

6. Conclusion 

This project demonstrated the development of a complete optical measurement pipeline capable of extracting a laser beam's width from an image and validating those measurements against known Gaussian beam physics. Working through image processing, Gaussian curve fitting, physical calibration, and uncertainty quantification gave hands-on experience with the type of experimental analysis and data interpretation skills required to support the development and testing of prototype laser systems from writing robust measurement software to identifying and explaining systematic effects in the results, as demonstrated in the discussion of fitting bias and uncertainty scaling above.

The clearest next step for this project is validating the same pipeline against a real, photographed laser beam. Because the software pipeline was built to be identical regardless of whether the input image comes from simulation or a physical camera, this would require no changes to the underlying code only a genuine laser measurement to test it against. This would allow direct comparison between simulated and real-world performance, including the influence of practical factors such as camera noise, lens artefacts, and beam alignment, which the current simulation could not capture.


More broadly, this project reflects a methodical, evidence-based approach to problem solving: building a tool, testing it against a known standard before trusting its results, and being explicit about its current limitations a mindset directly applicable to developing and troubleshooting laser systems in a real engineering environment.

7.appendix 

Repository Structure 

optical-measurement-toolkit/
├── data/raw/simulated/       # Generated beam images
├── src/
│   ├── beam_simulator.py     # Gaussian beam physics + image generation
│   ├── beam_analysis.py      # Image loading, centroid calculation
│   └── beam_fitting.py       # 1D Gaussian curve fitting
├── experiments/
│   ├── generate_dataset.py
│   ├── compare_measured_vs_theory.py
│   └── uncertainty_analysis.py
├── results/                  # Output plots
└── reports/                  # This report


Key Equations 

Gaussian beam width as a function of propagation distance:
w(z) = w0 * sqrt(1 + (z / z_R)^2)

Rayleigh range: 
z_R = (pi * w0^2) / wavelength