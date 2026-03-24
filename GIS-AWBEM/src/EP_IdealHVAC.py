import numpy as np
import pandas as pd
import os
from pathlib import Path
import subprocess
from datetime import datetime
from src.utilites import *

def simulation_control(idf,
                   do_zone_sizing='No',
                   do_system_sizing='No',
                   do_plant_sizing='No',
                   run_sizing_periods='No',
                   run_weather_file='Yes',
                   do_hvac_sizing_simulation='No',
                   max_hvac_sizing_passes=1):
    """
    Create and configure a SimulationControl object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add SimulationControl to.
    do_zone_sizing : str, optional
        Do zone sizing calculation. Default 'No'.
    do_system_sizing : str, optional
        Do system sizing calculation. Default 'No'.
    do_plant_sizing : str, optional
        Do plant sizing calculation. Default 'No'.
    run_sizing_periods : str, optional
        Run simulation for sizing periods. Default 'No'.
    run_weather_file : str, optional
        Run simulation for weather file run periods. Default 'Yes'.
    do_hvac_sizing_simulation : str, optional
        Do HVAC sizing simulation for sizing periods. Default 'No'.
    max_hvac_sizing_passes : int, optional
        Maximum number of HVAC sizing simulation passes. Default 1.
    
    Returns
    -------
    idf object
        SimulationControl object with configured attributes.
    """
    SimulationControl = idf.newidfobject('SimulationControl')
    SimulationControl.Do_Zone_Sizing_Calculation = do_zone_sizing
    SimulationControl.Do_System_Sizing_Calculation = do_system_sizing
    SimulationControl.Do_Plant_Sizing_Calculation = do_plant_sizing
    SimulationControl.Run_Simulation_for_Sizing_Periods = run_sizing_periods
    SimulationControl.Run_Simulation_for_Weather_File_Run_Periods = run_weather_file
    SimulationControl.Do_HVAC_Sizing_Simulation_for_Sizing_Periods = do_hvac_sizing_simulation
    SimulationControl.Maximum_Number_of_HVAC_Sizing_Simulation_Passes = max_hvac_sizing_passes

    return SimulationControl


def building(idf, name='Building1', north_axis=0, terrain='Suburbs',
                loads_convergence_tolerance='', 
                temperature_convergence_tolerance='',
                solar_distribution='FullExterior',
                maximum_warmup_days=25, minimum_warmup_days=6):
    """
    Create and configure a Building object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add Building to.
    name : str
        Building name identifier.
    north_axis : float, optional
        Building north axis angle. Default 0.
    terrain : str, optional
        Terrain type. Default 'Suburbs'.
    loads_convergence_tolerance : str, optional
        Loads convergence tolerance value. Default ''.
    temperature_convergence_tolerance : str, optional
        Temperature convergence tolerance value. Default ''.
    solar_distribution : str, optional
        Solar distribution algorithm. Default 'FullExteriorWithReflections'.
    maximum_warmup_days : int, optional
        Maximum number of warmup days. Default 25.
    minimum_warmup_days : int, optional
        Minimum number of warmup days. Default 6.
    
    Returns
    -------
    idf object
        Building object with configured attributes.
    """
    Building = idf.newidfobject('Building')
    Building.Name = name
    Building.North_Axis = north_axis
    Building.Terrain = terrain
    Building.Loads_Convergence_Tolerance_Value = loads_convergence_tolerance
    Building.Temperature_Convergence_Tolerance_Value = temperature_convergence_tolerance
    Building.Solar_Distribution = solar_distribution
    Building.Maximum_Number_of_Warmup_Days = maximum_warmup_days
    Building.Minimum_Number_of_Warmup_Days = minimum_warmup_days
    
    return Building


def shadow_calculation(idf,
                         shading_calculation_method='PolygonClipping',
                         shading_calculation_update_frequency_method='Periodic',
                         shading_calculation_update_frequency=7,
                         maximum_figures_in_shadow_overlap_calculations=15000,
                         polygon_clipping_algorithm='SutherlandHodgman',
                         pixel_counting_resolution=512,
                         sky_diffuse_modeling_algorithm='SimpleSkyDiffuseModeling',
                         output_external_shading_calculation_results='No',
                         disable_selfshading_within_shading_zone_groups='No',
                         disable_selfshading_from_shading_zone_groups_to_other_zones='No',
                         shading_zone_group_names=None):
    """
    Create and configure a ShadowCalculation object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add ShadowCalculation to.
    shading_calculation_method : str, optional
        Shading calculation method. Default 'PolygonClipping'.
    shading_calculation_update_frequency_method : str, optional
        Update frequency method. Default 'Periodic'.
    shading_calculation_update_frequency : int, optional
        Update frequency value. Default 7.
    maximum_figures_in_shadow_overlap_calculations : int, optional
        Maximum figures in shadow overlap calculations. Default 15000.
    polygon_clipping_algorithm : str, optional
        Polygon clipping algorithm. Default 'SutherlandHodgman'.
    pixel_counting_resolution : int, optional
        Pixel counting resolution. Default 512.
    sky_diffuse_modeling_algorithm : str, optional
        Sky diffuse modeling algorithm. Default 'SimpleSkyDiffuseModeling'.
    output_external_shading_calculation_results : str, optional
        Output external shading calculation results. Default 'No'.
    disable_selfshading_within_shading_zone_groups : str, optional
        Disable self-shading within shading zone groups. Default 'No'.
    disable_selfshading_from_shading_zone_groups_to_other_zones : str, optional
        Disable self-shading from shading zone groups to other zones. Default 'No'.
    shading_zone_group_names : list of str, optional
        Names for up to 6 shading zone groups. Default None (all empty strings).
    
    Returns
    -------
    idf object
        ShadowCalculation object with configured attributes.
    """
    ShadowCalculation = idf.newidfobject('ShadowCalculation')
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
        shading_zone_group_names = [''] * 6
    else:
        # Pad with empty strings if fewer than 6 provided
        shading_zone_group_names = list(shading_zone_group_names) + [''] * (6 - len(shading_zone_group_names))
    
    for i in range(6):
        ShadowCalculation[f'Shading_Zone_Group_{i+1}_ZoneList_Name'] = shading_zone_group_names[i]
    
    return ShadowCalculation


def surface_convection_algorithm_inside(idf, algorithm='Tarp'):
    """
    Create and configure a SurfaceConvectionAlgorithm:Inside object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add SurfaceConvectionAlgorithm:Inside to.
    algorithm : str, optional
        Inside surface convection algorithm. Default 'Tarp'.
    
    Returns
    -------
    idf object
        SurfaceConvectionAlgorithm:Inside object with configured attributes.
    """
    SurfaceConvectionAlgorithmInside = idf.newidfobject('SurfaceConvectionAlgorithm:Inside')
    SurfaceConvectionAlgorithmInside.Algorithm = algorithm
    
    return SurfaceConvectionAlgorithmInside


def surface_convection_algorithm_outside(idf, algorithm='DOE-2'):
    """
    Create and configure a SurfaceConvectionAlgorithm:Outside object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add SurfaceConvectionAlgorithm:Outside to.
    algorithm : str, optional
        Outside surface convection algorithm. Default 'DOE-2'.
    
    Returns
    -------
    idf object
        SurfaceConvectionAlgorithm:Outside object with configured attributes.
    """
    SurfaceConvectionAlgorithmOutside = idf.newidfobject('SurfaceConvectionAlgorithm:Outside')
    SurfaceConvectionAlgorithmOutside.Algorithm = algorithm
    
    return SurfaceConvectionAlgorithmOutside


