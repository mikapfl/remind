#!/usr/bin/env python
"""Convert a scenario_config file to a bunch of YAML files."""

import typing
import pathlib
import sys

import pandas as pd
import numpy as np
import yaml

SeparatedScenarios = typing.Dict[str, typing.Dict[str, typing.Union[str, typing.Dict[str, str]]]]

def main():
    scenario_config = sys.argv[1]
    scenario_config_name = scenario_config[16:-4]  # strip scenario_config_ and .csv
    if scenario_config == "scenario_config.csv":
        scenario_config_name = "default"
    scen_pd = read(scenario_config)
    scenarios = convert(scen_pd)
    scenarios = clean_na(scenarios)
    separated_scenarios = separate_meta_data(scenarios)
    separated_scenarios = add_ref_scenarios(separated_scenarios)
    separated_scenarios = reorder(separated_scenarios)
    write(separated_scenarios, pathlib.Path(scenario_config_name))


def read(fpath: str) -> pd.DataFrame:
    return pd.read_csv(fpath, sep=';', comment="#")


def convert(scen_pd: pd.DataFrame) -> typing.List[typing.Dict[str, str]]:
    return [dict(row) for _, row in scen_pd.iterrows()]


def clean_na(scenarios: typing.List[typing.Dict[str, str]]) -> typing.List[typing.Dict[str, str]]:
    for scenario in scenarios:
        to_delete = []
        for key, value in scenario.items():
            if value is None or value == "" or (isinstance(value, float) and np.isnan(value)):
                to_delete.append(key)
        for key in to_delete:
            del scenario[key]
    return scenarios


def separate_meta_data(scenarios: typing.List[typing.Dict[str, str]]) -> SeparatedScenarios:
    separated_scenarios = {}
    for scenario in scenarios:
        title = scenario.pop("title")
        separated_scenarios[title] = {
            "description": scenario.pop("description", ""),
            "start": str(scenario.pop("start"))
        }
        if "slurmConfig" in scenario:
            separated_scenarios[title]["slurmConfig"] = scenario.pop("slurmConfig")
        separated_scenarios[title]["settings"] = scenario
    return separated_scenarios


def add_ref_scenarios(scenarios: SeparatedScenarios) -> SeparatedScenarios:
    """Add reference scenarios and remove settings which are identical to ref scenario"""
    references = {}
    for title, scenario in scenarios.items():
        start = scenario["start"]
        if start in ("0", "1"):
            ref = '__default__'
        else:
            ref = start
        if ref not in references:
            references[ref] = title
        else:
            reference_title = references[ref]
            reference_scenario = scenarios[reference_title]
            ref_settings = reference_scenario["settings"]
            to_del = []
            for setting in scenario["settings"]:
                if setting in ref_settings and scenario["settings"][setting] == reference_scenario["settings"][setting]:
                    to_del.append(setting)
            for setting in to_del:
                del scenario["settings"][setting]
            if to_del:
                scenario["referenceScenario"] = reference_title
    return scenarios


def reorder(scenarios: SeparatedScenarios) -> SeparatedScenarios:
    ordered = {}
    for title, scenario in scenarios.items():
        ordered[title] = {
            "description": scenario["description"],
            "start": scenario["start"]
        }
        for key in "referenceScenario", "slurmConfig":
            if key in scenario:
                ordered[title][key] = scenario[key]
        ordered[title]["settings"] = scenario["settings"]
    return ordered

def write(scenarios: SeparatedScenarios, dirpath: pathlib.Path):
    dirpath.mkdir()
    for title, scenario in scenarios.items():
        path = dirpath
        if scenario["start"] not in ("0", "1"):
            path = path / scenario["start"]
        if not path.exists():
            path.mkdir()
        with (path / title).with_suffix(".yaml").open("w") as fd:
            yaml.dump(scenario, fd, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    main()