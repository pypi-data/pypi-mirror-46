"""
multi-objective optimization of supply systems for the CEA
"""

from __future__ import division
import os
from os import listdir
import pandas as pd
import numpy as np
import json
import cea.config
import cea.globalvar
import cea.inputlocator
from cea.optimization.prices import Prices as Prices
import cea.optimization.distribution.network_opt_main as network_opt
from cea.optimization.preprocessing.preprocessing_main import preproccessing
import cea.optimization.master.evaluation as evaluation
import cea.optimization.supportFn as sFn
from cea.optimization.constants import *
import cea.optimization.master.cost_model as eM
import cea.optimization.slave.cooling_main as coolMain
import cea.optimization.slave.slave_main as sM
import cea.optimization.master.check as cCheck
import cea.technologies.substation as sMain
import cea.optimization.master.summarize_network as nM
from cea.optimization.lca_calculations import lca_calculations
from cea.plots.supply_system.optimization_post_processing.individual_configuration import calc_opex_PV
from cea.technologies.solar.photovoltaic import calc_Cinv_pv
from cea.plots.supply_system.optimization_post_processing.electricity_imports_exports_script import electricity_import_and_exports


__author__ = "Sreepathi Bhargava Krishna"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Sreepathi Bhargava Krishna"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"

GENERATION_NUMBER = 100

# optimization