def heat_balance_algorithm(idf,
                              algorithm='ConductionTransferFunction',
                              surface_temperature_upper_limit='',
                              minimum_surface_convection_heat_transfer_coefficient_value='',
                              maximum_surface_convection_heat_transfer_coefficient_value=''):
    """
    Create and configure a HeatBalanceAlgorithm object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add HeatBalanceAlgorithm to.
    algorithm : str, optional
        Heat balance algorithm. Default 'ConductionTransferFunction'.
    surface_temperature_upper_limit : str, optional
        Surface temperature upper limit. Default ''.
    minimum_surface_convection_heat_transfer_coefficient_value : str, optional
        Minimum surface convection heat transfer coefficient value. Default ''.
    maximum_surface_convection_heat_transfer_coefficient_value : str, optional
        Maximum surface convection heat transfer coefficient value. Default ''.
    
    Returns
    -------
    idf object
        HeatBalanceAlgorithm object with configured attributes.
    """
    HeatBalanceAlgorithm = idf.newidfobject('HeatBalanceAlgorithm')
    HeatBalanceAlgorithm.Algorithm = algorithm
    HeatBalanceAlgorithm.Surface_Temperature_Upper_Limit = surface_temperature_upper_limit
    HeatBalanceAlgorithm.Minimum_Surface_Convection_Heat_Transfer_Coefficient_Value = minimum_surface_convection_heat_transfer_coefficient_value
    HeatBalanceAlgorithm.Maximum_Surface_Convection_Heat_Transfer_Coefficient_Value = maximum_surface_convection_heat_transfer_coefficient_value
    
    return HeatBalanceAlgorithm


def zone_air_heat_balance_algorithm(idf,
                                      algorithm='AnalyticalSolution',
                                      do_space_heat_balance_for_sizing='No',
                                      do_space_heat_balance_for_simulation='No'):
    """
    Create and configure a ZoneAirHeatBalanceAlgorithm object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add ZoneAirHeatBalanceAlgorithm to.
    algorithm : str, optional
        Zone air heat balance algorithm. Default 'AnalyticalSolution'.
    do_space_heat_balance_for_sizing : str, optional
        Do space heat balance for sizing. Default 'No'.
    do_space_heat_balance_for_simulation : str, optional
        Do space heat balance for simulation. Default 'No'.
    
    Returns
    -------
    idf object
        ZoneAirHeatBalanceAlgorithm object with configured attributes.
    """
    ZoneAirHeatBalanceAlgorithm = idf.newidfobject('ZoneAirHeatBalanceAlgorithm')
    ZoneAirHeatBalanceAlgorithm.Algorithm = algorithm
    ZoneAirHeatBalanceAlgorithm.Do_Space_Heat_Balance_for_Sizing = do_space_heat_balance_for_sizing
    ZoneAirHeatBalanceAlgorithm.Do_Space_Heat_Balance_for_Simulation = do_space_heat_balance_for_simulation
    
    return ZoneAirHeatBalanceAlgorithm


def timestep(idf, number_of_timesteps_per_hour=1):
    """
    Create and configure a Timestep object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add Timestep to.
    number_of_timesteps_per_hour : int, optional
        Number of timesteps per hour. Default 1.
    
    Returns
    -------
    idf object
        Timestep object with configured attributes.
    """
    Timestep = idf.newidfobject('Timestep')
    Timestep.Number_of_Timesteps_per_Hour = number_of_timesteps_per_hour
    
    return Timestep


def convergence_limits(idf,
                         minimum_system_timestep=1,
                         maximum_hvac_iterations='',
                         minimum_plant_iterations='',
                         maximum_plant_iterations=''):
    """
    Create and configure a ConvergenceLimits object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add ConvergenceLimits to.
    minimum_system_timestep : int, optional
        Minimum system timestep. Default 1.
    maximum_hvac_iterations : str, optional
        Maximum HVAC iterations. Default ''.
    minimum_plant_iterations : str, optional
        Minimum plant iterations. Default ''.
    maximum_plant_iterations : str, optional
        Maximum plant iterations. Default ''.
    
    Returns
    -------
    idf object
        ConvergenceLimits object with configured attributes.
    """
    ConvergenceLimits = idf.newidfobject('ConvergenceLimits')
    ConvergenceLimits.Minimum_System_Timestep = minimum_system_timestep
    ConvergenceLimits.Maximum_HVAC_Iterations = maximum_hvac_iterations
    ConvergenceLimits.Minimum_Plant_Iterations = minimum_plant_iterations
    ConvergenceLimits.Maximum_Plant_Iterations = maximum_plant_iterations
    
    return ConvergenceLimits


def site_location(idf,
                    name='Karlsruhe',
                    latitude=49.03300,
                    longitude=8.36700,
                    time_zone=1.0,
                    elevation=114.0):
    """
    Create and configure a Site:Location object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add Site:Location to.
    name : str, optional
        Location name. Default 'Karlsruhe'.
    latitude : float, optional
        Latitude. Default 49.03300.
    longitude : float, optional
        Longitude. Default 8.36700.
    time_zone : float, optional
        Time zone. Default 1.0.
    elevation : float, optional
        Elevation. Default 114.0.
    
    Returns
    -------
    idf object
        Site:Location object with configured attributes.
    """
    SiteLocation = idf.newidfobject('Site:Location')
    SiteLocation.Name = name
    SiteLocation.Latitude = latitude
    SiteLocation.Longitude = longitude
    SiteLocation.Time_Zone = time_zone
    SiteLocation.Elevation = elevation
    
    return SiteLocation


def run_period(idf,
                 name='Run Period 1',
                 begin_month=1,
                 begin_day_of_month=1,
                 end_month=12,
                 end_day_of_month=31,
                 use_weather_file_holidays_and_special_days='Yes',
                 use_weather_file_daylight_saving_period='Yes',
                 apply_weekend_holiday_rule='No',
                 use_weather_file_rain_indicators='Yes',
                 use_weather_file_snow_indicators='Yes'):
    """
    Create and configure a RunPeriod object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add RunPeriod to.
    name : str, optional
        Run period name. Default 'Run Period 1'.
    begin_month : int, optional
        Begin month. Default 1.
    begin_day_of_month : int, optional
        Begin day. Default 1.
    end_month : int, optional
        End month. Default 12.
    end_day_of_month : int, optional
        End day. Default 31.
    use_weather_file_holidays_and_special_days : str, optional
        Use weather file holidays. Default 'Yes'.
    use_weather_file_daylight_saving_period : str, optional
        Use daylight saving period. Default 'Yes'.
    apply_weekend_holiday_rule : str, optional
        Apply weekend holiday rule. Default 'No'.
    use_weather_file_rain_indicators : str, optional
        Use rain indicators. Default 'Yes'.
    use_weather_file_snow_indicators : str, optional
        Use snow indicators. Default 'Yes'.
    
    Returns
    -------
    idf object
        RunPeriod object with configured attributes.
    """
    RunPeriod = idf.newidfobject('RunPeriod')
    RunPeriod.Name = name
    RunPeriod.Begin_Month = begin_month
    RunPeriod.Begin_Day_of_Month = begin_day_of_month
    RunPeriod.End_Month = end_month
    RunPeriod.End_Day_of_Month = end_day_of_month
    RunPeriod.Use_Weather_File_Holidays_and_Special_Days = use_weather_file_holidays_and_special_days
    RunPeriod.Use_Weather_File_Daylight_Saving_Period = use_weather_file_daylight_saving_period
    RunPeriod.Apply_Weekend_Holiday_Rule = apply_weekend_holiday_rule
    RunPeriod.Use_Weather_File_Rain_Indicators = use_weather_file_rain_indicators
    RunPeriod.Use_Weather_File_Snow_Indicators = use_weather_file_snow_indicators
    
    return RunPeriod


