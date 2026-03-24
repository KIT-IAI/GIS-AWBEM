import numpy as np
import pandas as pd
import os
from src.pre_process import *
from src.EP_IdealHVAC import *


# Get files locations
path_src = Path(__file__).resolve().parent
path_input = path_src.parent
path_enrichment = path_input / "HUB4LCA"

# Load and process the geospatial data
df_geo = geo_process(path_input, "OSM_District.geojson")

# District geographic features for data enrichment
region = 'south'
mun_growth = 'stagnant'
mun_size = 'urban'

# execute the enrichment? "yes" or "no"
execute_enrich = 'yes'
dict_enrich, df_geo = enrich(df_geo, execute_enrich, path_enrichment, region, mun_growth, mun_size)


# Internal gain and setpoint temperature standard profiles
IG_file_name = 'Internal gain profiles.xlsx'
IG_profile, IG_intensity, Tset = internal_gains(IG_file_name)

# ==================== Generate IDFs ==================== #

# # reverse floor/roof
# specific_OSM = ['102570241']

# collinear vertices
# specific_OSM = ['102540564']
specific_OSM = ['59082234']

generation_time = {}


# check if the the IDF save folder exists
path_save = os.path.join(path_src, "IdealHVAC\Generated_IDFs")
if not os.path.exists(path_save):
    os.makedirs(path_save)


