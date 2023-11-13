# Groundwork ETI Model
This tool was developed by [Groundwork Data](https://www.groundworkdata.org/) in conjunction with the [University of Massachusetts Energy Transition Institute (ETI)](https://www.energytransitionumass.org/) to "evaluate costs, emissions, and infrastructure changes as a result of specific scenarios applied to connected buildings or the distribution systems." This tool was then used to conduct scenario analyses on two street segments. The inputs for these analyses can be found in the repository and the results are communicated in the associated project report. The tool is available under the MIT license.

## About the tool
The Groundwork ETI model is a local energy asset planning (LEAP) simulation tool. The user provides a number of configuration files describing the makeup, energy consumption, and assumed intervention costs along a street. The tool then executes a given intervention scenario and reports annual indicators, including total system costs, peak energy consumption, and emissions, among others.

Interventions at individual buildings are aggregated "up" the network to account for total cost and energy consumption, sometimes triggering upstream interventions. For example, this can occur when all gas-consuming building assets are shut off, triggering a shutoff of the gas service line to that building. The tool outputs a number of indicators that quantify how different intervention strategies impact costs, energy consumption patterns, and emissions.

## Running the tool
The model is run as a command line tool via `run.py`. Once all configuration files are created and with a proper python environment activated, the user can enter the following in a terminal:
```console
% python run.py <STREET_SEGMENT> <SCENARIO>
```
where `STREET_SEGMENT` and `SCENARIO` are the street segment and energy intervention scenario being investigated, respectively. The tool will display status updates to the user as the simulation is running.

The allowable values for `STREET_SEGMENT` are `"mf"` (multi-family) or `"sf"` (single family). The allowable values for `SCENARIO` are the following:
* `"continued_gas"`
* `"accelerated_elec"`
* `"accelerated_elec_higheff"`
* `"natural_elec"`
* `"natural_elec_higheff"`
* `"hybrid_gas"`
* `"hybrid_gas_immediate"`
* `"hybrid_npa"`

In addition to the scenarios listed above, the user may execute all scenarios at once by providing `"all"` for the `SCENARIO` argument.

More details on the street segments and scenarios are provided below. An example of simulating the hybrid NPA (non-pipe alternative) scenario for the single-family street segment would be the following:
```console
% python run.py sf hybrid_npa
```

Note that this is specific to the scenarios analyzed by Groundwork Data as part of the Groundwork-ETI project deliverable. A new scenario can be defined by creating a simulation settings configuration with the file name `<STREET_SEGMENT>_<SCENARIO>_settings_config.json`. Further information on creating a new scenario is detailed below.

If the user wants to investigate multiple scenarios, run each scenario individually and then run `python postprocessing.py`. This will combine output tables across scenarios for easier investigation. *In its current implementation, the post-processing script requires that all possible scenarios are executed for a given street segment; otherwise, the script will fail. Outputs from individual scenario runs can still be investigated independently.* For this reason, a recommended workflow would be the following:
```console
% python run.py <STREET_SEGMENT> all
% python postprocessing.py
```

Additionally, the output filenames are not unique by street segment; they are only unique by scenario. *For this reason, it is not recommended to run simulations for different street segments at the same time.* Rather, run simulations for one street segment, save a copy of the results, and then run simulation for another street segment.

### Outputs
All output tables are written to CSVs, which can be utilized for further investigation. The output tables for a scenario `SCENARIO_NAME` will be saved to `./outputs_combined/scenarios/<SCENARIO_NAME>/`. If the user executes the post-processing script, the combined results will be saved to `./outputs_combined/scenarios/combined/`. The output tables are as follows:
* `book_value`: The annual depreciated book value of all assets over the simulation timeframe.
* `consumption_costs`: The cost to an individual consumer for their energy consumption. This is organized by energy source (electricity, natural gas, etc).
* `consumption_emissions`: The carbon emissions associated with energy consumption. Note that these are different from leak emissions.
* `energy_consumption`: The total annual energy consumption, by energy source, of an entity.
* `fuel_type`: The dominant fuel type each year at a building
* `is_retrofit_vec_table`: This annual vector is `True` in the retrofit year and all subsequent years. It helps indicate whether or not a given entity has been retrofit.
* `methane_leaks`: The annual methane leaks in the system, organized by various entities (total leaks within the building, leaks within a given pipe, etc).
* `operating_costs`: The annual operating associated with an entity. Currently, this only outputs operating costs for gas utility assets.
* `peak_consump`: The annual peak consumption at electric transformers based on downstream energy consumption at connected buildings.
* `retrofit_cost`: The annual cost of retrofitting an asset.
* `retrofit_year`: Similar to the `is_retrofit_vec_table`, except this vector is only `True` in the asset's retrofit year.
* `stranded_val`: The stranded value of an asset in a given year if it is retrofit before the end of its useful life (before it fully depreciates).

## Running the provided scenarios
This repository includes all input values for simulating the scenarios detailed in Groundwork Data's project report. There are two street segments, a multifamily (coded `mf`) and a single-family (coded `sf`) segment. The energy intervention scenarios are coded as follows:
* `continued_gas`: Continued use of pipeline gas and gas consumption in the building.
* `hybrid_gas`: Hybridized heating using heat pumps with natural gas as a backup source.
* `hybrid_gas_immediate`: Same as `hybrid_gas`, with necessary interventions occurring at all homes in 2025, rather than naturally over a longer time period.
* `hybrid_npa`: Hybridized heating using heat pumps and non-pipeline gas alternatives (liquified propane gas) as backup heating fuels.
* `natual_elec`: Full electrification of all homes connected to the gas network occurs at the end of each home appliance's end of useful life.
* `accelerated_elec`: Full electrification of all homes connected to the gas network in 2025.

More details on the street segments and energy intervention scenarios can be found in the project report.

## Creating a new scenario
Creating a scenario for the tool requires the definition of a number of configuration files related the simulation settings, the buildings on the street segment, their energy consumption, and the utility network on the street segment. *Some code changes are also required to accommodate new scenarios - for this reason, creating new scenarios is not recommended.*

The simulation settings config details high-level attributes such as the start and end years of the simulation. It also defines the filepaths of the configuration files for the buildings and the utility network. The utility network configuration files define the utility assets, including how the assets are connected to one another. Some utility asset features are only defined for certain kinds of assets. For example, the configs for gas assets detail the pipe materials and lengths. Finally, the building configurations detail the assets present in each building and features such as the asset install dates and install costs.

## Development
The tool is developed in Python. Development and execution of the tool require an environment with Python >= 3.9 and the packages described in `requirements.txt`. The environment can be created using `pip` and `virtualenv`.
