# 🏹 Arrow Ballistic Simulator for Archers

**A physics-based arrow flight simulator for barebow and stringwalking archers.**
## 📄 Documentation

| | Italiano | English |
|---|---|---|
| **Introduction** | [📥 PDF](https://raw.githubusercontent.com/CP52/Arrow-balistic-simulator-for-Archers/main/Simulatore_balistico_Introduzione_v9_IT.pdf) | [📥 PDF](https://raw.githubusercontent.com/CP52/Arrow-balistic-simulator-for-Archers/main/Arrow_Ballistic_Simulator_Introduction_v9_EN.pdf) |
| **User Manual** | [📥 PDF](https://raw.githubusercontent.com/CP52/Arrow-balistic-simulator-for-Archers/main/Manuale_Simulatore_Balistico_v9_IT.pdf) | [📥 PDF](https://raw.githubusercontent.com/CP52/Arrow-balistic-simulator-for-Archers/main/Arrow_Ballistic_Simulator_UserManual_v9_EN.pdf) |

Single-file HTML/JS application — no installation, no server, no build step. Open in any browser.

---

## What it does

Given your arrow, bow, biometric and environmental parameters, the simulator:

- Computes the **optimal launch angle** to hit a target at a given distance and height
- Plots the **real trajectory** (with aerodynamic drag) vs. the ideal parabola and the sight line
- Generates a **sight mark table** with riser projection values for each distance
- Exports a **printable 1:1 PDF sight scale** with calibration rulers (verify 100% print scale)
- Exports data as **CSV** for further analysis in Excel or similar tools
- Generates a **stringwalking table**: for each distance, how many mm to walk
  down the string from the nock to hit the target — with the physics explained

Multilingual interface: 🇮🇹 IT · 🇬🇧 EN · 🇪🇸 ES · 🇫🇷 FR · 🇩🇪 DE  
Unit systems: metric (m / cm / m/s / J) and imperial (yd / in / ft/s / ft·lb)

---

## Physics model

Arrow flight is integrated using an **adaptive 4th-order Runge-Kutta (RK4)** method with automatic step-size control (error tolerance ~10⁻⁶ m).

**Aerodynamic drag** is computed from a Reynolds-number-dependent Cᴅ model with four modes:
- Laminar (low Re)
- Turbulent (high Re)
- Auto (Re-dependent transition)
- Transition scenario (mixed boundary layer)

Reference data from JAXA/MSBS wind tunnel measurements (Ortiz Enriquez doctoral thesis, UEC Tokyo 2021).

**Additional physical effects modelled:**
| Effect | Implementation |
|--------|---------------|
| Air density | CIPM-2007 formula (temp, pressure, humidity, altitude) |
| Altitude correction | ISA lapse rate for pressure and temperature |
| Wind | Lateral force model on arrow cross-section |
| Nocking point offset | Converts mm offset → angular deflection from arrow geometry |
| FOC influence | Drag penalty for FOC > 10% (stability/drag trade-off) |
| Postural correction | Iterative launch height update during T-stance rotation |
| Sight projection | Parallax geometry (eye–nock–riser triangle) |
| Stringwalking | Grip point ≡ dynamic nocking offset: gripMm = tan(α) × restToCock × 1000 |

---

## Parameters

### Arrow
| Parameter | Unit | Description |
|-----------|------|-------------|
| Mass | g / gr | Total assembled arrow weight |
| Length | m / in | Nock to tip |
| Diameter | mm / in | Shaft outer diameter |
| Spine | — | Shaft stiffness rating |
| Tip weight | g / gr | Point weight (influences FOC) |
| Balance point | m / in | Distance from nock to balance (FOC calculation) |
| Tip type | — | Standard / Broadhead / Blunt (affects Cᴅ) |
| Fletching | — | Type and size of vanes/feathers |

FOC is calculated automatically. Optimal range: **7–15%** (10–12% recommended for field).

### Bow
| Parameter | Unit | Description |
|-----------|------|-------------|
| Draw force | lb | Peak draw weight at your draw length |
| Draw length | m / in | Full draw distance |
| Brace height | m / in | String-to-riser gap at rest |
| Nocking offset | mm | Vertical nock point offset from perpendicular |
| Bow type | — | Longbow / Recurve / Compound (sets default efficiency) |
| Efficiency | 0–1 | Energy transfer ratio (auto-set by type) |

Typical efficiencies: Longbow ~73%, Recurve ~84%, Compound ~89%.

### Archer biometrics
- **Neutral launch height (m):** Arrow tip height with horizontal T-stance
- **Pelvis height (m):** Pivot point of the T-rotation (approx. navel)
- **Anchor length (m):** Shoulder-to-anchor distance (effective arm of the T)
- **Postural correction:** Iteratively adjusts launch height as aim angle changes

### Target
- **Distance (m/yd):** Horizontal distance to target centre
- **Height (m/in):** Target centre height above archer foot level (negative = downhill)
- **Measured v₀:** Override calculated velocity with chronograph measurement

### Environment
| Parameter | Effect |
|-----------|--------|
| Wind (m/s or ft/s) | Positive = tailwind, negative = headwind |
| Temperature | Air density |
| Pressure | Air density |
| Humidity | Air density (CIPM-2007) |
| Altitude | Corrects pressure and temperature via ISA model |

### Sight geometry
- **Eye–nock (m/in):** Vertical distance eye to arrow nock at full draw
- **Nock–riser (m/in):** Horizontal distance nock to riser plane
- **Distance range & step:** Controls the sight mark table

### Stringwalking/Under nock
- **Eye–nock (cm):** Set to 2–3 cm for stringwalking or less for under nock (vs. 10–15 cm for
  Mediterranean grip). This affects Sight tab projection only, not Stringwalking
  tab calculations.

---

## Outputs

### Summary metrics
After simulation: aim angle, initial velocity, flight time, max height, drop at target, max range with optimal angle.

### Charts (interactive, hover for values)
- **Trajectory:** Real (drag), ideal (no drag), sight line
- **Velocity:** Total, Vx, Vy components
- **Energy:** Residual kinetic energy percentage
- **Drop:** Arrow drop in cm/in per distance
- **Stringwalking:** Grip point (mm) per distance — how far below the nock to grip the string to hit the target.

### Sight mark table
For each distance: drop, riser projection, residual energy, residual velocity.  
The visual scale on the right shows mark positions graphically.  
A green dot marks the laser-at-30m reference (≈ eye–nock distance, geometrically exact beyond ~20 m).

### Stringwalking table 🤞
For each distance: grip point in mm below the nock, launch angle, residual
energy, residual velocity.
Positive value = walk down the string. Negative = above the nock (rare,
only at very short distances).
The row corresponding to the current target distance is highlighted in yellow.

### PDF export
- Full sight table
- 1:1 visual scale (riser marks actual size)
- Two 5 cm calibration rulers (vertical + horizontal) anchored at the scale zero — place a real ruler on the printout to verify 100% scale

### CSV export
Copy to clipboard or download. Compatible with Excel, LibreOffice Calc, etc.

---

## How to use it

### 🌐 Online (recommended)
Open directly in your browser:
**https://arrow-sim.vercel.app**
Works on PC, Mac, iPhone, Android and tablet — no installation required.

### 💾 Offline — standalone version
Download the file:
**`arrow_ballistic_simulator_v9_i18n_offline.html`**
Open it with any modern browser (Chrome, Firefox, Safari, Edge).
Works completely offline from the very first use — no internet connection needed.
Ideal for field use, via AirDrop, Files or USB drive.

### 🔧 Base version (for developers)
The file `arrow_ballistic_simulator_v9_i18n.html` is the main source.
Requires an internet connection on first launch to download React and jsPDF from CDN.
After the first load it works offline.

### 📱 iPhone / iPad
- **Option 1 (recommended):** open https://arrow-sim.vercel.app in Safari →
  tap Share → **Add to Home Screen** for a dedicated icon.
- **Option 2:** download `arrow_ballistic_simulator_v9_i18n_offline.html`,
  open it in Safari from Files — works without internet.
---

## 💬 Feedback & Community

- **Bug or problems:** open an [Issue](https://github.com/CP52/Arrow-balistic-simulator-for-Archers/issues)
- **Questions and Discussions:** use [Discussions](https://github.com/CP52/Arrow-balistic-simulator-for-Archers/discussions)
- **Email:** only for private matters — c.pagura@outlook.it

## Technical notes

- **Integration:** Adaptive RK4, step control via Richardson extrapolation, tolerance 10⁻⁶ m
- **Drag model:** Re-dependent Cᴅ with 7 transition zones; corrected for FOC and fletching type
- **Sight projection:** Full parallax geometry, not the simplified "eye–nock ≈ constant" approximation
- **Nocking offset:** Converts mm vertical offset to launch angle offset via arrow geometry (atan2)
- **No build step:** Pure HTML + vanilla JS + React (CDN) + jsPDF (CDN)
- **Single file:** ~1,800 lines, self-contained, no server required
- **Stringwalking:** grip point calculated by equivalence with nocking offset:
  gripMm = tan(α) × restToCock × 1000, where α is the RK4 optimal angle
---

## Limitations

- 2D trajectory only (no lateral wind drift, no gyroscopic effects from spin)
- Arrow treated as rigid body (no spine oscillation / archer's paradox)
- Energy calculation uses simplified bow efficiency (no measured draw curve)
- Magnus effect not modelled (negligible below ~1,500 RPM for field archery)
- Stringwalking model simplified: does not account for spine effects or residual vertical string force component (negligible for field archery angles)
---

## References

**Arrow aerodynamics & ballistics**
- Klopsteg, P.E. (1943). Physics of Bows and Arrows. *Am. J. Physics* 11(4).
- Park, J.L. (2011). The Aerodynamics of Archery Arrows. *Proc. IMechE Part P* 225(2).
- Ortiz Enriquez, R. (2021). *Arrow aerodynamics study*. Doctoral thesis, UEC Tokyo / JAXA MSBS.

**Aerodynamic drag & Reynolds**
- Hoerner, S.F. (1965). *Fluid-Dynamic Drag*. Hoerner Fluid Dynamics.
- Schlichting, H. & Gersten, K. (2017). *Boundary-Layer Theory*. 9th ed., Springer.

**Numerical methods**
- Press et al. (2007). *Numerical Recipes*. 3rd ed., Cambridge University Press.

**Atmospheric model**
- Picard et al. (2008). Revised formula for density of moist air (CIPM-2007). *Metrologia* 45(2).
- ISO 2533:1975 Standard Atmosphere.

---

## Authors

Developed by **Cesare Pagura** with **Claude** (Anthropic).  
Padova, Italy — 2025/2026

---

## License

Released for personal and educational use. No warranty. Attribution appreciated.