def individual_evaluation(individual, building_names, total_demand, locator, extra_costs, extra_CO2, extra_primary_energy,
                          solar_features, network_features, gv, config, prices, lca):
    """
    This function evaluates one supply system configuration of the case study.
    :param individual: a list that indicates the supply system configuration
    :type individual: list
    :param building_names: names of all building in the district
    :type building_names: ndarray
    :param locator:
    :param extra_costs: cost of decentralized supply systems
    :param extra_CO2: CO2 emission of decentralized supply systems
    :param extra_primary_energy: Primary energy of decentralized supply systems
    :param solar_features: Energy production potentials of solar technologies, including area of installed panels and annual production
    :type solar_features: dict
    :param network_features: hourly network operating conditions (thermal/pressure losses) and capital costs
    :type network_features: dict
    :param gv:
    :param config:
    :param prices:
    :return:
    """
    individual = evaluation.check_invalid(individual, len(building_names), config)

    # Initialize objective functions costs, CO2 and primary energy
    costs = 0
    CO2 = extra_CO2
    prim = extra_primary_energy
    QUncoveredDesign = 0
    QUncoveredAnnual = 0

    # Create the string representation of the individual
    DHN_barcode, DCN_barcode, DHN_configuration, DCN_configuration = sFn.individual_to_barcode(individual,
                                                                                               building_names)

    # read the total loads from buildings connected to thermal networks
    if DHN_barcode.count("1") == gv.num_tot_buildings:
        network_file_name_heating = "Network_summary_result_all.csv"
        Q_DHNf_W = pd.read_csv(locator.get_optimization_network_all_results_summary('all'), usecols=["Q_DHNf_W"]).values
        Q_heating_max_W = Q_DHNf_W.max()
    elif DHN_barcode.count("1") == 0:
        network_file_name_heating = "Network_summary_result_all.csv"
        Q_heating_max_W = 0
    else:
        # Run the substation and distribution routines
        sMain.substation_main(locator, total_demand, building_names, DHN_configuration, DCN_configuration, Flag=True)

        nM.network_main(locator, total_demand, building_names, config, gv, DHN_barcode)

        network_file_name_heating = "Network_summary_result_" + hex(int(str(DHN_barcode), 2)) + ".csv"
        Q_DHNf_W = pd.read_csv(locator.get_optimization_network_results_summary(DHN_barcode),
                               usecols=["Q_DHNf_W"]).values
        Q_heating_max_W = Q_DHNf_W.max()

    if DCN_barcode.count("1") == gv.num_tot_buildings:
        network_file_name_cooling = "Network_summary_result_all.csv"
        if individual[
                    N_HEAT * 2] == 1:  # if heat recovery is ON, then only need to satisfy cooling load of space cooling and refrigeration
            Q_DCNf_W = pd.read_csv(locator.get_optimization_network_all_results_summary('all'),
                                   usecols=["Q_DCNf_space_cooling_and_refrigeration_W"]).values
        else:
            Q_DCNf_W = pd.read_csv(locator.get_optimization_network_all_results_summary('all'),
                                   usecols=["Q_DCNf_space_cooling_data_center_and_refrigeration_W"]).values
        Q_cooling_max_W = Q_DCNf_W.max()
    elif DCN_barcode.count("1") == 0:
        network_file_name_cooling = "Network_summary_result_none.csv"
        Q_cooling_max_W = 0
    else:
        # Run the substation and distribution routines
        sMain.substation_main(locator, total_demand, building_names, DHN_configuration, DCN_configuration, Flag=True)

        nM.network_main(locator, total_demand, building_names, config, gv, DCN_barcode)

        network_file_name_cooling = "Network_summary_result_" + hex(int(str(DCN_barcode), 2)) + ".csv"

        if individual[
                    N_HEAT * 2] == 1:  # if heat recovery is ON, then only need to satisfy cooling load of space cooling and refrigeration
            Q_DCNf_W = pd.read_csv(locator.get_optimization_network_results_summary(DCN_barcode),
                                   usecols=["Q_DCNf_space_cooling_and_refrigeration_W"]).values
        else:
            Q_DCNf_W = pd.read_csv(locator.get_optimization_network_results_summary(DCN_barcode),
                                   usecols=["Q_DCNf_space_cooling_data_center_and_refrigeration_W"]).values
        Q_cooling_max_W = Q_DCNf_W.max()

    Q_heating_nom_W = Q_heating_max_W * (1 + Q_MARGIN_FOR_NETWORK)
    Q_cooling_nom_W = Q_cooling_max_W * (1 + Q_MARGIN_FOR_NETWORK)

    # Modify the individual with the extra GHP constraint
    try:
        cCheck.GHPCheck(individual, locator, Q_heating_nom_W, gv)
    except:
        print "No GHP constraint check possible \n"

    # Export to context
    individual_number = calc_individual_number(locator)
    master_to_slave_vars = evaluation.calc_master_to_slave_variables(individual, Q_heating_max_W, Q_cooling_max_W,
                                                                     building_names, individual_number, GENERATION_NUMBER)
    master_to_slave_vars.network_data_file_heating = network_file_name_heating
    master_to_slave_vars.network_data_file_cooling = network_file_name_cooling
    master_to_slave_vars.total_buildings = len(building_names)

    if master_to_slave_vars.number_of_buildings_connected_heating > 1:
        if DHN_barcode.count("0") == 0:
            master_to_slave_vars.fNameTotalCSV = locator.get_total_demand()
        else:
            master_to_slave_vars.fNameTotalCSV = os.path.join(locator.get_optimization_network_totals_folder(),
                                                              "Total_%(DHN_barcode)s.csv" % locals())
    else:
        master_to_slave_vars.fNameTotalCSV = locator.get_optimization_substations_total_file(DHN_barcode)

    if master_to_slave_vars.number_of_buildings_connected_cooling > 1:
        if DCN_barcode.count("0") == 0:
            master_to_slave_vars.fNameTotalCSV = locator.get_total_demand()
        else:
            master_to_slave_vars.fNameTotalCSV = os.path.join(locator.get_optimization_network_totals_folder(),
                                                              "Total_%(DCN_barcode)s.csv" % locals())
    else:
        master_to_slave_vars.fNameTotalCSV = locator.get_optimization_substations_total_file(DCN_barcode)

    # slave optimization of heating networks
    if config.optimization.isheating:
        if DHN_barcode.count("1") > 0:
            (slavePrim, slaveCO2, slaveCosts, QUncoveredDesign, QUncoveredAnnual) = sM.slave_main(locator,
                                                                                                  master_to_slave_vars,
                                                                                                  solar_features, gv,
                                                                                                  config, prices)
        else:
            slaveCO2 = 0
            slaveCosts = 0
            slavePrim = 0
    else:
        slaveCO2 = 0
        slaveCosts = 0
        slavePrim = 0

    costs += slaveCosts
    CO2 += slaveCO2
    prim += slavePrim

    # slave optimization of cooling networks
    if gv.ZernezFlag == 1:
        coolCosts, coolCO2, coolPrim = 0, 0, 0
    elif config.optimization.iscooling and DCN_barcode.count("1") > 0:
        reduced_timesteps_flag = config.supply_system_simulation.reduced_timesteps
        (coolCosts, coolCO2, coolPrim) = coolMain.coolingMain(locator, master_to_slave_vars, network_features, gv,
                                                              prices, lca, config, reduced_timesteps_flag)
        # if reduced_timesteps_flag:
        #     # reduced timesteps simulation for a month (May)
        #     coolCosts = coolCosts * (8760/(3624/2880))
        #     coolCO2 = coolCO2 * (8760/(3624/2880))
        #     coolPrim = coolPrim * (8760/(3624/2880))
        #     # FIXME: check results
    else:
        coolCosts, coolCO2, coolPrim = 0, 0, 0

    print "Add extra costs"
    # add costs of disconnected buildings (best configuration)
    (addCosts, addCO2, addPrim) = eM.addCosts(DHN_barcode, DCN_barcode, building_names, locator, master_to_slave_vars,
                                              QUncoveredDesign, QUncoveredAnnual, solar_features, network_features, gv,
                                              config, prices, lca)

    # recalculate the addCosts by substracting the decentralized costs and add back to corresponding supply system
    Cost_diff, CO2_diff, Prim_diff = calc_decentralized_building_costs(config, locator, master_to_slave_vars,
                                                                       DHN_barcode, DCN_barcode, building_names)
    addCosts = addCosts + Cost_diff
    addCO2 = addCO2 + CO2_diff
    addPrim = addPrim + Prim_diff

    # add Capex and Opex of PV
    data_electricity = pd.read_csv(os.path.join(
        locator.get_optimization_slave_electricity_activation_pattern_cooling(individual_number, GENERATION_NUMBER)))

    total_area_for_pv = data_electricity['Area_PV_m2'].max()
    # remove the area installed with solar collectors
    sc_installed_area = 0
    if config.supply_system_simulation.decentralized_systems == 'Single-effect Absorption Chiller':
        for (index, building_name) in zip(DCN_barcode, building_names):
            if index == "0":
                sc_installed_area = sc_installed_area + pd.read_csv(locator.PV_results(building_name))['Area_PV_m2'].max()
    pv_installed_area = total_area_for_pv - sc_installed_area
    Capex_a_PV, Opex_fixed_PV = calc_Cinv_pv(pv_installed_area, locator, config)
    pv_annual_production_kWh = (data_electricity['E_PV_W'].sum()) / 1000

    # electricity calculations
    data_network_electricity = pd.read_csv(os.path.join(
        locator.get_optimization_slave_electricity_activation_pattern_cooling(individual_number, GENERATION_NUMBER)))

    data_cooling = pd.read_csv(
        os.path.join(locator.get_optimization_slave_cooling_activation_pattern(individual_number, GENERATION_NUMBER)))

    total_demand = pd.read_csv(locator.get_total_demand())
    building_names = total_demand.Name.values
    total_electricity_demand_W = data_network_electricity['E_total_req_W']
    E_decentralized_appliances_W = np.zeros(8760)

    for i, name in zip(DCN_barcode, building_names):  # adding the electricity demand from the decentralized buildings
        if i is '0':
            building_demand = pd.read_csv(locator.get_demand_results_folder() + '//' + name + ".csv",
                                          usecols=['E_sys_kWh'])
            E_decentralized_appliances_W += building_demand['E_sys_kWh'] * 1000

    total_electricity_demand_W = total_electricity_demand_W.add(E_decentralized_appliances_W)
    E_for_hot_water_demand_W = np.zeros(8760)

    for i, name in zip(DCN_barcode, building_names):  # adding the electricity demand for hot water from all buildings
        building_demand = pd.read_csv(locator.get_demand_results_folder() + '//' + name + ".csv",
                                      usecols=['E_ww_kWh'])
        E_for_hot_water_demand_W += building_demand['E_ww_kWh'] * 1000

    total_electricity_demand_W = total_electricity_demand_W.add(E_for_hot_water_demand_W)
    # Electricity of Energy Systems
    lca = lca_calculations(locator, config)
    E_VCC_W = data_cooling['Opex_var_VCC'] / lca.ELEC_PRICE
    E_VCC_backup_W = data_cooling['Opex_var_VCC_backup'] / lca.ELEC_PRICE
    E_ACH_W = data_cooling['Opex_var_ACH'] / lca.ELEC_PRICE
    E_CT_W = abs(data_cooling['Opex_var_CT']) / lca.ELEC_PRICE
    total_electricity_demand_W = total_electricity_demand_W.add(E_VCC_W)
    total_electricity_demand_W = total_electricity_demand_W.add(E_VCC_backup_W)
    total_electricity_demand_W = total_electricity_demand_W.add(E_ACH_W)
    total_electricity_demand_W = total_electricity_demand_W.add(E_CT_W)
    E_from_CHP_W = data_network_electricity['E_CHP_to_directload_W'] + data_network_electricity['E_CHP_to_grid_W']
    E_from_PV_W = data_network_electricity['E_PV_to_directload_W'] + data_network_electricity['E_PV_to_grid_W']

    E_CHP_to_directload_W = np.zeros(8760)
    E_CHP_to_grid_W = np.zeros(8760)
    E_PV_to_directload_W = np.zeros(8760)
    E_PV_to_grid_W = np.zeros(8760)
    E_from_grid_W = np.zeros(8760)

    # modify simulation timesteps
    if reduced_timesteps_flag == False:
        start_t = 0
        stop_t = 8760
    else:
        # timesteps in May
        start_t = 2880
        stop_t = 3624
    timesteps = range(start_t, stop_t)

    for hour in timesteps:
        E_hour_W = total_electricity_demand_W[hour]
        if E_hour_W > 0:
            if E_from_PV_W[hour] > E_hour_W:
                E_PV_to_directload_W[hour] = E_hour_W
                E_PV_to_grid_W[hour] = E_from_PV_W[hour] - total_electricity_demand_W[hour]
                E_hour_W = 0
            else:
                E_hour_W = E_hour_W - E_from_PV_W[hour]
                E_PV_to_directload_W[hour] = E_from_PV_W[hour]

            if E_from_CHP_W[hour] > E_hour_W:
                E_CHP_to_directload_W[hour] = E_hour_W
                E_CHP_to_grid_W[hour] = E_from_CHP_W[hour] - E_hour_W
                E_hour_W = 0
            else:
                E_hour_W = E_hour_W - E_from_CHP_W[hour]
                E_CHP_to_directload_W[hour] = E_from_CHP_W[hour]

            E_from_grid_W[hour] = E_hour_W

    date = data_network_electricity.DATE.values

    results = pd.DataFrame({"DATE": date,
                            "E_total_req_W": total_electricity_demand_W,
                            "E_from_grid_W": E_from_grid_W,
                            "E_VCC_W": E_VCC_W,
                            "E_VCC_backup_W": E_VCC_backup_W,
                            "E_ACH_W": E_ACH_W,
                            "E_CT_W": E_CT_W,
                            "E_PV_to_directload_W": E_PV_to_directload_W,
                            "E_CHP_to_directload_W": E_CHP_to_directload_W,
                            "E_CHP_to_grid_W": E_CHP_to_grid_W,
                            "E_PV_to_grid_W": E_PV_to_grid_W,
                            "E_for_hot_water_demand_W": E_for_hot_water_demand_W,
                            "E_decentralized_appliances_W": E_decentralized_appliances_W,
                            "E_total_to_grid_W_negative": - E_PV_to_grid_W - E_CHP_to_grid_W})  # let's keep this negative so it is something exported, we can use it in the graphs of likelihood

    if reduced_timesteps_flag:
        reduced_el_costs = (
                    (results['E_from_grid_W'].sum() + results['E_total_to_grid_W_negative'].sum()) * lca.ELEC_PRICE)
        electricity_costs = reduced_el_costs * (8760 / (stop_t - start_t))
    else:
        electricity_costs = ((results['E_from_grid_W'].sum() + results['E_total_to_grid_W_negative'].sum()) * lca.ELEC_PRICE)

    costs += addCosts + coolCosts + electricity_costs + Capex_a_PV + Opex_fixed_PV # FIXME
    CO2 += addCO2 + coolCO2
    prim += addPrim + coolPrim
    # Converting costs into float64 to avoid longer values
    costs = np.float64(costs)
    CO2 = np.float64(CO2)
    prim = np.float64(prim)

    # add electricity costs corresponding to

    print ('Additional costs = ' + str(addCosts))
    print ('Additional CO2 = ' + str(addCO2))
    print ('Additional prim = ' + str(addPrim))

    print ('Total costs = ' + str(costs))
    print ('Total CO2 = ' + str(CO2))
    print ('Total prim = ' + str(prim))

    results = {'TAC':[costs.round(2)],'CO2_ton_per_yr':[CO2.round(2)],'Primary_Energy_GJ_per_yr':[prim.round(2)]}
    results_df = pd.DataFrame(results)
    results_path = os.path.join(locator.get_optimization_slave_results_folder(GENERATION_NUMBER),'ind_'+str(individual_number)+'_results.csv')
    results_df.to_csv(results_path)

    with open(locator.get_optimization_checkpoint_initial(), "wb") as fp:
        pop = []
        g = GENERATION_NUMBER
        epsInd = []
        invalid_ind =[]
        fitnesses =[]
        capacities =[]
        disconnected_capacities =[]
        halloffame =[]
        halloffame_fitness = []
        euclidean_distance =[]
        spread =[]
        cp = dict(population=pop, generation=g, epsIndicator=epsInd, testedPop=invalid_ind,
                  population_fitness=fitnesses, capacities=capacities, disconnected_capacities=disconnected_capacities,
                  halloffame=halloffame, halloffame_fitness=halloffame_fitness,
                  euclidean_distance=euclidean_distance, spread=spread)
        json.dump(cp, fp)

    return costs, CO2, prim, master_to_slave_vars, individual