def ground_temperature_building_surface(idf,
                                          jan=17.75, feb=17.48, mar=17.46, apr=19.03,
                                          may=19.37, jun=19.44, jul=21.02, aug=21.31,
                                          sep=21.32, oct=21.29, nov=19.69, dec=19.36):
    """
    Create and configure a Site:GroundTemperature:BuildingSurface object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add the ground temperature object to.
    jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec : float, optional
        Monthly ground temperatures in Celsius. Default values provided.
    
    Returns
    -------
    idf object
        Site:GroundTemperature:BuildingSurface object with configured attributes.
    """
    GroundTemperatureBuildingSurface = idf.newidfobject('Site:GroundTemperature:BuildingSurface')
    GroundTemperatureBuildingSurface.January_Ground_Temperature = jan
    GroundTemperatureBuildingSurface.February_Ground_Temperature = feb
    GroundTemperatureBuildingSurface.March_Ground_Temperature = mar
    GroundTemperatureBuildingSurface.April_Ground_Temperature = apr
    GroundTemperatureBuildingSurface.May_Ground_Temperature = may
    GroundTemperatureBuildingSurface.June_Ground_Temperature = jun
    GroundTemperatureBuildingSurface.July_Ground_Temperature = jul
    GroundTemperatureBuildingSurface.August_Ground_Temperature = aug
    GroundTemperatureBuildingSurface.September_Ground_Temperature = sep
    GroundTemperatureBuildingSurface.October_Ground_Temperature = oct
    GroundTemperatureBuildingSurface.November_Ground_Temperature = nov
    GroundTemperatureBuildingSurface.December_Ground_Temperature = dec
    
    return GroundTemperatureBuildingSurface


def schedule_type_limits(idf, name, lower_limit='', upper_limit='', numeric_type='', unit_type=''):
    """
    Create and configure a ScheduleTypeLimits object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add ScheduleTypeLimits to.
    name : str
        Schedule type limits name.
    lower_limit : str or int or float, optional
        Lower limit value. Default ''.
    upper_limit : str or int or float, optional
        Upper limit value. Default ''.
    numeric_type : str, optional
        Numeric type. Default ''.
    unit_type : str, optional
        Unit type. Default ''.
    
    Returns
    -------
    idf object
        ScheduleTypeLimits object with configured attributes.
    """
    ScheduleTypeLimits = idf.newidfobject('ScheduleTypeLimits')
    ScheduleTypeLimits.Name = name
    ScheduleTypeLimits.Lower_Limit_Value = lower_limit
    ScheduleTypeLimits.Upper_Limit_Value = upper_limit
    ScheduleTypeLimits.Numeric_Type = numeric_type
    ScheduleTypeLimits.Unit_Type = unit_type
    
    return ScheduleTypeLimits

def schedule_from_profile(idf, profile, name, type_limit):
    ScheduleCompact = idf.newidfobject('Schedule:Compact')
    ScheduleCompact.Name = name
    ScheduleCompact.Schedule_Type_Limits_Name = type_limit
    ScheduleCompact.Field_1 = 'Through: 12/31'
    ScheduleCompact.Field_2 = 'For: AllDays'
    for i, v in enumerate(profile):
        ScheduleCompact[f'Field_{i+3}'] = f'Until: {i+1}:00, {v}'
    
    return

def schedule_heating_nonres(idf, profile_wd, profile_we, name, type_limit):
    ScheduleCompact = idf.newidfobject('Schedule:Compact')
    ScheduleCompact.Name = 'Heating_setpoint_schedule'
    ScheduleCompact.Schedule_Type_Limits_Name = 'Temperature'
    ScheduleCompact.Field_1 = 'Through: 12/31'
    ScheduleCompact.Field_2 = 'For: Weekdays'
    
    for i, v in enumerate(profile_wd):
        ScheduleCompact[f'Field_{i+3}'] = f'Until: {i+1}:00, {v}'
    
    count = i
    ScheduleCompact[f'Field_{count+4}'] = 'For: Weekends AllOtherDays'
    for j, v in enumerate(profile_we):
        ScheduleCompact[f'Field_{count+5}'] = f'Until: {j+1}:00, {v}'
        count += 1
    
    return

def activity_schedule(idf, value, name, type_limit):
    ScheduleCompact = idf.newidfobject('Schedule:Compact')
    ScheduleCompact.Name = name
    ScheduleCompact.Schedule_Type_Limits_Name = type_limit
    ScheduleCompact.Field_1 = 'Through: 12/31'
    ScheduleCompact.Field_2 = 'For: AllDays'
    ScheduleCompact.Field_3 = 'Until: 24:00'
    ScheduleCompact.Field_4 = value
    return

def heat_supply_schedule(idf, value, name, type_limit):
    ScheduleCompact = idf.newidfobject('Schedule:Compact')
    ScheduleCompact.Name = name
    ScheduleCompact.Schedule_Type_Limits_Name = type_limit
    ScheduleCompact.Field_1 = 'Through: 12/31'
    ScheduleCompact.Field_2 = 'For: AllDays'
    ScheduleCompact.Field_3 = 'Until: 24:00'
    ScheduleCompact.Field_4 = value
    return

def active_summer_schedule(idf):
    ScheduleCompact = idf.newidfobject('Schedule:Compact')
    ScheduleCompact.Name = 'Active_summer'
    ScheduleCompact.Schedule_Type_Limits_Name = 'Fraction'
    ScheduleCompact.Field_1 = 'Through: 4/30'
    ScheduleCompact.Field_2 = 'For: AllDays'
    ScheduleCompact.Field_3 = 'Until: 24:00'
    ScheduleCompact.Field_4 = 0
    ScheduleCompact.Field_5 = 'Through: 9/30'
    ScheduleCompact.Field_6 = 'For: AllDays'
    ScheduleCompact.Field_7 = 'Until: 24:00'
    ScheduleCompact.Field_8 = 1
    ScheduleCompact.Field_9 = 'Through: 12/31'
    ScheduleCompact.Field_10 = 'For: AllDays'
    ScheduleCompact.Field_11 = 'Until: 24:00'
    ScheduleCompact.Field_12 = 0
    return

def active_winter_schedule(idf):
    ScheduleCompact = idf.newidfobject('Schedule:Compact')
    ScheduleCompact.Name = 'Active_winter'
    ScheduleCompact.Schedule_Type_Limits_Name = 'Fraction'
    ScheduleCompact.Field_1 = 'Through: 4/30'
    ScheduleCompact.Field_2 = 'For: AllDays'
    ScheduleCompact.Field_3 = 'Until: 24:00'
    ScheduleCompact.Field_4 = 1
    ScheduleCompact.Field_5 = 'Through: 9/30'
    ScheduleCompact.Field_6 = 'For: AllDays'
    ScheduleCompact.Field_7 = 'Until: 24:00'
    ScheduleCompact.Field_8 = 0
    ScheduleCompact.Field_9 = 'Through: 12/31'
    ScheduleCompact.Field_10 = 'For: AllDays'
    ScheduleCompact.Field_11 = 'Until: 24:00'
    ScheduleCompact.Field_12 = 1
    return

def always_ON_schedule(idf):
    ScheduleCompact = idf.newidfobject('Schedule:Compact')
    ScheduleCompact.Name = 'Always ON'
    ScheduleCompact.Schedule_Type_Limits_Name = 'Fraction'
    ScheduleCompact.Field_1 = 'Through: 12/31'
    ScheduleCompact.Field_2 = 'For: AllDays'
    ScheduleCompact.Field_3 = 'Until: 24:00'
    ScheduleCompact.Field_4 = 1
    return

def set_thermostat1(idf):
    ScheduleCompact = idf.newidfobject('Schedule:Compact')
    ScheduleCompact.Name = 'Thermostat_control_type'
    ScheduleCompact.Schedule_Type_Limits_Name = 'Control Type'
    ScheduleCompact.Field_1 = 'Through: 4/30'
    ScheduleCompact.Field_2 = 'For: AllDays'
    ScheduleCompact.Field_3 = 'Until: 24:00'
    ScheduleCompact.Field_4 = 1
    ScheduleCompact.Field_5 = 'Through: 9/30'
    ScheduleCompact.Field_6 = 'For: AllDays'
    ScheduleCompact.Field_7 = 'Until: 24:00'
    ScheduleCompact.Field_8 = 2
    ScheduleCompact.Field_9 = 'Through: 12/31'
    ScheduleCompact.Field_10 = 'For: AllDays'
    ScheduleCompact.Field_11 = 'Until: 24:00'
    ScheduleCompact.Field_12 = 1
    return

