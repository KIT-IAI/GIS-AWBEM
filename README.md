
[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![EnergyPlus](https://img.shields.io/badge/EnergyPlus-25.1-green)](https://energyplus.net/)
[![Paper](https://img.shields.io/badge/Paper-IEEE-red)](https://ieeexplore.ieee.org/document/11457217)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 


# GIS-AWBEM

GIS-based Automated White-Box Building Energy Modeling (GIS-AWBEM) is an open-source framework for conducting district-scale building energy analysis. Starting from publicly available GIS data, the framework automatically constructs Level of Detail 1 (LOD1) 3D building models.

This framework is primarily developed for urban planners, building energy analysts, energy suppliers, researchers, and scientists.

---

# Motivation

Studying urban district energy transitions requires flexible and detailed building-specific energy performance analysis. Many existing tools and workflows simplify either the building envelope characteristics or the HVAC system representation.

GIS-AWBEM was developed to address these limitations by:

1. Employing a dynamic white-box modeling approach that includes detailed building physics and thermal mass properties
2. Providing detailed HVAC system models for the design and performance evaluation of specific energy systems
3. Using a single building energy simulator, EnergyPlus, thereby avoiding the need for multiple software integrations and interface developments
4. Offering a modular structure that requires only minor reconfiguration for future implementations
5. Being fully open-source, eliminating the dependency on commercial software
---

# Workflow

<img src="img/Workflow.svg">


---

# Repository Structure

```
GIS-AWBEM/
├── LICENSE.md                          # MIT license
├── README.md                           # Project overview and installation
├── pyproject.toml                      # Python package configuration
│
├── img/
│   └── Workflow.svg                    # Framework pipeline diagram
│
├── examples/
│   ├── Example 1/
│   │   └── run_example1.py             # Demo run script (single building)
│   └── Example 2/
│       └── run_example2.py             # Demo run script (district)
│
├── GIS-AWBEM/                          # Core framework package
│   ├── src/
│   │   └── GIS_AWBEM/
│   │       ├── __init__.py
│   │       ├── Run.py                  # Main entry point
│   │       ├── pre_process.py          # GIS parsing & geometry construction
│   │       ├── EP.py                   # EnergyPlus interface
│   │       ├── Gen_IDF_IdealHVAC.py    # IDF generator — ideal HVAC system
│   │       ├── Gen_IDF_Boiler_DXcoil.py# IDF generator — boiler + DX coil
│   │       ├── Gen_IDF_PTHP.py         # IDF generator — packaged terminal heat pump
│   │       ├── Simulate.py             # Simulation runner (district loop)
│   │       ├── post_process.py         # Results extraction & processing
│   │       └── utilities.py            # Shared helper functions
│   └── readme.md
│
└── GIS-AWBEM/Inputs/                   # Input data files
    ├── Bergwald.geojson                 # Example GIS footprint data
    ├── Bergwald_truncated.geojson       # Truncated version of above
    ├── Bergwald_enrich.csv              # Enrichment attributes for Bergwald
    ├── Heidelberg.geojson               # GIS footprint data — Heidelberg
    ├── Tabula_Uvalues.csv               # TABULA U-values reference table
    ├── Internal gain profiles.xlsx      # Occupancy & internal gain schedules
    ├── Mannheim_04177.epw               # EnergyPlus weather file — Mannheim
    ├── Rheinstetten_04177.epw           # EnergyPlus weather file — Rheinstetten
    │
    └── HUB4LCA/                        # Building envelope data (HUB4LCA database)
        │                               # Keyed by: use type / climate zone /
        │                               # construction period / construction type
        ├── Residential/
        │   ├── AB/                     # Apartment blocks       (41 .xlsx files)
        │   ├── MFH/                    # Multi-family houses    (444 .xlsx files)
        │   └── SFH/                    # Single-family houses   (468 .xlsx files)
        ├── Culture/                    # (2 .xlsx files)
        ├── Education/                  # (2 .xlsx files)
        ├── Health/                     # (1 .xlsx file)
        ├── Hospitality/                # (9 .xlsx files)
        ├── Industrial/                 # (1 .xlsx file)
        ├── Office/                     # (4 .xlsx files)
        └── Retail/                     # (5 .xlsx files)
```


---

# Getting Started

Clone the repository:

```bash
git clone https://github.com/KIT-IAI/GIS-AWBEM.git
```

Install the package in editable mode:

```bash
pip install -e GIS-AWBEM
```


---

# Examples

Two examples are provided to demonstrate the main functionalities of the framework:

- **Example 1** models a district with an enrichment process for building envelope data
- **Example 2** models a district without enrichment

In both examples, multiple HVAC systems can be applied.

---

<details>

<summary><strong>Example 1</strong></summary>

# District in Karlsruhe

This example models the **Bergwald** district (48.9723° N, 8.4648° E), which contains **241 buildings**.

The following sections describe how to collect the required input data and run the simulation.

---

## 1. Collect Geospatial Data from OpenStreetMap (OSM)

Geospatial data must be queried from OpenStreetMap using Overpass Turbo:

https://overpass-turbo.eu/#

Set the bounding box around the district and run the following query:

```text
[out:xml][timeout:25];
(
  way["building"]({{bbox}});
  relation["building"]({{bbox}});
);
out body;
>;
out skel qt;
```

Export the result as a GeoJSON file (e.g., `Bergwald.geojson`) and place it inside the `Inputs` directory.

If missing building-level values are detected (e.g., in `District_geo.csv`), they should preferably be corrected manually using tools such as Google Earth. Otherwise, missing values will be replaced with the district mean values.

---

## 2. Weather Data

Weather data should be obtained from the German Weather Service (DWD) using the station closest to the district, i.e., **Rheinstetten**.

https://www.dwd.de/EN/Home/home_node.html

The weather file must use the EnergyPlus weather format (`.epw`).

---

## 3. Internal Gains and Setpoint Temperatures

Daily schedules for internal gains/losses and setpoint temperatures are provided in:

```text
Inputs/Internal gain profiles.xlsx
```

---

## 4. TABULA U-values

The overall heat transfer coefficients (U-values) for external walls, floors, roofs, and windows are adapted from the TABULA WebTool:

https://webtool.building-typology.eu/#bm

Wall, floor, and roof U-values are only used when enrichment is **not** enabled.

---

## 5. Enrichment

Building heights, archetypes, and construction years are enriched using the following ETHOS.BUILDA datasets:

### Building Heights

https://zenodo.org/records/11845992

### Archetypes and Construction Years

https://zenodo.org/records/12069755

The enriched data are stored in:

```text
Bergwald_enrich.csv
```

Material properties, as well as layer numbers and thicknesses, are adapted from HUB4LCA:

https://hub4lca.e3d.rwth-aachen.de/

If a different enrichment methodology is required, modify the `enrich()` function in `pre_process.py` accordingly.

---

## 6. Simulation Configuration

After collecting all required input data, configure the `enrich` and `config` dictionaries in `run.py`.

The following HVAC systems are currently supported:

- Ideal HVAC
- Boiler and DX coil
- Packaged Terminal Heat Pump

Further details are available in the following publication:

https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=11457217

---

## 7. Results

An overall district performance summary is printed to the Python console.

Depending on the selected HVAC system, transient HVAC component results are stored in the `Results` directory for detailed analysis.

Additional output variables can be added in `post_process.py` if required.

Available EnergyPlus output variables are listed in the *Input Output Reference*:

https://energyplus.net/assets/nrel_custom/pdfs/pdfs_v26.1.0/InputOutputReference.pdf

</details>

---

<details>

<summary><strong>Example 2</strong></summary>

# District in Heidelberg

This example models a district in the southern area of Heidelberg (49.37386° N, 8.68910° E), containing **58 buildings**.

---

## 1. Collect Geospatial Data from OpenStreetMap (OSM)

Geospatial data must be queried from OpenStreetMap using Overpass Turbo:

https://overpass-turbo.eu/#

Set the bounding box around the district and run the following query:

```text
[out:xml][timeout:25];
(
  way["building"]({{bbox}});
  relation["building"]({{bbox}});
);
out body;
>;
out skel qt;
```

Export the result as a GeoJSON file (e.g., `Heidelberg.geojson`) and place it inside the `Inputs` directory.

If missing building-level values are detected (e.g., in `District_geo.csv`), they should preferably be corrected manually using tools such as Google Earth. Otherwise, missing values will be replaced with the district mean values.

---

## 2. Weather Data

Weather data should be obtained from the German Weather Service (DWD) using the closest station, i.e., **Mannheim**.

https://www.dwd.de/EN/Home/home_node.html

The weather file must use the EnergyPlus weather format (`.epw`).

---

## 3. Internal Gains and Setpoint Temperatures

Daily schedules for internal gains/losses and setpoint temperatures are provided in:

```text
Inputs/Internal gain profiles.xlsx
```

---

## 4. TABULA U-values

The overall heat transfer coefficients (U-values) for external walls, floors, roofs, and windows are adapted from the TABULA WebTool:

https://webtool.building-typology.eu/#bm

---

## 5. Enrichment

This example does not include an enrichment process.

---

## 6. Simulation Configuration

After collecting all required input data, configure the `enrich` and `config` dictionaries in `run.py`.

The following HVAC systems are currently supported:

- Ideal HVAC
- Boiler and DX coil
- Packaged Terminal Heat Pump

Further details are available in the following publication:

https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=11457217

---

## 7. Results

An overall district performance summary is printed to the Python console.

Depending on the selected HVAC system, transient HVAC component results are stored in the `Results` directory for detailed analysis.

Additional output variables can be added in `post_process.py` if required.

Available EnergyPlus output variables are listed in the *Input Output Reference*:

https://energyplus.net/assets/nrel_custom/pdfs/pdfs_v26.1.0/InputOutputReference.pdf

</details>

---

# Minimum Required Data

- Geospatial data from OpenStreetMap in GeoJSON format
- Daily profiles for internal gains/losses and setpoint temperatures
- EnergyPlus weather data file (`.epw`)
- Overall heat transfer coefficients based on TABULA building archetypes

Please refer to **Example 2** for a minimum-data simulation workflow.

---

# Requirements

## Python Packages

- numpy
- pandas
- utm
- eppy
- sympy
- openpyxl

## Energy Simulator

- EnergyPlus 25.1

---

# Acknowledgment

We acknowledge the financial support of the Helmholtz Association of German Research Centres (HGF) within the framework of the Program-Oriented Funding POF IV under the Energy System Design (ESD) program.

---

# License

The GIS-AWBEM framework is developed and released by the Institute for Automation and Applied Informatics, Karlsruhe Institute of Technology, under the [MIT License](https://github.com/KIT-IAI/GIS-AWBEM/blob/main/LICENSE.md).

---

# How to Cite

```bibtex
@article{GIS-AWBEM2026,
  author={Tajalli-Ardekani, Erfan and Cheng, Haozhen and Kocher, Alexander and Kovačević, Jovana and Waczowicz, Simon and Çakmak, Hüseyin K. and Delibra, Giovanni and Corsini, Alessandro and Hagenmeyer, Veit},
  booktitle={2026 Open Source Modelling and Simulation of Energy Systems (OSMSES)},
  title={GIS-AWBEM: GIS-based Automated White-Box Building Energy Modeling},
  year={2026},
  pages={1-6},
  keywords={HVAC;Three-dimensional displays;Heat pumps;Computational modeling;Atmospheric modeling;Buildings;Urban planning;Ventilation;Computational efficiency;Glass box;Building Energy Modeling;District Energy Modeling;HVAC;Automated Framework;EnergyPlus},
  doi={10.1109/OSMSES69376.2026.11457217}
}
```
