import pytest
from .fetcher.xls_fetcher import xlsFetcher


@pytest.fixture
def fetcher_instance() -> xlsFetcher:
    """creates a instance of jsonFetcher

    Returns
    -------
    jsonFetcher
        instance of jsonFetcher
    """
    xls = xlsFetcher()
    return xls


def test_verify_df_correct(fetcher_instance):
    df, flag_df = fetcher_instance.load_data(
        url="https://offenedaten-konstanz.de/sites/default/files/%C3%96ffentlichen%20M%C3%BClltonnen.xls"
    )
    flag = fetcher_instance.verify_df(
        df1=df,
        url="https://offenedaten-konstanz.de/sites/default/files/%C3%96ffentlichen%20M%C3%BClltonnen.xls",
        encoding="utf-8",
        sep=";",
    )
    assert flag == True
    assert flag == flag_df


def test_load_data_correct(fetcher_instance):
    """checks if data is really a pandas core frame, this tests also parse_csv already

    Parameters
    ----------
    fetcher_instance : csvFetcher
        csv fetcher instance
    """
    df, flag = fetcher_instance.load_data(
        url="https://offenedaten-konstanz.de/sites/default/files/%C3%96ffentlichen%20M%C3%BClltonnen.xls"
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
        url="https://offenedaten-konstanz.de/sites/default/files/%C3%96ffentlichen%20M%C3%BClltonen.xls"
    )
    assert len(df) == 0
    assert flag == False
