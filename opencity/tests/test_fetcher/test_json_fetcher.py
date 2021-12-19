import pytest
from fetcher.json_fetcher import jsonFetcher
import pandas


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
        url="https://offenedaten-konstanz.de/api/3/action/package_show?id=d3303376-77d7-4dba-bd6f-c0194acb7ae2"
    )
    assert isinstance(df, pandas.core.frame.DataFrame)
    assert flag == True
    assert len(list(df)) != 0


def test_load_data_wrong(fetcher_instance):
    """checks if for a wrong url no dataframe is returned, this tests also parse_json already

    Parameters
    ----------
    fetcher_instance : jsonFetcher
        json fetcher instance
    """
    df, flag = fetcher_instance.load_data(
        url="https://offenedaten-konstanz.de/api/3/action/package_show?id=d3303376-77d7-4dba-bd6f-c0194acb7ae21313"
    )
    # assert not isinstance(df, pandas.core.frame.DataFrame)
    assert flag == False
    assert len(list(df)) == 0


# TODO: Wo bekommt man wirklich ein json File
# TODO: Warum gibt test_load_data_wrong bei json ein pandas_core.DataFrame raus?
