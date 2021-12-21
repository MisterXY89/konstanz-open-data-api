from typing import overload
from opencity import opencity
import pytest
from pandas import DataFrame


@pytest.fixture
def opencity_instance(monkeypatch) -> opencity.OpenCity:
    monkeypatch.setattr("builtins.input", lambda _: "y")
    open_city = opencity.OpenCity()
    return open_city


@pytest.fixture
def current_list(opencity_instance):
    df = opencity_instance.id_helper.current_list
    return df


def test_without_arguments(capfd, opencity_instance, current_list) -> None:
    """This test checks whether show_data without arguments print an overview about the number of datasets and output categories, but nothing else

    Parameters
    ----------
    capfd : [type]
        pytest fixture for output check
    opencity_instance : [type]
        pytest fixture with opencity object
    """
    opencity_instance.show_data()
    out, err = capfd.readouterr()
    assert (
        "There are in total"
        and "different categories"
        and len(current_list)
        and "These categories are" in out
    )
    assert "Title" not in out


def test_overview_true(capfd, opencity_instance, current_list) -> None:
    """checks if output with parameter overview = True only prints Title, Shortname and Tags

    Parameters
    ----------
    capfd : [type]
        [description]
    opencity_instance : [type]
        [description]
    """
    opencity_instance.show_data(overview=True)
    out, err = capfd.readouterr()
    assert "Title" and "Shortname" and "Tags" and str(len(current_list) - 1) in out


@pytest.mark.parametrize(
    argnames="df_",
    argvalues=[
        "einwohner",
        "abfallstatistik",
    ],
)
def test_overview_true_data(capfd, opencity_instance, current_list, df_) -> None:
    """checks if output with parameter overview = True and given certain dataset prints Title, Shortname and Tags only for the the given datasets

    Parameters
    ----------
    capfd : [type]
        [description]
    opencity_instance : [type]
        [description]
    """

    opencity_instance.show_data(overview=True, data=[df_])
    df = current_list[current_list["name"] == df_]
    indexes = df.index.tolist()
    out, err = capfd.readouterr()
    assert df_ in out
    assert "Title" and "Shortname" and "Tags" in out
    assert len(indexes) == 1  # check for next line
    assert str(indexes[0]) in out


@pytest.mark.parametrize(
    argnames="tags_",
    argvalues=["Politik und Wahlen", "Bildung und Wissenschaft", "Soziales"],
)
def test_tag(capfd, opencity_instance, current_list, tags_):
    """checks if output with parameter overview = True and Tag = True + given tag list prints Title, Shortname and Tags only for the given Tag

    Parameters
    ----------
    capfd : [type]
        [description]
    opencity_instance : [type]
        [description]
    curren_list : [type]
        [description]
    tags_ : [type]
        [description]
    """
    opencity_instance.show_data(overview=True, data=[tags_], tag=True)
    out, err = capfd.readouterr()
    indexes = current_list[current_list["tags"] == tags_].index.tolist()
    for index in indexes:
        assert str(index) in out
    assert "Title" and "Shortname" and "Tags" in out
    assert tags_ in out
    assert "Gesetze und Justiz" not in out


# def test_meta_true(capfd, opencity_instance, current_list):
#     opencity_instance.show_data(meta=True)
#     out, err = capfd.readouterr()
#     assert (
#         "There are in total"
#         and "different categories"
#         and len(current_list)
#         and "These categories are" in out
#         and "In the following popup you will see detailed information on all the datasets:"
#     )
#     assert "Title" not in out


def test_wrong_only_data(capfd, opencity_instance):
    opencity_instance.show_data(data=["einwohner"])
    out, err = capfd.readouterr()
    assert "You did not use the function correctly" in out


def test_wrong_no_overview(capfd, opencity_instance):
    opencity_instance.show_data(data=["einwohner"], tag=True)
    out, err = capfd.readouterr()
    assert "You did not use the function correctly" in out


def test_wrong_data_name(capfd, opencity_instance):
    opencity_instance.show_data(overview=True, data=["eiwohner"])
    out, err = capfd.readouterr()
    assert "The provided names or tags are incorrect" in out
