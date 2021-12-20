import pytest

from API_helper import FetchHelper
from fetcher.csv_fetcher import csvFetcher
from fetcher.shp_fetcher import shpFetcher
from fetcher.txt_fetcher import txtFetcher


@pytest.fixture
def fetcher_helper() -> FetchHelper:
    fetcher_helper = FetchHelper()
    return fetcher_helper


fetcher_data = [
    ("csv", csvFetcher),
    ("txt", txtFetcher),
    ("geojson", shpFetcher),
]


@pytest.mark.parametrize(argnames="file, fetcher", argvalues=fetcher_data)
def test_get_instance(file, fetcher):
    """test if correct instance is returend

    Parameters
    ----------
    file : string
        string with format of data
    fetcher : class of fetcher
        fetcher with correct class
    """
    fetcher_class = FetchHelper.get_instance(file)
    assert isinstance(fetcher_class(), fetcher)


fetch_resource_urls_correct_data = [
    ("db8d5dc2-b740-45cf-9c42-c0fa8e271051", "Modal Split"),
    ("2c6ae437-883b-4395-9780-23a16edb6720", "Bodanstraße Richtung Bahnhof"),
    ("d7cb3b4e-8f74-49f9-a670-7f0b1c70ac37", "Freizeiteinrichtungen - Bäder"),
]


@pytest.mark.parametrize(
    argnames="ids_, output", argvalues=fetch_resource_urls_correct_data
)
def test_fetch_datase_urls(ids_, output):
    """test if url is returned given id

    Parameters
    ----------
    ids_ : String
        package id
    output : String
        correct name
    """
    assert next(FetchHelper.fetch_dataset_urls(id=ids_))[2] == output


fetch_resource_urls_correct_data = [
    ("db8d5dc2-b740-45cf-9c42-c0fa8e271051", "Modal Split"),
    ("2c6ae437-883b-4395-9780-23a16edb6720", "Bodanstraße Richtung Bahnhof"),
    ("d7cb3b4e-8f74-49f9-a670-7f0b1c70ac37", "Freizeiteinrichtungen - Bäder"),
]


@pytest.mark.parametrize(
    argnames="ids_, output", argvalues=fetch_resource_urls_correct_data
)
def test_fetch_dataset_meta(ids_, output):
    """test if url is returned given id as meta

    Parameters
    ----------
    ids_ : String
        package id
    output : String
        correct name
    """
    status_iterator = next(FetchHelper.fetch_dataset_meta(id=ids_))
    assert status_iterator[3] == output
    assert len(status_iterator) == 7


def test_get_url_ending():
    """test if ending is correctly extracted"""
    assert (
        FetchHelper.get_url_ending(
            url="https://offenedaten-konstanz.de/sites/default/files/M%C3%BClleimer.shp_.xml"
        )
        == "xml"
    )


def test_verfiy_url(fetcher_helper):
    assert (
        fetcher_helper.verify_url(
            url="https://offenedaten-konstanz.de/sites/default/files/M%C3%BClleimer.shp_.xml"
        )
        == True
    )


def test_verify_url_wrong(fetcher_helper):
    assert (
        fetcher_helper.verify_url(
            "https://data-konstanz.de/sites/default/files/M%C3%BClleimer.shp_.xml"
        )
        == False
    )


# TODO: hat das einen Grund, warum wir die classes manchmal mit static method gemacht haben?