# for idx_b, osm_id in enumerate(df_geo['osm_id']):
for osm_id in specific_OSM:
    
    # sim_start = datetime.now()
    
    # To be removed
    idx_b = df_geo.index[df_geo['osm_id']==osm_id][0]



    # Round and keep the coordinations up to 9 decimals
    Bxy_coords = np.array(df_geo.loc[idx_b, 'xy_coordinates'][0])
    Bxy_coords = np.round(Bxy_coords, 9)

    height_arr = np.ones(Bxy_coords.shape[0]) * df_geo.loc[idx_b, 'height']
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
    if get_polygon_orientaion(polygon) == 'CCW':
        Btop_coords_CCW = Btop_coords
    elif get_polygon_orientaion(polygon) == 'CW':
        Btop_coords_CCW = Btop_coords[::-1]
    else:
        print(f"{osm_id}: Building coordinates are not oriented either CW or CCW")


    # Floor coordinate polygon should be CW
    floor_coords_CW = np.copy(Btop_coords_CCW[::-1])
    floor_coords_CW[:, -1] = 0

    
    # Building type and levels
    bldg_type = df_geo.loc[idx_b, 'building_type']
    bldg_levels = float(df_geo.loc[idx_b, 'building_levels'])


    # Building application
    if bldg_type in ['AB', 'MFH', 'SFH', 'TH']:
        bldg_app = 'Residential'
    else:
        bldg_app = bldg_type
    


    # ====================================================================
    # ******************* EnergyPlus IDF Generation *******************
    # ====================================================================

    # Sepcify EnergyPlus Input Data Dictionary
    iddfile = r'C:\EnergyPlusV25-1-0\Energy+.idd'
    IDF.setiddname(iddfile)

    # Define E+ version
    version = '25.1'
    
    # Initaite the IDF file
    start_idf = f'Version, {version};'
    idf = IDF(StringIO(start_idf))
    # idf.printidf()

    
    # ====================================================================
    # ******************* Group: Simulation Parameters *******************
    # ====================================================================
    
    # ============== Simulation Control ============== 
    SimulationControl = simulation_control(idf)
    
    # ============== Building ============== 
    Building = building(idf,
                    name=osm_id,
                    solar_distribution='FullExteriorWithReflections')


    # ============== ShadowCalculation ============== 
    ShadowCalculation = shadow_calculation(idf)


    # ============== SurfaceConvectionAlgorithm:Inside ============== 
    SurfaceConvectionAlgorithmInside = surface_convection_algorithm_inside(idf)

    # ============== SurfaceConvectionAlgorithm:Outside ============== 
    SurfaceConvectionAlgorithmOutside = surface_convection_algorithm_outside(idf)

    # ============== HeatBalanceAlgorithm ============== 
    HeatBalanceAlgorithm = heat_balance_algorithm(idf)
    
    # ============== ZoneAirHeatBalanceAlgorithm ============== 
    ZoneAirHeatBalanceAlgorithm = zone_air_heat_balance_algorithm(idf)
    
    # ============== Timestep ============== 
    Timestep = timestep(idf)
    
    # ============== ConvergenceLimits ============== 
    ConvergenceLimits = convergence_limits(idf)

    # ====================================================================
    # ********** Group: Location, Climate, Weather File Access **********
    # ====================================================================


    # ============== Site location ============== 
    SiteLocation = site_location(idf)
    
    # ============== Run Period ============== 
    RunPeriod = run_period(idf)
    
    # ============== Ground Temperature Building Surface ============== 
    GroundTemperatureBuildingSurface = ground_temperature_building_surface(idf)



    # ====================================================================
    # ************************* Group: Schedules *************************
    # ====================================================================
    
    # ============== ScheduleTypeLimits ============== 
    schedule_type_limits(idf, 'Any Number')
    schedule_type_limits(idf, 'Fraction', 0, 1, 'Continuous')
    schedule_type_limits(idf, 'Temperature', -60, 200, 'Continuous', 'Temperature')
    schedule_type_limits(idf, 'Control Type', 0, 4, 'Discrete', 'Temperature')
    

    # ============== Schedule:Compact ==============
    occ_profile = IG_profile[bldg_app]['Occupancy']
    schedule_from_profile(idf,
                            profile = occ_profile,
                            name = 'Occupancy_schedule',
                            type_limit = 'Fraction')


    light_profile = IG_profile[bldg_app]['Light']
    schedule_from_profile(idf,
                            profile = light_profile,
                            name = 'Lights_schedule',
                            type_limit = 'Fraction')


    equipment_profile = IG_profile[bldg_app]['Equipment']
    schedule_from_profile(idf,
                            profile = equipment_profile,
                            name = 'Equipment_schedule',
                            type_limit = 'Fraction')



    ventilation_profile = IG_profile[bldg_app]['Ventilation']
    schedule_from_profile(idf,
                            profile = ventilation_profile,
                            name = 'Ventilation_schedule',
                            type_limit = 'Any Number')



    if bldg_app in ['Residential', 'Commercial']:
        Tset_heating = Tset[bldg_app]['T_set_winter']
        schedule_from_profile(idf,
                                profile = Tset_heating,
                                name = 'Heating_setpoint_schedule',
                                type_limit = 'Temperature')

        Tset_cooling = Tset[bldg_app]['T_set_summer']
        schedule_from_profile(idf,
                                profile = Tset_cooling,
                                name = 'Cooling_setpoint_schedule',
                                type_limit = 'Temperature')

        # Set the heating and cooling thermostat
        set_thermostat1(idf)



        
        
    else: # bldg_app in ['School', 'Office']
        Tset_heating_wd = Tset[bldg_app]['T_set_winter_wd']
        Tset_heating_we = Tset[bldg_app]['T_set_winter_we']
        schedule_heating_nonres(idf,
                                profile_wd = Tset_heating_wd,
                                profile_we = Tset_heating_we,
                                name = 'Heating_setpoint_schedule',
                                type_limit = 'Temperature')


        Tset_cooling = Tset[bldg_app]['T_set_summer']
        schedule_from_profile(idf,
                                profile = Tset_cooling,
                                name = 'Cooling_setpoint_schedule',
                                type_limit = 'Temperature')



        set_thermostat2(idf)


    activity_schedule(idf,
                        value = IG_intensity[bldg_app]['People_activity [W/person]'],
                        name = 'Activity_schedule',
                        type_limit = 'Any Number')
    

    heat_supply_schedule(idf,
                        value = 85,
                        name = 'Heating_supply_schedule',
                        type_limit = 'Temperature')
       

    active_summer_schedule(idf)
    active_winter_schedule(idf)
    always_ON_schedule(idf)
    
    # ====================================================================
    # *************** Group: Surface Construction Elements ***************
    # ====================================================================

    # ============== Material Object ==============
    wall_mat_dict = dict_enrich[osm_id]['wall']
    wall_material(idf, wall_mat_dict)



    roof_mat_dict = dict_enrich[osm_id]['roof']
    roof_material(idf, roof_mat_dict)



    floor_mat_dict = dict_enrich[osm_id]['floor']
    floor_material(idf, floor_mat_dict)


    window_u_value = dict_enrich[osm_id]['window']
    window_material(idf, window_u_value)

    
    
    # ====================================================================
    # ************* Group: Thermal Zone Description/Geometry *************
    # ====================================================================
    
    # ============== GlobalGeometryRules ============== 
    GlobalGeometryRules = global_geometry_rules(idf)

    # ============== Zone ============== 
    Zone = zone(idf)

    # ============== Space ============== 
    Space = space(idf)
    

    SpaceList = space_list(idf)

    # ============== Roof Object ==============

    roof_surface(idf, Btop_coords_CCW)

    # ============== Floor Object ============== 
    floor_surface(idf, floor_coords_CW)

    
    
    # ============== Wall Objects ============== 
    wall_dict = wall_surface(idf, Btop_coords_CCW)


    # ============== Window Objects ==============
    # Window to wall ratio
    WWR = dict_enrich[osm_id]['WWR']
    window_surface(idf, wall_dict, WWR)



    
    # ====================================================================
    # ********************** Group: Internal Gains ***********************
    # ====================================================================
    # ============== People ==============
    ppl_m2 = IG_intensity[bldg_app]['People_density [person/m2]'] * bldg_levels
    People = people(idf, people_per_floor_area=ppl_m2)

    # ============== Lights ==============
    lights_m2 = IG_intensity[bldg_app]['Lighting_level [W/m2]'] * bldg_levels
    Lights = lights(idf, watts_per_floor_area=lights_m2)

    # ============== Equipment ==============
    equipment_m2 = IG_intensity[bldg_app]['Electric_equipment [W/m2]'] * bldg_levels
    Equipment = electric_equipment(idf, watts_per_floor_area=equipment_m2)
    
    # ====================================================================
    # ************************* Group: Air flow **************************
    # ====================================================================
    
    # ============== ZoneVentilationDesignFlowRate ============== 
    ZoneVentilationDesignFlowRate = zone_ventilation_design_flow_rate(idf)

    # ====================================================================
    # ******** Group: Zone Control - Thermostats and Humidistats *********
    # ====================================================================

    # ============== ZoneControl:Thermostat ============== 
    ZoneControlThermostat = zone_control_thermostat(idf)

    # ============== ThermostatSetpoint:SingleHeating ============== 
    ThermostatSetpointSingleHeating = thermostat_setpoint_single_heating(idf)

    # ============== ThermostatSetpoint:SingleCooling ============== 
    ThermostatSetpointSingleCooling = thermostat_setpoint_single_cooling(idf)


    # ====================================================================
    # ****************** Group – Zone Forced Air Units  ******************
    # ====================================================================
    
    # ============== ZoneHVAC:IdealLoadsAirSystem ============== 
    ZoneHVACIdealLoadsAirSystem = zone_hvac_ideal_loads_air_system(idf)
    
    # ============== ZoneHVAC:EquipmentList ============== 
    ZoneHVACEquipmentList = zone_hvac_equipment_list(idf)

    # ============== ZoneHVAC:EquipmentConnections ============== 
    ZoneHVACEquipmentConnections = zone_hvac_equipment_connections(idf)
    

    # ====================================================================
    # ************************** Group: Reports **************************
    # ====================================================================

    # ============== Output:VariableDictionary ==============
    OutputVariableDictionary = output_variable_dictionary(idf)

    # ============== Output:Variable ==============
    out_var_list = ['Site Outdoor Air Drybulb Temperature', 'Zone Air Temperature',
                    'Zone Ideal Loads Supply Air Total Heating Rate', 'Zone Ideal Loads Supply Air Total Cooling Rate',
                    'Zone Ideal Loads Supply Air Mass Flow Rate', 'Zone Ideal Loads Supply Air Temperature ',
                    'Zone Thermostat Heating Setpoint Temperature', 'Zone Thermostat Cooling Setpoint Temperature',
                    'Zone Thermostat Control Type'
                    ]
    for var in out_var_list:
        output_variable(idf,  var)

    # ============== Output:Meters ==============
    OutputMeter = output_meter(idf)
    
    # ============== Output:Table:SummaryReports ==============
    OutputTableSummaryReports = output_table_summary_reports(idf)


    # ============== OutputControl:Files ==============
    OutputControlFiles = output_control_files(idf)


    idf.saveas(path_save + f'{osm_id}_IdealHVAC.idf')
    print(f'{idx_b+1}) {osm_id} Generated')

