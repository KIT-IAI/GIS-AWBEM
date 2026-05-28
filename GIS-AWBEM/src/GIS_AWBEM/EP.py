import numpy as np
from GIS_AWBEM.utilities import *

def simulation_control(
        idf,
        do_zone_sizing="",
        do_system_sizing="",
        do_plant_sizing="",
        run_sizing_periods="",
        run_weather_file="",
        do_hvac_sizing_simulation="",
        max_hvac_sizing_passes=""):
    """
    Create and configure a SimulationControl object for EnergyPlus IDF.
    """
    SimulationControl = idf.newidfobject("SimulationControl")
    SimulationControl.Do_Zone_Sizing_Calculation = do_zone_sizing
    SimulationControl.Do_System_Sizing_Calculation = do_system_sizing
    SimulationControl.Do_Plant_Sizing_Calculation = do_plant_sizing
    SimulationControl.Run_Simulation_for_Sizing_Periods = run_sizing_periods
    SimulationControl.Run_Simulation_for_Weather_File_Run_Periods = run_weather_file
    SimulationControl.Do_HVAC_Sizing_Simulation_for_Sizing_Periods = do_hvac_sizing_simulation
    SimulationControl.Maximum_Number_of_HVAC_Sizing_Simulation_Passes = max_hvac_sizing_passes
    return SimulationControl


def building(
        idf,
        name="Building1",
        north_axis=0,
        terrain="Suburbs",
        loads_convergence_tolerance="",
        temperature_convergence_tolerance="",
        solar_distribution="",
        maximum_warmup_days=25,
        minimum_warmup_days=6):
    """
    Create and configure a Building object for EnergyPlus IDF.
    """
    Building = idf.newidfobject("Building")
    Building.Name = name
    Building.North_Axis = north_axis
    Building.Terrain = terrain
    Building.Loads_Convergence_Tolerance_Value = loads_convergence_tolerance
    Building.Temperature_Convergence_Tolerance_Value = temperature_convergence_tolerance
    Building.Solar_Distribution = solar_distribution
    Building.Maximum_Number_of_Warmup_Days = maximum_warmup_days
    Building.Minimum_Number_of_Warmup_Days = minimum_warmup_days
    return Building


def shadow_calculation(
        idf,
        shading_calculation_method="PolygonClipping",
        shading_calculation_update_frequency_method="Periodic",
        shading_calculation_update_frequency=7,
        maximum_figures_in_shadow_overlap_calculations=15000,
        polygon_clipping_algorithm="SutherlandHodgman",
        pixel_counting_resolution=512,
        sky_diffuse_modeling_algorithm="SimpleSkyDiffuseModeling",
        output_external_shading_calculation_results="No",
        disable_selfshading_within_shading_zone_groups="No",
        disable_selfshading_from_shading_zone_groups_to_other_zones="No",
        shading_zone_group_names=""):
    """
    Create and configure a ShadowCalculation object for EnergyPlus IDF.
    """
    ShadowCalculation = idf.newidfobject("ShadowCalculation")
    ShadowCalculation.Shading_Calculation_Method = shading_calculation_method
    ShadowCalculation.Shading_Calculation_Update_Frequency_Method = shading_calculation_update_frequency_method
    ShadowCalculation.Shading_Calculation_Update_Frequency = shading_calculation_update_frequency
    ShadowCalculation.Maximum_Figures_in_Shadow_Overlap_Calculations = maximum_figures_in_shadow_overlap_calculations
    ShadowCalculation.Polygon_Clipping_Algorithm = polygon_clipping_algorithm
    ShadowCalculation.Pixel_Counting_Resolution = pixel_counting_resolution
    ShadowCalculation.Sky_Diffuse_Modeling_Algorithm = sky_diffuse_modeling_algorithm
    ShadowCalculation.Output_External_Shading_Calculation_Results = output_external_shading_calculation_results
    ShadowCalculation.Disable_SelfShading_Within_Shading_Zone_Groups = disable_selfshading_within_shading_zone_groups
    ShadowCalculation.Disable_SelfShading_From_Shading_Zone_Groups_to_Other_Zones = disable_selfshading_from_shading_zone_groups_to_other_zones
    
    # Set shading zone group names (up to 6 groups)
    if shading_zone_group_names is None:
        shading_zone_group_names = [""] * 6
    else:
        # Pad with empty strings if fewer than 6 provided
        shading_zone_group_names = list(shading_zone_group_names) + [""] * (6 - len(shading_zone_group_names))
    
    for i in range(6):
        ShadowCalculation[f"Shading_Zone_Group_{i+1}_ZoneList_Name"] = shading_zone_group_names[i]
    return ShadowCalculation


def surface_convection_algorithm_inside(
        idf,
        algorithm="Tarp"):
    """
    Create and configure a SurfaceConvectionAlgorithm:Inside object for EnergyPlus IDF.
    """
    SurfaceConvectionAlgorithmInside = idf.newidfobject("SurfaceConvectionAlgorithm:Inside")
    SurfaceConvectionAlgorithmInside.Algorithm = algorithm
    return SurfaceConvectionAlgorithmInside


def surface_convection_algorithm_outside(
        idf,
        algorithm="DOE-2"):
    """
    Create and configure a SurfaceConvectionAlgorithm:Outside object for EnergyPlus IDF.
    """
    SurfaceConvectionAlgorithmOutside = idf.newidfobject("SurfaceConvectionAlgorithm:Outside")
    SurfaceConvectionAlgorithmOutside.Algorithm = algorithm
    return SurfaceConvectionAlgorithmOutside


def heat_balance_algorithm(
        idf,
        algorithm="ConductionTransferFunction",
        surface_temperature_upper_limit="",
        minimum_surface_convection_heat_transfer_coefficient_value="",
        maximum_surface_convection_heat_transfer_coefficient_value=""):
    """
    Create and configure a HeatBalanceAlgorithm object for EnergyPlus IDF.
    """
    HeatBalanceAlgorithm = idf.newidfobject("HeatBalanceAlgorithm")
    HeatBalanceAlgorithm.Algorithm = algorithm
    HeatBalanceAlgorithm.Surface_Temperature_Upper_Limit = surface_temperature_upper_limit
    HeatBalanceAlgorithm.Minimum_Surface_Convection_Heat_Transfer_Coefficient_Value = minimum_surface_convection_heat_transfer_coefficient_value
    HeatBalanceAlgorithm.Maximum_Surface_Convection_Heat_Transfer_Coefficient_Value = maximum_surface_convection_heat_transfer_coefficient_value
    return HeatBalanceAlgorithm


def zone_air_heat_balance_algorithm(
        idf,
        algorithm="AnalyticalSolution",
        do_space_heat_balance_for_sizing="No",
        do_space_heat_balance_for_simulation="No"):
    """
    Create and configure a ZoneAirHeatBalanceAlgorithm object for EnergyPlus IDF.
    """
    ZoneAirHeatBalanceAlgorithm = idf.newidfobject("ZoneAirHeatBalanceAlgorithm")
    ZoneAirHeatBalanceAlgorithm.Algorithm = algorithm
    ZoneAirHeatBalanceAlgorithm.Do_Space_Heat_Balance_for_Sizing = do_space_heat_balance_for_sizing
    ZoneAirHeatBalanceAlgorithm.Do_Space_Heat_Balance_for_Simulation = do_space_heat_balance_for_simulation
    return ZoneAirHeatBalanceAlgorithm


def timestep(
        idf,
        number_of_timesteps_per_hour=""):
    """
    Create and configure a Timestep object for EnergyPlus IDF.
    """
    Timestep = idf.newidfobject("Timestep")
    Timestep.Number_of_Timesteps_per_Hour = number_of_timesteps_per_hour
    return Timestep


def convergence_limits(
        idf,
        minimum_system_timestep=1,
        maximum_hvac_iterations="",
        minimum_plant_iterations="",
        maximum_plant_iterations=""):
    """
    Create and configure a ConvergenceLimits object for EnergyPlus IDF.
    """
    ConvergenceLimits = idf.newidfobject("ConvergenceLimits")
    ConvergenceLimits.Minimum_System_Timestep = minimum_system_timestep
    ConvergenceLimits.Maximum_HVAC_Iterations = maximum_hvac_iterations
    ConvergenceLimits.Minimum_Plant_Iterations = minimum_plant_iterations
    ConvergenceLimits.Maximum_Plant_Iterations = maximum_plant_iterations
    return ConvergenceLimits


def site_location(
        idf,
        name="urban_district",
        latitude="",
        longitude="",
        time_zone="",
        elevation="",
        keep_site_location_information=""):
    """
    Create and configure a Site:Location object for EnergyPlus IDF.
    """
    SiteLocation = idf.newidfobject("Site:Location")
    SiteLocation.Name = name
    SiteLocation.Latitude = latitude
    SiteLocation.Longitude = longitude
    SiteLocation.Time_Zone = time_zone
    SiteLocation.Elevation = elevation
    SiteLocation.Keep_Site_Location_Information = keep_site_location_information
    return SiteLocation


def sizing_period_design_day(
        idf,
        name="winter_design_day",
        month=1,
        day_of_month=21,
        day_type="WinterDesignDay",
        maximum_drybulb_temperature="",
        daily_drybulb_temperature_range="",
        drybulb_temperature_range_modifier_type="",
        drybulb_temperature_range_modifier_day_schedule_name="",
        humidity_condition_type="",
        wetbulb_or_dewpoint_at_maximum_drybulb="",
        humidity_condition_day_schedule_name="",
        humidity_ratio_at_maximum_drybulb="",
        enthalpy_at_maximum_drybulb="",
        daily_wetbulb_temperature_range="",
        barometric_pressure="",
        wind_speed=5,
        wind_direction=270,
        rain_indicator="",
        snow_indicator="",
        daylight_saving_time_indicator="Yes",
        solar_model_indicator="",
        beam_solar_day_schedule_name="",
        diffuse_solar_day_schedule_name="",
        ashrae_clear_sky_optical_depth_for_beam_irradiance_taub="",
        ashrae_clear_sky_optical_depth_for_diffuse_irradiance_taud="",
        sky_clearness="",
        maximum_number_warmup_days="",
        begin_environment_reset_mode=""):
    """
    Create and configure a SizingPeriod:DesignDay object for EnergyPlus IDF.
    """
    SizingPeriodDesignDay = idf.newidfobject("SizingPeriod:DesignDay")
    SizingPeriodDesignDay.Name = name
    SizingPeriodDesignDay.Month = month
    SizingPeriodDesignDay.Day_of_Month = day_of_month
    SizingPeriodDesignDay.Day_Type = day_type
    SizingPeriodDesignDay.Maximum_DryBulb_Temperature = maximum_drybulb_temperature
    SizingPeriodDesignDay.Daily_DryBulb_Temperature_Range = daily_drybulb_temperature_range
    SizingPeriodDesignDay.DryBulb_Temperature_Range_Modifier_Type = drybulb_temperature_range_modifier_type
    SizingPeriodDesignDay.DryBulb_Temperature_Range_Modifier_Day_Schedule_Name = drybulb_temperature_range_modifier_day_schedule_name
    SizingPeriodDesignDay.Humidity_Condition_Type = humidity_condition_type
    SizingPeriodDesignDay.Wetbulb_or_DewPoint_at_Maximum_DryBulb = wetbulb_or_dewpoint_at_maximum_drybulb
    SizingPeriodDesignDay.Humidity_Condition_Day_Schedule_Name = humidity_condition_day_schedule_name
    SizingPeriodDesignDay.Humidity_Ratio_at_Maximum_DryBulb = humidity_ratio_at_maximum_drybulb
    SizingPeriodDesignDay.Enthalpy_at_Maximum_DryBulb = enthalpy_at_maximum_drybulb
    SizingPeriodDesignDay.Daily_WetBulb_Temperature_Range = daily_wetbulb_temperature_range
    SizingPeriodDesignDay.Barometric_Pressure = barometric_pressure
    SizingPeriodDesignDay.Wind_Speed = wind_speed
    SizingPeriodDesignDay.Wind_Direction = wind_direction
    SizingPeriodDesignDay.Rain_Indicator = rain_indicator
    SizingPeriodDesignDay.Snow_Indicator = snow_indicator
    SizingPeriodDesignDay.Daylight_Saving_Time_Indicator = daylight_saving_time_indicator
    SizingPeriodDesignDay.Solar_Model_Indicator = solar_model_indicator
    SizingPeriodDesignDay.Beam_Solar_Day_Schedule_Name = beam_solar_day_schedule_name
    SizingPeriodDesignDay.Diffuse_Solar_Day_Schedule_Name = diffuse_solar_day_schedule_name
    SizingPeriodDesignDay.ASHRAE_Clear_Sky_Optical_Depth_for_Beam_Irradiance_taub = ashrae_clear_sky_optical_depth_for_beam_irradiance_taub
    SizingPeriodDesignDay.ASHRAE_Clear_Sky_Optical_Depth_for_Diffuse_Irradiance_taud = ashrae_clear_sky_optical_depth_for_diffuse_irradiance_taud
    SizingPeriodDesignDay.Sky_Clearness = sky_clearness
    SizingPeriodDesignDay.Maximum_Number_Warmup_Days = maximum_number_warmup_days
    SizingPeriodDesignDay.Begin_Environment_Reset_Mode = begin_environment_reset_mode
    return SizingPeriodDesignDay


def run_period(
        idf,
        name="name",
        begin_month=1,
        begin_day_of_month=1,
        begin_year=2024,
        end_month=12,
        end_day_of_month=31,
        end_year=2024,
        use_weather_file_holidays_and_special_days="Yes",
        use_weather_file_daylight_saving_period="Yes",
        apply_weekend_holiday_rule="No",
        use_weather_file_rain_indicators="Yes",
        use_weather_file_snow_indicators="Yes",
        treat_weather_as_actual="No",
        first_hour_interpolation_starting_values="Hour24"):
    """
    Create and configure a RunPeriod object for EnergyPlus IDF.
    """
    RunPeriod = idf.newidfobject("RunPeriod")
    RunPeriod.Name = name
    RunPeriod.Begin_Month = begin_month
    RunPeriod.Begin_Day_of_Month = begin_day_of_month
    RunPeriod.Begin_Year = begin_year
    RunPeriod.End_Month = end_month
    RunPeriod.End_Day_of_Month = end_day_of_month
    RunPeriod.End_Year = end_year
    RunPeriod.Use_Weather_File_Holidays_and_Special_Days = use_weather_file_holidays_and_special_days
    RunPeriod.Use_Weather_File_Daylight_Saving_Period = use_weather_file_daylight_saving_period
    RunPeriod.Apply_Weekend_Holiday_Rule = apply_weekend_holiday_rule
    RunPeriod.Use_Weather_File_Rain_Indicators = use_weather_file_rain_indicators
    RunPeriod.Use_Weather_File_Snow_Indicators = use_weather_file_snow_indicators
    RunPeriod.Treat_Weather_as_Actual = treat_weather_as_actual
    RunPeriod.First_Hour_Interpolation_Starting_Values = first_hour_interpolation_starting_values
    return RunPeriod


def ground_temperature_building_surface(
        idf,
        Jan="",
        Feb="",
        Mar="",
        Apr="",
        May="",
        Jun="",
        Jul="",
        Aug="",
        Sep="",
        Oct="",
        Nov="",
        Dec=""):
    """
    Create and configure a Site:GroundTemperature:BuildingSurface object for EnergyPlus IDF.
    """
    GroundTemperatureBuildingSurface = idf.newidfobject("Site:GroundTemperature:BuildingSurface")
    GroundTemperatureBuildingSurface.January_Ground_Temperature = Jan
    GroundTemperatureBuildingSurface.February_Ground_Temperature = Feb
    GroundTemperatureBuildingSurface.March_Ground_Temperature = Mar
    GroundTemperatureBuildingSurface.April_Ground_Temperature = Apr
    GroundTemperatureBuildingSurface.May_Ground_Temperature = May
    GroundTemperatureBuildingSurface.June_Ground_Temperature = Jun
    GroundTemperatureBuildingSurface.July_Ground_Temperature = Jul
    GroundTemperatureBuildingSurface.August_Ground_Temperature = Aug
    GroundTemperatureBuildingSurface.September_Ground_Temperature = Sep
    GroundTemperatureBuildingSurface.October_Ground_Temperature = Oct
    GroundTemperatureBuildingSurface.November_Ground_Temperature = Nov
    GroundTemperatureBuildingSurface.December_Ground_Temperature = Dec
    return GroundTemperatureBuildingSurface



