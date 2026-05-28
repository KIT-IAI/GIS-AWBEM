import importlib
import os
from GIS_AWBEM.Simulate import simulate_district
from GIS_AWBEM.post_process import analyze


def execute():
    
    # Manage paths
    path_file = os.path.dirname(os.path.realpath(__file__))
    path_input = os.path.realpath(os.path.join(path_file, "..", "..", "GIS-AWBEM", "Inputs")) + "\\"
    
    # Define enrichment dictionary
    enrich = {
        "execute_enrichment" : "yes", # if yes, providing the following info is required
        "enrichment_file": "Bergwald_enrich.csv",
        "region" : "south",         # region: ["north", "south", "east"]
        "mun_growth" : "stagnant",  # municipality growth: ["growing", "stagnant"]
        "mun_size" : "urban"        # municipality size: ["rural", "urban"]
        }
    
    # District general configuration
    config = {
        "geo_file" : "Bergwald.geojson", # use "Bergwald_truncated.geojson" for a smaller version (with lower number of buildings)
        "weather_file": "Rheinstetten_04177.epw",
        "IG_file" : "Internal gain profiles.xlsx",
        "enrich" : enrich,
        "HVAC_type" : "IdealHVAC" # select from ["IdealHVAC", "Boiler_DXcoil", "PTHP"]
        }
    
    
    # -------- Step 1: Import the HVAC module --------
    # import the specific HVAC type moodule
    module = importlib.import_module(f"GIS_AWBEM.Gen_IDF_{config['HVAC_type']}")
    
    
    # -------- Step 2: IDF generation --------
    # Configure district IDF generation module
    DistIDF = module.GenIDF(*list(config.values()))
    
    # Generate EnergyPlus IDFs for all district buidlings. Note: this step takes time depending on the distrtict size
    DistIDF.generate(path_file=path_file)
    
    
    # -------- Step 3: Simulate district buildings providing a weather data --------
    # Provide weather data (.epw)
    epw_file = os.path.join(path_input, f"{config['weather_file']}")
    
    # IDF stored directory
    idf_dir = os.path.join(path_file, DistIDF.HVAC_type, "Generated_IDFs")
    
    # Output dir
    output_dir = os.path.join(path_file, DistIDF.HVAC_type, "Results")
    
    # Run all buildings in the district. Note: this step might take a while depending on the distrtict size
    simulate_district(idf_dir, epw_file, output_dir)
    
    
    # -------- Step 4: analyze the results --------
    # post-process. Note: this step might take a while depending on the distrtict size
    df_summary = analyze(output_dir, DistIDF.HVAC_type)



if __name__ == "__main__":
    execute()

