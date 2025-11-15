# Propeller Optimizer: Quick Empirical Design for High-Speed Vessels 🚀

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Marine Engineering](https://img.shields.io/badge/Marine-Engineering-blue)](https://github.com/JasonMa6602/propeller-optimizer)

## Overview

High-speed patrol boat propeller design can be challenging—balancing ventilation, efficiency, and thrust. This tool provides a **fast empirical workflow** that skips lengthy CFD simulations:

- **Savitsky formula** for speed prediction
- **Gawn-Burrill series** for propeller optimization
- **Iterative refinement** (2000+ simulations for stability)
- **CSV-based decision rules** for propeller type selection

Based on a real **13.5m patrol boat** achieving **58 knots** with **9.72t displacement**.

### Key Features

- **Diameter (D) Sizing**: Automated calculation using CSV rules (D ≤ draft)
- **P/D Optimization**: Pitch-to-diameter ratio optimization for high-speed performance
- **KT/KQ/η Calculations**: Thrust coefficient, torque coefficient, and efficiency
- **Iteration Engine**: 2000+ simulations for parameter stability
- **Surface Propeller Focus**: Arneson-style surface-piercing propellers
- **No Heavy Dependencies**: Runs anywhere with basic Python installation

### Why This Tool?

Traditional CFD-based propeller design can take **weeks**. This tool provides preliminary designs in **hours**, achieving up to **28% efficiency gains** through systematic optimization.

Perfect for:
- Marine engineers doing preliminary propeller selection
- Naval architects in early design phases
- Students learning propeller design principles
- Boat builders evaluating propeller options

## Quick Demo: 13.5m Patrol Boat
Vessel: 13.5m LOA, 2.96m beam, 0.65m draft, twin VOLVO D12-715 (1430hp@2300rpm), 1.03:1 ratio.

### Why Surface Props?
Ventilation cuts drag at high speeds (Fn_b≈4.2), but KT/KQ needs precision. Pain? CFD weeks—we do prelims in hours.

### Workflow Steps
1-2. **Speed Validation** (Savitsky): Predicted 57.8 knots (spot-on!).
3-4. **D & Ratio**: D=0.6m (<draft), rpm=2233 (safe).
5. **Core Params** (J=1.27, high-J opt):

| Parameter | Value | Highlight |
|-----------|-------|-----------|
| **D** | 0.6m | Balances ventilation, 16-18" std |
| **P/D** | 1.50 | High-RPM low-load match |
| **KT** | 0.144 | 14% margin, ventilation boost |
| **KQ** | 0.041 | Power at 1045kW |
| **η** | 0.707 | 0.5-0.72 sweet spot |

6-7. **Blade + Iteration**: MAU type (V≥28kt trigger), +28% eff via KT-J curves.
8. **Sensitivity**: P/D tweak → KT+12%, balance holds.

Thrust T=23.3kN > R=22.1kN (5% margin). Prototype-ready!

## Setup & Usage
1. Clone: `git clone https://github.com/JasonMa6602/propeller-optimizer.git`
2. Install: `pip install -r requirements.txt`
3. Run: `python src/optimizer.py --vessel patrol_boat`
4. Or Jupyter: Open `examples/patrol_boat_demo.ipynb`.

### Example Output

```
Optimization Complete:
D: 0.60 m
P/D: 1.50
KT: 0.144, KQ: 0.041, η: 0.707
Efficiency Gain: +28% (4 iterations)
```

## Technical Background

### Savitsky Formula
The tool uses the Savitsky planing hull formula for speed prediction:
```
V = √(2Δg / (ρ·C_L·B·λ))
```
Where:
- Δ = displacement volume
- g = gravitational acceleration
- ρ = water density
- C_L = lift coefficient
- B = beam width
- λ = length-to-beam ratio

### Gawn-Burrill Series
Empirical propeller series for surface-piercing propellers, providing KT and KQ coefficients based on:
- Advance ratio (J)
- Pitch-to-diameter ratio (P/D)
- Blade area ratio (EAR)
- Number of blades (Z)

### CSV Rules Engine
The `/data/` folder contains decision rules for propeller selection:
- **Cavitation criteria**: σ < 0.12 triggers special propeller types
- **Speed thresholds**: V ≥ 28 knots selects MAU-type propellers
- **Efficiency limits**: Automatic fallback to conservative designs
- **Diameter constraints**: D_max = min(0.6, V/(0.12σ))

## Project Structure

```
propeller-optimizer/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
├── data/
│   └── propeller_type.csv       # Propeller selection rules
├── src/
│   ├── __init__.py
│   └── optimizer.py             # Core optimization engine
├── tests/
│   └── test_optimization.py     # Unit tests
└── examples/
    └── (Jupyter notebooks)      # Interactive examples
```

## Workflow Steps Explained

### Step 1-2: Speed Validation
Uses Savitsky formula to predict planing hull speed based on vessel characteristics.

### Step 3-4: Diameter & RPM Selection
- Calculates maximum diameter based on draft and cavitation number
- Determines propeller RPM from engine specifications and gear ratio

### Step 5: Core Parameter Calculation
- Computes advance ratio (J = Va / nD)
- Calculates required thrust coefficient (KT)
- Optimizes pitch-to-diameter ratio (P/D)

### Step 6-7: Iteration & Refinement
- Runs 2000+ Monte Carlo simulations
- Refines KT, KQ, and efficiency (η)
- Validates against empirical data

### Step 8: Sensitivity Analysis
- Tests parameter variations (±10%)
- Ensures robust design
- Validates thrust-resistance balance

## Future Enhancements

Planned features for future versions:
- [ ] Wageningen B-series propeller support
- [ ] Interactive GUI using Streamlit
- [ ] KT-J and KQ-J curve plotting
- [ ] Export to CAD formats
- [ ] Multi-propeller optimization
- [ ] Integration with vessel resistance calculators
- [ ] GitHub Actions for automated testing

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

Suggested contributions:
- Add more propeller series (Wageningen, Au, etc.)
- Create visualization tools
- Improve optimization algorithms
- Add more test cases
- Improve documentation

## References

- Savitsky, D. "Hydrodynamic Design of Planing Hulls"
- Gawn, R.W.L. "Effect of Pitch and Blade Width on Propeller Performance"
- Burrill, L.C. "Surface Piercing Propellers"
- Arneson Surface Drive documentation

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Disclaimer

This is an **initial assessment tool** for preliminary propeller design. Always consult professional marine engineers and conduct proper model testing before manufacturing. The authors assume no liability for designs based on this tool.

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/JasonMa6602/propeller-optimizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JasonMa6602/propeller-optimizer/discussions)

---

**Tags**: #MarineEngineering #PropellerDesign #HighSpeedBoats #NavalArchitecture #Python #OpenSource

*Built with passion for marine engineering excellence* 🌊⚓