def schedule_type_limits(
        idf,
        name="",
        low="",
        up="",
        numeric_type="",
        unit_type=""):
    """
    Create and configure a ScheduleTypeLimits object for EnergyPlus IDF.
    """
    ScheduleTypeLimits = idf.newidfobject("ScheduleTypeLimits")
    ScheduleTypeLimits.Name = name
    ScheduleTypeLimits.Lower_Limit_Value = low
    ScheduleTypeLimits.Upper_Limit_Value = up
    ScheduleTypeLimits.Numeric_Type = numeric_type
    ScheduleTypeLimits.Unit_Type = unit_type
    return ScheduleTypeLimits

def schedule_from_profile(
        idf,
        profile="",
        name="",
        type_limit=""):
    """
    Create and configure hourly-based daily ScheduleCompact object for EnergyPlus for internal gains and temperature setpoint schedules.
    """
    ScheduleCompact = idf.newidfobject("Schedule:Compact")
    ScheduleCompact.Name = name
    ScheduleCompact.Schedule_Type_Limits_Name = type_limit
    ScheduleCompact.Field_1 = "Through: 12/31"
    ScheduleCompact.Field_2 = "For: AllDays"
    for i, v in enumerate(profile):
        ScheduleCompact[f"Field_{i+3}"] = f"Until: {i+1}:00, {v}"
    return

def schedule_heating_nonres(
        idf,
        profile_wd="",
        profile_we="",
        name="",
        type_limit=""):
    """
    Create and configure a ScheduleCompact object for EnergyPlus for temperature setpoint schedules of non-residential buildings.
    """
    ScheduleCompact = idf.newidfobject("Schedule:Compact")
    ScheduleCompact.Name = name
    ScheduleCompact.Schedule_Type_Limits_Name = type_limit
    ScheduleCompact.Field_1 = "Through: 12/31"
    ScheduleCompact.Field_2 = "For: Weekdays"
    
    for i, v in enumerate(profile_wd):
        ScheduleCompact[f"Field_{i+3}"] = f"Until: {i+1}:00, {v}"
    
    count = i
    ScheduleCompact[f"Field_{count+4}"] = "For: Weekends AllOtherDays"
    for j, v in enumerate(profile_we):
        ScheduleCompact[f"Field_{count+5}"] = f"Until: {j+1}:00, {v}"
        count += 1
    return 

def constant_schedule(
        idf,
        value="",
        name="",
        type_limit=""):
    """
    Create and configure a ScheduleCompact object with constant value for the whole year.
    """
    ScheduleCompact = idf.newidfobject("Schedule:Compact")
    ScheduleCompact.Name = name
    ScheduleCompact.Schedule_Type_Limits_Name = type_limit
    ScheduleCompact.Field_1 = "Through: 12/31"
    ScheduleCompact.Field_2 = "For: AllDays"
    ScheduleCompact.Field_3 = "Until: 24:00"
    ScheduleCompact.Field_4 = value
    return

def active_summer_schedule(idf):
    """
    Create and configure a ScheduleCompact object bein active in summer time.
    """
    ScheduleCompact = idf.newidfobject("Schedule:Compact")
    ScheduleCompact.Name = "Active_summer"
    ScheduleCompact.Schedule_Type_Limits_Name = "Fraction"
    ScheduleCompact.Field_1 = "Through: 4/30"
    ScheduleCompact.Field_2 = "For: AllDays"
    ScheduleCompact.Field_3 = "Until: 24:00"
    ScheduleCompact.Field_4 = 0
    ScheduleCompact.Field_5 = "Through: 9/30"
    ScheduleCompact.Field_6 = "For: AllDays"
    ScheduleCompact.Field_7 = "Until: 24:00"
    ScheduleCompact.Field_8 = 1
    ScheduleCompact.Field_9 = "Through: 12/31"
    ScheduleCompact.Field_10 = "For: AllDays"
    ScheduleCompact.Field_11 = "Until: 24:00"
    ScheduleCompact.Field_12 = 0
    return

def active_winter_schedule(idf):
    """
    Create and configure a ScheduleCompact object bein active in winter time.
    """
    ScheduleCompact = idf.newidfobject("Schedule:Compact")
    ScheduleCompact.Name = "Active_winter"
    ScheduleCompact.Schedule_Type_Limits_Name = "Fraction"
    ScheduleCompact.Field_1 = "Through: 4/30"
    ScheduleCompact.Field_2 = "For: AllDays"
    ScheduleCompact.Field_3 = "Until: 24:00"
    ScheduleCompact.Field_4 = 1
    ScheduleCompact.Field_5 = "Through: 9/30"
    ScheduleCompact.Field_6 = "For: AllDays"
    ScheduleCompact.Field_7 = "Until: 24:00"
    ScheduleCompact.Field_8 = 0
    ScheduleCompact.Field_9 = "Through: 12/31"
    ScheduleCompact.Field_10 = "For: AllDays"
    ScheduleCompact.Field_11 = "Until: 24:00"
    ScheduleCompact.Field_12 = 1
    return

def always_ON_schedule(idf):
    """
    Create and configure a ScheduleCompact object to keep a device always on.
    """
    ScheduleCompact = idf.newidfobject("Schedule:Compact")
    ScheduleCompact.Name = "Always ON"
    ScheduleCompact.Schedule_Type_Limits_Name = "Fraction"
    ScheduleCompact.Field_1 = "Through: 12/31"
    ScheduleCompact.Field_2 = "For: AllDays"
    ScheduleCompact.Field_3 = "Until: 24:00"
    ScheduleCompact.Field_4 = 1
    return

def set_thermostat1(idf):
    """
    Create and configure a ScheduleCompact object for thermostat control type 1.
    """
    ScheduleCompact = idf.newidfobject("Schedule:Compact")
    ScheduleCompact.Name = "Thermostat_control_type"
    ScheduleCompact.Schedule_Type_Limits_Name = "Control Type"
    ScheduleCompact.Field_1 = "Through: 4/30"
    ScheduleCompact.Field_2 = "For: AllDays"
    ScheduleCompact.Field_3 = "Until: 24:00"
    ScheduleCompact.Field_4 = 1
    ScheduleCompact.Field_5 = "Through: 9/30"
    ScheduleCompact.Field_6 = "For: AllDays"
    ScheduleCompact.Field_7 = "Until: 24:00"
    ScheduleCompact.Field_8 = 2
    ScheduleCompact.Field_9 = "Through: 12/31"
    ScheduleCompact.Field_10 = "For: AllDays"
    ScheduleCompact.Field_11 = "Until: 24:00"
    ScheduleCompact.Field_12 = 1
    return

def set_thermostat2(idf):
    """
    Create and configure a ScheduleCompact object for thermostat control type 2.
    """
    ScheduleCompact = idf.newidfobject("Schedule:Compact")
    ScheduleCompact.Name = "Thermostat_control_type"
    ScheduleCompact.Schedule_Type_Limits_Name = "Control Type"
    ScheduleCompact.Field_1 = "Through: 4/30"
    ScheduleCompact.Field_2 = "For: AllDays"
    ScheduleCompact.Field_3 = "Until: 07:00"
    ScheduleCompact.Field_4 = 0
    ScheduleCompact.Field_5 = "Until: 19:00"
    ScheduleCompact.Field_6 = 1
    ScheduleCompact.Field_7 = "Until: 24:00"
    ScheduleCompact.Field_8 = 0
    ScheduleCompact.Field_9 = "Through: 9/30"
    ScheduleCompact.Field_10 = "For: AllDays"
    ScheduleCompact.Field_11 = "Until: 07:00"
    ScheduleCompact.Field_12 = 0
    ScheduleCompact.Field_13 = "Until: 19:00"
    ScheduleCompact.Field_14 = 2
    ScheduleCompact.Field_15 = "Until: 24:00"
    ScheduleCompact.Field_16 = 0
    ScheduleCompact.Field_17 = "Through: 12/31"
    ScheduleCompact.Field_18 = "For: AllDays"
    ScheduleCompact.Field_19 = "Until: 07:00"
    ScheduleCompact.Field_20 = 0
    ScheduleCompact.Field_21 = "Until: 19:00"
    ScheduleCompact.Field_22 = 1
    ScheduleCompact.Field_23 = "Until: 24:00"
    ScheduleCompact.Field_24 = 0
    return


def wall_material(idf,
                  wall_mat_dict):
    """
    Create and configure wall material and construction objects for EnergyPlus IDF.
    Either a dictionary of material layers (each with keys: "name", "thickness",
    "lambda", "rho", "c"), or a single numeric value representing the overall U-value.
    """

    # no enrichment: only a U-value is provided
    if not isinstance(wall_mat_dict, dict):
        u_value = wall_mat_dict
        wall_mat = idf.newidfobject("Material:NoMass")
        wall_mat.Name = "wall_no_mass"
        wall_mat.Roughness = "MediumRough"
        wall_mat.Thermal_Resistance = 1.0 / u_value  # R = 1/U [m²K/W]

        wall_const = idf.newidfobject("Construction")
        wall_const.Name = "wall_const"
        wall_const.Outside_Layer = wall_mat.Name
        return

    # with enrichment: material properties of layers are provided
    wall_mat_list = []
    for i, (k, v) in enumerate(wall_mat_dict.items()):
        if "air" in v["name"] or v["c"] < 100:
            wall_mat = idf.newidfobject("Material:AirGap")
            wall_mat.Name = f"L{i+1} wall " + v["name"]
            wall_mat.Thermal_Resistance = v["thickness"]/100 / v["lambda"]
        else:
            wall_mat = idf.newidfobject("Material")
            wall_mat.Name = f"L{i+1} wall " + v["name"]
            wall_mat.Roughness = "MediumRough"
            wall_mat.Thickness = v["thickness"]/100 # [cm] to [m]
            wall_mat.Conductivity = v["lambda"]
            wall_mat.Density = v["rho"]
            wall_mat.Specific_Heat = v["c"]
            wall_mat.Thermal_Absorptance = ""
            wall_mat.Solar_Absorptance = ""
            wall_mat.Visible_Absorptance = ""
    
        wall_mat_list.append(wall_mat)
    
    # E+ construction orders the layers from outside to inside
    wall_mat_list = wall_mat_list[::-1]
    
    wall_const = idf.newidfobject("Construction")
    wall_const.Name = "wall_const"
    wall_const.Outside_Layer = wall_mat_list[0]["Name"]
    for i in range(1, len(wall_mat_list)):
        wall_const[f"Layer_{i+1}"] = wall_mat_list[i]["Name"]
    
    return

def roof_material(idf,
                 roof_mat_dict):
    """
    Create and configure roof material and construction objects for EnergyPlus IDF.
    Either a dictionary of material layers (each with keys: "name", "thickness",
    "lambda", "rho", "c"), or a single numeric value representing the overall U-value.
    """

    # no enrichment: only a U-value is provided
    if not isinstance(roof_mat_dict, dict):
        u_value = roof_mat_dict
        roof_mat = idf.newidfobject("Material:NoMass")
        roof_mat.Name = "roof_no_mass"
        roof_mat.Roughness = "MediumRough"
        roof_mat.Thermal_Resistance = 1.0 / u_value  # R = 1/U [m²K/W]

        roof_const = idf.newidfobject("Construction")
        roof_const.Name = "roof_const"
        roof_const.Outside_Layer = roof_mat.Name
        return

    roof_mat_list = []
    for i, (k, v) in enumerate(roof_mat_dict.items()):
        if "air" in v["name"] or v["c"] < 100:
            roof_mat = idf.newidfobject("Material:AirGap")
            roof_mat.Name = f"L{i+1} roof " + v["name"]
            roof_mat.Thermal_Resistance = v["thickness"]/100 / v["lambda"]
        else:
            roof_mat = idf.newidfobject("Material")
            roof_mat.Name = f"L{i+1} roof " + v["name"]
            roof_mat.Roughness = "MediumRough"
            roof_mat.Thickness = v["thickness"]/100 # [cm] to [m]
            roof_mat.Conductivity = v["lambda"]
            roof_mat.Density = v["rho"]
            roof_mat.Specific_Heat = v["c"]
            roof_mat.Thermal_Absorptance = ""
            roof_mat.Solar_Absorptance = ""
            roof_mat.Visible_Absorptance = ""
            
        roof_mat_list.append(roof_mat)
    
    # E+ construction orders the layers from outside to inside
    roof_mat_list = roof_mat_list[::-1]
    
    # roof
    roof_const = idf.newidfobject("Construction")
    roof_const.Name = "roof_const"
    roof_const.Outside_Layer = roof_mat_list[0]["Name"]
    for i in range(1, len(roof_mat_list)):
        roof_const[f"Layer_{i+1}"] = roof_mat_list[i]["Name"]
    
    return

def floor_material(idf,
                  floor_mat_dict):
    """
    Create and configure floor material and construction objects for EnergyPlus IDF.
    Either a dictionary of material layers (each with keys: "name", "thickness",
    "lambda", "rho", "c"), or a single numeric value representing the overall U-value.
    """

    # no enrichment: only a U-value is provided
    if not isinstance(floor_mat_dict, dict):
        u_value = floor_mat_dict
        floor_mat = idf.newidfobject("Material:NoMass")
        floor_mat.Name = "floor_no_mass"
        floor_mat.Roughness = "MediumRough"
        floor_mat.Thermal_Resistance = 1.0 / u_value  # R = 1/U [m²K/W]

        floor_const = idf.newidfobject("Construction")
        floor_const.Name = "floor_const"
        floor_const.Outside_Layer = floor_mat.Name
        return

    floor_mat_list = []
    for i, (k, v) in enumerate(floor_mat_dict.items()):
        if "air" in v["name"] or v["c"] < 100:
            floor_mat = idf.newidfobject("Material:AirGap")
            floor_mat.Name = f"L{i+1} floor " + v["name"]
            floor_mat.Thermal_Resistance = v["thickness"]/100 / v["lambda"]
        else:
            floor_mat = idf.newidfobject("Material")
            floor_mat.Name = f"L{i+1} floor " + v["name"]
            floor_mat.Roughness = "MediumRough"
            floor_mat.Thickness = v["thickness"]/100 # [cm] to [m]
            floor_mat.Conductivity = v["lambda"]
            floor_mat.Density = v["rho"]
            floor_mat.Specific_Heat = v["c"]
            floor_mat.Thermal_Absorptance = ""
            floor_mat.Solar_Absorptance = ""
            floor_mat.Visible_Absorptance = ""
            
        floor_mat_list.append(floor_mat)
    
    # E+ construction orders the layers from outside to inside
    floor_mat_list = floor_mat_list[::-1]
    
    # floor
    floor_const = idf.newidfobject("Construction")
    floor_const.Name = "floor_const"
    floor_const.Outside_Layer = floor_mat_list[0]["Name"]
    for i in range(1, len(floor_mat_list)):
        floor_const[f"Layer_{i+1}"] = floor_mat_list[i]["Name"]
    
    return

def window_material(idf,
                    window_u_value):
    """
    Create and configure a window material and construction object for EnergyPlus IDF.
    """

    window_mat = idf.newidfobject("WindowMaterial:SimpleGlazingSystem")
    window_mat.Name = "window_mat"
    window_mat.UFactor = window_u_value
    window_mat.Solar_Heat_Gain_Coefficient = 0.58
    window_mat.Visible_Transmittance = 0.57
    
    # Constructions (with NoMass materials)
    window_const = idf.newidfobject("Construction")
    window_const.Name = "window_const"
    window_const.Outside_Layer = "window_mat"
    return


def global_geometry_rules(
        idf,
        starting_vertex_position="UpperLeftCorner",
        vertex_entry_direction="Counterclockwise",
        coordinate_system="Relative",
        daylighting_reference_point_coordinate_system="",
        rectangular_surface_coordinate_system=""):
    """
    Create and configure a GlobalGeometryRules object for EnergyPlus IDF.
    """
    GlobalGeometryRules = idf.newidfobject("GlobalGeometryRules")
    GlobalGeometryRules.Starting_Vertex_Position = starting_vertex_position
    GlobalGeometryRules.Vertex_Entry_Direction = vertex_entry_direction
    GlobalGeometryRules.Coordinate_System = coordinate_system
    GlobalGeometryRules.Daylighting_Reference_Point_Coordinate_System = daylighting_reference_point_coordinate_system
    GlobalGeometryRules.Rectangular_Surface_Coordinate_System = rectangular_surface_coordinate_system
    return GlobalGeometryRules