def set_thermostat2(idf):
    ScheduleCompact = idf.newidfobject('Schedule:Compact')
    ScheduleCompact.Name = 'Thermostat_control_type'
    ScheduleCompact.Schedule_Type_Limits_Name = 'Control Type'
    ScheduleCompact.Field_1 = 'Through: 4/30'
    ScheduleCompact.Field_2 = 'For: AllDays'
    ScheduleCompact.Field_3 = 'Until: 07:00'
    ScheduleCompact.Field_4 = 0
    ScheduleCompact.Field_5 = 'Until: 19:00'
    ScheduleCompact.Field_6 = 1
    ScheduleCompact.Field_7 = 'Until: 24:00'
    ScheduleCompact.Field_8 = 0
    ScheduleCompact.Field_9 = 'Through: 9/30'
    ScheduleCompact.Field_10 = 'For: AllDays'
    ScheduleCompact.Field_11 = 'Until: 07:00'
    ScheduleCompact.Field_12 = 0
    ScheduleCompact.Field_13 = 'Until: 19:00'
    ScheduleCompact.Field_14 = 2
    ScheduleCompact.Field_15 = 'Until: 24:00'
    ScheduleCompact.Field_16 = 0
    ScheduleCompact.Field_17 = 'Through: 12/31'
    ScheduleCompact.Field_18 = 'For: AllDays'
    ScheduleCompact.Field_19 = 'Until: 07:00'
    ScheduleCompact.Field_20 = 0
    ScheduleCompact.Field_21 = 'Until: 19:00'
    ScheduleCompact.Field_22 = 1
    ScheduleCompact.Field_23 = 'Until: 24:00'
    ScheduleCompact.Field_24 = 0
    return


def wall_material(idf, wall_mat_dict):
    wall_mat_list = []
    for i, (k, v) in enumerate(wall_mat_dict.items()):
        if 'air' in v['name'] or v['c'] < 100:
            wall_mat = idf.newidfobject('Material:AirGap')
            wall_mat.Name = f'L{i+1} wall ' + v['name']
            wall_mat.Thermal_Resistance = v['thickness']/100 / v['lambda']
        else:
            wall_mat = idf.newidfobject('Material')
            wall_mat.Name = f'L{i+1} wall ' + v['name']
            wall_mat.Roughness = 'MediumRough'
            wall_mat.Thickness = v['thickness']/100 # [cm] to [m]
            wall_mat.Conductivity = v['lambda']
            wall_mat.Density = v['rho']
            wall_mat.Specific_Heat = v['c']
            wall_mat.Thermal_Absorptance = ''
            wall_mat.Solar_Absorptance = ''
            wall_mat.Visible_Absorptance = ''
    
        wall_mat_list.append(wall_mat)
    
    # E+ construction orders the layers from outside to inside
    wall_mat_list = wall_mat_list[::-1]
    
    wall_const = idf.newidfobject('Construction')
    wall_const.Name = 'wall_const'
    wall_const.Outside_Layer = wall_mat_list[0]['Name']
    for i in range(1, len(wall_mat_list)):
        wall_const[f'Layer_{i+1}'] = wall_mat_list[i]['Name']
    
    return

def roof_material(idf, roof_mat_dict):
    roof_mat_list = []
    for i, (k, v) in enumerate(roof_mat_dict.items()):
        if 'air' in v['name'] or v['c'] < 100:
            roof_mat = idf.newidfobject('Material:AirGap')
            roof_mat.Name = f'L{i+1} roof ' + v['name']
            roof_mat.Thermal_Resistance = v['thickness']/100 / v['lambda']
        else:
            roof_mat = idf.newidfobject('Material')
            roof_mat.Name = f'L{i+1} roof ' + v['name']
            roof_mat.Roughness = 'MediumRough'
            roof_mat.Thickness = v['thickness']/100 # [cm] to [m]
            roof_mat.Conductivity = v['lambda']
            roof_mat.Density = v['rho']
            roof_mat.Specific_Heat = v['c']
            roof_mat.Thermal_Absorptance = ''
            roof_mat.Solar_Absorptance = ''
            roof_mat.Visible_Absorptance = ''
            
        roof_mat_list.append(roof_mat)
    
    # E+ construction orders the layers from outside to inside
    roof_mat_list = roof_mat_list[::-1]
    
    # roof
    roof_const = idf.newidfobject('Construction')
    roof_const.Name = 'roof_const'
    roof_const.Outside_Layer = roof_mat_list[0]['Name']
    for i in range(1, len(roof_mat_list)):
        roof_const[f'Layer_{i+1}'] = roof_mat_list[i]['Name']
    
    return

def floor_material(idf, floor_mat_dict):
    floor_mat_list = []
    for i, (k, v) in enumerate(floor_mat_dict.items()):
        if 'air' in v['name'] or v['c'] < 100:
            floor_mat = idf.newidfobject('Material:AirGap')
            floor_mat.Name = f'L{i+1} floor ' + v['name']
            floor_mat.Thermal_Resistance = v['thickness']/100 / v['lambda']
        else:
            floor_mat = idf.newidfobject('Material')
            floor_mat.Name = f'L{i+1} floor ' + v['name']
            floor_mat.Roughness = 'MediumRough'
            floor_mat.Thickness = v['thickness']/100 # [cm] to [m]
            floor_mat.Conductivity = v['lambda']
            floor_mat.Density = v['rho']
            floor_mat.Specific_Heat = v['c']
            floor_mat.Thermal_Absorptance = ''
            floor_mat.Solar_Absorptance = ''
            floor_mat.Visible_Absorptance = ''
            
        floor_mat_list.append(floor_mat)
    
    # E+ construction orders the layers from outside to inside
    floor_mat_list = floor_mat_list[::-1]
    
    # floor
    floor_const = idf.newidfobject('Construction')
    floor_const.Name = 'floor_const'
    floor_const.Outside_Layer = floor_mat_list[0]['Name']
    for i in range(1, len(floor_mat_list)):
        floor_const[f'Layer_{i+1}'] = floor_mat_list[i]['Name']
    
    return

def window_material(idf, window_u_value):

    window_mat = idf.newidfobject('WindowMaterial:SimpleGlazingSystem')
    window_mat.Name = 'window_mat'
    window_mat.UFactor = window_u_value
    window_mat.Solar_Heat_Gain_Coefficient = 0.58
    window_mat.Visible_Transmittance = 0.57
    
    # Constructions (with NoMass materials)
    window_const = idf.newidfobject('Construction')
    window_const.Name = 'window_const'
    window_const.Outside_Layer = 'window_mat'
    return


def global_geometry_rules(idf,
                            starting_vertex_position='UpperLeftCorner',
                            vertex_entry_direction='Counterclockwise',
                            coordinate_system='Relative',
                            daylighting_reference_point_coordinate_system='',
                            rectangular_surface_coordinate_system=''):
    """
    Create and configure a GlobalGeometryRules object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add GlobalGeometryRules to.
    starting_vertex_position : str, optional
        Starting vertex position. Default 'UpperLeftCorner'.
    vertex_entry_direction : str, optional
        Vertex entry direction. Default 'Counterclockwise'.
    coordinate_system : str, optional
        Coordinate system. Default 'Relative'.
    daylighting_reference_point_coordinate_system : str, optional
        Daylighting reference point coordinate system. Default ''.
    rectangular_surface_coordinate_system : str, optional
        Rectangular surface coordinate system. Default ''.
    
    Returns
    -------
    idf object
        GlobalGeometryRules object with configured attributes.
    """
    GlobalGeometryRules = idf.newidfobject('GlobalGeometryRules')
    GlobalGeometryRules.Starting_Vertex_Position = starting_vertex_position
    GlobalGeometryRules.Vertex_Entry_Direction = vertex_entry_direction
    GlobalGeometryRules.Coordinate_System = coordinate_system
    GlobalGeometryRules.Daylighting_Reference_Point_Coordinate_System = daylighting_reference_point_coordinate_system
    GlobalGeometryRules.Rectangular_Surface_Coordinate_System = rectangular_surface_coordinate_system
    
    return GlobalGeometryRules


