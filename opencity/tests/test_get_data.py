import pytest
from opencity import opencity
import pandas as pd


@pytest.fixture
def opencity_instance(monkeypatch) -> opencity.OpenCity:
    monkeypatch.setattr("builtins.input", lambda _: "y")
    open_city = opencity.OpenCity()
    return open_city


# TODO: Opencity kontaktieren
# def test_with_one_dataset(opencity_instance, capfd):
#     result = opencity_instance.get_data(data=["einwohner"])
#     out, err = capfd.readouterr()
#     assert isinstance(result, pd.core.frame.DataFrame)
#     assert "Successfully loaded data set" in out
#     assert len(result) > 0
#     assert "'Stand_Einwohner" in list(result.column)


def test_with_wrong_dataset(opencity_instance, capfd):
    opencity_instance.get_data(data=["einwhner"])
    out, err = capfd.readouterr()
    assert "The provided names or tags are incorrect." in out


# TODO: Opencity kontaktieren
# def test_with_one_dataset(opencity_instance, capfd):
#     keys = [
#         "solarpotenzial_2018_csv",
#         "solarpotenzial_2018_xml",
#         "solarpotenzial_2018_zip",
#         "solarpotenzial_2018_json",
#     ]
#     result = opencity_instance.get_data(data=["solarpotenzial"])
#     out, err = capfd.readouterr()
#     assert isinstance(result, dict)
#     assert "Successfully loaded data set" in out
#     assert len(result) > 1
#     for key, value in result.items():
#         assert key in keys
#         assert len(value) > 0


def test_meta_true(opencity_instance):
    column_names = [
        "id",
        "url",
        "format",
        "name",
        "created",
        "last_modified",
        "description",
    ]
    result_meta_true = opencity_instance.get_data(data=["einwohner"], meta=True)
    for column in list(result_meta_true.columns):
        assert column in column_names
