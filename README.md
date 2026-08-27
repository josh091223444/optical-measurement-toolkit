# Optical Measurement Toolkit

A Python-based optical measurement and validation toolkit for analysing Gaussian laser beam profiles.

The project investigates how accurately beam radius and beam shape can be recovered from simulated intensity images using Gaussian fitting, image processing and numerical analysis.

## Project Objectives

The toolkit was developed to:

- Simulate Gaussian laser beam intensity profiles.
- Model Gaussian beam propagation using the standard beam-radius equation.
- Extract 1D intensity profiles from beam images.
- Fit Gaussian functions to intensity data.
- Fit 2D Gaussian models to complete beam images.
- Calculate 1/e² beam radius in physical units.
- Measure beam ellipticity.
- Compare measured results with theoretical predictions.
- Quantify measurement error and repeatability.
- Investigate the effect of simulated sensor noise on measurement accuracy.

## Project Structure


optical-measurement-toolkit/
│
├── data/
│   └── raw/
│       └── simulated/
│
├── experiments/
│   ├── compare_measured_vs_theory.py
│   ├── uncertainty_analysis.py
│   ├── test_2d_fitting.py
│   ├── test_elliptical_beam.py
│   └── noise_sensitivity.py
│
├── results/
│   ├── beam_measurements.csv
│   ├── uncertainty_measurements.csv
│   ├── noise_sensitivity.csv
│   ├── measured_vs_theoretical.png
│   ├── uncertainty_analysis.png
│   ├── 2d_gaussian_fit.png
│   ├── 2d_gaussian_residual.png
│   ├── elliptical_beam_fit.png
│   ├── elliptical_beam_residual.png
│   ├── noise_radius_error.png
│   └── noise_ellipticity_error.png
│
├── src/
│   ├── beam_simulator.py
│   ├── beam_fitting.py
│   └── metrics.py
│
├── requirements.txt
└── README.md

## Methodology

## Gaussian Beam Simulation

The simulator generates synthetic 2D Gaussian beam intensity distributions using the standard Gaussian beam propagation model.
The theoretical 1/e² beam radius is calculated using:
w(z) = w0 * sqrt(1 + (z / zR)^2)

zR = pi * w0^2 / wavelength
where:
w0 is the beam waist.
w(z) is the beam radius at propagation distance z.
wavelength is the optical wavelength.
zR is the Rayleigh range.
The simulations use millimetres as the physical unit.

For example:
650 nm = 0.00065 mm

## 1D Gaussian Fitting
A horizontal intensity profile is extracted from the beam image and fitted using a 1D Gaussian function.

The fitted Gaussian standard deviation is converted to the 1/e² beam radius using:
w = 2 * sigma

The measured radius is then converted from pixels to millimetres using the assumed pixel calibration.

## 2D Gaussian Fitting
The toolkit also fits a 2D Gaussian model to the complete beam image.

This allows independent measurement of:

Horizontal beam radius wx
Vertical beam radius wy
Beam centre
Beam ellipticity

Ellipticity is calculated as:

ellipticity = wx / wy
A circular beam therefore has an ellipticity close to 1.


Validation Results
Theory vs Measurement
Beam radii were measured at propagation distances of:
100, 200, 300, 400 and 500 mm
The measured results showed approximately 1% agreement with the theoretical Gaussian beam model.
Distance	Measured Radius	Theoretical Radius	Error
100 mm	0.4121 mm	0.4168 mm	1.12%
200 mm	0.8223 mm	0.8291 mm	0.82%
300 mm	1.2302 mm	1.2424 mm	0.98%
400 mm	1.6343 mm	1.6560 mm	1.31%
500 mm	2.0318 mm	2.0696 mm	1.83%

Uncertainty Analysis

At each propagation distance, 20 simulated measurements were performed.

The resulting standard deviations were:

Distance	Standard Deviation
100 mm	±0.0045 mm
200 mm	±0.0047 mm
300 mm	±0.0063 mm
400 mm	±0.0074 mm
500 mm	±0.0083 mm

This provided an estimate of measurement repeatability under the simulated noise conditions.

## 2D Elliptical Beam Validation

A known elliptical Gaussian beam was generated with:

True wx = 1.20 mm
True wy = 0.90 mm

The 2D fitting algorithm recovered:

Measured wx = 1.18 mm
Measured wy = 0.8858 mm

giving errors of:
wx error = 1.66%
wy error = 1.58%

The true ellipticity was:
1.3333

while the measured ellipticity was:

1.3322

corresponding to an ellipticity error of:

0.09%

## Noise Sensitivity

The robustness of the measurement process was investigated by varying simulated sensor noise and performing 20 measurements at each noise level.

Noise levels from 0 to 20 were tested.

At the highest tested noise level:

wx error ≈ 4.13%
wy error ≈ 4.32%
ellipticity error ≈ 0.20%

The experiment showed that absolute beam-radius accuracy decreased as simulated noise increased, while ellipticity remained relatively robust.

## Technologies

Python
NumPy
OpenCV
SciPy
Matplotlib
Pandas
Engineering Skills Demonstrated
This project demonstrates practical experience with:
Optical modelling
Gaussian beam physics
Image processing
Numerical optimisation
Experimental design
Data analysis
Measurement uncertainty
Statistical repeatability
Error analysis
Scientific visualisation
Python development
Reproducible experiments
Limitations

The current validation is based on simulated beam images rather than measurements from a physical laser and camera system.

The pixel scale is therefore an assumed calibration parameter.

The noise model is also simplified and represents Gaussian sensor noise rather than a complete physical camera model.

These limitations are important when interpreting the reported measurement errors.

## Reproducibility

Install the required Python packages using:

python -m pip install -r requirements.txt

Experiments can be run from the project root using Python's module syntax.

Compare measurement with theory

python -m experiments.compare_measured_vs_theory
Uncertainty analysis

python -m experiments.uncertainty_analysis
2D Gaussian fitting

python -m experiments.test_2d_fitting
Elliptical beam validation

python -m experiments.test_elliptical_beam
Noise sensitivity analysis

python -m experiments.noise_sensitivity

Results are saved in the results/ directory.

## Future Development

Potential extensions include:

Experimental camera-image validation.
Improved camera noise modelling.
Automated pixel calibration.
Rotated elliptical beam fitting.
Additional beam-quality metrics.
Automated experiment reporting.
Comparison with experimentally acquired optical data.