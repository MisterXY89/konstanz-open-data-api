from opencity import opencity
import pytest
import os


@pytest.fixture
def opencity_instance(monkeypatch) -> opencity.OpenCity:
    monkeypatch.setattr("builtins.input", lambda _: "y")
    open_city = opencity.OpenCity()
    return open_city


def test_data_parameter(opencity_instance, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    opencity_instance.save_data(data=["einwohner"])
    assert os.path.exists(os.getcwd() + "/Einwohner nach Stadtvierteln.csv")


def test_data_parameter_e_wrong(opencity_instance, monkeypatch, capfd):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    opencity_instance.save_data(data=["einwoner"])
    out, err = capfd.readouterr()
    assert "The provided names or tags are incorrect." in out


def test_tag_parameter(opencity_instance, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    opencity_instance.save_data(data=["Geo"], tag=True, folder="data_tag")
    assert os.path.exists(
        os.getcwd() + "/data_tag/Stadtteilgrenzen-Stadtteilfläche.xls"
    )
    assert os.path.exists(
        os.getcwd()
        + "/data_tag/Georeferenzierte Standorte Fahrradmietsytsem (konrad, TINK).xls"
    )
    assert os.path.exists(os.getcwd() + "/data_tag/Solarpotenzial 2018.geojson")
    assert os.path.exists(
        os.getcwd() + "/data_tag/Öffentlichen Papiereimer - Stadt Konstanz.csv"
    )


def test_data_parameter_wrong(opencity_instance, monkeypatch, capfd):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    opencity_instance.save_data(data=["geo"])
    out, err = capfd.readouterr()
    assert "The provided names or tags are incorrect." in out


def test_special_path(opencity_instance, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    path = os.getcwd() + "/data_special_path"
    opencity_instance.save_data(data=["einwohner"], folder=path)
    assert os.path.exists(path + "/Einwohner nach Stadtvierteln.csv")


def test_supressed_path():
    flag = False
    open_city = opencity.OpenCity()
    open_city.save_data(data=["einwohner"], suppress=True)
    flag = True
    assert flag == True


def test_supressed_path_false():
    open_city = opencity.OpenCity()
    try:
        open_city.save_data(data=["einwohner"], suppress=False)
    except:
        flag = False
    assert flag == False
