import pytest
from .config import Config as cf
from .fetch_dataset_list import DataSetUrlFetcher
import pandas as pd


@pytest.fixture
def url_fetcher(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    url_fetcher = DataSetUrlFetcher(cf)
    return url_fetcher


def test_read_curr_packages(url_fetcher):
    """test if current package list is correctly extracted

    Parameters
    ----------
    url_fetcher :  DataSetUrlFetcher
         DataSetUrlFetcher
    """
    data = url_fetcher.read_curr_packages()
    check_columns = [
        "id",
        "title",
        "source",
        "url",
        "created",
        "modified",
        "notes",
        "tags",
        "name",
    ]
    assert len(data) > 0
    for column in data:
        assert column in check_columns


def test_fetch(url_fetcher):
    """test if url is correctly fetched

    Parameters
    ----------
    url_fetcher :  DataSetUrlFetcher
         DataSetUrlFetcher
    """
    dict_ = url_fetcher.fetch()
    check_keys = list(dict_.keys())
    assert len(dict_) > 0
    for key in check_keys:
        assert key in ["help", "success", "result"]


def test_get_names(url_fetcher):
    """test if names are extracted correctly

    Parameters
    ----------
    url_fetcher :  DataSetUrlFetcher
         DataSetUrlFetcher
    """
    names = url_fetcher._get_names()
    check_columns = list(names.columns)
    assert len(names) > 0
    for column in check_columns:
        assert column in ["id", "name"]


def test_wrong_df_store(url_fetcher):
    """Test for wrong dataframe instance

    Parameters
    ----------
    url_fetcher :  DataSetUrlFetcher
         DataSetUrlFetcher
    """
    df = pd.DataFrame([{"test_id": 3, "value": 1}, {"test_id": 5, "value": 2}])
    status = url_fetcher._store(df)
    assert status == False


def test_wrong_type_store(url_fetcher):
    """test for wrong type of function

    Parameters
    ----------
    url_fetcher :  DataSetUrlFetcher
         DataSetUrlFetcher
    """
    df = [{"test_id": 3, "value": 1}, {"test_id": 5, "value": 2}]
    status = url_fetcher._store(df)
    assert status == False


# TODO: Was muss man einfügen bei url_fetcher._store damit die Liste ausgegeben wird?


def test_get_notes(url_fetcher):
    """Test if notes are correctly extracted

    Parameters
    ----------
    url_fetcher : instance of  DataSetUrlFetcher
        instance of  DataSetUrlFetcher
    """
    df = url_fetcher.read_curr_packages()
    notes = url_fetcher._get_notes(df)
    assert len(df) == len(notes)


# TODO parse data correct, what is data? + fetcher update


def test_parse_data_wrong(url_fetcher):
    """Test for wrong format

    Parameters
    ----------
    url_fetcher :  DataSetUrlFetcher
         DataSetUrlFetcher instance
    """
    df = url_fetcher.read_curr_packages()
    status = url_fetcher._parse_data(df)
    assert status == False


def test_update_wrong(url_fetcher):
    """tests if flag is False if incorrect data parsing"""
    df = pd.DataFrame()
    url_fetcher._parse_data(df)
    status = url_fetcher.update()
    assert status == False
