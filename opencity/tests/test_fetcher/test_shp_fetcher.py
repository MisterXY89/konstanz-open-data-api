import pytest
from .fetcher.shp_fetcher import shpFetcher
import pandas


@pytest.fixture
def fetcher_instance() -> shpFetcher:
    """creates a instance of jsonFetcher

    Returns
    -------
    jsonFetcher
        instance of jsonFetcher
    """
    shp = shpFetcher()
    return shp


def test_load_data_correct(fetcher_instance):
    """checks if data is really a pandas core frame, this tests also parse_csv already

    Parameters
    ----------
    fetcher_instance : csvFetcher
        csv fetcher instance
    """
    df, flag = fetcher_instance.load_data(
        url="https://offenedaten-konstanz.de/sites/default/files/Fahrradmietsytsem_Konrad_TINK.zip"
    )
    assert len(df) > 0
    assert flag == True


def test_load_data_wrong(fetcher_instance):
    """checks if for a wrong url no dataframe is returned, this tests also parse_csv already

    Parameters
    ----------
    fetcher_instance : csvFetcher
        csv fetcher instance
    """
    df, flag = fetcher_instance.load_data(
        url="https://offenedaten-konstanz.de/sites/default/files/Fahrradmiesytsem_Konrad_TINK.zip"
    )

    assert len(df) == 0
    assert flag == False