def space(idf,
            name="Space1",
            zone_name="Zone1",
            ceiling_height="",
            volume="",
            floor_area="",
            space_type="",
            tag_1="",
            tag_2="",
            tag_3=""):
    """
    Create and configure a Space object for EnergyPlus IDF.
    """
    Space = idf.newidfobject("Space")
    Space.Name = name
    Space.Zone_Name = zone_name
    Space.Ceiling_Height = ceiling_height
    Space.Volume = volume
    Space.Floor_Area = floor_area
    Space.Space_Type = space_type
    Space.Tag_1 = tag_1
    Space.Tag_2 = tag_2
    Space.Tag_3 = tag_3
    return Space


def space_list(
        idf,
        name="Space_list1",
        space_names=None):
    """
    Create and configure a SpaceList object for EnergyPlus IDF.
    """
    if space_names is None:
        space_names = ["Space1"]
    
    SpaceList = idf.newidfobject("SpaceList")
    SpaceList.Name = name
    
    for i, space_name in enumerate(space_names, 1):
        SpaceList[f"Space_{i}_Name"] = space_name
    return SpaceList


def zone(
        idf,
        name="Zone1",
        direction_of_relative_north="",
        x_origin="",
        y_origin="",
        z_origin="",
        zone_type=1,
        multiplier=1,
        ceiling_height="autocalculate",
        volume="autocalculate",
        floor_area="autocalculate",
        zone_inside_convection_algorithm="",
        zone_outside_convection_algorithm="",
        part_of_total_floor_area=""):
    """
    Create and configure a Zone object for EnergyPlus IDF.
    """
    Zone = idf.newidfobject("Zone")
    Zone.Name = name
    Zone.Direction_of_Relative_North = direction_of_relative_north
    Zone.X_Origin = x_origin
    Zone.Y_Origin = y_origin
    Zone.Z_Origin = z_origin
    Zone.Type = zone_type
    Zone.Multiplier = multiplier
    Zone.Ceiling_Height = ceiling_height
    Zone.Volume = volume
    Zone.Floor_Area = floor_area
    Zone.Zone_Inside_Convection_Algorithm = zone_inside_convection_algorithm
    Zone.Zone_Outside_Convection_Algorithm = zone_outside_convection_algorithm
    Zone.Part_of_Total_Floor_Area = part_of_total_floor_area
    return Zone

def roof_surface(
        idf,
        coords):
    """
    Create and configure a Roof surface object for EnergyPlus IDF.
    """
    Roof = idf.newidfobject("BuildingSurface:Detailed")
    Roof.Name = "Roof"
    Roof.Surface_Type = "Roof"
    Roof.Construction_Name = "roof_const"
    Roof.Zone_Name = "Zone1"
    Roof.Space_Name = ""
    Roof.Outside_Boundary_Condition = "Outdoors"
    Roof.Outside_Boundary_Condition_Object = ""
    Roof.Sun_Exposure = "SunExposed"
    Roof.Wind_Exposure = "WindExposed"
    Roof.View_Factor_to_Ground = "autocalculate"
    Roof.Number_of_Vertices = coords.shape[0]
    for i, point in enumerate(coords):
        NO = i+1
        Roof[f"Vertex_{NO}_Xcoordinate"] = point[0]
        Roof[f"Vertex_{NO}_Ycoordinate"] = point[1]
        Roof[f"Vertex_{NO}_Zcoordinate"] = point[2]
    return

def floor_surface(
        idf,
        floor_coords_CW):
    """
    Create and configure a Floor surface object for EnergyPlus IDF.
    """
    Floor = idf.newidfobject("BuildingSurface:Detailed")
    Floor.Name = "Floor"
    Floor.Surface_Type = "Floor"
    Floor.Construction_Name = "floor_const"
    Floor.Zone_Name = "Zone1"
    Floor.Space_Name = ""
    Floor.Outside_Boundary_Condition = "Ground"
    Floor.Outside_Boundary_Condition_Object = ""
    Floor.Sun_Exposure = "NoSun"
    Floor.Wind_Exposure = "NoWind"
    Floor.View_Factor_to_Ground = "autocalculate"
    Floor.Number_of_Vertices = floor_coords_CW.shape[0]
    
    # Surfaces of Floor and Roof need to have opposite tilt angles i.e. 0,180. Reversing the vertices order solves this.
    for i, point in enumerate(floor_coords_CW):
        NO = i+1
        Floor[f"Vertex_{NO}_Xcoordinate"] = point[0]
        Floor[f"Vertex_{NO}_Ycoordinate"] = point[1]
        Floor[f"Vertex_{NO}_Zcoordinate"] = point[2]

    return

def wall_surface(
        idf,
        coords):
    """
    Create and configure wall surface objects for EnergyPlus IDF.
    """
    No_of_walls = coords.shape[0]
    floor_coords_CW = np.copy(coords[::-1])
    floor_coords_CW[:, -1] = 0
    
    # Add first element to the end to close the polygon
    Btop_coords_extended = np.vstack((coords, coords[0,:]))
    wall_dict = {}
    for i in range(No_of_walls):
        Wall = idf.newidfobject("BuildingSurface:Detailed")
        Wall.Name = f"Wall_{i}"
        Wall.Surface_Type = "Wall"
        Wall.Construction_Name = "wall_const"
        Wall.Zone_Name = "Zone1"
        Wall.Space_Name = ""
        Wall.Outside_Boundary_Condition = "Outdoors"
        Wall.Outside_Boundary_Condition_Object = ""
        Wall.Sun_Exposure = "SunExposed"
        Wall.Wind_Exposure = "WindExposed"
        Wall.View_Factor_to_Ground = "autocalculate"
        Wall.Number_of_Vertices = 4
    
        # roof and floor vertices for each wall
        rf_ver = Btop_coords_extended[i:i+2, :]
        fl_vert = np.hstack((Btop_coords_extended[i:i+2, :-1], np.array([0,0])[:,None]))            
        wall_vert = np.vstack((rf_ver, fl_vert))    
    
        # Sort/align the vertices
        wall_vert_sorted = sort_CCW_wall(wall_vert, floor_coords_CW)
        # wall_vert_sorted = wall_vert

        for w in range(Wall.Number_of_Vertices):
            NO = w+1 
            Wall[f"Vertex_{NO}_Xcoordinate"] = wall_vert_sorted[w, 0]
            Wall[f"Vertex_{NO}_Ycoordinate"] = wall_vert_sorted[w, 1]
            Wall[f"Vertex_{NO}_Zcoordinate"] = wall_vert_sorted[w, 2]
        
        wall_dict[Wall.Name] = wall_vert_sorted
    
    return wall_dict


def window_surface(
        idf,
        wall_dict,
        WWR):
    """
    Create and configure window surface objects for EnergyPlus IDF.
    """
    # Assumption: each wall contains a window
    No_of_windows = len(wall_dict)
    
    window_dict = {}
    for i in range(No_of_windows):
        Window = idf.newidfobject("FenestrationSurface:Detailed")
        Window.Name = f"Window_{i}"
        Window.Surface_Type = "Window"
        Window.Construction_Name = "window_const"
        Window.Building_Surface_Name = f"Wall_{i}"
        Window.Outside_Boundary_Condition_Object = ""
        Window.View_Factor_to_Ground = "autocalculate"
        Window.Number_of_Vertices = 4
        
        window_vert_sorted = generate_window_vertices(wall_dict[f"Wall_{i}"], WWR)
        for w in range(Window.Number_of_Vertices):
            NO = w+1 
            Window[f"Vertex_{NO}_Xcoordinate"] = window_vert_sorted[w, 0]
            Window[f"Vertex_{NO}_Ycoordinate"] = window_vert_sorted[w, 1]
            Window[f"Vertex_{NO}_Zcoordinate"] = window_vert_sorted[w, 2]
        
        window_dict[Window.Name] = window_vert_sorted
    
    return


def generate_window_vertices(wall_vertices, WWR):
    """
    Generate window vertices based on wall vertices and WWR."""

    # assumptions:
    #     aspect ratio of wall and window are equal
    #     center points of wall and window are the same
    #     vertices are already sorted
    
    if wall_vertices[0,2] == wall_vertices[1,2]:
        L_hor = distance(wall_vertices[0], wall_vertices[1])
        L_ver = distance(wall_vertices[0], wall_vertices[-1])
    else:
        L_ver = distance(wall_vertices[0], wall_vertices[1])
        L_hor = distance(wall_vertices[0], wall_vertices[-1])
    
    
    # angle between the wall and the xz plane
    xz_plane = Plane(Point3D(0,0,0), Point3D(1,0,0), Point3D(0,0,1))
    pp1 = Plane(Point3D(wall_vertices[0]), Point3D(wall_vertices[1]), Point3D(wall_vertices[2]))
    theta = float(pp1.angle_between(xz_plane)) # radian
    pi_rad = np.pi 
    if theta > pi_rad/2: theta = pi_rad - theta
    
    # Center vertice
    CP = Centroid(wall_vertices)
    
    # Move the points: relative (to the origin) vertices
    ver_rel = wall_vertices - CP
    
    # rotation around z axis. x-axis will be coplanar. y-axis will be normal vector
    r = np.sqrt(ver_rel[:,0]**2 + ver_rel[:,1]**2)
    X_vert_rotated = r * np.sign(ver_rel[:,0])
    Y_vert_rotated = np.zeros((ver_rel[:,1].shape[0]))
    Z_vert_rotated = ver_rel[:,-1]
    Vert_rotated = np.array((X_vert_rotated, Y_vert_rotated, Z_vert_rotated)).T
    
    # assumption: length to width (aspec) ratio of wall and window are equal
    window_Z = L_ver * np.sqrt(WWR)
    window_X = window_Z * L_hor/L_ver
    
    # window vertices
    verts = np.array((window_X/2, 0, window_Z/2)) * np.ones(Vert_rotated.shape)
    window_vertices_rotated = np.sign(Vert_rotated) * verts
    
    # rotate back (around z axis)   
    rw = np.sqrt(window_vertices_rotated[:,0]**2 + window_vertices_rotated[:,1]**2)
    window_vertices_X = rw * np.cos(theta)
    window_vertices_Y = rw * np.sin(theta)
    window_vertices_Z = window_vertices_rotated[:,-1]
    window_vertices_rotated_back = np.array([np.sign(ver_rel[:,0])*window_vertices_X, np.sign(ver_rel[:,1])*window_vertices_Y, window_vertices_Z]).T
    
    # Move the vertices back
    window_vertices = window_vertices_rotated_back + CP
    
    return window_vertices


def people(
        idf,
        name="People1",
        zone_or_zonelist_or_space_or_spacelist_name="Zone1",
        number_of_people_schedule_name="Occupancy_schedule",
        number_of_people_calculation_method="People/Area",
        number_of_people="",
        people_per_floor_area="",
        floor_area_per_person="",
        fraction_radiant="",
        sensible_heat_fraction="",
        activity_level_schedule_name="Activity_schedule",
        carbon_dioxide_generation_rate="",
        enable_ashrae_55_comfort_warnings="",
        mean_radiant_temperature_calculation_type="",
        surface_name_angle_factor_list_name="",
        work_efficiency_schedule_name="",
        clothing_insulation_calculation_method="",
        clothing_insulation_calculation_method_schedule_name="",
        clothing_insulation_schedule_name="",
        air_velocity_schedule_name="",
        thermal_comfort_model_1_type="",
        thermal_comfort_model_2_type="",
        thermal_comfort_model_3_type="",
        thermal_comfort_model_4_type="",
        thermal_comfort_model_5_type="",
        thermal_comfort_model_6_type="",
        thermal_comfort_model_7_type="",
        ankle_level_air_velocity_schedule_name="",
        cold_stress_temperature_threshold="",
        heat_stress_temperature_threshold=""):
    """
    Create and configure a People object for EnergyPlus IDF.
    """
    People = idf.newidfobject("People")
    People.Name = name
    People.Zone_or_ZoneList_or_Space_or_SpaceList_Name = zone_or_zonelist_or_space_or_spacelist_name
    People.Number_of_People_Schedule_Name = number_of_people_schedule_name
    People.Number_of_People_Calculation_Method = number_of_people_calculation_method
    People.Number_of_People = number_of_people
    People.People_per_Floor_Area = people_per_floor_area
    People.Floor_Area_per_Person = floor_area_per_person
    People.Fraction_Radiant = fraction_radiant
    People.Sensible_Heat_Fraction = sensible_heat_fraction
    People.Activity_Level_Schedule_Name = activity_level_schedule_name
    People.Carbon_Dioxide_Generation_Rate = carbon_dioxide_generation_rate
    People.Enable_ASHRAE_55_Comfort_Warnings = enable_ashrae_55_comfort_warnings
    People.Mean_Radiant_Temperature_Calculation_Type = mean_radiant_temperature_calculation_type
    People.Surface_NameAngle_Factor_List_Name = surface_name_angle_factor_list_name
    People.Work_Efficiency_Schedule_Name = work_efficiency_schedule_name
    People.Clothing_Insulation_Calculation_Method = clothing_insulation_calculation_method
    People.Clothing_Insulation_Calculation_Method_Schedule_Name = clothing_insulation_calculation_method_schedule_name
    People.Clothing_Insulation_Schedule_Name = clothing_insulation_schedule_name
    People.Air_Velocity_Schedule_Name = air_velocity_schedule_name
    People.Thermal_Comfort_Model_1_Type = thermal_comfort_model_1_type
    People.Thermal_Comfort_Model_2_Type = thermal_comfort_model_2_type
    People.Thermal_Comfort_Model_3_Type = thermal_comfort_model_3_type
    People.Thermal_Comfort_Model_4_Type = thermal_comfort_model_4_type
    People.Thermal_Comfort_Model_5_Type = thermal_comfort_model_5_type
    People.Thermal_Comfort_Model_6_Type = thermal_comfort_model_6_type
    People.Thermal_Comfort_Model_7_Type = thermal_comfort_model_7_type
    People.Ankle_Level_Air_Velocity_Schedule_Name = ankle_level_air_velocity_schedule_name
    People.Cold_Stress_Temperature_Threshold = cold_stress_temperature_threshold
    People.Heat_Stress_Temperature_Threshold = heat_stress_temperature_threshold
    return People


def lights(
        idf,
        name="Lights1",
        zone_or_zonelist_or_space_or_spacelist_name="Zone1",
        schedule_name="Lights_schedule",
        design_level_calculation_method="",
        lighting_level="",
        watts_per_floor_area="",
        watts_per_person="",
        return_air_fraction="",
        fraction_radiant="",
        fraction_visible="",
        fraction_replaceable="",
        enduse_subcategory="",
        return_air_fraction_calculated_from_plenum_temperature="",
        return_air_fraction_function_of_plenum_temperature_coefficient_1="",
        return_air_fraction_function_of_plenum_temperature_coefficient_2="",
        return_air_heat_gain_node_name="",
        exhaust_air_heat_gain_node_name=""):
    """
    Create and configure a Lights object for EnergyPlus IDF.
    """
    Lights = idf.newidfobject("Lights")
    Lights.Name = name
    Lights.Zone_or_ZoneList_or_Space_or_SpaceList_Name = zone_or_zonelist_or_space_or_spacelist_name
    Lights.Schedule_Name = schedule_name
    Lights.Design_Level_Calculation_Method = design_level_calculation_method
    Lights.Lighting_Level = lighting_level
    Lights.Watts_per_Floor_Area = watts_per_floor_area
    Lights.Watts_per_Person = watts_per_person
    Lights.Return_Air_Fraction = return_air_fraction
    Lights.Fraction_Radiant = fraction_radiant
    Lights.Fraction_Visible = fraction_visible
    Lights.Fraction_Replaceable = fraction_replaceable
    Lights.EndUse_Subcategory = enduse_subcategory
    Lights.Return_Air_Fraction_Calculated_from_Plenum_Temperature = return_air_fraction_calculated_from_plenum_temperature
    Lights.Return_Air_Fraction_Function_of_Plenum_Temperature_Coefficient_1 = return_air_fraction_function_of_plenum_temperature_coefficient_1
    Lights.Return_Air_Fraction_Function_of_Plenum_Temperature_Coefficient_2 = return_air_fraction_function_of_plenum_temperature_coefficient_2
    Lights.Return_Air_Heat_Gain_Node_Name = return_air_heat_gain_node_name
    Lights.Exhaust_Air_Heat_Gain_Node_Name = exhaust_air_heat_gain_node_name
    return Lights


