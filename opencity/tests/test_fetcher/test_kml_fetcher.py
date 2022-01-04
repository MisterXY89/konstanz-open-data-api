from .fetcher.kml_fetcher import kmlFetcher
import pytest
import pandas


@pytest.fixture
def fetcher_instance() -> kmlFetcher:
    """creates a instance of jsonFetcher

    Returns
    -------
    jsonFetcher
        instance of jsonFetcher
    """
    kml = kmlFetcher()
    return kml


def test_load_data_correct(fetcher_instance):
    """checks if data is really a pandas core frame, this tests also parse_kml already

    Parameters
    ----------
    fetcher_instance : kmlFetcher
        json kml instance
    """
    df, flag = fetcher_instance.load_data(
        url="https://opendata.arcgis.com/datasets/1600ac31789c4779b4613f74e70c1f3f_0.kml"
    )

    assert flag == True
    assert len(df) > 0


def test_load_data_wrong(fetcher_instance):
    """checks if for a wrong url no dataframe is returned, this tests also parse_json already

    Parameters
    ----------
    fetcher_instance : kmlFetcher
        kml fetcher instance
    """
    df, flag = fetcher_instance.load_data(
        url="https://offenedaten-konstanz.de/api/3/action/package_show?id=d3303376-77d7-4dba-bd6-c0194acb7ae21313"
    )
    # assert not isinstance(df, pandas.core.frame.DataFrame)
    assert flag == False
    assert len(df) == 0