def calc_individual_number(locator):
    if os.path.exists(locator.get_optimization_slave_results_folder(GENERATION_NUMBER)):
        path = locator.get_optimization_slave_results_folder(GENERATION_NUMBER)
        files = listdir(path)
        if np.isclose(len(files), 0.0):
            individual_number = 0
        else:
            individual_number = 0
            existing_numbers = []
            for file in files:
                existing_number = file.split('_')[1]
                existing_numbers.extend([float(existing_number)])
            individual_number = int(max(existing_numbers) + 1)
    else:
        individual_number = 0
    return individual_number


def calc_decentralized_building_costs(config, locator, master_to_slave_vars, DHN_barcode, DCN_barcode, buildList):
    CostDiscBuild_BEST = 0
    CO2DiscBuild_BEST = 0
    PrimDiscBuild_BEST = 0

    if config.optimization.isheating:
        raise ValueError('This function only works for heating case at the moment.')
    if config.optimization.iscooling:
        PV_barcode = ''
        for (index, building_name) in zip(DCN_barcode, buildList):
            if index == "0":  # choose the best decentralized configuration
                df = pd.read_csv(locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                                      configuration='AHU_ARU_SCU'))
                dfBest = df[df["Best configuration"] == 1]
                CostDiscBuild_BEST += dfBest["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                CO2DiscBuild_BEST += dfBest["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                PrimDiscBuild_BEST += dfBest["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]
                to_PV = 1
                if dfBest["single effect ACH to AHU_ARU_SCU Share (FP)"].iloc[0] == 1:
                    to_PV = 0
                if dfBest["single effect ACH to AHU_ARU_SCU Share (ET)"].iloc[0] == 1:
                    to_PV = 0
                if dfBest["single effect ACH to SCU Share (FP)"].iloc[0] == 1:
                    to_PV = 0


            else:  # adding costs for buildings in which the centralized plant provides a part of the load requirements
                #DCN_unit_configuration = master_to_slave_vars.DCN_supplyunits
                DCN_unit_configuration = 7 # TODO: fixed to one configuration at the moment
                if DCN_unit_configuration == 1:  # corresponds to AHU in the central plant, so remaining load need to be provided by decentralized plant
                    decentralized_configuration = 'ARU_SCU'
                    df = pd.read_csv(
                        locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                             decentralized_configuration))
                    dfBest = df[df["Best configuration"] == 1]
                    CostDiscBuild_BEST += dfBest["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                    CO2DiscBuild_BEST += dfBest["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                    PrimDiscBuild_BEST += dfBest["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]
                    to_PV = 1
                    if dfBest["single effect ACH to ARU_SCU Share (FP)"].iloc[0] == 1:
                        to_PV = 0
                    if dfBest["single effect ACH to ARU_SCU Share (ET)"].iloc[0] == 1:
                        to_PV = 0

                if DCN_unit_configuration == 2:  # corresponds to ARU in the central plant, so remaining load need to be provided by decentralized plant
                    decentralized_configuration = 'AHU_SCU'
                    df = pd.read_csv(
                        locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                             decentralized_configuration))
                    dfBest = df[df["Best configuration"] == 1]
                    CostDiscBuild_BEST += dfBest["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                    CO2DiscBuild_BEST += dfBest["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                    PrimDiscBuild_BEST += dfBest["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]
                    to_PV = 1
                    if dfBest["single effect ACH to AHU_SCU Share (FP)"].iloc[0] == 1:
                        to_PV = 0
                    if dfBest["single effect ACH to AHU_SCU Share (ET)"].iloc[0] == 1:
                        to_PV = 0

                if DCN_unit_configuration == 3:  # corresponds to SCU in the central plant, so remaining load need to be provided by decentralized plant
                    decentralized_configuration = 'AHU_ARU'
                    df = pd.read_csv(
                        locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                             decentralized_configuration))
                    dfBest = df[df["Best configuration"] == 1]
                    CostDiscBuild_BEST += dfBest["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                    CO2DiscBuild_BEST += dfBest["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                    PrimDiscBuild_BEST += dfBest["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]
                    to_PV = 1
                    if dfBest["single effect ACH to AHU_ARU Share (FP)"].iloc[0] == 1:
                        to_PV = 0
                    if dfBest["single effect ACH to AHU_ARU Share (ET)"].iloc[0] == 1:
                        to_PV = 0

                if DCN_unit_configuration == 4:  # corresponds to AHU + ARU in the central plant, so remaining load need to be provided by decentralized plant
                    decentralized_configuration = 'SCU'
                    df = pd.read_csv(
                        locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                             decentralized_configuration))
                    dfBest = df[df["Best configuration"] == 1]
                    CostDiscBuild_BEST += dfBest["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                    CO2DiscBuild_BEST += dfBest["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                    PrimDiscBuild_BEST += dfBest["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]
                    to_PV = 1
                    if dfBest["single effect ACH to SCU Share (FP)"].iloc[0] == 1:
                        to_PV = 0
                    if dfBest["single effect ACH to SCU Share (ET)"].iloc[0] == 1:
                        to_PV = 0

                if DCN_unit_configuration == 5:  # corresponds to AHU + SCU in the central plant, so remaining load need to be provided by decentralized plant
                    decentralized_configuration = 'ARU'
                    df = pd.read_csv(
                        locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                             decentralized_configuration))
                    dfBest = df[df["Best configuration"] == 1]
                    CostDiscBuild_BEST += dfBest["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                    CO2DiscBuild_BEST += dfBest["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                    PrimDiscBuild_BEST += dfBest["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]
                    to_PV = 1
                    if dfBest["single effect ACH to ARU Share (FP)"].iloc[0] == 1:
                        to_PV = 0
                    if dfBest["single effect ACH to ARU Share (ET)"].iloc[0] == 1:
                        to_PV = 0

                if DCN_unit_configuration == 6:  # corresponds to ARU + SCU in the central plant, so remaining load need to be provided by decentralized plant
                    decentralized_configuration = 'AHU'
                    df = pd.read_csv(
                        locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                             decentralized_configuration))
                    dfBest = df[df["Best configuration"] == 1]
                    CostDiscBuild_BEST += dfBest["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                    CO2DiscBuild_BEST += dfBest["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                    PrimDiscBuild_BEST += dfBest["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]
                    to_PV = 1
                    if dfBest["single effect ACH to AHU Share (FP)"].iloc[0] == 1:
                        to_PV = 0
                    if dfBest["single effect ACH to AHU Share (ET)"].iloc[0] == 1:
                        to_PV = 0

                if DCN_unit_configuration == 7:  # corresponds to AHU + ARU + SCU from central plant
                    to_PV = 1

        CostDiscBuild_from_config = 0
        CO2DiscBuild_from_config = 0
        PrimDiscBuild_from_config = 0

        for (index, building_name) in zip(DCN_barcode, buildList):
            if index == "0": # for decentralized buildings
                if config.supply_system_simulation.decentralized_systems == 'Vapor Compression Chiller':
                    df = pd.read_csv(locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                                          configuration='AHU_ARU_SCU'))
                    df_config = df[df["VCC to AHU_ARU_SCU Share"] == 1]
                    CostDiscBuild_from_config += df_config["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                    CO2DiscBuild_from_config += df_config["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                    PrimDiscBuild_from_config += df_config["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]

                elif config.supply_system_simulation.decentralized_systems == 'Mini-split Unit':
                    df = pd.read_csv(locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                                          configuration='AHU_ARU_SCU'))
                    df_config = df[df["DX to AHU_ARU_SCU Share"] == 1]
                    CostDiscBuild_from_config += df_config["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                    CO2DiscBuild_from_config += df_config["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                    PrimDiscBuild_from_config += df_config["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]

                elif config.supply_system_simulation.decentralized_systems == 'Single-effect Absorption Chiller':
                    df = pd.read_csv(locator.get_optimization_disconnected_folder_building_result_cooling(building_name,
                                                                                                          configuration='AHU_ARU_SCU'))
                    df_config = df[df["single effect ACH to AHU_ARU_SCU Share (ET)"] == 1]
                    CostDiscBuild_from_config += df_config["Annualized Investment Costs [CHF]"].iloc[0]  # [CHF]
                    CO2DiscBuild_from_config += df_config["CO2 Emissions [kgCO2-eq]"].iloc[0]  # [kg CO2]
                    PrimDiscBuild_from_config += df_config["Primary Energy Needs [MJoil-eq]"].iloc[0]  # [MJ-oil-eq]

                else:
                    raise ValueError('this technology is not available in disconnected buildings')

    Cost_diff = CostDiscBuild_from_config - CostDiscBuild_BEST
    CO2_diff = CO2DiscBuild_from_config - CO2DiscBuild_BEST
    Prim_diff = PrimDiscBuild_from_config - PrimDiscBuild_BEST

    return Cost_diff, CO2_diff, Prim_diff


# ============================
# test
# ============================


def main(config):
    """
    run the whole optimization routine
    """
    gv = cea.globalvar.GlobalVariables()
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)
    weather_file = config.weather

    try:
        if not demand_files_exist(config, locator):
            raise ValueError("Missing demand data of the scenario. Consider running demand script first")

        if not os.path.exists(locator.get_total_demand()):
            raise ValueError("Missing total demand of the scenario. Consider running demand script first")

        if not os.path.exists(locator.PV_totals()):
            raise ValueError("Missing PV potential of the scenario. Consider running photovoltaic script first")

        if config.optimization.isheating:
            if not os.path.exists(locator.PVT_totals()):
                raise ValueError(
                    "Missing PVT potential of the scenario. Consider running photovoltaic-thermal script first")

        if not os.path.exists(locator.SC_totals(panel_type='FP')):
            raise ValueError(
                "Missing SC potential of panel type 'FP' of the scenario. Consider running solar-collector script first with panel_type as SC1 and t-in-SC as 75")

        if not os.path.exists(locator.SC_totals(panel_type='ET')):
            raise ValueError(
                "Missing SC potential of panel type 'ET' of the scenario. Consider running solar-collector script first with panel_type as SC2 and t-in-SC as 150")

        if not os.path.exists(locator.get_sewage_heat_potential()):
            raise ValueError(
                "Missing sewage potential of the scenario. Consider running sewage heat exchanger script first")

        if not os.path.exists(locator.get_optimization_network_edge_list_file(config.thermal_network.network_type, '')):
            raise ValueError("Missing network edge list. Consider running thermal network script first")
    except ValueError as err:
        import sys
        print(err.message)
        sys.exit(1)

    # read total demand file and names and number of all buildings
    total_demand = pd.read_csv(locator.get_total_demand())
    building_names = total_demand.Name.values
    gv.num_tot_buildings = total_demand.Name.count()
    prices = Prices(locator, config)
    lca = lca_calculations(locator, config)

    # pre-process information regarding resources and technologies (they are treated before the optimization)
    # optimize best systems for every individual building (they will compete against a district distribution solution)
    extra_costs, extra_CO2, extra_primary_energy, solarFeat = preproccessing(locator, total_demand, building_names,
                                                                             weather_file, gv, config, prices, lca)

    # optimize the distribution and linearize the results(at the moment, there is only a linearization of values in Zug)
    network_features = network_opt.network_opt_main(config, locator)

    ## generate individual from config
    # heating technologies at the centralized plant
    heating_block = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90.0, 6]
    # FIXME: connect PV to config
    # cooling technologies at the centralized plant
    centralized_vcc_size = config.supply_system_simulation.centralized_vcc
    centralized_ach_size = config.supply_system_simulation.centralized_ach
    centralized_storage_size = config.supply_system_simulation.centralized_storage
    cooling_block = [0, 0, 1, 0.3, 1, 0.4, 1, 0.2, 6, 7]
    cooling_block[2:4] = [1, centralized_vcc_size] if (centralized_vcc_size != 0) else [0, 0]
    cooling_block[4:6] = [1, centralized_ach_size] if (centralized_ach_size != 0) else [0, 0]
    cooling_block[6:8] = [1, centralized_storage_size] if (centralized_storage_size != 0) else [0, 0]

    total_demand = pd.read_csv(locator.get_total_demand())
    building_names = total_demand.Name.values
    #read list of buildings connected to DC from config
    if len(config.supply_system_simulation.dc_connected_buildings) == 0:
        dc_connected_buildings = building_names  # default, all connected
    else:
        dc_connected_buildings = config.supply_system_simulation.dc_connected_buildings
    #dc_connected_buildings = building_names  # default, all connected

    # buildings connected to networks
    heating_network = [0] * building_names.size
    cooling_network = [0] * building_names.size
    for building in dc_connected_buildings:
        index = np.where(building_names == building)[0][0]
        cooling_network[index] = 1

    individual = heating_block + cooling_block + heating_network + cooling_network
    #individual = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0.01,1,0.535812211,0,0,0,0,10,7,1,0,1,1,0,1,0,0,0,0,1,1,1,1,0,1,1,0,1,1]

    individual_evaluation(individual, building_names, total_demand, locator, extra_costs, extra_CO2, extra_primary_energy,
                          solarFeat, network_features, gv, config, prices, lca)

    print 'individual evaluation succeeded'


def demand_files_exist(config, locator):
    # verify that the necessary demand files exist
    return all(os.path.exists(locator.get_demand_results_file(building_name)) for building_name in
               locator.get_zone_building_names())


if __name__ == '__main__':
    main(cea.config.Configuration())