def electric_equipment(
        idf,
        name="Equipment1",
        zone_or_zonelist_or_space_or_spacelist_name="Zone1",
        schedule_name="Equipment_schedule",
        design_level_calculation_method="Watts/Area",
        design_level="",
        watts_per_floor_area="",
        watts_per_person="",
        fraction_latent="",
        fraction_radiant="",
        fraction_lost="",
        enduse_subcategory=""):
    """
    Create and configure an ElectricEquipment object for EnergyPlus IDF.
    """
    Equipment = idf.newidfobject("ElectricEquipment")
    Equipment.Name = name
    Equipment.Zone_or_ZoneList_or_Space_or_SpaceList_Name = zone_or_zonelist_or_space_or_spacelist_name
    Equipment.Schedule_Name = schedule_name
    Equipment.Design_Level_Calculation_Method = design_level_calculation_method
    Equipment.Design_Level = design_level
    Equipment.Watts_per_Floor_Area = watts_per_floor_area
    Equipment.Watts_per_Person = watts_per_person
    Equipment.Fraction_Latent = fraction_latent
    Equipment.Fraction_Radiant = fraction_radiant
    Equipment.Fraction_Lost = fraction_lost
    Equipment.EndUse_Subcategory = enduse_subcategory
    return Equipment


def zone_ventilation_design_flow_rate(
        idf,
        name="Ventilation",
        zone_or_zonelist_or_space_or_spacelist_name="Zone1",
        schedule_name="",
        design_flow_rate_calculation_method="",
        design_flow_rate="",
        flow_rate_per_floor_area="",
        flow_rate_per_person="",
        air_changes_per_hour="",
        ventilation_type="",
        fan_pressure_rise="",
        fan_total_efficiency="",
        constant_term_coefficient="",
        temperature_term_coefficient="",
        velocity_term_coefficient="",
        velocity_squared_term_coefficient="",
        minimum_indoor_temperature="",
        minimum_indoor_temperature_schedule_name="",
        maximum_indoor_temperature="",
        maximum_indoor_temperature_schedule_name="",
        delta_temperature="",
        delta_temperature_schedule_name="",
        minimum_outdoor_temperature="",
        minimum_outdoor_temperature_schedule_name="",
        maximum_outdoor_temperature="",
        maximum_outdoor_temperature_schedule_name="",
        maximum_wind_speed="",
        density_basis=""):
    """
    Create and configure a ZoneVentilation:DesignFlowRate object for EnergyPlus IDF.
    """
    ZoneVentilation = idf.newidfobject("ZoneVentilation:DesignFlowRate")
    ZoneVentilation.Name = name
    ZoneVentilation.Zone_or_ZoneList_or_Space_or_SpaceList_Name = zone_or_zonelist_or_space_or_spacelist_name
    ZoneVentilation.Schedule_Name = schedule_name
    ZoneVentilation.Design_Flow_Rate_Calculation_Method = design_flow_rate_calculation_method
    ZoneVentilation.Design_Flow_Rate = design_flow_rate
    ZoneVentilation.Flow_Rate_per_Floor_Area = flow_rate_per_floor_area
    ZoneVentilation.Flow_Rate_per_Person = flow_rate_per_person
    ZoneVentilation.Air_Changes_per_Hour = air_changes_per_hour
    ZoneVentilation.Ventilation_Type = ventilation_type
    ZoneVentilation.Fan_Pressure_Rise = fan_pressure_rise
    ZoneVentilation.Fan_Total_Efficiency = fan_total_efficiency
    ZoneVentilation.Constant_Term_Coefficient = constant_term_coefficient
    ZoneVentilation.Temperature_Term_Coefficient = temperature_term_coefficient
    ZoneVentilation.Velocity_Term_Coefficient = velocity_term_coefficient
    ZoneVentilation.Velocity_Squared_Term_Coefficient = velocity_squared_term_coefficient
    ZoneVentilation.Minimum_Indoor_Temperature = minimum_indoor_temperature
    ZoneVentilation.Minimum_Indoor_Temperature_Schedule_Name = minimum_indoor_temperature_schedule_name
    ZoneVentilation.Maximum_Indoor_Temperature = maximum_indoor_temperature
    ZoneVentilation.Maximum_Indoor_Temperature_Schedule_Name = maximum_indoor_temperature_schedule_name
    ZoneVentilation.Delta_Temperature = delta_temperature
    ZoneVentilation.Delta_Temperature_Schedule_Name = delta_temperature_schedule_name
    ZoneVentilation.Minimum_Outdoor_Temperature = minimum_outdoor_temperature
    ZoneVentilation.Minimum_Outdoor_Temperature_Schedule_Name = minimum_outdoor_temperature_schedule_name
    ZoneVentilation.Maximum_Outdoor_Temperature = maximum_outdoor_temperature
    ZoneVentilation.Maximum_Outdoor_Temperature_Schedule_Name = maximum_outdoor_temperature_schedule_name
    ZoneVentilation.Maximum_Wind_Speed = maximum_wind_speed
    ZoneVentilation.Density_Basis = density_basis
    return ZoneVentilation


def zone_control_thermostat(
        idf,
        name="Heating_thermostat",
        zone_or_zonelist_name="Zone1",
        control_type_schedule_name="Thermostat_control_type",
        control_1_object_type="ThermostatSetpoint:SingleHeating",
        control_1_name="Heating_thermostat",
        control_2_object_type="ThermostatSetpoint:SingleCooling",
        control_2_name="Cooling_thermostat",
        control_3_object_type="",
        control_3_name="",
        control_4_object_type="",
        control_4_name="",
        temperature_difference_between_cutout_and_setpoint=""):
    """
    Create and configure a ZoneControl:Thermostat object for EnergyPlus IDF.
    """
    ZoneControlThermostat = idf.newidfobject("ZoneControl:Thermostat")
    ZoneControlThermostat.Name = name
    ZoneControlThermostat.Zone_or_ZoneList_Name = zone_or_zonelist_name
    ZoneControlThermostat.Control_Type_Schedule_Name = control_type_schedule_name
    ZoneControlThermostat.Control_1_Object_Type = control_1_object_type
    ZoneControlThermostat.Control_1_Name = control_1_name
    ZoneControlThermostat.Control_2_Object_Type = control_2_object_type
    ZoneControlThermostat.Control_2_Name = control_2_name
    ZoneControlThermostat.Control_3_Object_Type = control_3_object_type
    ZoneControlThermostat.Control_3_Name = control_3_name
    ZoneControlThermostat.Control_4_Object_Type = control_4_object_type
    ZoneControlThermostat.Control_4_Name = control_4_name
    ZoneControlThermostat.Temperature_Difference_Between_Cutout_And_Setpoint = temperature_difference_between_cutout_and_setpoint
    return ZoneControlThermostat


def thermostat_setpoint_single_heating(
        idf,
        name="Heating_thermostat",
        setpoint_temperature_schedule_name=""):
    """
    Create and configure a ThermostatSetpoint:SingleHeating object for EnergyPlus IDF.
    """
    ThermostatSetpoint = idf.newidfobject("ThermostatSetpoint:SingleHeating")
    ThermostatSetpoint.Name = name
    ThermostatSetpoint.Setpoint_Temperature_Schedule_Name = setpoint_temperature_schedule_name
    return ThermostatSetpoint


def thermostat_setpoint_single_cooling(
        idf,
        name="Cooling_thermostat",
        setpoint_temperature_schedule_name=""):
    """
    Create and configure a ThermostatSetpoint:SingleCooling object for EnergyPlus IDF.
    """
    ThermostatSetpoint = idf.newidfobject("ThermostatSetpoint:SingleCooling")
    ThermostatSetpoint.Name = name
    ThermostatSetpoint.Setpoint_Temperature_Schedule_Name = setpoint_temperature_schedule_name
    return ThermostatSetpoint


def design_specification_outdoor_air(
        idf,
        name="Outdoor_specification",
        outdoor_air_method="",
        outdoor_air_flow_per_person="",
        outdoor_air_flow_per_zone_floor_area="",
        outdoor_air_flow_per_zone="",
        outdoor_air_flow_air_changes_per_hour="",
        outdoor_air_schedule_name="",
        proportional_control_minimum_outdoor_air_flow_rate_schedule_name=""):
    """
    Create and configure a DesignSpecification:OutdoorAir object for EnergyPlus IDF.
    """
    OutdoorAir = idf.newidfobject("DesignSpecification:OutdoorAir")
    OutdoorAir.Name = name
    OutdoorAir.Outdoor_Air_Method = outdoor_air_method
    OutdoorAir.Outdoor_Air_Flow_per_Person = outdoor_air_flow_per_person
    OutdoorAir.Outdoor_Air_Flow_per_Zone_Floor_Area = outdoor_air_flow_per_zone_floor_area
    OutdoorAir.Outdoor_Air_Flow_per_Zone = outdoor_air_flow_per_zone
    OutdoorAir.Outdoor_Air_Flow_Air_Changes_per_Hour = outdoor_air_flow_air_changes_per_hour
    OutdoorAir.Outdoor_Air_Schedule_Name = outdoor_air_schedule_name
    OutdoorAir.Proportional_Control_Minimum_Outdoor_Air_Flow_Rate_Schedule_Name = proportional_control_minimum_outdoor_air_flow_rate_schedule_name
    return OutdoorAir


def sizing_zone(
        idf,
        zone_or_zone_list_name="Zone1",
        zone_cooling_design_supply_air_temperature_input_method="SupplyAirTemperature",
        zone_cooling_design_supply_air_temperature=12,
        zone_cooling_design_supply_air_temperature_difference="",
        zone_heating_design_supply_air_temperature_input_method="SupplyAirTemperature",
        zone_heating_design_supply_air_temperature=50,
        zone_heating_design_supply_air_temperature_difference="",
        zone_cooling_design_supply_air_humidity_ratio=0.008,
        zone_heating_design_supply_air_humidity_ratio=0.008,
        design_specification_outdoor_air_object_name="",
        zone_heating_sizing_factor="",
        zone_cooling_sizing_factor="",
        cooling_design_air_flow_method="DesignDay",
        cooling_design_air_flow_rate="",
        cooling_minimum_air_flow_per_zone_floor_area="",
        cooling_minimum_air_flow="",
        cooling_minimum_air_flow_fraction="",
        heating_design_air_flow_method="DesignDay",
        heating_design_air_flow_rate="",
        heating_maximum_air_flow_per_zone_floor_area="",
        heating_maximum_air_flow="",
        heating_maximum_air_flow_fraction="",
        design_specification_zone_air_distribution_object_name="",
        account_for_dedicated_outdoor_air_system="No",
        dedicated_outdoor_air_system_control_strategy="NeutralSupplyAir",
        dedicated_outdoor_air_low_setpoint_temperature_for_design="autosize",
        dedicated_outdoor_air_high_setpoint_temperature_for_design="autosize",
        zone_load_sizing_method="Sensible Load Only No Latent Load",
        zone_latent_cooling_design_supply_air_humidity_ratio_input_method="HumidityRatioDifference",
        zone_dehumidification_design_supply_air_humidity_ratio="",
        zone_cooling_design_supply_air_humidity_ratio_difference="",
        zone_latent_heating_design_supply_air_humidity_ratio_input_method="HumidityRatioDifference",
        zone_humidification_design_supply_air_humidity_ratio="",
        zone_humidification_design_supply_air_humidity_ratio_difference="",
        zone_humidistat_dehumidification_set_point_schedule_name="",
        zone_humidistat_humidification_set_point_schedule_name="",
        type_of_space_sum_to_use="Coincident"):
    """
    Create and configure a Sizing:Zone object for EnergyPlus IDF.
    """
    SizingZone = idf.newidfobject("Sizing:Zone")
    SizingZone.Zone_or_ZoneList_Name = zone_or_zone_list_name
    SizingZone.Zone_Cooling_Design_Supply_Air_Temperature_Input_Method = zone_cooling_design_supply_air_temperature_input_method
    SizingZone.Zone_Cooling_Design_Supply_Air_Temperature = zone_cooling_design_supply_air_temperature
    SizingZone.Zone_Cooling_Design_Supply_Air_Temperature_Difference = zone_cooling_design_supply_air_temperature_difference
    SizingZone.Zone_Heating_Design_Supply_Air_Temperature_Input_Method = zone_heating_design_supply_air_temperature_input_method
    SizingZone.Zone_Heating_Design_Supply_Air_Temperature = zone_heating_design_supply_air_temperature
    SizingZone.Zone_Heating_Design_Supply_Air_Temperature_Difference = zone_heating_design_supply_air_temperature_difference
    SizingZone.Zone_Cooling_Design_Supply_Air_Humidity_Ratio = zone_cooling_design_supply_air_humidity_ratio
    SizingZone.Zone_Heating_Design_Supply_Air_Humidity_Ratio = zone_heating_design_supply_air_humidity_ratio
    SizingZone.Design_Specification_Outdoor_Air_Object_Name = design_specification_outdoor_air_object_name
    SizingZone.Zone_Heating_Sizing_Factor = zone_heating_sizing_factor
    SizingZone.Zone_Cooling_Sizing_Factor = zone_cooling_sizing_factor
    SizingZone.Cooling_Design_Air_Flow_Method = cooling_design_air_flow_method
    SizingZone.Cooling_Design_Air_Flow_Rate = cooling_design_air_flow_rate
    SizingZone.Cooling_Minimum_Air_Flow_per_Zone_Floor_Area = cooling_minimum_air_flow_per_zone_floor_area
    SizingZone.Cooling_Minimum_Air_Flow = cooling_minimum_air_flow
    SizingZone.Cooling_Minimum_Air_Flow_Fraction = cooling_minimum_air_flow_fraction
    SizingZone.Heating_Design_Air_Flow_Method = heating_design_air_flow_method
    SizingZone.Heating_Design_Air_Flow_Rate = heating_design_air_flow_rate
    SizingZone.Heating_Maximum_Air_Flow_per_Zone_Floor_Area = heating_maximum_air_flow_per_zone_floor_area
    SizingZone.Heating_Maximum_Air_Flow = heating_maximum_air_flow
    SizingZone.Heating_Maximum_Air_Flow_Fraction = heating_maximum_air_flow_fraction
    SizingZone.Design_Specification_Zone_Air_Distribution_Object_Name = design_specification_zone_air_distribution_object_name
    SizingZone.Account_for_Dedicated_Outdoor_Air_System = account_for_dedicated_outdoor_air_system
    SizingZone.Dedicated_Outdoor_Air_System_Control_Strategy = dedicated_outdoor_air_system_control_strategy
    SizingZone.Dedicated_Outdoor_Air_Low_Setpoint_Temperature_for_Design = dedicated_outdoor_air_low_setpoint_temperature_for_design
    SizingZone.Dedicated_Outdoor_Air_High_Setpoint_Temperature_for_Design = dedicated_outdoor_air_high_setpoint_temperature_for_design
    SizingZone.Zone_Load_Sizing_Method = zone_load_sizing_method
    SizingZone.Zone_Latent_Cooling_Design_Supply_Air_Humidity_Ratio_Input_Method = zone_latent_cooling_design_supply_air_humidity_ratio_input_method
    SizingZone.Zone_Dehumidification_Design_Supply_Air_Humidity_Ratio = zone_dehumidification_design_supply_air_humidity_ratio
    SizingZone.Zone_Cooling_Design_Supply_Air_Humidity_Ratio_Difference = zone_cooling_design_supply_air_humidity_ratio_difference
    SizingZone.Zone_Latent_Heating_Design_Supply_Air_Humidity_Ratio_Input_Method = zone_latent_heating_design_supply_air_humidity_ratio_input_method
    SizingZone.Zone_Humidification_Design_Supply_Air_Humidity_Ratio = zone_humidification_design_supply_air_humidity_ratio
    SizingZone.Zone_Humidification_Design_Supply_Air_Humidity_Ratio_Difference = zone_humidification_design_supply_air_humidity_ratio_difference
    SizingZone.Zone_Humidistat_Dehumidification_Set_Point_Schedule_Name = zone_humidistat_dehumidification_set_point_schedule_name
    SizingZone.Zone_Humidistat_Humidification_Set_Point_Schedule_Name = zone_humidistat_humidification_set_point_schedule_name
    SizingZone.Type_of_Space_Sum_to_Use = type_of_space_sum_to_use
    return SizingZone


def sizing_plant(
        idf,
        plant_or_condenser_loop_name="Plant_loop1",
        loop_type="Heating",
        design_loop_exit_temperature=85,
        loop_design_temperature_difference=10,
        sizing_option="",
        zone_timesteps_in_averaging_window="",
        coincident_sizing_factor_mode=""):
    """
    Create and configure a Sizing:Plant object for EnergyPlus IDF.
    """
    SizingPlant = idf.newidfobject("Sizing:Plant")
    SizingPlant.Plant_or_Condenser_Loop_Name = plant_or_condenser_loop_name
    SizingPlant.Loop_Type = loop_type
    SizingPlant.Design_Loop_Exit_Temperature = design_loop_exit_temperature
    SizingPlant.Loop_Design_Temperature_Difference = loop_design_temperature_difference
    SizingPlant.Sizing_Option = sizing_option
    SizingPlant.Zone_Timesteps_in_Averaging_Window = zone_timesteps_in_averaging_window
    SizingPlant.Coincident_Sizing_Factor_Mode = coincident_sizing_factor_mode
    return SizingPlant