def zone(idf,
           name='Zone1',
           direction_of_relative_north='',
           x_origin='',
           y_origin='',
           z_origin='',
           zone_type=1,
           multiplier=1,
           ceiling_height='autocalculate',
           volume='autocalculate',
           floor_area='autocalculate',
           zone_inside_convection_algorithm='',
           zone_outside_convection_algorithm='',
           part_of_total_floor_area=''):
    """
    Create and configure a Zone object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add Zone to.
    name : str, optional
        Zone name. Default 'Zone1'.
    direction_of_relative_north : str, optional
        Direction of relative north. Default ''.
    x_origin : str, optional
        X origin. Default ''.
    y_origin : str, optional
        Y origin. Default ''.
    z_origin : str, optional
        Z origin. Default ''.
    zone_type : int, optional
        Zone type. Default 1.
    multiplier : int, optional
        Multiplier. Default 1.
    ceiling_height : str, optional
        Ceiling height. Default 'autocalculate'.
    volume : str, optional
        Volume. Default 'autocalculate'.
    floor_area : str, optional
        Floor area. Default 'autocalculate'.
    zone_inside_convection_algorithm : str, optional
        Zone inside convection algorithm. Default ''.
    zone_outside_convection_algorithm : str, optional
        Zone outside convection algorithm. Default ''.
    part_of_total_floor_area : str, optional
        Part of total floor area. Default ''.
    
    Returns
    -------
    idf object
        Zone object with configured attributes.
    """
    Zone = idf.newidfobject('Zone')
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

def roof_surface(idf, Btop_coords_CCW):
    Roof = idf.newidfobject('BUILDINGSURFACE:DETAILED')
    Roof.Name = 'Roof'
    Roof.Surface_Type = 'Roof'
    Roof.Construction_Name = 'roof_const'
    Roof.Zone_Name = 'Zone1'
    Roof.Space_Name = ''
    Roof.Outside_Boundary_Condition = 'Outdoors'
    Roof.Outside_Boundary_Condition_Object = ''
    Roof.Sun_Exposure = 'SunExposed'
    Roof.Wind_Exposure = 'WindExposed'
    Roof.View_Factor_to_Ground = 'autocalculate'
    Roof.Number_of_Vertices = Btop_coords_CCW.shape[0]
    for i, point in enumerate(Btop_coords_CCW):
        NO = i+1
        Roof[f'Vertex_{NO}_Xcoordinate'] = point[0]
        Roof[f'Vertex_{NO}_Ycoordinate'] = point[1]
        Roof[f'Vertex_{NO}_Zcoordinate'] = point[2]
    return

def floor_surface(idf, floor_coords_CW):
    Floor = idf.newidfobject('BUILDINGSURFACE:DETAILED')
    Floor.Name = 'Floor'
    Floor.Surface_Type = 'Floor'
    Floor.Construction_Name = 'floor_const'
    Floor.Zone_Name = 'Zone1'
    Floor.Space_Name = ''
    Floor.Outside_Boundary_Condition = 'Ground'
    Floor.Outside_Boundary_Condition_Object = ''
    Floor.Sun_Exposure = 'NoSun'
    Floor.Wind_Exposure = 'NoWind'
    Floor.View_Factor_to_Ground = 'autocalculate'
    Floor.Number_of_Vertices = floor_coords_CW.shape[0]
    
    # Surfaces of Floor and Roof need to have opposite tilt angles i.e. 0,180. Reversing the vertices order solves this.
    for i, point in enumerate(floor_coords_CW):
        NO = i+1
        Floor[f'Vertex_{NO}_Xcoordinate'] = point[0]
        Floor[f'Vertex_{NO}_Ycoordinate'] = point[1]
        Floor[f'Vertex_{NO}_Zcoordinate'] = point[2]
    
    return

def wall_surface(idf, Btop_coords_CCW):
    No_of_walls = Btop_coords_CCW.shape[0]
    
    # Add first element to the end to close the polygon
    Btop_coords_extended = np.vstack((Btop_coords_CCW, Btop_coords_CCW[0,:]))
    wall_dict = {}
    for i in range(No_of_walls):
        Wall = idf.newidfobject('BUILDINGSURFACE:DETAILED')
        Wall.Name = f'Wall_{i}'
        Wall.Surface_Type = 'Wall'
        Wall.Construction_Name = 'wall_const'
        Wall.Zone_Name = 'Zone1'
        Wall.Space_Name = ''
        Wall.Outside_Boundary_Condition = 'Outdoors'
        Wall.Outside_Boundary_Condition_Object = ''
        Wall.Sun_Exposure = 'SunExposed'
        Wall.Wind_Exposure = 'WindExposed'
        Wall.View_Factor_to_Ground = 'autocalculate'
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
            Wall[f'Vertex_{NO}_Xcoordinate'] = wall_vert_sorted[w, 0]
            Wall[f'Vertex_{NO}_Ycoordinate'] = wall_vert_sorted[w, 1]
            Wall[f'Vertex_{NO}_Zcoordinate'] = wall_vert_sorted[w, 2]
        
        wall_dict[Wall.Name] = wall_vert_sorted
    
    return wall_dict


def window_surface(idf, wall_dict, WWR):
    # Assumption: each wall contains a window
    No_of_windows = len(wall_dict)
    
    window_dict = {}
    for i in range(No_of_windows):
        Window = idf.newidfobject('FENESTRATIONSURFACE:DETAILED')
        Window.Name = f'Window_{i}'
        Window.Surface_Type = 'Window'
        Window.Construction_Name = 'window_const'
        Window.Building_Surface_Name = f'Wall_{i}'
        Window.Outside_Boundary_Condition_Object = ''
        Window.View_Factor_to_Ground = 'autocalculate'
        Window.Number_of_Vertices = 4
        
        # Note: vertices should be sorted that already happened in Wall Obj definition
        # window_vert = generate_window_vertices(wall_dict_for_win[f'Wall_{i}'], WWR)
        
        window_vert_sorted = generate_window_vertices(wall_dict[f'Wall_{i}'], WWR)
    
    
        for w in range(Window.Number_of_Vertices):
            NO = w+1 
            Window[f'Vertex_{NO}_Xcoordinate'] = window_vert_sorted[w, 0]
            Window[f'Vertex_{NO}_Ycoordinate'] = window_vert_sorted[w, 1]
            Window[f'Vertex_{NO}_Zcoordinate'] = window_vert_sorted[w, 2]
        
        window_dict[Window.Name] = window_vert_sorted
    
    return


def generate_window_vertices(wall_vertices, WWR):

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




def space(idf,
            name='Space1',
            zone_name='Zone1',
            ceiling_height='',
            volume='',
            floor_area='',
            space_type='',
            tag_1='',
            tag_2='',
            tag_3=''):
    """
    Create and configure a Space object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add Space to.
    name : str, optional
        Space name. Default 'Space1'.
    zone_name : str, optional
        Zone name. Default 'Zone1'.
    ceiling_height : str, optional
        Ceiling height. Default ''.
    volume : str, optional
        Volume. Default ''.
    floor_area : str, optional
        Floor area. Default ''.
    space_type : str, optional
        Space type. Default ''.
    tag_1 : str, optional
        Tag 1. Default ''.
    tag_2 : str, optional
        Tag 2. Default ''.
    tag_3 : str, optional
        Tag 3. Default ''.
    
    Returns
    -------
    idf object
        Space object with configured attributes.
    """
    Space = idf.newidfobject('Space')
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


