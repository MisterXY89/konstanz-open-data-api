import pandas as pd
import xlrd

class xlsFetcher(object):
    """
    docstring tbd
    """

    def __init__(self):
        self.flag_final = False

    def verify_url(self, url):
        """
        check if an url belongs to offene-daten-konstanz.de
        """
        return "offenedaten-konstanz.de" in url

    def get_file_ending(self, url):
        """
        extract file ending from an url
        """
        return url.split(".")[::-1][0]

    def parse_xls(self, url):
        try:
            df = pd.read_excel(url, sheet_name=None)
            return df
        except:
            self.flag_final = True
            return pd.DataFrame()

    def load_data(self, url):

        if self.verify_url(url) and self.get_file_ending(url) == "xls":
            data = self.parse_xls(url)
        else:
            print(f"> 3rd-Party Url/Dataset detected and therefore skipped:\n> {url}")
        return data, self.flag_final

#url = "https://offenedaten-konstanz.de/sites/default/files/%C3%96ffentlichen%20M%C3%BClltonnen.xls"
#url = "https://offenedaten-konstanz.de/sites/default/files/Standorte_Parkh%C3%A4user.xls"
#url = "https://offenedaten-konstanz.de/sites/default/files/KLRG_Stadtteilgrenzen.xls"
url = "https://offenedaten-konstanz.de/sites/default/files/Fahrradmietsytsem_Konrad_TINK_0.xls"

dsf_xls = xlsFetcher()
result, flag = dsf_xls.load_data(url)
print(flag)
print(result)