def zone_hvac_ideal_loads_air_system(
        idf,
        name="HVAC1",
        availability_schedule_name="Always ON",
        zone_supply_air_node_name="Zone_supply_inlet",
        zone_exhaust_air_node_name="",
        system_inlet_air_node_name="",
        maximum_heating_supply_air_temperature="",
        minimum_cooling_supply_air_temperature="",
        maximum_heating_supply_air_humidity_ratio="",
        minimum_cooling_supply_air_humidity_ratio="",
        heating_limit="",
        maximum_heating_air_flow_rate="",
        maximum_sensible_heating_capacity="",
        cooling_limit="",
        maximum_cooling_air_flow_rate="",
        maximum_total_cooling_capacity="",
        heating_availability_schedule_name="",
        cooling_availability_schedule_name="",
        dehumidification_control_type="",
        cooling_sensible_heat_ratio="",
        humidification_control_type="",
        design_specification_outdoor_air_object_name="",
        outdoor_air_inlet_node_name="",
        demand_controlled_ventilation_type="",
        outdoor_air_economizer_type="",
        heat_recovery_type="",
        sensible_heat_recovery_effectiveness="",
        latent_heat_recovery_effectiveness="",
        design_specification_zonehvac_sizing_object_name=""):
    """
    Create and configure a ZoneHVAC:IdealLoadsAirSystem object for EnergyPlus IDF.
    """
    ZoneHVAC = idf.newidfobject("ZoneHVAC:IdealLoadsAirSystem")
    ZoneHVAC.Name = name
    ZoneHVAC.Availability_Schedule_Name = availability_schedule_name
    ZoneHVAC.Zone_Supply_Air_Node_Name = zone_supply_air_node_name
    ZoneHVAC.Zone_Exhaust_Air_Node_Name = zone_exhaust_air_node_name
    ZoneHVAC.System_Inlet_Air_Node_Name = system_inlet_air_node_name
    ZoneHVAC.Maximum_Heating_Supply_Air_Temperature = maximum_heating_supply_air_temperature
    ZoneHVAC.Minimum_Cooling_Supply_Air_Temperature = minimum_cooling_supply_air_temperature
    ZoneHVAC.Maximum_Heating_Supply_Air_Humidity_Ratio = maximum_heating_supply_air_humidity_ratio
    ZoneHVAC.Minimum_Cooling_Supply_Air_Humidity_Ratio = minimum_cooling_supply_air_humidity_ratio
    ZoneHVAC.Heating_Limit = heating_limit
    ZoneHVAC.Maximum_Heating_Air_Flow_Rate = maximum_heating_air_flow_rate
    ZoneHVAC.Maximum_Sensible_Heating_Capacity = maximum_sensible_heating_capacity
    ZoneHVAC.Cooling_Limit = cooling_limit
    ZoneHVAC.Maximum_Cooling_Air_Flow_Rate = maximum_cooling_air_flow_rate
    ZoneHVAC.Maximum_Total_Cooling_Capacity = maximum_total_cooling_capacity
    ZoneHVAC.Heating_Availability_Schedule_Name = heating_availability_schedule_name
    ZoneHVAC.Cooling_Availability_Schedule_Name = cooling_availability_schedule_name
    ZoneHVAC.Dehumidification_Control_Type = dehumidification_control_type
    ZoneHVAC.Cooling_Sensible_Heat_Ratio = cooling_sensible_heat_ratio
    ZoneHVAC.Humidification_Control_Type = humidification_control_type
    ZoneHVAC.Design_Specification_Outdoor_Air_Object_Name = design_specification_outdoor_air_object_name
    ZoneHVAC.Outdoor_Air_Inlet_Node_Name = outdoor_air_inlet_node_name
    ZoneHVAC.Demand_Controlled_Ventilation_Type = demand_controlled_ventilation_type
    ZoneHVAC.Outdoor_Air_Economizer_Type = outdoor_air_economizer_type
    ZoneHVAC.Heat_Recovery_Type = heat_recovery_type
    ZoneHVAC.Sensible_Heat_Recovery_Effectiveness = sensible_heat_recovery_effectiveness
    ZoneHVAC.Latent_Heat_Recovery_Effectiveness = latent_heat_recovery_effectiveness
    ZoneHVAC.Design_Specification_ZoneHVAC_Sizing_Object_Name = design_specification_zonehvac_sizing_object_name
    return ZoneHVAC


def zone_hvac_packaged_terminal_air_conditioner(
        idf,
        name="",
        availability_schedule_name="",
        air_inlet_node_name="",
        air_outlet_node_name="",
        outdoor_air_mixer_object_type="",
        outdoor_air_mixer_name="",
        cooling_supply_air_flow_rate="",
        heating_supply_air_flow_rate="",
        no_load_supply_air_flow_rate="",
        no_load_supply_air_flow_rate_control_set_to_low_speed="",
        cooling_outdoor_air_flow_rate="",
        heating_outdoor_air_flow_rate="",
        no_load_outdoor_air_flow_rate="",
        supply_air_fan_object_type="",
        supply_air_fan_name="",
        heating_coil_object_type="",
        heating_coil_name="",
        cooling_coil_object_type="",
        cooling_coil_name="",
        fan_placement="",
        supply_air_fan_operating_mode_schedule_name="",
        availability_manager_list_name="",
        design_specification_zonehvac_sizing_object_name="",
        capacity_control_method="",
        minimum_supply_air_temperature_in_cooling_mode="",
        maximum_supply_air_temperature_in_heating_mode=""):
    """
    Create and configure a ZoneHVAC:PackagedTerminalAirConditioner object for EnergyPlus IDF.
    """
    TerminalAC = idf.newidfobject("ZoneHVAC:PackagedTerminalAirConditioner")
    TerminalAC.Name = name
    TerminalAC.Availability_Schedule_Name = availability_schedule_name
    TerminalAC.Air_Inlet_Node_Name = air_inlet_node_name
    TerminalAC.Air_Outlet_Node_Name = air_outlet_node_name
    TerminalAC.Outdoor_Air_Mixer_Object_Type = outdoor_air_mixer_object_type
    TerminalAC.Outdoor_Air_Mixer_Name = outdoor_air_mixer_name
    TerminalAC.Cooling_Supply_Air_Flow_Rate = cooling_supply_air_flow_rate
    TerminalAC.Heating_Supply_Air_Flow_Rate = heating_supply_air_flow_rate
    TerminalAC.No_Load_Supply_Air_Flow_Rate = no_load_supply_air_flow_rate
    TerminalAC.No_Load_Supply_Air_Flow_Rate_Control_Set_To_Low_Speed = no_load_supply_air_flow_rate_control_set_to_low_speed
    TerminalAC.Cooling_Outdoor_Air_Flow_Rate = cooling_outdoor_air_flow_rate
    TerminalAC.Heating_Outdoor_Air_Flow_Rate = heating_outdoor_air_flow_rate
    TerminalAC.No_Load_Outdoor_Air_Flow_Rate = no_load_outdoor_air_flow_rate
    TerminalAC.Supply_Air_Fan_Object_Type = supply_air_fan_object_type
    TerminalAC.Supply_Air_Fan_Name = supply_air_fan_name
    TerminalAC.Heating_Coil_Object_Type = heating_coil_object_type
    TerminalAC.Heating_Coil_Name = heating_coil_name
    TerminalAC.Cooling_Coil_Object_Type = cooling_coil_object_type
    TerminalAC.Cooling_Coil_Name = cooling_coil_name
    TerminalAC.Fan_Placement = fan_placement
    TerminalAC.Supply_Air_Fan_Operating_Mode_Schedule_Name = supply_air_fan_operating_mode_schedule_name
    TerminalAC.Availability_Manager_List_Name = availability_manager_list_name
    TerminalAC.Design_Specification_ZoneHVAC_Sizing_Object_Name = design_specification_zonehvac_sizing_object_name
    TerminalAC.Capacity_Control_Method = capacity_control_method
    TerminalAC.Minimum_Supply_Air_Temperature_in_Cooling_Mode = minimum_supply_air_temperature_in_cooling_mode
    TerminalAC.Maximum_Supply_Air_Temperature_in_Heating_Mode = maximum_supply_air_temperature_in_heating_mode
    return TerminalAC


def zone_hvac_packaged_terminal_heat_pump(
        idf,
        name="Heat_pump1",
        availability_schedule_name="",
        air_inlet_node_name="Zone_air_inlet_node",
        air_outlet_node_name="Electric_heater_outlet_node",
        outdoor_air_mixer_object_type="",
        outdoor_air_mixer_name="",
        cooling_supply_air_flow_rate="autosize",
        heating_supply_air_flow_rate="autosize",
        no_load_supply_air_flow_rate="",
        no_load_supply_air_flow_rate_control_set_to_low_speed="",
        cooling_outdoor_air_flow_rate="autosize",
        heating_outdoor_air_flow_rate="autosize",
        no_load_outdoor_air_flow_rate="",
        supply_air_fan_object_type="Fan:SystemModel",
        supply_air_fan_name="Fan1",
        heating_coil_object_type="Coil:Heating:DX:SingleSpeed",
        heating_coil_name="Heating_coil1",
        heating_convergence_tolerance="",
        cooling_coil_object_type="Coil:Cooling:DX:SingleSpeed",
        cooling_coil_name="Cooling_coil1",
        cooling_convergence_tolerance="",
        supplemental_heating_coil_object_type="Coil:Heating:Electric",
        supplemental_heating_coil_name="Electric_heater1",
        maximum_supply_air_temperature_from_supplemental_heater="autosize",
        maximum_outdoor_drybulb_temperature_for_supplemental_heater_operation="",
        fan_placement="",
        supply_air_fan_operating_mode_schedule_name="",
        availability_manager_list_name="",
        design_specification_zonehvac_sizing_object_name="",
        capacity_control_method="",
        minimum_supply_air_temperature_in_cooling_mode="",
        maximum_supply_air_temperature_in_heating_mode=""):
    """
    Create and configure a ZoneHVAC:PackagedTerminalHeatPump object for EnergyPlus IDF.
    """
    ZoneHVACPackagedTerminalHeatPump = idf.newidfobject("ZoneHVAC:PackagedTerminalHeatPump")
    ZoneHVACPackagedTerminalHeatPump.Name = name
    ZoneHVACPackagedTerminalHeatPump.Availability_Schedule_Name = availability_schedule_name
    ZoneHVACPackagedTerminalHeatPump.Air_Inlet_Node_Name = air_inlet_node_name
    ZoneHVACPackagedTerminalHeatPump.Air_Outlet_Node_Name = air_outlet_node_name
    ZoneHVACPackagedTerminalHeatPump.Outdoor_Air_Mixer_Object_Type = outdoor_air_mixer_object_type
    ZoneHVACPackagedTerminalHeatPump.Outdoor_Air_Mixer_Name = outdoor_air_mixer_name
    ZoneHVACPackagedTerminalHeatPump.Cooling_Supply_Air_Flow_Rate = cooling_supply_air_flow_rate
    ZoneHVACPackagedTerminalHeatPump.Heating_Supply_Air_Flow_Rate = heating_supply_air_flow_rate
    ZoneHVACPackagedTerminalHeatPump.No_Load_Supply_Air_Flow_Rate = no_load_supply_air_flow_rate
    ZoneHVACPackagedTerminalHeatPump.No_Load_Supply_Air_Flow_Rate_Control_Set_To_Low_Speed = no_load_supply_air_flow_rate_control_set_to_low_speed
    ZoneHVACPackagedTerminalHeatPump.Cooling_Outdoor_Air_Flow_Rate = cooling_outdoor_air_flow_rate
    ZoneHVACPackagedTerminalHeatPump.Heating_Outdoor_Air_Flow_Rate = heating_outdoor_air_flow_rate
    ZoneHVACPackagedTerminalHeatPump.No_Load_Outdoor_Air_Flow_Rate = no_load_outdoor_air_flow_rate
    ZoneHVACPackagedTerminalHeatPump.Supply_Air_Fan_Object_Type = supply_air_fan_object_type
    ZoneHVACPackagedTerminalHeatPump.Supply_Air_Fan_Name = supply_air_fan_name
    ZoneHVACPackagedTerminalHeatPump.Heating_Coil_Object_Type = heating_coil_object_type
    ZoneHVACPackagedTerminalHeatPump.Heating_Coil_Name = heating_coil_name
    ZoneHVACPackagedTerminalHeatPump.Heating_Convergence_Tolerance = heating_convergence_tolerance
    ZoneHVACPackagedTerminalHeatPump.Cooling_Coil_Object_Type = cooling_coil_object_type
    ZoneHVACPackagedTerminalHeatPump.Cooling_Coil_Name = cooling_coil_name
    ZoneHVACPackagedTerminalHeatPump.Cooling_Convergence_Tolerance = cooling_convergence_tolerance
    ZoneHVACPackagedTerminalHeatPump.Supplemental_Heating_Coil_Object_Type = supplemental_heating_coil_object_type
    ZoneHVACPackagedTerminalHeatPump.Supplemental_Heating_Coil_Name = supplemental_heating_coil_name
    ZoneHVACPackagedTerminalHeatPump.Maximum_Supply_Air_Temperature_from_Supplemental_Heater = maximum_supply_air_temperature_from_supplemental_heater
    ZoneHVACPackagedTerminalHeatPump.Maximum_Outdoor_DryBulb_Temperature_for_Supplemental_Heater_Operation = maximum_outdoor_drybulb_temperature_for_supplemental_heater_operation
    ZoneHVACPackagedTerminalHeatPump.Fan_Placement = fan_placement
    ZoneHVACPackagedTerminalHeatPump.Supply_Air_Fan_Operating_Mode_Schedule_Name = supply_air_fan_operating_mode_schedule_name
    ZoneHVACPackagedTerminalHeatPump.Availability_Manager_List_Name = availability_manager_list_name
    ZoneHVACPackagedTerminalHeatPump.Design_Specification_ZoneHVAC_Sizing_Object_Name = design_specification_zonehvac_sizing_object_name
    ZoneHVACPackagedTerminalHeatPump.Capacity_Control_Method = capacity_control_method
    ZoneHVACPackagedTerminalHeatPump.Minimum_Supply_Air_Temperature_in_Cooling_Mode = minimum_supply_air_temperature_in_cooling_mode
    ZoneHVACPackagedTerminalHeatPump.Maximum_Supply_Air_Temperature_in_Heating_Mode = maximum_supply_air_temperature_in_heating_mode
    return ZoneHVACPackagedTerminalHeatPump


def zone_hvac_baseboard_convective_water(
        idf,
        name="Baseboard1",
        availability_schedule_name="",
        inlet_node_name="Zone_baseboard_inlet_node",
        outlet_node_name="Zone_baseboard_outlet_node",
        heating_design_capacity_method="HeatingDesignCapacity",
        heating_design_capacity="autosize",
        heating_design_capacity_per_floor_area="",
        fraction_of_autosized_heating_design_capacity="",
        ufactor_times_area_value="autosize",
        maximum_water_flow_rate="autosize",
        convergence_tolerance=""):
    """
    Create and configure a ZoneHVAC:Baseboard:Convective:Water object for EnergyPlus IDF.
    """
    Baseboard = idf.newidfobject("ZoneHVAC:Baseboard:Convective:Water")
    Baseboard.Name = name
    Baseboard.Availability_Schedule_Name = availability_schedule_name
    Baseboard.Inlet_Node_Name = inlet_node_name
    Baseboard.Outlet_Node_Name = outlet_node_name
    Baseboard.Heating_Design_Capacity_Method = heating_design_capacity_method
    Baseboard.Heating_Design_Capacity = heating_design_capacity
    Baseboard.Heating_Design_Capacity_Per_Floor_Area = heating_design_capacity_per_floor_area
    Baseboard.Fraction_of_Autosized_Heating_Design_Capacity = fraction_of_autosized_heating_design_capacity
    Baseboard.UFactor_Times_Area_Value = ufactor_times_area_value
    Baseboard.Maximum_Water_Flow_Rate = maximum_water_flow_rate
    Baseboard.Convergence_Tolerance = convergence_tolerance
    return Baseboard


