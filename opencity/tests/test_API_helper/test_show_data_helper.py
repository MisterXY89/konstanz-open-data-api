from .API_helper import ShowDataHelper
from .API_helper import DataSetUrlFetcher
import pytest
from .config import Config as cf


@pytest.fixture
def show_data_helper(monkeypatch) -> ShowDataHelper:
    monkeypatch.setattr("builtins.input", lambda _: "y")
    dsuf = DataSetUrlFetcher(cf=cf)
    show_data_helper = ShowDataHelper(dsuf.current_list)
    return show_data_helper


@pytest.fixture
def current_list(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    dsuf = DataSetUrlFetcher(cf=cf)
    return dsuf.current_list


def test_summary(capfd, show_data_helper, current_list):
    show_data_helper.summary()
    out, err = capfd.readouterr()
    assert (
        "There are in total"
        and "different categories"
        and len(current_list)
        and "These categories are" in out
    )
    assert "Title" not in out


def test_short(capfd, show_data_helper, current_list):
    show_data_helper.short(current_list)
    out, err = capfd.readouterr()
    assert ("Title" and "Shortname" and "Tags") in out
    assert ("Variable") not in out


def test_long(capfd, show_data_helper, current_list):
    show_data_helper.long(current_list)
    out, err = capfd.readouterr()
    assert ("Title" and "Shortname" and "Variable" and "Tags" and "Value") in out


def test_meta(show_data_helper, current_list):
    show_data_helper.meta(current_list, destroy_=True)
    assert True
