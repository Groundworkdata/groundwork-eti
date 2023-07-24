"""
Main script to run the simulation
"""
import argparse

from scenario_creator.create_scenario import ScenarioCreator


def main():
    parser = argparse.ArgumentParser(
        description="Groundwork ETI local energy asset planning model"
    )

    parser.add_argument("street_segment", help="The street segment you would like to analyze")
    parser.add_argument("scenario", help="The scenario you would like to run")
    args = parser.parse_args()

    street_segment = args.street_segment.lower()
    decarb_scenario = args.scenario.lower()

    allowable_segments = ["sf", "mf"]
    allowable_scenarios = [
        "continued_gas",
        "accelerated_elec",
        "natural_elec",
        "hybrid_gas",
        "hybrid_gas_immediate",
        "hybrid_npa"
    ]

    if street_segment not in allowable_segments:
        raise ValueError(
            f"Street segment must be in {allowable_segments}. Received {street_segment}."
        )
    
    if decarb_scenario not in allowable_scenarios:
        raise ValueError(
            f"Scenario must be in {allowable_scenarios}. Received {decarb_scenario}."
        )
    
    settings_filepath = f"./config_files/settings/{street_segment}_{decarb_scenario}_settings_config.json"

    scenario = ScenarioCreator(
        settings_filepath
    )

    scenario.create_scenario()

    print("Buildings: {}".format(list(scenario.buildings.keys())))
    print("==================")

if __name__ == "__main__":
    main()