def zone_hvac_equipment_list(
        idf,
        name="Zone_equipment_list",
        load_distribution_scheme="",
        zone_equipment_1_object_type="ZoneHVAC:Baseboard:Convective:Water",
        zone_equipment_1_name="Baseboard1",
        zone_equipment_1_cooling_sequence=1,
        zone_equipment_1_heating_or_noload_sequence=1,
        zone_equipment_1_sequential_cooling_fraction_schedule_name="",
        zone_equipment_1_sequential_heating_fraction_schedule_name="",
        zone_equipment_2_object_type=";!",
        zone_equipment_2_name="!",
        zone_equipment_2_cooling_sequence="!",
        zone_equipment_2_heating_or_noload_sequence="!",
        zone_equipment_2_sequential_cooling_fraction_schedule_name="!",
        zone_equipment_2_sequential_heating_fraction_schedule_name=";!"):
    """
    Create and configure a ZoneHVAC:EquipmentList object for EnergyPlus IDF.
    """
    EquipmentList = idf.newidfobject("ZoneHVAC:EquipmentList")
    EquipmentList.Name = name
    EquipmentList.Load_Distribution_Scheme = load_distribution_scheme
    EquipmentList.Zone_Equipment_1_Object_Type = zone_equipment_1_object_type
    EquipmentList.Zone_Equipment_1_Name = zone_equipment_1_name
    EquipmentList.Zone_Equipment_1_Cooling_Sequence = zone_equipment_1_cooling_sequence
    EquipmentList.Zone_Equipment_1_Heating_or_NoLoad_Sequence = zone_equipment_1_heating_or_noload_sequence
    EquipmentList.Zone_Equipment_1_Sequential_Cooling_Fraction_Schedule_Name = zone_equipment_1_sequential_cooling_fraction_schedule_name
    EquipmentList.Zone_Equipment_1_Sequential_Heating_Fraction_Schedule_Name = zone_equipment_1_sequential_heating_fraction_schedule_name
    EquipmentList.Zone_Equipment_2_Object_Type = zone_equipment_2_object_type
    EquipmentList.Zone_Equipment_2_Name = zone_equipment_2_name
    EquipmentList.Zone_Equipment_2_Cooling_Sequence = zone_equipment_2_cooling_sequence
    EquipmentList.Zone_Equipment_2_Heating_or_NoLoad_Sequence = zone_equipment_2_heating_or_noload_sequence
    EquipmentList.Zone_Equipment_2_Sequential_Cooling_Fraction_Schedule_Name = zone_equipment_2_sequential_cooling_fraction_schedule_name
    EquipmentList.Zone_Equipment_2_Sequential_Heating_Fraction_Schedule_Name = zone_equipment_2_sequential_heating_fraction_schedule_name
    return EquipmentList


def zone_hvac_equipment_connections(
        idf,
        zone_name="Zone1",
        zone_conditioning_equipment_list_name="Zone_equipment_list",
        zone_air_inlet_node_or_nodelist_name="",
        zone_air_exhaust_node_or_nodelist_name="",
        zone_air_node_name="Zone_air_node",
        zone_return_air_node_or_nodelist_name="",
        zone_return_air_node_1_flow_rate_fraction_schedule_name="",
        zone_return_air_node_1_flow_rate_basis_node_or_nodelist_name=""):
    """
    Create and configure a ZoneHVAC:EquipmentConnections object for EnergyPlus IDF.
    """
    EquipmentConnections = idf.newidfobject("ZoneHVAC:EquipmentConnections")
    EquipmentConnections.Zone_Name = zone_name
    EquipmentConnections.Zone_Conditioning_Equipment_List_Name = zone_conditioning_equipment_list_name
    EquipmentConnections.Zone_Air_Inlet_Node_or_NodeList_Name = zone_air_inlet_node_or_nodelist_name
    EquipmentConnections.Zone_Air_Exhaust_Node_or_NodeList_Name = zone_air_exhaust_node_or_nodelist_name
    EquipmentConnections.Zone_Air_Node_Name = zone_air_node_name
    EquipmentConnections.Zone_Return_Air_Node_or_NodeList_Name = zone_return_air_node_or_nodelist_name
    EquipmentConnections.Zone_Return_Air_Node_1_Flow_Rate_Fraction_Schedule_Name = zone_return_air_node_1_flow_rate_fraction_schedule_name
    EquipmentConnections.Zone_Return_Air_Node_1_Flow_Rate_Basis_Node_or_NodeList_Name = zone_return_air_node_1_flow_rate_basis_node_or_nodelist_name
    return EquipmentConnections


def fan_system_model(
        idf,
        name="Fan1",
        availability_schedule_name="",
        air_inlet_node_name="Zone_air_inlet_node",
        air_outlet_node_name="Fan_outlet_node",
        design_maximum_air_flow_rate="autosize",
        speed_control_method="",
        electric_power_minimum_flow_rate_fraction="",
        design_pressure_rise=80,
        motor_efficiency="",
        motor_in_air_stream_fraction="",
        design_electric_power_consumption="",
        design_power_sizing_method="",
        electric_power_per_unit_flow_rate="",
        electric_power_per_unit_flow_rate_per_unit_pressure="",
        fan_total_efficiency="",
        electric_power_function_of_flow_fraction_curve_name="",
        night_ventilation_mode_pressure_rise="",
        night_ventilation_mode_flow_fraction="",
        motor_loss_zone_name="",
        motor_loss_radiative_fraction="",
        enduse_subcategory="",
        number_of_speeds="",
        speed_1_flow_fraction="",
        speed_1_electric_power_fraction="",
        speed_2_flow_fraction="",
        speed_2_electric_power_fraction="",
        speed_3_flow_fraction="",
        speed_3_electric_power_fraction="",
        speed_n_flow_fraction="",
        speed_n_electric_power_fraction=""):
    """
    Create and configure a Fan:SystemModel object for EnergyPlus IDF.
    """
    Fan = idf.newidfobject("Fan:SystemModel")
    Fan.Name = name
    Fan.Availability_Schedule_Name = availability_schedule_name
    Fan.Air_Inlet_Node_Name = air_inlet_node_name
    Fan.Air_Outlet_Node_Name = air_outlet_node_name
    Fan.Design_Maximum_Air_Flow_Rate = design_maximum_air_flow_rate
    Fan.Speed_Control_Method = speed_control_method
    Fan.Electric_Power_Minimum_Flow_Rate_Fraction = electric_power_minimum_flow_rate_fraction
    Fan.Design_Pressure_Rise = design_pressure_rise
    Fan.Motor_Efficiency = motor_efficiency
    Fan.Motor_In_Air_Stream_Fraction = motor_in_air_stream_fraction
    Fan.Design_Electric_Power_Consumption = design_electric_power_consumption
    Fan.Design_Power_Sizing_Method = design_power_sizing_method
    Fan.Electric_Power_Per_Unit_Flow_Rate = electric_power_per_unit_flow_rate
    Fan.Electric_Power_Per_Unit_Flow_Rate_Per_Unit_Pressure = electric_power_per_unit_flow_rate_per_unit_pressure
    Fan.Fan_Total_Efficiency = fan_total_efficiency
    Fan.Electric_Power_Function_of_Flow_Fraction_Curve_Name = electric_power_function_of_flow_fraction_curve_name
    Fan.Night_Ventilation_Mode_Pressure_Rise = night_ventilation_mode_pressure_rise
    Fan.Night_Ventilation_Mode_Flow_Fraction = night_ventilation_mode_flow_fraction
    Fan.Motor_Loss_Zone_Name = motor_loss_zone_name
    Fan.Motor_Loss_Radiative_Fraction = motor_loss_radiative_fraction
    Fan.EndUse_Subcategory = enduse_subcategory
    Fan.Number_of_Speeds = number_of_speeds
    Fan.Speed_1_Flow_Fraction = speed_1_flow_fraction
    Fan.Speed_1_Electric_Power_Fraction = speed_1_electric_power_fraction
    Fan.Speed_2_Flow_Fraction = speed_2_flow_fraction
    Fan.Speed_2_Electric_Power_Fraction = speed_2_electric_power_fraction
    Fan.Speed_3_Flow_Fraction = speed_3_flow_fraction
    Fan.Speed_3_Electric_Power_Fraction = speed_3_electric_power_fraction
    Fan.Speed_n_Flow_Fraction = speed_n_flow_fraction
    Fan.Speed_n_Electric_Power_Fraction = speed_n_electric_power_fraction
    return Fan


def coil_cooling_dx_single_speed(
        idf,
        name="Cooling_coil1",
        availability_schedule_name="Active_summer",
        gross_rated_total_cooling_capacity="autosize",
        gross_rated_sensible_heat_ratio="autosize",
        gross_rated_cooling_cop="",
        rated_air_flow_rate="autosize",
        rated_evaporator_fan_power_per_volume_flow_rate_2017="",
        rated_evaporator_fan_power_per_volume_flow_rate_2023="",
        air_inlet_node_name="Fan_outlet_node",
        air_outlet_node_name="Cooling_coil_outlet_node",
        total_cooling_capacity_function_of_temperature_curve_name="HPACCoolCapFT",
        total_cooling_capacity_function_of_flow_fraction_curve_name="HPACCoolCapFFF",
        energy_input_ratio_function_of_temperature_curve_name="HPACCoolCapFT",
        energy_input_ratio_function_of_flow_fraction_curve_name="HPACEIRFFF",
        part_load_fraction_correlation_curve_name="HPACPLFFPLR",
        minimum_outdoor_drybulb_temperature_for_compressor_operation="",
        nominal_time_for_condensate_removal_to_begin="",
        ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity="",
        maximum_cycling_rate="",
        latent_capacity_time_constant="",
        condenser_air_inlet_node_name="",
        condenser_type="",
        evaporative_condenser_effectiveness="",
        evaporative_condenser_air_flow_rate="",
        evaporative_condenser_pump_rated_power_consumption="",
        crankcase_heater_capacity="",
        crankcase_heater_capacity_function_of_temperature_curve_name="",
        maximum_outdoor_drybulb_temperature_for_crankcase_heater_operation="",
        supply_water_storage_tank_name="",
        condensate_collection_water_storage_tank_name="",
        basin_heater_capacity="",
        basin_heater_setpoint_temperature="",
        basin_heater_operating_schedule_name="",
        sensible_heat_ratio_function_of_temperature_curve_name="",
        sensible_heat_ratio_function_of_flow_fraction_curve_name="",
        report_ashrae_standard_127_performance_ratings="",
        zone_name_for_condenser_placement=""):
    """
    Create and configure a Coil:Cooling:DX:SingleSpeed object for EnergyPlus IDF.
    """
    CoolingCoil = idf.newidfobject("Coil:Cooling:DX:SingleSpeed")
    CoolingCoil.Name = name
    CoolingCoil.Availability_Schedule_Name = availability_schedule_name
    CoolingCoil.Gross_Rated_Total_Cooling_Capacity = gross_rated_total_cooling_capacity
    CoolingCoil.Gross_Rated_Sensible_Heat_Ratio = gross_rated_sensible_heat_ratio
    CoolingCoil.Gross_Rated_Cooling_COP = gross_rated_cooling_cop
    CoolingCoil.Rated_Air_Flow_Rate = rated_air_flow_rate
    setattr(CoolingCoil, "2017_Rated_Evaporator_Fan_Power_Per_Volume_Flow_Rate", rated_evaporator_fan_power_per_volume_flow_rate_2017)
    setattr(CoolingCoil, "2023_Rated_Evaporator_Fan_Power_Per_Volume_Flow_Rate", rated_evaporator_fan_power_per_volume_flow_rate_2023)
    # CoolingCoil.Rated_Evaporator_Fan_Power_Per_Volume_Flow_Rate_2017 = rated_evaporator_fan_power_per_volume_flow_rate_2017
    # CoolingCoil.Rated_Evaporator_Fan_Power_Per_Volume_Flow_Rate_2023 = rated_evaporator_fan_power_per_volume_flow_rate_2023
    CoolingCoil.Air_Inlet_Node_Name = air_inlet_node_name
    CoolingCoil.Air_Outlet_Node_Name = air_outlet_node_name
    CoolingCoil.Total_Cooling_Capacity_Function_of_Temperature_Curve_Name = total_cooling_capacity_function_of_temperature_curve_name
    CoolingCoil.Total_Cooling_Capacity_Function_of_Flow_Fraction_Curve_Name = total_cooling_capacity_function_of_flow_fraction_curve_name
    CoolingCoil.Energy_Input_Ratio_Function_of_Temperature_Curve_Name = energy_input_ratio_function_of_temperature_curve_name
    CoolingCoil.Energy_Input_Ratio_Function_of_Flow_Fraction_Curve_Name = energy_input_ratio_function_of_flow_fraction_curve_name
    CoolingCoil.Part_Load_Fraction_Correlation_Curve_Name = part_load_fraction_correlation_curve_name
    CoolingCoil.Minimum_Outdoor_DryBulb_Temperature_for_Compressor_Operation = minimum_outdoor_drybulb_temperature_for_compressor_operation
    CoolingCoil.Nominal_Time_for_Condensate_Removal_to_Begin = nominal_time_for_condensate_removal_to_begin
    CoolingCoil.Ratio_of_Initial_Moisture_Evaporation_Rate_and_Steady_State_Latent_Capacity = ratio_of_initial_moisture_evaporation_rate_and_steady_state_latent_capacity
    CoolingCoil.Maximum_Cycling_Rate = maximum_cycling_rate
    CoolingCoil.Latent_Capacity_Time_Constant = latent_capacity_time_constant
    CoolingCoil.Condenser_Air_Inlet_Node_Name = condenser_air_inlet_node_name
    CoolingCoil.Condenser_Type = condenser_type
    CoolingCoil.Evaporative_Condenser_Effectiveness = evaporative_condenser_effectiveness
    CoolingCoil.Evaporative_Condenser_Air_Flow_Rate = evaporative_condenser_air_flow_rate
    CoolingCoil.Evaporative_Condenser_Pump_Rated_Power_Consumption = evaporative_condenser_pump_rated_power_consumption
    CoolingCoil.Crankcase_Heater_Capacity = crankcase_heater_capacity
    CoolingCoil.Crankcase_Heater_Capacity_Function_of_Temperature_Curve_Name = crankcase_heater_capacity_function_of_temperature_curve_name
    CoolingCoil.Maximum_Outdoor_DryBulb_Temperature_for_Crankcase_Heater_Operation = maximum_outdoor_drybulb_temperature_for_crankcase_heater_operation
    CoolingCoil.Supply_Water_Storage_Tank_Name = supply_water_storage_tank_name
    CoolingCoil.Condensate_Collection_Water_Storage_Tank_Name = condensate_collection_water_storage_tank_name
    CoolingCoil.Basin_Heater_Capacity = basin_heater_capacity
    CoolingCoil.Basin_Heater_Setpoint_Temperature = basin_heater_setpoint_temperature
    CoolingCoil.Basin_Heater_Operating_Schedule_Name = basin_heater_operating_schedule_name
    CoolingCoil.Sensible_Heat_Ratio_Function_of_Temperature_Curve_Name = sensible_heat_ratio_function_of_temperature_curve_name
    CoolingCoil.Sensible_Heat_Ratio_Function_of_Flow_Fraction_Curve_Name = sensible_heat_ratio_function_of_flow_fraction_curve_name
    CoolingCoil.Report_ASHRAE_Standard_127_Performance_Ratings = report_ashrae_standard_127_performance_ratings
    CoolingCoil.Zone_Name_for_Condenser_Placement = zone_name_for_condenser_placement
    return CoolingCoil


def coil_heating_electric(
        idf,
        name="",
        availability_schedule_name="",
        efficiency="",
        nominal_capacity="",
        air_inlet_node_name="Cooling_coil_outlet_node",
        air_outlet_node_name="Heating_coil_outlet_node",
        temperature_setpoint_node_name=""):
    """
    Create and configure a Coil:Heating:Electric object for EnergyPlus IDF.
    """
    HeatingCoil = idf.newidfobject("Coil:Heating:Electric")
    HeatingCoil.Name = name
    HeatingCoil.Availability_Schedule_Name = availability_schedule_name
    HeatingCoil.Efficiency = efficiency
    HeatingCoil.Nominal_Capacity = nominal_capacity
    HeatingCoil.Air_Inlet_Node_Name = air_inlet_node_name
    HeatingCoil.Air_Outlet_Node_Name = air_outlet_node_name
    HeatingCoil.Temperature_Setpoint_Node_Name = temperature_setpoint_node_name
    return HeatingCoil


