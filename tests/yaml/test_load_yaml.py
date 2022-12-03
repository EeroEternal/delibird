"""test load yaml"""

from re import A

import pytest
import yaml

from delibird.util.show import show


@pytest.mark.parametrize(
    "yaml_file ",
    ["tests/yaml/filemock.yaml"],
)
def test_load_yaml(yaml_file):
    """test yaml file load

    Args:
        yaml_file (str): yaml file path
    """
    with open(yaml_file, "r", encoding="utf-8") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    show(f"config:{config}")

    # dict can use "in" directly, not need to use "has_key" or "keys()"
    if "mocks" not in config:
        show("no mock in config file")
    else:
        show("mocks in config file")

    if "temp" in config and config["temp"]:
        show("temp in config file")
        show(f"temp:{config['temp']} exist")