def space_list(idf, name='Space_list1', space_names=None):
    """
    Create and configure a SpaceList object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add SpaceList to.
    name : str, optional
        SpaceList name. Default 'Space_list1'.
    space_names : list of str, optional
        List of space names to include. Default ['Space1'].
    
    Returns
    -------
    idf object
        SpaceList object with configured attributes.
    """
    if space_names is None:
        space_names = ['Space1']
    
    SpaceList = idf.newidfobject('SpaceList')
    SpaceList.Name = name
    
    for i, space_name in enumerate(space_names, 1):
        SpaceList[f'Space_{i}_Name'] = space_name
    
    return SpaceList


def people(idf,
             name='People1',
             zone_or_zonelist_or_space_or_spacelist_name='Zone1',
             number_of_people_schedule_name='Occupancy_schedule',
             people_per_floor_area='',
             activity_level_schedule_name='Activity_schedule'):
    """
    Create and configure a People object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add People to.
    name : str, optional
        People object name. Default 'People1'.
    zone_or_zonelist_or_space_or_spacelist_name : str, optional
        Zone/Space name. Default 'Zone1'.
    number_of_people_schedule_name : str, optional
        Schedule name for occupancy. Default 'Occupancy_schedule'.
    people_per_floor_area : float, optional
        People per floor area. Default 0.0.
    activity_level_schedule_name : str, optional
        Activity level schedule name. Default 'Activity_schedule'.
    
    Returns
    -------
    idf object
        People object with configured attributes.
    """
    People = idf.newidfobject('People')
    People.Name = name
    People.Zone_or_ZoneList_or_Space_or_SpaceList_Name = zone_or_zonelist_or_space_or_spacelist_name
    People.Number_of_People_Schedule_Name = number_of_people_schedule_name
    People.Number_of_People_Calculation_Method = 'People/Area'
    People.Number_of_People = ''
    People.People_per_Floor_Area = people_per_floor_area
    People.Floor_Area_per_Person = ''
    People.Fraction_Radiant = ''
    People.Sensible_Heat_Fraction = ''
    People.Activity_Level_Schedule_Name = activity_level_schedule_name
    People.Carbon_Dioxide_Generation_Rate = ''
    People.Enable_ASHRAE_55_Comfort_Warnings = ''
    People.Mean_Radiant_Temperature_Calculation_Type = ''
    People.Surface_NameAngle_Factor_List_Name = ''
    People.Work_Efficiency_Schedule_Name = ''
    People.Clothing_Insulation_Calculation_Method = ''
    People.Clothing_Insulation_Calculation_Method_Schedule_Name = ''
    People.Clothing_Insulation_Schedule_Name = ''
    People.Air_Velocity_Schedule_Name = ''
    People.Thermal_Comfort_Model_1_Type = ''
    People.Thermal_Comfort_Model_2_Type = ''
    People.Thermal_Comfort_Model_3_Type = ''
    People.Thermal_Comfort_Model_4_Type = ''
    People.Thermal_Comfort_Model_5_Type = ''
    People.Thermal_Comfort_Model_6_Type = ''
    People.Thermal_Comfort_Model_7_Type = ''
    People.Ankle_Level_Air_Velocity_Schedule_Name = ''
    People.Cold_Stress_Temperature_Threshold = ''
    People.Heat_Stress_Temperature_Threshold = ''
    
    return People


def lights(idf,
             name='Lights1',
             zone_or_zonelist_or_space_or_spacelist_name='Zone1',
             schedule_name='Lights_schedule',
             watts_per_floor_area=0.0):
    """
    Create and configure a Lights object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add Lights to.
    name : str, optional
        Lights object name. Default 'Lights1'.
    zone_or_zonelist_or_space_or_spacelist_name : str, optional
        Zone/Space name. Default 'Zone1'.
    schedule_name : str, optional
        Schedule name. Default 'Lights_schedule'.
    watts_per_floor_area : float, optional
        Watts per floor area. Default 0.0.
    
    Returns
    -------
    idf object
        Lights object with configured attributes.
    """
    Lights = idf.newidfobject('Lights')
    Lights.Name = name
    Lights.Zone_or_ZoneList_or_Space_or_SpaceList_Name = zone_or_zonelist_or_space_or_spacelist_name
    Lights.Schedule_Name = schedule_name
    Lights.Design_Level_Calculation_Method = 'Watts/Area'
    Lights.Lighting_Level = ''
    Lights.Watts_per_Floor_Area = watts_per_floor_area
    Lights.Watts_per_Person = ''
    Lights.Return_Air_Fraction = ''
    Lights.Fraction_Radiant = ''
    Lights.Fraction_Visible = ''
    Lights.Fraction_Replaceable = ''
    Lights.EndUse_Subcategory = ''
    Lights.Return_Air_Fraction_Calculated_from_Plenum_Temperature = ''
    Lights.Return_Air_Fraction_Function_of_Plenum_Temperature_Coefficient_1 = ''
    Lights.Return_Air_Fraction_Function_of_Plenum_Temperature_Coefficient_2 = ''
    Lights.Return_Air_Heat_Gain_Node_Name = ''
    Lights.Exhaust_Air_Heat_Gain_Node_Name = ''
    
    return Lights


def electric_equipment(idf,
                         name='Equipment',
                         zone_or_zonelist_or_space_or_spacelist_name='Zone1',
                         schedule_name='Equipment_schedule',
                         watts_per_floor_area=0.0):
    """
    Create and configure an ElectricEquipment object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add ElectricEquipment to.
    name : str, optional
        Equipment name. Default 'Equipment'.
    zone_or_zonelist_or_space_or_spacelist_name : str, optional
        Zone/Space name. Default 'Zone1'.
    schedule_name : str, optional
        Schedule name. Default 'Equipment_schedule'.
    watts_per_floor_area : float, optional
        Watts per floor area. Default 0.0.
    
    Returns
    -------
    idf object
        ElectricEquipment object with configured attributes.
    """
    Equipment = idf.newidfobject('ElectricEquipment')
    Equipment.Name = name
    Equipment.Zone_or_ZoneList_or_Space_or_SpaceList_Name = zone_or_zonelist_or_space_or_spacelist_name
    Equipment.Schedule_Name = schedule_name
    Equipment.Design_Level_Calculation_Method = 'Watts/Area'
    Equipment.Design_Level = ''
    Equipment.Watts_per_Floor_Area = watts_per_floor_area
    Equipment.Watts_per_Person = ''
    Equipment.Fraction_Latent = ''
    Equipment.Fraction_Radiant = ''
    Equipment.Fraction_Lost = ''
    Equipment.EndUse_Subcategory = ''
    
    return Equipment


