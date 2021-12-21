from opencity.API_helper import IdHelper
import pytest
from opencity.config import Config as cf
from opencity.fetch_dataset_list import DataSetUrlFetcher


@pytest.fixture
def id_helper(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    url_fetcher = DataSetUrlFetcher(cf)
    id_helper = IdHelper(url_fetcher)
    return id_helper


create_id_list_data = [
    (["einwohner"], ["591d86a9-9626-46af-8d93-a25da74040bc"]),
    (["abfallstatistik"], ["a47fac75-1d4d-4dc4-9b76-b400d483f73f"]),
]


@pytest.mark.parametrize(argnames="tag, id_", argvalues=create_id_list_data)
def test_create_id_list_correct_tag(id_helper, tag, id_):
    output = id_helper.create_id_list(data=tag)
    assert output[0] == id_
    assert output[1] == True


def test_create_id_list_wrong_tag(id_helper):
    output = id_helper.create_id_list(data=["test"])
    assert output[0] == []
    assert output[1] == False
