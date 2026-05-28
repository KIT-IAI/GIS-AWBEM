import numpy as np
import pandas as pd
import os
import shutil
from datetime import datetime
from io import StringIO
from eppy.modeleditor import IDF
from GIS_AWBEM.utilities import get_polygon_orientaion
from GIS_AWBEM.pre_process import geo_process, enrich, internal_gains
import GIS_AWBEM.EP as EP

# Define the source code directory
path_src = os.path.dirname(os.path.realpath(__file__))

class GenIDF:

    def __init__(self, geo_file, weather_file, IG_file, enrich_dict, HVAC_type):

        self.geo_file = geo_file
        self.weather = weather_file
        self.IG_file = IG_file
        self.enrich_dict = enrich_dict
        self.HVAC_type = HVAC_type

    def generate(self, path_file):

        # Define the directory of the selected HVAC system
        path_HVAC = os.path.join(path_file, self.HVAC_type)
        if not os.path.exists(path_HVAC):
            os.makedirs(path_HVAC)

        # Define the directory of the input data and enrichment data
        path_input = os.path.realpath(os.path.join(path_src, "..", "..", "Inputs")) + "\\"
        

        # Load and process the geospatial data
        print("---------- pre-processing ----------")
        df_geo = geo_process(path_input, self.geo_file)
        print("Geospatial data processing completed")

        # execute the enrichment? "yes" or "no"
        execute_enrichment = self.enrich_dict["execute_enrichment"]
        dict_enrich, df_geo = enrich(df_geo, self.enrich_dict)
        print(f"Enrichment ({execute_enrichment}) completed")

        selected_cols = ["osm_id", "addr_country", "addr_city", "addr_street", "addr_housenumber",
                         "addr_postcode", "building", "area", "height"]
        
        # Save the processed geospatial dataset
        df_geo[selected_cols].to_csv(path_HVAC + "\District_geo.csv", index=None)
        print("Geospatial dataset saved")

        # Internal gain and setpoint temperature profiles
        IG_profile, IG_intensity, Tset = internal_gains(self.IG_file)
        print("Internal gains and setpoint temperature profiles imported")


        # check if the IDF save directory exists
        path_save = os.path.join(path_HVAC, "Generated_IDFs")
        path_save_backup = os.path.join(path_HVAC, "Generated_IDFs_backup")
        
        # If the folder already exists, rename it
        if os.path.exists(path_save):
        
            # Remove previous backup folder if it already exists
            if os.path.exists(path_save_backup):
                shutil.rmtree(path_save_backup)
        
            os.rename(path_save, path_save_backup)
        
        # Create a fresh folder
        os.makedirs(path_save)


        # Sepcify EnergyPlus Input Data Dictionary
        iddfile = r"C:\EnergyPlusV25-1-0\Energy+.idd"
        IDF.setiddname(iddfile)

        # Loop through the district buildings
        print("\n---------- EnergyPlus file generation --------------")
        gen_time = {}
        for idx_b, osm_id in enumerate(df_geo["osm_id"]):
        
            # Starting point of IDF generation
            sim_start = datetime.now()
            
            # Round and keep the coordinations up to 9 decimals
            Bxy_coords = np.array(df_geo.loc[idx_b, "xy_coordinates"][0])
            Bxy_coords = np.round(Bxy_coords, 9)
        
            height_arr = np.ones(Bxy_coords.shape[0]) * df_geo.loc[idx_b, "height"]
            height_arr = height_arr.reshape(Bxy_coords.shape[0], 1)
            Btop_coords = np.hstack((Bxy_coords, height_arr))
        
            # Check if the vertices are CCW or CW
            if get_polygon_orientaion(Btop_coords[:,:-1]):
                Btop_coords_CCW = Btop_coords
                Btop_coords_CW = Btop_coords_CCW[::-1]
            else:
                Btop_coords_CW = Btop_coords
                Btop_coords_CCW = Btop_coords_CW[::-1]
        
            # Check the polygon orientation of building coordinates
            polygon = Btop_coords[:,:-1]
            if get_polygon_orientaion(polygon) == "CCW":
                Btop_coords_CCW = Btop_coords
            elif get_polygon_orientaion(polygon) == "CW":
                Btop_coords_CCW = Btop_coords[::-1]
            else:
                print(f"{osm_id}: Building coordinates are not oriented either CW or CCW")
        
        
            # Floor coordinate polygon should be CW
            floor_coords_CW = np.copy(Btop_coords_CCW[::-1])
            floor_coords_CW[:, -1] = 0

            # Building type and levels
            bldg_type = df_geo.loc[idx_b, "building_type"]
            bldg_levels = float(df_geo.loc[idx_b, "building_levels"])

            # Building application
            if bldg_type in ["AB", "MFH", "SFH", "TH"]:
                bldg_app = "Residential"
            else:
                bldg_app = bldg_type

            # ====================================================================
            # ************************ EnergyPlus Objects ************************
            # ====================================================================

            # Define E+ version
            version = "25.1"

            # Initaite the IDF file
            start_idf = f"Version, {version};"
            idf = IDF(StringIO(start_idf))

            # =================== Group – Simulation Parameters ===================
            # Simulation Control 
            EP.simulation_control(idf, run_sizing_periods = "No")
            
            # Building environment
            EP.building(idf, name=osm_id, solar_distribution="FullExteriorWithReflections")
        
            # Shadow calculation 
            EP.shadow_calculation(idf)

            # Surface convection algorithm: inside
            EP.surface_convection_algorithm_inside(idf)
        
            # Surface convection algorithm: outside
            EP.surface_convection_algorithm_outside(idf)
        
            # Heat balance algorithm 
            EP.heat_balance_algorithm(idf)
            
            # Zone air heat balance algorithm 
            EP.zone_air_heat_balance_algorithm(idf)
            
            # Timestep (per hour)
            EP.timestep(idf, 1)
            
            # Convergence limits 
            EP.convergence_limits(idf)


            # =================== Group – Location – Climate – Weather File Access ===================
            # Site location 
            EP.site_location(
                idf,
                name="Bergwald",
                latitude=48.973816,
                longitude=8.466103,
                time_zone=1.0,
                elevation=220.0)
            
            # Run Period
            EP.run_period(
                idf,
                name="Run_period1", 
                begin_month=1, 
                begin_day_of_month=1, 
                end_month=12, 
                end_day_of_month=31)

            # Ground Temperature Building Surface
            EP.ground_temperature_building_surface(
                idf,
                Jan=17.75,
                Feb=17.48,
                Mar=17.46,
                Apr=19.03,
                May=19.37,
                Jun=19.44,
                Jul=21.02,
                Aug=21.31,
                Sep=21.32,
                Oct=21.29,
                Nov=19.69,
                Dec=19.36)


            # =================== Group – Schedules ===================
            # ScheduleTypeLimits 
            EP.schedule_type_limits(idf, "Any Number")
            EP.schedule_type_limits(idf, "Fraction", 0, 1, "Continuous")
            EP.schedule_type_limits(idf, "Temperature", -60, 200, "Continuous", "Temperature")
            EP.schedule_type_limits(idf, "Control Type", 0, 4, "Discrete", "Temperature")

            # Occupancy, lighting, equipment, and ventilation schedules from the internal gain profiles
            occ_profile = IG_profile[bldg_app]["Occupancy"]
            EP.schedule_from_profile(idf, profile=occ_profile, name="Occupancy_schedule", type_limit="Fraction")

            light_profile = IG_profile[bldg_app]["Light"]
            EP.schedule_from_profile(idf, profile=light_profile, name="Lights_schedule", type_limit="Fraction")

            equipment_profile = IG_profile[bldg_app]["Equipment"]
            EP.schedule_from_profile(idf, profile=equipment_profile, name="Equipment_schedule", type_limit="Fraction")

            ventilation_profile = IG_profile[bldg_app]["Ventilation"]
            EP.schedule_from_profile(idf, profile=ventilation_profile, name="Ventilation_schedule", type_limit="Any Number")
        
            # Temperature setpoint schedules 
            if bldg_app in ["Residential", "Commercial"]:
                Tset_heating = Tset[bldg_app]["T_set_winter"]
                EP.schedule_from_profile(idf, profile=Tset_heating, name="Heating_setpoint_schedule", type_limit="Temperature")
        
                Tset_cooling = Tset[bldg_app]["T_set_summer"]
                EP.schedule_from_profile(idf, profile=Tset_cooling, name="Cooling_setpoint_schedule", type_limit="Temperature")
        
                # Set the heating and cooling thermostat
                EP.set_thermostat1(idf)


            else: # bldg_app in ["School", "Office"]
                Tset_heating_wd = Tset[bldg_app]["T_set_winter_wd"]
                Tset_heating_we = Tset[bldg_app]["T_set_winter_we"]
                EP.schedule_heating_nonres(idf, profile_wd=Tset_heating_wd, profile_we=Tset_heating_we, name="Heating_setpoint_schedule", type_limit="Temperature")

                Tset_cooling = Tset[bldg_app]["T_set_summer"]
                EP.schedule_from_profile(idf, profile=Tset_cooling, name="Cooling_setpoint_schedule", type_limit="Temperature")

                # Set the heating and cooling thermostat
                EP.set_thermostat2(idf)

            # Intensity and constant schedules
            EP.constant_schedule(idf, value=IG_intensity[bldg_app]["People_activity [W/person]"], name="Activity_schedule", type_limit="Any Number")
            EP.constant_schedule(idf, value=85, name="Heating_supply_schedule", type_limit="Temperature")
            EP.active_summer_schedule(idf)
            EP.active_winter_schedule(idf)
            EP.always_ON_schedule(idf)


            # =================== Group – Surface Construction Elements ===================
            # Wall material
            wall_mat_dict = dict_enrich[osm_id]["wall"]
            EP.wall_material(idf, wall_mat_dict)

            # Roof material
            roof_mat_dict = dict_enrich[osm_id]["roof"]
            EP.roof_material(idf, roof_mat_dict)

            # Floor material
            floor_mat_dict = dict_enrich[osm_id]["floor"]
            EP.floor_material(idf, floor_mat_dict)

            # Window material
            window_u_value = dict_enrich[osm_id]["window"]
            EP.window_material(idf, window_u_value)
            
            
            # =================== Group – Thermal Zone Description/Geometry ===================
            # Global geometry rules 
            EP.global_geometry_rules(
                idf,
                starting_vertex_position="UpperLeftCorner",
                vertex_entry_direction="Counterclockwise",
                coordinate_system="Relative")
        
            # Zone 
            EP.zone(idf)
        
            # Space 
            EP.space(idf)
            
            # Space list
            EP.space_list(idf)
        
            # Roof surface
            EP.roof_surface(idf, Btop_coords_CCW)
        
            # Floor surface 
            EP.floor_surface(idf, floor_coords_CW)

            # Wall surfaces
            wall_dict = EP.wall_surface(idf, Btop_coords_CCW)

            # Window surface and Window-to-Wall Ratio (WWR)
            WWR = dict_enrich[osm_id]["WWR"]
            EP.window_surface(idf, wall_dict, WWR)
        
        
            # =================== Group – Internal Gains ===================
            # People
            ppl_m2 = IG_intensity[bldg_app]["People_density [person/m2]"] * bldg_levels
            EP.people(
                idf,
                zone_or_zonelist_or_space_or_spacelist_name="Zone1",
                number_of_people_schedule_name="Occupancy_schedule",
                number_of_people_calculation_method="People/Area",
                people_per_floor_area=ppl_m2,
                activity_level_schedule_name="Activity_schedule")

            # Lights
            lights_m2 = IG_intensity[bldg_app]["Lighting_level [W/m2]"] * bldg_levels
            EP.lights(
                idf,
                name="Lights1",
                zone_or_zonelist_or_space_or_spacelist_name="Zone1",
                schedule_name="Lights_schedule",
                design_level_calculation_method="Watts/Area",
                watts_per_floor_area=lights_m2)
        
            # Equipment
            equipment_m2 = IG_intensity[bldg_app]["Electric_equipment [W/m2]"] * bldg_levels
            EP.electric_equipment(
                idf,
                name="Equipment1",
                zone_or_zonelist_or_space_or_spacelist_name="Zone1",
                schedule_name="Equipment_schedule",
                design_level_calculation_method="Watts/Area",
                watts_per_floor_area=equipment_m2)
            

            # =================== Group – Air flow ===================
            # Zone ventilation
            EP.zone_ventilation_design_flow_rate(
                idf,
                name="Ventilation",
                zone_or_zonelist_or_space_or_spacelist_name="Zone1",
                schedule_name="Ventilation_schedule",
                design_flow_rate_calculation_method="AirChanges/Hour",
                air_changes_per_hour=1.0)


            # =================== Group – Zone Control - Thermostats and Humidistat ===================
            # Thermostat control
            EP.zone_control_thermostat(
                idf,
                name="Heating_thermostat",
                zone_or_zonelist_name="Zone1",
                control_type_schedule_name="Thermostat_control_type",
                control_1_object_type="ThermostatSetpoint:SingleHeating",
                control_1_name="Heating_thermostat")

            # Thermostat setpoint: SingleHeating
            EP.thermostat_setpoint_single_heating(
                idf, 
                name="Heating_thermostat",
                setpoint_temperature_schedule_name="Heating_setpoint_schedule")

            # Thermostat setpoint: SingleCooling
            EP.thermostat_setpoint_single_cooling(
                idf,
                name="Cooling_thermostat",
                setpoint_temperature_schedule_name="Cooling_setpoint_schedule")


            # =================== Group – Zone Forced Air Units ===================
            # HVAC: IdealLoadsAirSystem
            EP.zone_hvac_ideal_loads_air_system(idf,
                                                 name="HVAC1",
                                                 availability_schedule_name="Always ON")
            
            # HVAC: equipment list
            EP.zone_hvac_equipment_list(idf,
                                        name="Zone_equipment_list",
                                        load_distribution_scheme="SequentialLoad",
                                        zone_equipment_1_object_type="ZoneHVAC:IdealLoadsAirSystem",
                                        zone_equipment_1_name="HVAC1",
                                        zone_equipment_1_cooling_sequence=1,
                                        zone_equipment_1_heating_or_noload_sequence=1)

            # HVAC: equipment connections
            EP.zone_hvac_equipment_connections(idf,
                                                zone_name="Zone1",
                                                zone_conditioning_equipment_list_name="Zone_equipment_list",
                                                zone_air_inlet_node_or_nodelist_name="Zone_supply_inlet",
                                                zone_air_node_name="Zone_air_node",
                                                zone_return_air_node_or_nodelist_name="Zone_return_air_node")



            # =================== Group – Reports ===================
            # Output: variable dictionary
            EP.output_variable_dictionary(idf)
        
            # Output: variable
            out_var_list = ["Site Outdoor Air Drybulb Temperature", "Zone Air Temperature",
                            "Zone Ideal Loads Supply Air Total Heating Rate", "Zone Ideal Loads Supply Air Total Cooling Rate",
                            "Zone Ideal Loads Supply Air Mass Flow Rate", "Zone Ideal Loads Supply Air Temperature ",
                            "Zone Thermostat Heating Setpoint Temperature", "Zone Thermostat Cooling Setpoint Temperature",
                            "Zone Thermostat Control Type"
                            ]
            for var in out_var_list:
                EP.output_variable(idf, var)
        
            # Output: meters
            EP.output_meter(idf, "Electricity:Facility", "Timestep")
            
            # Output: summary reports
            EP.output_table_summary_reports(idf, ["AllSummary"])
            
            # Output: files
            EP.output_control_files(idf)
        
            # Output: timestamp
            EP.output_control_timestamp(idf)

            # save the IDF
            idf.saveas(os.path.join(path_save, f"{osm_id}_{self.HVAC_type}.idf"))

            # Record the IDF generation time
            sim_end = datetime.now()
            elapsed_time = sim_end - sim_start
            duration = elapsed_time.seconds + np.round(elapsed_time.microseconds/1e6, 2)
            gen_time[osm_id] = duration
            print(f"{idx_b+1}) {osm_id} --> Generated [{duration} s]")


        # Total distrcit IDF generation time
        t_gen_tot = int(sum(gen_time.values()))
        t_gen_hms = f"{t_gen_tot//3600:02}:{t_gen_tot%3600//60:02}:{t_gen_tot%60:02}"
        # print(f"----------District IDF generation completed in {t_gen_hms} ----------\n")
        
        # save the IDF generation runtime results
        df_gen = pd.DataFrame(gen_time.items(), columns=["osm_id", "Time (s)"])
        df_gen.to_csv(path_HVAC + "\\Generation_time.csv", index=False)

        return
    