def zone_ventilation_design_flow_rate(idf,
                                        name='Ventilation',
                                        zone_or_zonelist_or_space_or_spacelist_name='Zone1',
                                        schedule_name='Ventilation_schedule',
                                        air_changes_per_hour=1.0):
    """
    Create and configure a ZoneVentilation:DesignFlowRate object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add ZoneVentilation to.
    name : str, optional
        Ventilation name. Default 'Ventilation'.
    zone_or_zonelist_or_space_or_spacelist_name : str, optional
        Zone/Space name. Default 'Zone1'.
    schedule_name : str, optional
        Schedule name. Default 'Ventilation_schedule'.
    air_changes_per_hour : float, optional
        Air changes per hour. Default 1.0.
    
    Returns
    -------
    idf object
        ZoneVentilation:DesignFlowRate object with configured attributes.
    """
    ZoneVentilation = idf.newidfobject('ZoneVentilation:DesignFlowRate')
    ZoneVentilation.Name = name
    ZoneVentilation.Zone_or_ZoneList_or_Space_or_SpaceList_Name = zone_or_zonelist_or_space_or_spacelist_name
    ZoneVentilation.Schedule_Name = schedule_name
    ZoneVentilation.Design_Flow_Rate_Calculation_Method = 'AirChanges/Hour'
    ZoneVentilation.Design_Flow_Rate = ''
    ZoneVentilation.Flow_Rate_per_Floor_Area = ''
    ZoneVentilation.Flow_Rate_per_Person = ''
    ZoneVentilation.Air_Changes_per_Hour = air_changes_per_hour
    ZoneVentilation.Ventilation_Type = ''
    ZoneVentilation.Fan_Pressure_Rise = ''
    ZoneVentilation.Fan_Total_Efficiency = ''
    ZoneVentilation.Constant_Term_Coefficient = ''
    ZoneVentilation.Temperature_Term_Coefficient = ''
    ZoneVentilation.Velocity_Term_Coefficient = ''
    ZoneVentilation.Velocity_Squared_Term_Coefficient = ''
    ZoneVentilation.Minimum_Indoor_Temperature = ''
    ZoneVentilation.Minimum_Indoor_Temperature_Schedule_Name = ''
    ZoneVentilation.Maximum_Indoor_Temperature = ''
    ZoneVentilation.Maximum_Indoor_Temperature_Schedule_Name = ''
    ZoneVentilation.Delta_Temperature = ''
    ZoneVentilation.Delta_Temperature_Schedule_Name = ''
    ZoneVentilation.Minimum_Outdoor_Temperature = ''
    ZoneVentilation.Minimum_Outdoor_Temperature_Schedule_Name = ''
    ZoneVentilation.Maximum_Outdoor_Temperature = ''
    ZoneVentilation.Maximum_Outdoor_Temperature_Schedule_Name = ''
    ZoneVentilation.Maximum_Wind_Speed = ''
    ZoneVentilation.Density_Basis = ''
    
    return ZoneVentilation


def zone_control_thermostat(idf,
                              name='Heating_thermostat',
                              zone_or_zonelist_name='Zone1',
                              control_type_schedule_name='Thermostat_control_type'):
    """
    Create and configure a ZoneControl:Thermostat object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add ZoneControl:Thermostat to.
    name : str, optional
        Thermostat name. Default 'Heating_thermostat'.
    zone_or_zonelist_name : str, optional
        Zone name. Default 'Zone1'.
    control_type_schedule_name : str, optional
        Control type schedule name. Default 'Thermostat_control_type'.
    
    Returns
    -------
    idf object
        ZoneControl:Thermostat object with configured attributes.
    """
    ZoneControlThermostat = idf.newidfobject('ZoneControl:Thermostat')
    ZoneControlThermostat.Name = name
    ZoneControlThermostat.Zone_or_ZoneList_Name = zone_or_zonelist_name
    ZoneControlThermostat.Control_Type_Schedule_Name = control_type_schedule_name
    ZoneControlThermostat.Control_1_Object_Type = 'ThermostatSetpoint:SingleHeating'
    ZoneControlThermostat.Control_1_Name = 'Heating_thermostat'
    ZoneControlThermostat.Control_2_Object_Type = 'ThermostatSetpoint:SingleCooling'
    ZoneControlThermostat.Control_2_Name = 'Cooling_thermostat'
    ZoneControlThermostat.Control_3_Object_Type = ''
    ZoneControlThermostat.Control_3_Name = ''
    ZoneControlThermostat.Control_4_Object_Type = ''
    ZoneControlThermostat.Control_4_Name = ''
    ZoneControlThermostat.Temperature_Difference_Between_Cutout_And_Setpoint = ''
    
    return ZoneControlThermostat


def thermostat_setpoint_single_heating(idf,
                                         name='Heating_thermostat',
                                         setpoint_temperature_schedule_name='Heating_setpoint_schedule'):
    """
    Create and configure a ThermostatSetpoint:SingleHeating object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add heating thermostat to.
    name : str, optional
        Name. Default 'Heating_thermostat'.
    setpoint_temperature_schedule_name : str, optional
        Schedule name. Default 'Heating_setpoint_schedule'.
    
    Returns
    -------
    idf object
        ThermostatSetpoint:SingleHeating object with configured attributes.
    """
    ThermostatSetpoint = idf.newidfobject('ThermostatSetpoint:SingleHeating')
    ThermostatSetpoint.Name = name
    ThermostatSetpoint.Setpoint_Temperature_Schedule_Name = setpoint_temperature_schedule_name
    
    return ThermostatSetpoint


def thermostat_setpoint_single_cooling(idf,
                                         name='Cooling_thermostat',
                                         setpoint_temperature_schedule_name='Cooling_setpoint_schedule'):
    """
    Create and configure a ThermostatSetpoint:SingleCooling object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add cooling thermostat to.
    name : str, optional
        Name. Default 'Cooling_thermostat'.
    setpoint_temperature_schedule_name : str, optional
        Schedule name. Default 'Cooling_setpoint_schedule'.
    
    Returns
    -------
    idf object
        ThermostatSetpoint:SingleCooling object with configured attributes.
    """
    ThermostatSetpoint = idf.newidfobject('ThermostatSetpoint:SingleCooling')
    ThermostatSetpoint.Name = name
    ThermostatSetpoint.Setpoint_Temperature_Schedule_Name = setpoint_temperature_schedule_name
    
    return ThermostatSetpoint


def zone_hvac_ideal_loads_air_system(idf, name='HVAC1', availability_schedule_name='Always ON'):
    """
    Create and configure a ZoneHVAC:IdealLoadsAirSystem object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add HVAC system to.
    name : str, optional
        HVAC system name. Default 'HVAC1'.
    availability_schedule_name : str, optional
        Availability schedule name. Default 'Always ON'.
    
    Returns
    -------
    idf object
        ZoneHVAC:IdealLoadsAirSystem object with configured attributes.
    """
    ZoneHVAC = idf.newidfobject('ZoneHVAC:IdealLoadsAirSystem')
    ZoneHVAC.Name = name
    ZoneHVAC.Availability_Schedule_Name = availability_schedule_name
    ZoneHVAC.Zone_Supply_Air_Node_Name = 'Zone_supply_inlet'
    ZoneHVAC.Zone_Exhaust_Air_Node_Name = ''
    ZoneHVAC.System_Inlet_Air_Node_Name = ''
    ZoneHVAC.Maximum_Heating_Supply_Air_Temperature = ''
    ZoneHVAC.Minimum_Cooling_Supply_Air_Temperature = ''
    ZoneHVAC.Maximum_Heating_Supply_Air_Humidity_Ratio = ''
    ZoneHVAC.Minimum_Cooling_Supply_Air_Humidity_Ratio = ''
    ZoneHVAC.Heating_Limit = ''
    ZoneHVAC.Maximum_Heating_Air_Flow_Rate = ''
    ZoneHVAC.Maximum_Sensible_Heating_Capacity = ''
    ZoneHVAC.Cooling_Limit = ''
    ZoneHVAC.Maximum_Cooling_Air_Flow_Rate = ''
    ZoneHVAC.Maximum_Total_Cooling_Capacity = ''
    ZoneHVAC.Heating_Availability_Schedule_Name = ''
    ZoneHVAC.Cooling_Availability_Schedule_Name = ''
    ZoneHVAC.Dehumidification_Control_Type = ''
    ZoneHVAC.Cooling_Sensible_Heat_Ratio = ''
    ZoneHVAC.Humidification_Control_Type = ''
    ZoneHVAC.Design_Specification_Outdoor_Air_Object_Name = ''
    ZoneHVAC.Outdoor_Air_Inlet_Node_Name = ''
    ZoneHVAC.Demand_Controlled_Ventilation_Type = ''
    ZoneHVAC.Outdoor_Air_Economizer_Type = ''
    ZoneHVAC.Heat_Recovery_Type = ''
    ZoneHVAC.Sensible_Heat_Recovery_Effectiveness = ''
    ZoneHVAC.Latent_Heat_Recovery_Effectiveness = ''
    ZoneHVAC.Design_Specification_ZoneHVAC_Sizing_Object_Name = ''

    return ZoneHVAC