def coil_heating_dx_single_speed(
        idf,
        name="Heating_coil1",
        availability_schedule_name="Active_winter",
        gross_rated_heating_capacity="autosize",
        gross_rated_heating_cop="3",
        rated_air_flow_rate="autosize",
        rated_supply_fan_power_per_volume_flow_rate_2017="",
        rated_supply_fan_power_per_volume_flow_rate_2023="",
        air_inlet_node_name="Cooling_coil_outlet_node",
        air_outlet_node_name="Heating_coil_outlet_node",
        heating_capacity_function_of_temperature_curve_name="HPACHeatCapFT",
        heating_capacity_function_of_flow_fraction_curve_name="HPACHeatCapFFF",
        energy_input_ratio_function_of_temperature_curve_name="HPACHeatEIRFT",
        energy_input_ratio_function_of_flow_fraction_curve_name="HPACHeatEIRFFF",
        part_load_fraction_correlation_curve_name="HPACCOOLPLFFPLR",
        defrost_energy_input_ratio_function_of_temperature_curve_name="",
        minimum_outdoor_drybulb_temperature_for_compressor_operation="",
        outdoor_drybulb_temperature_to_turn_on_compressor="",
        maximum_outdoor_drybulb_temperature_for_defrost_operation="",
        crankcase_heater_capacity="",
        crankcase_heater_capacity_function_of_temperature_curve_name="",
        maximum_outdoor_drybulb_temperature_for_crankcase_heater_operation="",
        defrost_strategy="",
        defrost_control="",
        defrost_time_period_fraction="",
        resistive_defrost_heater_capacity="",
        region_number_for_calculating_hspf="",
        evaporator_air_inlet_node_name="",
        zone_name_for_evaporator_placement="",
        secondary_coil_air_flow_rate="",
        secondary_coil_fan_flow_scaling_factor="",
        nominal_sensible_heat_ratio_of_secondary_coil="",
        sensible_heat_ratio_modifier_function_of_temperature_curve_name="",
        sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name=""):
    """
    Create and configure a Coil:Heating:DX:SingleSpeed object for EnergyPlus IDF.
    """
    CoilHeatingDXSingleSpeed = idf.newidfobject("Coil:Heating:DX:SingleSpeed")
    CoilHeatingDXSingleSpeed.Name = name
    CoilHeatingDXSingleSpeed.Availability_Schedule_Name = availability_schedule_name
    CoilHeatingDXSingleSpeed.Gross_Rated_Heating_Capacity = gross_rated_heating_capacity
    CoilHeatingDXSingleSpeed.Gross_Rated_Heating_COP = gross_rated_heating_cop
    CoilHeatingDXSingleSpeed.Rated_Air_Flow_Rate = rated_air_flow_rate
    setattr(CoilHeatingDXSingleSpeed, "2017_Rated_Supply_Fan_Power_Per_Volume_Flow_Rate", rated_supply_fan_power_per_volume_flow_rate_2017)
    setattr(CoilHeatingDXSingleSpeed, "2023_Rated_Supply_Fan_Power_Per_Volume_Flow_Rate", rated_supply_fan_power_per_volume_flow_rate_2023)
    CoilHeatingDXSingleSpeed.Air_Inlet_Node_Name = air_inlet_node_name
    CoilHeatingDXSingleSpeed.Air_Outlet_Node_Name = air_outlet_node_name
    CoilHeatingDXSingleSpeed.Heating_Capacity_Function_of_Temperature_Curve_Name = heating_capacity_function_of_temperature_curve_name
    CoilHeatingDXSingleSpeed.Heating_Capacity_Function_of_Flow_Fraction_Curve_Name = heating_capacity_function_of_flow_fraction_curve_name
    CoilHeatingDXSingleSpeed.Energy_Input_Ratio_Function_of_Temperature_Curve_Name = energy_input_ratio_function_of_temperature_curve_name
    CoilHeatingDXSingleSpeed.Energy_Input_Ratio_Function_of_Flow_Fraction_Curve_Name = energy_input_ratio_function_of_flow_fraction_curve_name
    CoilHeatingDXSingleSpeed.Part_Load_Fraction_Correlation_Curve_Name = part_load_fraction_correlation_curve_name
    CoilHeatingDXSingleSpeed.Defrost_Energy_Input_Ratio_Function_of_Temperature_Curve_Name = defrost_energy_input_ratio_function_of_temperature_curve_name
    CoilHeatingDXSingleSpeed.Minimum_Outdoor_DryBulb_Temperature_for_Compressor_Operation = minimum_outdoor_drybulb_temperature_for_compressor_operation
    CoilHeatingDXSingleSpeed.Outdoor_DryBulb_Temperature_to_Turn_On_Compressor = outdoor_drybulb_temperature_to_turn_on_compressor
    CoilHeatingDXSingleSpeed.Maximum_Outdoor_DryBulb_Temperature_for_Defrost_Operation = maximum_outdoor_drybulb_temperature_for_defrost_operation
    CoilHeatingDXSingleSpeed.Crankcase_Heater_Capacity = crankcase_heater_capacity
    CoilHeatingDXSingleSpeed.Crankcase_Heater_Capacity_Function_of_Temperature_Curve_Name = crankcase_heater_capacity_function_of_temperature_curve_name
    CoilHeatingDXSingleSpeed.Maximum_Outdoor_DryBulb_Temperature_for_Crankcase_Heater_Operation = maximum_outdoor_drybulb_temperature_for_crankcase_heater_operation
    CoilHeatingDXSingleSpeed.Defrost_Strategy = defrost_strategy
    CoilHeatingDXSingleSpeed.Defrost_Control = defrost_control
    CoilHeatingDXSingleSpeed.Defrost_Time_Period_Fraction = defrost_time_period_fraction
    CoilHeatingDXSingleSpeed.Resistive_Defrost_Heater_Capacity = resistive_defrost_heater_capacity
    CoilHeatingDXSingleSpeed.Region_number_for_calculating_HSPF = region_number_for_calculating_hspf
    CoilHeatingDXSingleSpeed.Evaporator_Air_Inlet_Node_Name = evaporator_air_inlet_node_name
    CoilHeatingDXSingleSpeed.Zone_Name_for_Evaporator_Placement = zone_name_for_evaporator_placement
    CoilHeatingDXSingleSpeed.Secondary_Coil_Air_Flow_Rate = secondary_coil_air_flow_rate
    CoilHeatingDXSingleSpeed.Secondary_Coil_Fan_Flow_Scaling_Factor = secondary_coil_fan_flow_scaling_factor
    CoilHeatingDXSingleSpeed.Nominal_Sensible_Heat_Ratio_of_Secondary_Coil = nominal_sensible_heat_ratio_of_secondary_coil
    CoilHeatingDXSingleSpeed.Sensible_Heat_Ratio_Modifier_Function_of_Temperature_Curve_Name = sensible_heat_ratio_modifier_function_of_temperature_curve_name
    CoilHeatingDXSingleSpeed.Sensible_Heat_Ratio_Modifier_Function_of_Flow_Fraction_Curve_Name = sensible_heat_ratio_modifier_function_of_flow_fraction_curve_name
    return CoilHeatingDXSingleSpeed


def branch(
        idf,
        name="branch_name",
        pressure_drop_curve_name="",
        component_1_object_type="object_type",
        component_1_name="component_name",
        component_1_inlet_node_name="inlet_node_name",
        component_1_outlet_node_name="outlet_node_name"):
    """
    Create and configure a Branch object for EnergyPlus IDF.
    """
    BranchObject = idf.newidfobject("Branch")
    BranchObject.Name = name
    BranchObject.Pressure_Drop_Curve_Name = pressure_drop_curve_name
    BranchObject.Component_1_Object_Type = component_1_object_type
    BranchObject.Component_1_Name = component_1_name
    BranchObject.Component_1_Inlet_Node_Name = component_1_inlet_node_name
    BranchObject.Component_1_Outlet_Node_Name = component_1_outlet_node_name
    return BranchObject


def branchlist(
        idf,
        name="branch_list_name",
        branch_1_name="branch_1_name",
        branch_2_name="branch_2_name",
        branch_3_name="branch_3_name",
        branch_4_name="branch_4_name"):
    """
    Create and configure a BranchList object for EnergyPlus IDF.
    """
    BranchList = idf.newidfobject("BranchList")
    BranchList.Name = name
    BranchList.Branch_1_Name = branch_1_name
    BranchList.Branch_2_Name = branch_2_name
    BranchList.Branch_3_Name = branch_3_name
    BranchList.Branch_4_Name = branch_4_name
    return BranchList


def connector_splitter(
        idf,
        name="splitter_name",
        inlet_branch_name="inlet_branch_name",
        outlet_branch_1_name="outlet_branch_1_name",
        outlet_branch_2_name="outlet_branch_2_name"):
    """
    Create and configure a Connector:Splitter object for EnergyPlus IDF.
    """
    Splitter = idf.newidfobject("Connector:Splitter")
    Splitter.Name = name
    Splitter.Inlet_Branch_Name = inlet_branch_name
    Splitter.Outlet_Branch_1_Name = outlet_branch_1_name
    Splitter.Outlet_Branch_2_Name = outlet_branch_2_name
    return Splitter


def connector_mixer(
        idf,
        name="mixer_name",
        outlet_branch_name="outlet_branch_name",
        inlet_branch_1_name="inlet_branch_1_name",
        inlet_branch_2_name="inlet_branch_2_name"):
    """
    Create and configure a Connector:Mixer object for EnergyPlus IDF.
    """
    Mixer = idf.newidfobject("Connector:Mixer")
    Mixer.Name = name
    Mixer.Outlet_Branch_Name = outlet_branch_name
    Mixer.Inlet_Branch_1_Name = inlet_branch_1_name
    Mixer.Inlet_Branch_2_Name = inlet_branch_2_name
    return Mixer


def connectorlist(
        idf,
        name="connector_list_name",
        connector_1_object_type="connector1_object_type",
        connector_1_name="connector1_name",
        connector_2_object_type="connector2_object_type",
        connector_2_name="connector2_name"):
    """
    Create and configure a ConnectorList object for EnergyPlus IDF.
    """
    ConnectorList = idf.newidfobject("ConnectorList")
    ConnectorList.Name = name
    ConnectorList.Connector_1_Object_Type = connector_1_object_type
    ConnectorList.Connector_1_Name = connector_1_name
    ConnectorList.Connector_2_Object_Type = connector_2_object_type
    ConnectorList.Connector_2_Name = connector_2_name
    return ConnectorList


def nodelist(
        idf,
        name="nodelist_name",
        node_1_name="node_1_name"):
    """
    Create and configure a NodeList object for EnergyPlus IDF.
    """
    NodeList = idf.newidfobject("NodeList")
    NodeList.Name = name
    NodeList.Node_1_Name = node_1_name
    return NodeList


def pipe_adiabatic(
        idf,
        name="pipe_name",
        inlet_node_name="inlet_node_name",
        outlet_node_name="outlet_node_name"):
    """
    Create and configure a Pipe:Adiabatic object for EnergyPlus IDF.
    """
    Pipe = idf.newidfobject("Pipe:Adiabatic")
    Pipe.Name = name
    Pipe.Inlet_Node_Name = inlet_node_name
    Pipe.Outlet_Node_Name = outlet_node_name
    return Pipe


def pump_variable_speed(
        idf,
        name="Pump1",
        inlet_node_name="Supply_pump_inlet_node",
        outlet_node_name="Supply_pump_outlet_node",
        design_maximum_flow_rate="",
        design_pump_head="",
        design_power_consumption="",
        motor_efficiency="",
        fraction_of_motor_inefficiencies_to_fluid_stream="",
        coefficient_1_of_the_part_load_performance_curve="",
        coefficient_2_of_the_part_load_performance_curve="",
        coefficient_3_of_the_part_load_performance_curve="",
        coefficient_4_of_the_part_load_performance_curve="",
        design_minimum_flow_rate="",
        pump_control_type="",
        pump_flow_rate_schedule_name="",
        pump_curve_name="",
        impeller_diameter="",
        vfd_control_type="",
        pump_rpm_schedule_name="",
        minimum_pressure_schedule="",
        maximum_pressure_schedule="",
        minimum_rpm_schedule="",
        maximum_rpm_schedule="",
        zone_name="",
        skin_loss_radiative_fraction="",
        design_power_sizing_method="",
        design_electric_power_per_unit_flow_rate="",
        design_shaft_power_per_unit_flow_rate_per_unit_head="",
        design_minimum_flow_rate_fraction="",
        enduse_subcategory=""):
    """
    Create and configure a Pump:VariableSpeed object for EnergyPlus IDF.
    """
    Pump = idf.newidfobject("Pump:VariableSpeed")
    Pump.Name = name
    Pump.Inlet_Node_Name = inlet_node_name
    Pump.Outlet_Node_Name = outlet_node_name
    Pump.Design_Maximum_Flow_Rate = design_maximum_flow_rate
    Pump.Design_Pump_Head = design_pump_head
    Pump.Design_Power_Consumption = design_power_consumption
    Pump.Motor_Efficiency = motor_efficiency
    Pump.Fraction_of_Motor_Inefficiencies_to_Fluid_Stream = fraction_of_motor_inefficiencies_to_fluid_stream
    Pump.Coefficient_1_of_the_Part_Load_Performance_Curve = coefficient_1_of_the_part_load_performance_curve
    Pump.Coefficient_2_of_the_Part_Load_Performance_Curve = coefficient_2_of_the_part_load_performance_curve
    Pump.Coefficient_3_of_the_Part_Load_Performance_Curve = coefficient_3_of_the_part_load_performance_curve
    Pump.Coefficient_4_of_the_Part_Load_Performance_Curve = coefficient_4_of_the_part_load_performance_curve
    Pump.Design_Minimum_Flow_Rate = design_minimum_flow_rate
    Pump.Pump_Control_Type = pump_control_type
    Pump.Pump_Flow_Rate_Schedule_Name = pump_flow_rate_schedule_name
    Pump.Pump_Curve_Name = pump_curve_name
    Pump.Impeller_Diameter = impeller_diameter
    Pump.VFD_Control_Type = vfd_control_type
    Pump.Pump_RPM_Schedule_Name = pump_rpm_schedule_name
    Pump.Minimum_Pressure_Schedule = minimum_pressure_schedule
    Pump.Maximum_Pressure_Schedule = maximum_pressure_schedule
    Pump.Minimum_RPM_Schedule = minimum_rpm_schedule
    Pump.Maximum_RPM_Schedule = maximum_rpm_schedule
    Pump.Zone_Name = zone_name
    Pump.Skin_Loss_Radiative_Fraction = skin_loss_radiative_fraction
    Pump.Design_Power_Sizing_Method = design_power_sizing_method
    Pump.Design_Electric_Power_per_Unit_Flow_Rate = design_electric_power_per_unit_flow_rate
    Pump.Design_Shaft_Power_per_Unit_Flow_Rate_per_Unit_Head = design_shaft_power_per_unit_flow_rate_per_unit_head
    Pump.Design_Minimum_Flow_Rate_Fraction = design_minimum_flow_rate_fraction
    Pump.EndUse_Subcategory = enduse_subcategory
    return Pump


def boiler_hot_water(
        idf,
        name="Boiler1",
        fuel_type="NaturalGas",
        nominal_capacity="",
        nominal_thermal_efficiency=0.8,
        efficiency_curve_temperature_evaluation_variable="",
        normalized_boiler_efficiency_curve_name="",
        design_water_flow_rate="",
        minimum_part_load_ratio="",
        maximum_part_load_ratio="",
        optimum_part_load_ratio="",
        boiler_water_inlet_node_name="Boiler_inlet_node",
        boiler_water_outlet_node_name="Boiler_outlet_node",
        water_outlet_upper_temperature_limit="",
        boiler_flow_mode="",
        on_cycle_parasitic_electric_load="",
        sizing_factor="",
        enduse_subcategory="",
        off_cycle_parasitic_fuel_load=""):
    """
    Create and configure a Boiler:HotWater object for EnergyPlus IDF.
    """
    Boiler = idf.newidfobject("Boiler:HotWater")
    Boiler.Name = name
    Boiler.Fuel_Type = fuel_type
    Boiler.Nominal_Capacity = nominal_capacity
    Boiler.Nominal_Thermal_Efficiency = nominal_thermal_efficiency
    Boiler.Efficiency_Curve_Temperature_Evaluation_Variable = efficiency_curve_temperature_evaluation_variable
    Boiler.Normalized_Boiler_Efficiency_Curve_Name = normalized_boiler_efficiency_curve_name
    Boiler.Design_Water_Flow_Rate = design_water_flow_rate
    Boiler.Minimum_Part_Load_Ratio = minimum_part_load_ratio
    Boiler.Maximum_Part_Load_Ratio = maximum_part_load_ratio
    Boiler.Optimum_Part_Load_Ratio = optimum_part_load_ratio
    Boiler.Boiler_Water_Inlet_Node_Name = boiler_water_inlet_node_name
    Boiler.Boiler_Water_Outlet_Node_Name = boiler_water_outlet_node_name
    Boiler.Water_Outlet_Upper_Temperature_Limit = water_outlet_upper_temperature_limit
    Boiler.Boiler_Flow_Mode = boiler_flow_mode
    Boiler.On_Cycle_Parasitic_Electric_Load = on_cycle_parasitic_electric_load
    Boiler.Sizing_Factor = sizing_factor
    Boiler.EndUse_Subcategory = enduse_subcategory
    Boiler.Off_Cycle_Parasitic_Fuel_Load = off_cycle_parasitic_fuel_load
    return Boiler


