import pytest
from fetcher.csv_fetcher import csvFetcher
import pandas


@pytest.fixture
def fetcher_instance() -> csvFetcher:
    """creates a instance of csvFetcher

    Returns
    -------
    csvFetcher
        instance of csvFetcher
    """
    csv = csvFetcher()
    return csv


def test_verify_df_correct(fetcher_instance):
    df, flag_df = fetcher_instance.load_data(
        url="https://offenedaten-konstanz.de/sites/default/files/Bodanstra%C3%9Fe_20210219_202100309_FR_Bahnhof.csv"
    )
    flag = fetcher_instance.verify_df(
        df1=df,
        url="https://offenedaten-konstanz.de/sites/default/files/Bodanstra%C3%9Fe_20210219_202100309_FR_Bahnhof.csv",
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
        url="https://offenedaten-konstanz.de/sites/default/files/Bodanstra%C3%9Fe_20210219_202100309_FR_Bahnhof.csv"
    )
    assert isinstance(df, pandas.core.frame.DataFrame)
    assert flag == True


def test_load_data_wrong(fetcher_instance):
    """checks if for a wrong url no dataframe is returned, this tests also parse_csv already

    Parameters
    ----------
    fetcher_instance : csvFetcher
        csv fetcher instance
    """
    df, flag = fetcher_instance.load_data(
        url="https://offenedaten-konstanz.de/sites/default/files/Bodanstra%C3%9Fe_20210219_22100309_FR_Bahnhof.csv"
    )
    assert not isinstance(df, pandas.core.frame.DataFrame)
    assert flag == False