def zone_hvac_equipment_list(idf, name='Zone_equipment_list'):
    """
    Create and configure a ZoneHVAC:EquipmentList object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add equipment list to.
    name : str, optional
        Equipment list name. Default 'Zone_equipment_list'.
    
    Returns
    -------
    idf object
        ZoneHVAC:EquipmentList object with configured attributes.
    """
    EquipmentList = idf.newidfobject('ZoneHVAC:EquipmentList')
    EquipmentList.Name = name
    EquipmentList.Load_Distribution_Scheme = 'SequentialLoad'
    EquipmentList.Zone_Equipment_1_Object_Type = 'ZoneHVAC:IdealLoadsAirSystem'
    EquipmentList.Zone_Equipment_1_Name = 'HVAC1'
    EquipmentList.Zone_Equipment_1_Cooling_Sequence = 1
    EquipmentList.Zone_Equipment_1_Heating_or_NoLoad_Sequence = 1
    EquipmentList.Zone_Equipment_1_Sequential_Cooling_Fraction_Schedule_Name = ''
    EquipmentList.Zone_Equipment_1_Sequential_Heating_Fraction_Schedule_Name = ''
    
    return EquipmentList


def zone_hvac_equipment_connections(idf, zone_name='Zone1'):
    """
    Create and configure a ZoneHVAC:EquipmentConnections object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add equipment connections to.
    zone_name : str, optional
        Zone name. Default 'Zone1'.
    
    Returns
    -------
    idf object
        ZoneHVAC:EquipmentConnections object with configured attributes.
    """
    EquipmentConnections = idf.newidfobject('ZoneHVAC:EquipmentConnections')
    EquipmentConnections.Zone_Name = zone_name
    EquipmentConnections.Zone_Conditioning_Equipment_List_Name = 'Zone_equipment_list'
    EquipmentConnections.Zone_Air_Inlet_Node_or_NodeList_Name = 'Zone_supply_inlet'
    EquipmentConnections.Zone_Air_Exhaust_Node_or_NodeList_Name = ''
    EquipmentConnections.Zone_Air_Node_Name = 'Zone_air_node'
    EquipmentConnections.Zone_Return_Air_Node_or_NodeList_Name = 'Zone_return_air_node'
    EquipmentConnections.Zone_Return_Air_Node_1_Flow_Rate_Fraction_Schedule_Name = ''
    EquipmentConnections.Zone_Return_Air_Node_1_Flow_Rate_Basis_Node_or_NodeList_Name = ''
    
    return EquipmentConnections


def output_variable_dictionary(idf, key_field='IDF', sort_option='Unsorted'):
    """
    Create and configure an Output:VariableDictionary object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add output variable dictionary to.
    key_field : str, optional
        Key field. Default 'IDF'.
    sort_option : str, optional
        Sort option. Default 'Unsorted'.
    
    Returns
    -------
    idf object
        Output:VariableDictionary object with configured attributes.
    """
    OutputVariableDictionary = idf.newidfobject('Output:VariableDictionary')
    OutputVariableDictionary.Key_Field = key_field
    OutputVariableDictionary.Sort_Option = sort_option
    
    return OutputVariableDictionary


def output_variable(idf, variable_name, reporting_frequency='Timestep'):
    """
    Create and configure an Output:Variable object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add output variable to.
    variable_name : str
        Variable name to output.
    reporting_frequency : str, optional
        Reporting frequency. Default 'Timestep'.
    
    Returns
    -------
    idf object
        Output:Variable object with configured attributes.
    """
    OutputVariable = idf.newidfobject('Output:Variable')
    OutputVariable.Variable_Name = variable_name
    OutputVariable.Reporting_Frequency = reporting_frequency
    
    return OutputVariable


def output_meter(idf, key_name='Electricity:Facility', reporting_frequency='Timestep'):
    """
    Create and configure an Output:Meter object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add output meter to.
    key_name : str, optional
        Meter key name. Default 'Electricity:Facility'.
    reporting_frequency : str, optional
        Reporting frequency. Default 'Timestep'.
    
    Returns
    -------
    idf object
        Output:Meter object with configured attributes.
    """
    OutputMeter = idf.newidfobject('Output:Meter')
    OutputMeter.Key_Name = key_name
    OutputMeter.Reporting_Frequency = reporting_frequency
    
    return OutputMeter


def output_table_summary_reports(idf, report_names=None):
    """
    Create and configure an Output:Table:SummaryReports object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add summary reports to.
    report_names : list of str, optional
        Report names to include. Default ['AllSummary'].
    
    Returns
    -------
    idf object
        Output:Table:SummaryReports object with configured attributes.
    """
    if report_names is None:
        report_names = ['AllSummary']
    
    OutputTableSummaryReports = idf.newidfobject('Output:Table:SummaryReports')
    
    for i, report_name in enumerate(report_names, 1):
        OutputTableSummaryReports[f'Report_{i}_Name'] = report_name
    
    return OutputTableSummaryReports


def output_control_files(idf,
                           output_csv='Yes',
                           output_rdd='Yes',
                           output_tabular='Yes'):
    """
    Create and configure an OutputControl:Files object for EnergyPlus IDF.
    
    Parameters
    ----------
    idf : IDF object
        The IDF model object to add output control files to.
    output_csv : str, optional
        Output CSV. Default 'Yes'.
    output_rdd : str, optional
        Output RDD. Default 'Yes'.
    output_tabular : str, optional
        Output Tabular. Default 'Yes'.
    
    Returns
    -------
    idf object
        OutputControl:Files object with configured attributes.
    """
    OutputControlFiles = idf.newidfobject('OutputControl:Files')
    OutputControlFiles.Output_CSV = output_csv
    OutputControlFiles.Output_MTR = 'No'
    OutputControlFiles.Output_ESO = 'No'
    OutputControlFiles.Output_EIO = 'No'
    OutputControlFiles.Output_Tabular = output_tabular
    OutputControlFiles.Output_SQLite = 'No'
    OutputControlFiles.Output_JSON = 'No'
    OutputControlFiles.Output_AUDIT = 'No'
    OutputControlFiles.Output_Space_Sizing = 'No'
    OutputControlFiles.Output_Zone_Sizing = 'No'
    OutputControlFiles.Output_System_Sizing = 'No'
    OutputControlFiles.Output_DXF = 'No'
    OutputControlFiles.Output_BND = 'No'
    OutputControlFiles.Output_RDD = output_rdd
    OutputControlFiles.Output_MDD = 'No'
    OutputControlFiles.Output_MTD = 'No'
    OutputControlFiles.Output_END = 'No'
    OutputControlFiles.Output_SHD = 'No'
    OutputControlFiles.Output_DFS = 'No'
    OutputControlFiles.Output_GLHE = 'No'
    OutputControlFiles.Output_DelightIn = 'No'
    OutputControlFiles.Output_DelightELdmp = 'No'
    OutputControlFiles.Output_DelightDFdmp = 'No'
    OutputControlFiles.Output_EDD = 'No'
    OutputControlFiles.Output_DBG = 'No'
    OutputControlFiles.Output_PerfLog = 'No'
    OutputControlFiles.Output_SLN = 'No'
    OutputControlFiles.Output_SCI = 'No'
    OutputControlFiles.Output_WRL = 'No'
    OutputControlFiles.Output_Screen = 'No'
    OutputControlFiles.Output_ExtShd = 'No'
    OutputControlFiles.Output_Tarcog = 'No'
    
    return OutputControlFiles

