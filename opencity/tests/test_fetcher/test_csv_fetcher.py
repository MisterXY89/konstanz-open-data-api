# import pytest
# from fetcher.csv_fetcher import csvFetcher
# import pandas


# @pytest.fixture
# def fetcher_instance() -> csvFetcher:
#     """creates a instance of csvFetcher

#     Returns
#     -------
#     csvFetcher
#         instance of csvFetcher
#     """
#     csv = csvFetcher()
#     return csv


# def test_verify_df_correct(fetcher_instance):
#     df, flag_df = fetcher_instance.load_data(
#         url="https://offenedaten-konstanz.de/api/3/action/package_show?id=2c6ae437-883b-4395-9780-23a16edb6720"
#     )
#     flag = fetcher_instance.verify_df(
#         df1=df,
#         url="https://offenedaten-konstanz.de/api/3/action/package_show?id=2c6ae437-883b-4395-9780-23a16edb6720",
#         encoding="utf-8",
#         sep=";",
#     )
#     assert flag == True
#     assert flag == flag_df


# def test_load_data_correct(fetcher_instance):
#     """checks if data is really a pandas core frame, this tests also parse_csv already

#     Parameters
#     ----------
#     fetcher_instance : csvFetcher
#         csv fetcher instance
#     """
#     df, flag = fetcher_instance.load_data(
#         url="https://offenedaten-konstanz.de/api/3/action/package_show?id=2c6ae437-883b-4395-9780-23a16edb6720"
#     )
#     assert isinstance(df, pandas.core.frame.DataFrame)
#     assert flag == True
#     assert len(list(df)) != 0


# def test_load_data_wrong(fetcher_instance):
#     """checks if for a wrong url no dataframe is returned, this tests also parse_csv already

#     Parameters
#     ----------
#     fetcher_instance : csvFetcher
#         csv fetcher instance
#     """
#     df, flag = fetcher_instance.load_data(
#         url="https://offenedaten-konstanz.de/api/3/action/package_show?id=2c6ae437-883b-4395-9780-23a16edb61231310"
#     )
#     assert not isinstance(df, pandas.core.frame.DataFrame)
#     assert flag == False
#     assert len(list(df)) == 2
