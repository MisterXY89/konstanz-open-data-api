import pytest
from .fetcher.json_fetcher import jsonFetcher


@pytest.fixture
def fetcher_instance() -> jsonFetcher:
    """creates a instance of jsonFetcher

    Returns
    -------
    jsonFetcher
        instance of jsonFetcher
    """
    json = jsonFetcher()
    return json


def test_load_data_correct(fetcher_instance):
    """checks if data is really a pandas core frame, this tests also parse_json already

    Parameters
    ----------
    fetcher_instance : jsonFetcher
        json fetcher instance
    """
    df, flag = fetcher_instance.load_data(
        url="https://offenedaten-konstanz.de/sites/default/files/Wahlbezirke-OB-Wahl-2020.json"
    )
    assert flag == True
    assert len(df) > 0


def test_load_data_wrong(fetcher_instance):
    """checks if for a wrong url no dataframe is returned, this tests also parse_json already

    Parameters
    ----------
    fetcher_instance : jsonFetcher
        json fetcher instance
    """
    df, flag = fetcher_instance.load_data(
        url="https://services2.arcgis.com/bvsdhqn48gvbFiYS/arcgis/rest/services/Solarpotenzial_2018/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=432&f=json"
    )
    # assert not isinstance(df, pandas.core.frame.DataFrame)
    assert len(df) == 0
    assert flag == False
