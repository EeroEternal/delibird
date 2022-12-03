"""test from yaml workflow"""

import pytest

from delibird.cli.workflow import workflow


@pytest.mark.parametrize(
    "yaml_file",
    [("./tests/yaml/workflow.yaml")],
)
def test_yaml(yaml_file):
    """test from_parquet function

    Args:
        yaml_file (str): yaml file with path
    """

    # test from parquet function
    workflow(yaml_file)

    assert True
