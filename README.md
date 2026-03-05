# GIS-AWBEM
GIS-based Automated White-Box Building Energy Modeling (GIS-AWBEM) is a framework for conducting building energy analysis at the district level. This open-source framework is developed mainly for urban planners, building energy analysts, energy suppliers, and related researchers and scientists. The framework provides an automated white-box modelling technique through a bottom-up approach to construct a detailed model of the building envelope and energy-supplying system. Starting from publicly available GIS data, the framework constructs a 3D model of buildings at Level of Detail (LOD) 1, equipping them with explicit Heating, Ventilation, and Air Conditioning (HVAC) systems, and upscaling the model from a single building to all district buildings.

<img width="980" height="802" alt="image" src="https://github.com/user-attachments/assets/d5dfc1f8-031d-4600-b6a6-b2ae0d0e3bef" />

# Motivation
Studying urban district energy transitions requires a flexible and detailed building-specific energy performance analysis. Many existing tools and workflows simplify the complexities of either building envelope details or implementing an ideal HVAC system. Therefore, a GIS-AWBEM is developed where it:
1) employs a dynamic white-box modeling approach that entails detailed building physics, including building mass properties
2) provides a detailed HVAC system enabling the design and performance evaluation of specific energy systems,
3) uses only one building energy simulator, EnergyPlus, thereby circumventing the need for multiple software integrations and interface developments
4) offers a modular structure, requiring only minor reconfiguration for subsequent framework implementations
5) is developed fully open-source to eliminate the need for commercial software

# Getting started
### GIS-AWBEM installation
Clone the repository using 

git clone https://github.com/KIT-IAI/GIS-AWBEM.git

# Requirements
Python packages:
* numpy
* pandas
* utm
* eppy
* sympy
* json

Energy simulator:
* EnergyPlus 25.1
  
# Acknowledgment
This work was conducted within the framework of the Helmholtz Program Energy System Design (ESD).

# License
The GIS-AWBEM framework is released by the Institute for Automation and Applied Informatics, Karlsruhe Institute of Technology under the [MIT License](https://github.com/KIT-IAI/GIS-AWBEM/blob/main/LICENSE.md).
