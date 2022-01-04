import pytest
from .fetcher.txt_fetcher import txtFetcher


@pytest.fixture
def fetcher_instance() -> txtFetcher:
    """creates a instance of jsonFetcher

    Returns
    -------
    jsonFetcher
        instance of jsonFetcher
    """
    txt = txtFetcher()
    return txt


# currently no txt file on open data konstanz, add test as soon as new data is uploaded (21.12.2021)