def plant_loop(
        idf,
        name="Plant_loop1",
        fluid_type="",
        user_defined_fluid_type="",
        plant_equipment_operation_scheme_name="Plant_operation_scheme1",
        loop_temperature_setpoint_node_name="Supply_exit_pipe_outlet_node",
        maximum_loop_temperature=100,
        minimum_loop_temperature=10,
        maximum_loop_flow_rate="autosize",
        minimum_loop_flow_rate="",
        plant_loop_volume="",
        plant_side_inlet_node_name="Supply_pump_inlet_node",
        plant_side_outlet_node_name="Supply_exit_pipe_outlet_node",
        plant_side_branch_list_name="Supply_branch_list",
        plant_side_connector_list_name="Supply_connector_list",
        demand_side_inlet_node_name="Zone_inlet_pipe_inlet_node",
        demand_side_outlet_node_name="Zone_outlet_pipe_outlet_node",
        demand_side_branch_list_name="Demand_branch_list",
        demand_side_connector_list_name="",
        load_distribution_scheme="",
        availability_manager_list_name="",
        plant_loop_demand_calculation_scheme="",
        common_pipe_simulation="",
        pressure_simulation_type="",
        loop_circulation_time=""):
    """
    Create and configure a PlantLoop object for EnergyPlus IDF.
    """
    Loop = idf.newidfobject("PlantLoop")
    Loop.Name = name
    Loop.Fluid_Type = fluid_type
    Loop.User_Defined_Fluid_Type = user_defined_fluid_type
    Loop.Plant_Equipment_Operation_Scheme_Name = plant_equipment_operation_scheme_name
    Loop.Loop_Temperature_Setpoint_Node_Name = loop_temperature_setpoint_node_name
    Loop.Maximum_Loop_Temperature = maximum_loop_temperature
    Loop.Minimum_Loop_Temperature = minimum_loop_temperature
    Loop.Maximum_Loop_Flow_Rate = maximum_loop_flow_rate
    Loop.Minimum_Loop_Flow_Rate = minimum_loop_flow_rate
    Loop.Plant_Loop_Volume = plant_loop_volume
    Loop.Plant_Side_Inlet_Node_Name = plant_side_inlet_node_name
    Loop.Plant_Side_Outlet_Node_Name = plant_side_outlet_node_name
    Loop.Plant_Side_Branch_List_Name = plant_side_branch_list_name
    Loop.Plant_Side_Connector_List_Name = plant_side_connector_list_name
    Loop.Demand_Side_Inlet_Node_Name = demand_side_inlet_node_name
    Loop.Demand_Side_Outlet_Node_Name = demand_side_outlet_node_name
    Loop.Demand_Side_Branch_List_Name = demand_side_branch_list_name
    Loop.Demand_Side_Connector_List_Name = demand_side_connector_list_name
    Loop.Load_Distribution_Scheme = load_distribution_scheme
    Loop.Availability_Manager_List_Name = availability_manager_list_name
    Loop.Plant_Loop_Demand_Calculation_Scheme = plant_loop_demand_calculation_scheme
    Loop.Common_Pipe_Simulation = common_pipe_simulation
    Loop.Pressure_Simulation_Type = pressure_simulation_type
    Loop.Loop_Circulation_Time = loop_circulation_time
    return Loop


def plant_equipment_list(
        idf,
        name="Plant_equipment_list1",
        equipment_1_object_type="",
        equipment_1_name=""):
    """
    Create and configure a PlantEquipmentList object for EnergyPlus IDF.
    """
    EquipmentList = idf.newidfobject("PlantEquipmentList")
    EquipmentList.Name = name
    EquipmentList.Equipment_1_Object_Type = equipment_1_object_type
    EquipmentList.Equipment_1_Name = equipment_1_name
    return EquipmentList


def plant_equipment_operation_heating_load(
        idf,
        name="Plant_heating_load1",
        load_range_1_lower_limit=0,
        load_range_1_upper_limit=100000,
        range_1_equipment_list_name="Plant_equipment_list1"):
    """
    Create and configure a PlantEquipmentOperation:HeatingLoad object for EnergyPlus IDF.
    """
    Operation = idf.newidfobject("PlantEquipmentOperation:HeatingLoad")
    Operation.Name = name
    Operation.Load_Range_1_Lower_Limit = load_range_1_lower_limit
    Operation.Load_Range_1_Upper_Limit = load_range_1_upper_limit
    Operation.Range_1_Equipment_List_Name = range_1_equipment_list_name
    return Operation


def plant_operation_scheme(
        idf,
        name="Plant_operation_scheme1",
        control_scheme_1_object_type="PlantEquipmentOperation:HeatingLoad",
        control_scheme_1_name="Plant_heating_load1",
        control_scheme_1_schedule_name="Always On"):
    """
    Create and configure a PlantEquipmentOperationSchemes object for EnergyPlus IDF.
    """
    Schemes = idf.newidfobject("PlantEquipmentOperationSchemes")
    Schemes.Name = name
    Schemes.Control_Scheme_1_Object_Type = control_scheme_1_object_type
    Schemes.Control_Scheme_1_Name = control_scheme_1_name
    Schemes.Control_Scheme_1_Schedule_Name = control_scheme_1_schedule_name
    return Schemes


def setpoint_manager_scheduled(
        idf,
        name="Supply_setpoint_manager_schedule1",
        control_variable="Temperature",
        schedule_name="Heating_supply_schedule",
        setpoint_node_or_nodelist_name="Supply_exit_pipe_outlet_node"):
    """
    Create and configure a SetpointManager:Scheduled object for EnergyPlus IDF.
    """
    SetpointManager = idf.newidfobject("SetpointManager:Scheduled")
    SetpointManager.Name = name
    SetpointManager.Control_Variable = control_variable
    SetpointManager.Schedule_Name = schedule_name
    SetpointManager.Setpoint_Node_or_NodeList_Name = setpoint_node_or_nodelist_name
    return SetpointManager



def curve_quadratic(
        idf,
        name="curve_name",
        coefficient1_constant=1,
        coefficient2_x=1,
        coefficient3_x2=1,
        minimum_value_of_x=-1,
        maximum_value_of_x=1,
        minimum_curve_output="",
        maximum_curve_output="",
        input_unit_type_for_x="",
        output_unit_type=""):
    """
    Create and configure a Curve:Quadratic object for EnergyPlus IDF.
    """
    Curve = idf.newidfobject("Curve:Quadratic")
    Curve.Name = name
    Curve.Coefficient1_Constant = coefficient1_constant
    Curve.Coefficient2_x = coefficient2_x
    Curve.Coefficient3_x2 = coefficient3_x2
    Curve.Minimum_Value_of_x = minimum_value_of_x
    Curve.Maximum_Value_of_x = maximum_value_of_x
    Curve.Minimum_Curve_Output = minimum_curve_output
    Curve.Maximum_Curve_Output = maximum_curve_output
    Curve.Input_Unit_Type_for_X = input_unit_type_for_x
    Curve.Output_Unit_Type = output_unit_type
    return Curve


def curve_cubic(
        idf,
        name="curve_name",
        coefficient1_constant=1,
        coefficient2_x=1,
        coefficient3_x2=1,
        coefficient4_x3=1,
        minimum_value_of_x=-1,
        maximum_value_of_x=1,
        minimum_curve_output="",
        maximum_curve_output="",
        input_unit_type_for_x="",
        output_unit_type=""):
    """
    Create and configure a Curve:Cubic object for EnergyPlus IDF.
    """
    Curve = idf.newidfobject("Curve:Cubic")
    Curve.Name = name
    Curve.Coefficient1_Constant = coefficient1_constant
    Curve.Coefficient2_x = coefficient2_x
    Curve.Coefficient3_x2 = coefficient3_x2
    Curve.Coefficient4_x3 = coefficient4_x3
    Curve.Minimum_Value_of_x = minimum_value_of_x
    Curve.Maximum_Value_of_x = maximum_value_of_x
    Curve.Minimum_Curve_Output = minimum_curve_output
    Curve.Maximum_Curve_Output = maximum_curve_output
    Curve.Input_Unit_Type_for_X = input_unit_type_for_x
    Curve.Output_Unit_Type = output_unit_type
    return Curve


def curve_exponent(
        idf,
        name="curve_name",
        coefficient1_constant=1,
        coefficient2_constant=1,
        coefficient3_constant=1,
        minimum_value_of_x=1,
        maximum_value_of_x=-1,
        minimum_curve_output="",
        maximum_curve_output="",
        input_unit_type_for_x="",
        output_unit_type=""):
    """
    Create and configure a Curve:Exponent object for EnergyPlus IDF.
    """
    Curve = idf.newidfobject("Curve:Exponent")
    Curve.Name = name
    Curve.Coefficient1_Constant = coefficient1_constant
    Curve.Coefficient2_Constant = coefficient2_constant
    Curve.Coefficient3_Constant = coefficient3_constant
    Curve.Minimum_Value_of_x = minimum_value_of_x
    Curve.Maximum_Value_of_x = maximum_value_of_x
    Curve.Minimum_Curve_Output = minimum_curve_output
    Curve.Maximum_Curve_Output = maximum_curve_output
    Curve.Input_Unit_Type_for_X = input_unit_type_for_x
    Curve.Output_Unit_Type = output_unit_type
    return Curve


def curve_biquadratic(
        idf,
        name="curve_name",
        coefficient1_constant=1,
        coefficient2_x=1,
        coefficient3_x2=1,
        coefficient4_y=1,
        coefficient5_y2=1,
        coefficient6_xy=1,
        minimum_value_of_x=-1,
        maximum_value_of_x=1,
        minimum_value_of_y=-1,
        maximum_value_of_y=1,
        minimum_curve_output="",
        maximum_curve_output="",
        input_unit_type_for_x="",
        input_unit_type_for_y="",
        output_unit_type=""):
    """
    Create and configure a Curve:Biquadratic object for EnergyPlus IDF.
    """
    Curve = idf.newidfobject("Curve:Biquadratic")
    Curve.Name = name
    Curve.Coefficient1_Constant = coefficient1_constant
    Curve.Coefficient2_x = coefficient2_x
    Curve.Coefficient3_x2 = coefficient3_x2
    Curve.Coefficient4_y = coefficient4_y
    Curve.Coefficient5_y2 = coefficient5_y2
    Curve.Coefficient6_xy = coefficient6_xy
    Curve.Minimum_Value_of_x = minimum_value_of_x
    Curve.Maximum_Value_of_x = maximum_value_of_x
    Curve.Minimum_Value_of_y = minimum_value_of_y
    Curve.Maximum_Value_of_y = maximum_value_of_y
    Curve.Minimum_Curve_Output = minimum_curve_output
    Curve.Maximum_Curve_Output = maximum_curve_output
    Curve.Input_Unit_Type_for_X = input_unit_type_for_x
    Curve.Input_Unit_Type_for_Y = input_unit_type_for_y
    Curve.Output_Unit_Type = output_unit_type
    return Curve



def output_variable_dictionary(
        idf, 
        key_field="IDF",
        sort_option="Unsorted"):
    """
    Create and configure an Output:VariableDictionary object for EnergyPlus IDF.
    """
    OutputVariableDictionary = idf.newidfobject("Output:VariableDictionary")
    OutputVariableDictionary.Key_Field = key_field
    OutputVariableDictionary.Sort_Option = sort_option
    
    return OutputVariableDictionary


def output_variable(
        idf,
        variable_name,
        reporting_frequency="Timestep"):
    """
    Create and configure an Output:Variable object for EnergyPlus IDF.
    """
    OutputVariable = idf.newidfobject("Output:Variable")
    OutputVariable.Variable_Name = variable_name
    OutputVariable.Reporting_Frequency = reporting_frequency
    
    return OutputVariable


def output_meter(
        idf,
        key_name="",
        reporting_frequency="Timestep"):
    """
    Create and configure an Output:Meter object for EnergyPlus IDF.
    """
    OutputMeter = idf.newidfobject("Output:Meter")
    OutputMeter.Key_Name = key_name
    OutputMeter.Reporting_Frequency = reporting_frequency
    
    return OutputMeter


def output_table_summary_reports(
        idf,
        report_names=None):
    """
    Create and configure an Output:Table:SummaryReports object for EnergyPlus IDF.
    """
    if report_names is None:
        report_names = ["AllSummary"]
    
    OutputTableSummaryReports = idf.newidfobject("Output:Table:SummaryReports")
    
    for i, report_name in enumerate(report_names, 1):
        OutputTableSummaryReports[f"Report_{i}_Name"] = report_name
    
    return OutputTableSummaryReports


def output_control_files(
        idf,
        output_csv="Yes",
        output_mtr="No",
        output_eso="No",
        output_eio="No",
        output_tabular="Yes",
        output_sqlite="No",
        output_json="No",
        output_audit="No",
        output_space_sizing="No",
        output_zone_sizing="No",
        output_system_sizing="No",
        output_dxf="No",
        output_bnd="No",
        output_rdd="Yes",
        output_mdd="No",
        output_mtd="No",
        output_end="No",
        output_shd="No",
        output_dfs="No",
        output_glhe="No",
        output_delightin="No",
        output_delighteldmp="No",
        output_delightdfdmp="No",
        output_edd="No",
        output_dbg="No",
        output_perflog="No",
        output_sln="No",
        output_sci="No",
        output_wrl="No",
        output_screen="No",
        output_extshd="No",
        output_tarcog="No"):
    """
    Create and configure an OutputControl:Files object for EnergyPlus IDF.
    """
    OutputControlFiles = idf.newidfobject("OutputControl:Files")
    OutputControlFiles.Output_CSV = output_csv
    OutputControlFiles.Output_MTR = output_mtr
    OutputControlFiles.Output_ESO = output_eso
    OutputControlFiles.Output_EIO = output_eio
    OutputControlFiles.Output_Tabular = output_tabular
    OutputControlFiles.Output_SQLite = output_sqlite
    OutputControlFiles.Output_JSON = output_json
    OutputControlFiles.Output_AUDIT = output_audit
    OutputControlFiles.Output_Space_Sizing = output_space_sizing
    OutputControlFiles.Output_Zone_Sizing = output_zone_sizing
    OutputControlFiles.Output_System_Sizing = output_system_sizing
    OutputControlFiles.Output_DXF = output_dxf
    OutputControlFiles.Output_BND = output_bnd
    OutputControlFiles.Output_RDD = output_rdd
    OutputControlFiles.Output_MDD = output_mdd
    OutputControlFiles.Output_MTD = output_mtd
    OutputControlFiles.Output_END = output_end
    OutputControlFiles.Output_SHD = output_shd
    OutputControlFiles.Output_DFS = output_dfs
    OutputControlFiles.Output_GLHE = output_glhe
    OutputControlFiles.Output_DelightIn = output_delightin
    OutputControlFiles.Output_DelightELdmp = output_delighteldmp
    OutputControlFiles.Output_DelightDFdmp = output_delightdfdmp
    OutputControlFiles.Output_EDD = output_edd
    OutputControlFiles.Output_DBG = output_dbg
    OutputControlFiles.Output_PerfLog = output_perflog
    OutputControlFiles.Output_SLN = output_sln
    OutputControlFiles.Output_SCI = output_sci
    OutputControlFiles.Output_WRL = output_wrl
    OutputControlFiles.Output_Screen = output_screen
    OutputControlFiles.Output_ExtShd = output_extshd
    OutputControlFiles.Output_Tarcog = output_tarcog
    
    return OutputControlFiles

def output_control_timestamp(
        idf,
        ISO_8601_Format="Yes",
        Timestamp_at_Beginning_of_Interval="Yes"):
    """
    Create and configure an OutputControl:Timestamp object for EnergyPlus IDF.
    """
    OutputControlTimestamp = idf.newidfobject("OutputControl:Timestamp")
    OutputControlTimestamp.ISO_8601_Format = ISO_8601_Format
    OutputControlTimestamp.Timestamp_at_Beginning_of_Interval = Timestamp_at_Beginning_of_Interval

    return OutputControlTimestamp
