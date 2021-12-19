from fetcher.basic_fetcher import BasicFetcher
import pytest


@pytest.fixture
def basic_fetcher() -> BasicFetcher:
    basic_fetcher = BasicFetcher()
    return basic_fetcher


fetch_resource_urls_correct_data = [
    ("db8d5dc2-b740-45cf-9c42-c0fa8e271051", "Modal Split"),
    ("2c6ae437-883b-4395-9780-23a16edb6720", "Bodanstraße Richtung Bahnhof"),
    ("d7cb3b4e-8f74-49f9-a670-7f0b1c70ac37", "Freizeiteinrichtungen - Bäder"),
]


@pytest.mark.parametrize(
    argnames="ids_, output", argvalues=fetch_resource_urls_correct_data
)
def test_fetch_resource_urls_correct(basic_fetcher, ids_, output):
    """test for fetch resource with correct ids

    Parameters
    ----------
    basic_fetcher: BasicFetcher
        basic fetcher instance
    ids_ : List
        list of ids
    output : List
        list of outputs
    """
    assert next(basic_fetcher.fetch_resource_urls(p_id=ids_))[1] == output


def test_fetch_resource_urls_incorrec(basic_fetcher):
    """test for fetch resource with incorrect id

    Parameters
    ----------
    basic_fetcher : Basic Fetcher
        basic fetcher instance
    """
    with pytest.raises(StopIteration):
        next(basic_fetcher.fetch_resource_urls(p_id="2313"))


def test_get_file_ending(basic_fetcher):
    ending = basic_fetcher.get_file_ending(
        "https://offenedaten-konstanz.de/sites/default/files/M%C3%BClleimer.shp_.xml"
    )
    assert ending == "xml"
