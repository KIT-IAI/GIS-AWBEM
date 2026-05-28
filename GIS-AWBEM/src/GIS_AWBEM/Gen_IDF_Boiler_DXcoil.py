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
            EP.simulation_control(
                idf,
                do_zone_sizing="Yes",
                do_system_sizing="Yes",
                do_plant_sizing="No",
                run_sizing_periods="No",
                run_weather_file="Yes",
                do_hvac_sizing_simulation="No",
                max_hvac_sizing_passes="1")
            
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

            # Winter design day
            EP.sizing_period_design_day(
                idf,
                name="winter_design_day",
                month=1,
                day_of_month=21,
                day_type="WinterDesignDay",
                maximum_drybulb_temperature=-12.0,
                humidity_condition_type="WetBulb",
                wetbulb_or_dewpoint_at_maximum_drybulb=-17.3,
                wind_speed=5,
                wind_direction=270,
                daylight_saving_time_indicator="Yes",
                sky_clearness=1)
            
            # Summer design day
            EP.sizing_period_design_day(
                idf,
                name="summer_design_day",
                month=7,
                day_of_month=21,
                day_type="SummerDesignDay",
                maximum_drybulb_temperature=34.2,
                humidity_condition_type="WetBulb",
                wetbulb_or_dewpoint_at_maximum_drybulb=23,
                wind_speed=5,
                wind_direction=270,
                daylight_saving_time_indicator="Yes",
                sky_clearness=1)
            
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


            # =================== Group – Design Objects ===================
            # Outdoor air
            EP.design_specification_outdoor_air(
                idf,
                name="Outdoor_specification",
                outdoor_air_method="Flow/Person",
                outdoor_air_flow_per_person=0.00944)

            # Sizing zone
            EP.sizing_zone(
                idf,
                zone_or_zone_list_name="Zone1",
                zone_cooling_design_supply_air_humidity_ratio=0.008,
                zone_heating_design_supply_air_humidity_ratio=0.008,
                design_specification_outdoor_air_object_name="Outdoor_specification")
            
            # Sizing plant
            EP.sizing_plant(
                idf,
                plant_or_condenser_loop_name="Plant_loop1",
                loop_type="Heating",
                design_loop_exit_temperature=85,
                loop_design_temperature_difference=10)
            

            # =================== Group – Node-Branch Management ===================
            # ------ Branches ------
            # Supply inlet branch
            EP.branch(idf, "Supply_inlet_branch", "", "Pump:VariableSpeed", "Pump1", "Supply_pump_inlet_node", "Supply_pump_outlet_node")

            # Boiler branch
            EP.branch(idf, "Boiler_branch", "", "Boiler:HotWater", "Boiler1", "Boiler_inlet_node", "Boiler_outlet_node")

            # Supply bypass branch
            EP.branch(idf, "Supply_bypass_branch", "", "Pipe:Adiabatic", "Supply_bypass_pipe", "Supply_bypass_inlet_node", "Supply_bypass_outlet_node")

            # Supply outlet branch
            EP.branch(idf, "Supply_outlet_branch", "", "Pipe:Adiabatic", "Supply_outlet_pipe", "Supply_exit_pipe_inlet_node", "Supply_exit_pipe_outlet_node")

            # Zone inlet branch
            EP.branch(idf, "Zone_inlet_branch", "", "Pipe:Adiabatic", "Zone_inlet_pipe", "Zone_inlet_pipe_inlet_node", "Zone_inlet_pipe_outlet_node")

            # Zone baseboard branch
            EP.branch(idf, "Zone_baseboard_branch", "", "ZoneHVAC:Baseboard:Convective:Water", "Baseboard1", "Zone_baseboard_inlet_node", "Zone_baseboard_outlet_node")

            # Zone bypass branch
            EP.branch(idf, "Zone_bypass_branch", "", "Pipe:Adiabatic", "Zone_bypass_pipe", "Zone_bypass_inlet_node", "Zone_bypass_outlet_node")

            # Zone outlet branch
            EP.branch(idf, "Zone_outlet_branch", "", "Pipe:Adiabatic", "Zone_outlet_pipe", "Zone_outlet_pipe_inlet_node", "Zone_outlet_pipe_outlet_node")


            # ------ BranchList ------
            # Supply branch list
            EP.branchlist(idf, "Supply_branch_list", "Supply_inlet_branch", "Boiler_branch", "Supply_bypass_branch", "Supply_outlet_branch")
            
            # Demand branch list
            EP.branchlist(idf, "Demand_branch_list", "Zone_inlet_branch", "Zone_baseboard_branch", "Zone_bypass_branch", "Zone_outlet_branch")
            

            # ------ Connector:Splitter ------
            # Supply splitter
            EP.connector_splitter(idf, "Supply_splitter1", "Supply_inlet_branch", "Boiler_branch", "Supply_bypass_branch")
            
            # Demand splitter
            EP.connector_splitter(idf, "Demand_splitter1", "Zone_inlet_branch", "Zone_baseboard_branch", "Zone_bypass_branch")
            

            # ------ Connector:Mixer ------
            # Supply mixer
            EP.connector_mixer(idf, "Supply_mixer1", "Supply_outlet_branch", "Boiler_branch", "Supply_bypass_branch")
            
            # Demand mixer
            EP.connector_mixer(idf, "Demand_mixer1", "Zone_outlet_branch", "Zone_baseboard_branch", "Zone_bypass_branch")

            
            # ------ ConnectorList ------
            # Supply connector list
            EP.connectorlist(idf, "Supply_connector_list", "Connector:Splitter", "Supply_splitter1", "Connector:Mixer", "Supply_mixer1")
            
            # Demand connector list
            EP.connectorlist(idf, "Demand_connector_list", "Connector:Splitter", "Demand_splitter1", "Connector:Mixer", "Demand_mixer1")
            
            # ------ NodeList ------
            # NodeLists
            EP.nodelist(idf, "Supply_setpoint_node_list", "Supply_exit_pipe_outlet_node")
            EP.nodelist(idf, "Outside_air_node_list", "Outside_air_inlet_node")
            EP.nodelist(idf, "Zone_air_intake_node_list", "Zone_air_intake_node")
            EP.nodelist(idf, "Zone_air_exhaust_node_list", "Zone_air_exhaust_node")
            
            # ------ Pipe:Adiabatic ------
            # Adiabatic pipes
            EP.pipe_adiabatic(idf, "Supply_bypass_pipe", "Supply_bypass_inlet_node", "Supply_bypass_outlet_node")
            EP.pipe_adiabatic(idf, "Supply_outlet_pipe", "Supply_exit_pipe_inlet_node", "Supply_exit_pipe_outlet_node")
            EP.pipe_adiabatic(idf, "Zone_inlet_pipe", "Zone_inlet_pipe_inlet_node", "Zone_inlet_pipe_outlet_node")
            EP.pipe_adiabatic(idf, "Zone_bypass_pipe", "Zone_bypass_inlet_node", "Zone_bypass_outlet_node")
            EP.pipe_adiabatic(idf, "Zone_outlet_pipe", "Zone_outlet_pipe_inlet_node", "Zone_outlet_pipe_outlet_node")
            

            # =================== Group – Zone Forced Air Units ===================
            # Packaged Terminal Air Conditioner
            EP.zone_hvac_packaged_terminal_air_conditioner(
                idf,
                name="Air_conditioner1",
                availability_schedule_name="Active_summer",
                air_inlet_node_name="Zone_air_inlet_node",
                air_outlet_node_name="Heating_coil_outlet_node",
                cooling_supply_air_flow_rate="autosize",
                heating_supply_air_flow_rate="autosize",
                cooling_outdoor_air_flow_rate="autosize",
                heating_outdoor_air_flow_rate="autosize",
                supply_air_fan_object_type="Fan:SystemModel",
                supply_air_fan_name="Fan1",
                heating_coil_object_type="Coil:Heating:Electric",
                heating_coil_name="Electric_heater1",
                cooling_coil_object_type="Coil:Cooling:DX:SingleSpeed",
                cooling_coil_name="Cooling_coil1",
                fan_placement="BlowThrough")


            # =================== Group – Radiative / Convective Units ===================
            # Baseboard radiator
            EP.zone_hvac_baseboard_convective_water(
                idf,
                name="Baseboard1",
                availability_schedule_name="Active_winter",
                inlet_node_name="Zone_baseboard_inlet_node",
                outlet_node_name="Zone_baseboard_outlet_node",
                heating_design_capacity_method="HeatingDesignCapacity",
                heating_design_capacity="autosize",
                ufactor_times_area_value="autosize",
                maximum_water_flow_rate="autosize")
            

            # =================== Group – Zone Equipment ===================
            # Zone equipment list
            EP.zone_hvac_equipment_list(
                idf,
                name="Zone_equipment_list",
                load_distribution_scheme="SequentialLoad",
                zone_equipment_1_object_type="ZoneHVAC:Baseboard:Convective:Water",
                zone_equipment_1_name="Baseboard1",
                zone_equipment_1_cooling_sequence=1,
                zone_equipment_1_heating_or_noload_sequence=1,
                zone_equipment_2_object_type="ZoneHVAC:PackagedTerminalAirConditioner",
                zone_equipment_2_name="Air_conditioner1",
                zone_equipment_2_cooling_sequence=2,
                zone_equipment_2_heating_or_noload_sequence=2)
                                            
            # Zone equipment connections
            EP.zone_hvac_equipment_connections(
                idf,
                zone_name="Zone1",
                zone_conditioning_equipment_list_name="Zone_equipment_list",
                zone_air_inlet_node_or_nodelist_name="Heating_coil_outlet_node",
                zone_air_exhaust_node_or_nodelist_name="Zone_air_inlet_node",
                zone_air_node_name="Zone_air_node",
                zone_return_air_node_or_nodelist_name="Zone_return_air_node")


            # =================== Group – Heating and Cooling Coils ===================
            # Cooling coil
            EP.coil_cooling_dx_single_speed(
                idf,
                name="Cooling_coil1",
                availability_schedule_name="Active_summer",
                gross_rated_total_cooling_capacity="autosize",
                gross_rated_sensible_heat_ratio="autosize",
                rated_air_flow_rate="autosize",
                air_inlet_node_name="Fan_outlet_node",
                air_outlet_node_name="Cooling_coil_outlet_node",
                total_cooling_capacity_function_of_temperature_curve_name="HPACCoolCapFT",
                total_cooling_capacity_function_of_flow_fraction_curve_name="HPACCoolCapFFF",
                energy_input_ratio_function_of_temperature_curve_name="HPACCoolCapFT",
                energy_input_ratio_function_of_flow_fraction_curve_name="HPACEIRFFF",
                part_load_fraction_correlation_curve_name="HPACPLFFPLR")
                # Note: The curves for the cooling coil are defined later in the code, after the plant equipment

            # Heating coil
            EP.coil_heating_electric(
                idf,
                name="Electric_heater1",
                availability_schedule_name="Active_winter",
                efficiency="",
                nominal_capacity=0,
                air_inlet_node_name="Cooling_coil_outlet_node",
                air_outlet_node_name="Heating_coil_outlet_node",
                temperature_setpoint_node_name="")

            # =================== Group – Fans ===================
            # Fan
            EP.fan_system_model(
                idf,
                name="Fan1",
                availability_schedule_name="Always ON",
                air_inlet_node_name="Zone_air_inlet_node",
                air_outlet_node_name="Fan_outlet_node",
                design_maximum_air_flow_rate="autosize",
                speed_control_method="Discrete",
                design_pressure_rise=80)

            # =================== Group – Pumps ===================
            # Pump
            EP.pump_variable_speed(
                idf,
                name="Pump1",
                inlet_node_name="Supply_pump_inlet_node",
                outlet_node_name="Supply_pump_outlet_node",
                design_maximum_flow_rate="autosize",
                design_power_consumption="autosize")


            # =================== Group – Plant Equipment ===================
            # Boiler
            EP.boiler_hot_water(
                idf,
                name="Boiler1",
                fuel_type="NaturalGas",
                nominal_capacity="autosize",
                nominal_thermal_efficiency=0.8,
                efficiency_curve_temperature_evaluation_variable="LeavingBoiler",
                normalized_boiler_efficiency_curve_name="BoilerEfficiency",
                design_water_flow_rate="autosize",
                minimum_part_load_ratio=0,
                maximum_part_load_ratio=1.2,
                optimum_part_load_ratio=1,
                boiler_water_inlet_node_name="Boiler_inlet_node",
                boiler_water_outlet_node_name="Boiler_outlet_node",
                water_outlet_upper_temperature_limit=99.9,
                boiler_flow_mode="LeavingSetpointModulated")

            # =================== Group – Plant-Condenser Loops ===================
            # Plant loop
            EP.plant_loop(
                idf,
                name="Plant_loop1",
                plant_equipment_operation_scheme_name="Plant_operation_scheme1",
                loop_temperature_setpoint_node_name="Supply_exit_pipe_outlet_node",
                maximum_loop_temperature=100,
                minimum_loop_temperature=10,
                maximum_loop_flow_rate="autosize",
                plant_side_inlet_node_name="Supply_pump_inlet_node",
                plant_side_outlet_node_name="Supply_exit_pipe_outlet_node",
                plant_side_branch_list_name="Supply_branch_list",
                plant_side_connector_list_name="Supply_connector_list",
                demand_side_inlet_node_name="Zone_inlet_pipe_inlet_node",
                demand_side_outlet_node_name="Zone_outlet_pipe_outlet_node",
                demand_side_branch_list_name="Demand_branch_list",
                demand_side_connector_list_name="Demand_connector_list",
                load_distribution_scheme="Optimal")

            # =================== Group – Plant-Condenser Control ===================
            # Plant equipment list
            EP.plant_equipment_list(
                idf,
                name="Plant_equipment_list1",
                equipment_1_object_type="Boiler:HotWater",
                equipment_1_name="Boiler1")


            # Plant equipment operation heating load
            EP.plant_equipment_operation_heating_load(
                idf,
                load_range_1_lower_limit=0,
                load_range_1_upper_limit=100000,
                range_1_equipment_list_name="Plant_equipment_list1")

            # Plant operation scheme
            EP.plant_operation_scheme(
                idf,
                name="Plant_operation_scheme1",
                control_scheme_1_object_type="PlantEquipmentOperation:HeatingLoad",
                control_scheme_1_name="Plant_heating_load1",
                control_scheme_1_schedule_name="Always On")
            
            # =================== Group – Setpoint Managers ===================
            # Setpoint manager
            EP.setpoint_manager_scheduled(
                idf, 
                name="Supply_setpoint_manager_schedule1",
                control_variable="Temperature",
                schedule_name="Heating_supply_schedule",
                setpoint_node_or_nodelist_name="Supply_exit_pipe_outlet_node")

            EP.setpoint_manager_scheduled(
                idf, 
                name="Supply_setpoint_manager_schedule2",
                control_variable="Temperature",
                schedule_name="Heating_supply_schedule",
                setpoint_node_or_nodelist_name="Boiler_outlet_node")


            # =================== Group – Performance Curves ===================
            # Quadratic curves
            EP.curve_quadratic(idf, "HPACCoolCapFFF", 0.8, 0.2, 0.0, 0.5, 1.5)
            EP.curve_quadratic(idf, "HPACEIRFFF", 1.1552, -0.1808, 0.0256, 0.5, 1.5)
            EP.curve_quadratic(idf, "HPACPLFFPLR", 0.85, 0.15, 0.0, 0.0, 1.0)
            EP.curve_quadratic(idf, "BoilerEfficiency", 1.0, 0.0, 0.0, 0.0, 1.0)

            # Exponential curves
            EP.curve_exponent(idf, "FanPowerRatioCurve", 0, 1, 3, 0.0, 1.5, 0.01, 1.5)

            # Biquadratic curves
            EP.curve_biquadratic(idf, "HPACCoolCapFT", 0.942587793, 0.009543347, 0.00068377, -0.011042676, 0.000005249, -0.00000972, 12.77778, 23.88889, 18.0, 46.11111)


            # =================== Group – Reports ===================
            # Output objects
            EP.output_variable_dictionary(idf, "IDF", "Unsorted")

            # Output variables
            EP.output_variable(idf, "Site Outdoor Air Drybulb Temperature", "Timestep")
            EP.output_variable(idf, "Zone Air Temperature", "Timestep")
            EP.output_variable(idf, "Boiler Heating Rate", "Timestep")
            EP.output_variable(idf, "Boiler Inlet Temperature", "Timestep")
            EP.output_variable(idf, "Boiler Outlet Temperature", "Timestep")
            EP.output_variable(idf, "Boiler Mass Flow Rate", "Timestep")
            EP.output_variable(idf, "Boiler NaturalGas Rate", "Timestep")
            EP.output_variable(idf, "Baseboard Total Heating Rate", "Timestep")
            EP.output_variable(idf, "Baseboard Water Inlet Temperature", "Timestep")
            EP.output_variable(idf, "Baseboard Water Outlet Temperature", "Timestep")
            EP.output_variable(idf, "Baseboard Hot Water Mass Flow Rate", "Timestep")
            EP.output_variable(idf, "Pump Mass Flow Rate", "Timestep")
            EP.output_variable(idf, "Debug Plant Loop Bypass Fraction", "Timestep")
            EP.output_variable(idf, "Cooling Coil Total Cooling Rate", "Timestep")
            EP.output_variable(idf, "Zone Packaged Terminal Air Conditioner Total Cooling Rate", "Timestep")
            EP.output_variable(idf, "Zone Thermostat Heating Setpoint Temperature", "Timestep")
            EP.output_variable(idf, "Zone Thermostat Cooling Setpoint Temperature", "Timestep")
            EP.output_variable(idf, "Zone Thermostat Control Type", "Timestep")

            # Output meters
            EP.output_meter(idf, "Electricity:Facility", "Timestep")
            EP.output_meter(idf, "Electricity:HVAC", "Timestep")
            EP.output_meter(idf, "NaturalGas:Facility", "Timestep")

            # Output table summary reports
            EP.output_table_summary_reports(idf, ["AllSummary"])

            # Output control files
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



























