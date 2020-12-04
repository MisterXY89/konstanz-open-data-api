import pandas as pd


class jsonFetcher(object):
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

    def parse_json(self, url):
        try:
            df = pd.read_json(url)
            # TO DO : different encodings
            return df
        except:
            self.flag_final = True
            return pd.DataFrame()

    def load_data(self, url):

        if self.verify_url(url) and self.get_file_ending(url) == "json":
            data = self.parse_json(url)
        else:
            print(f"> 3rd-Party Url/Dataset detected and therefore skipped:\n> {url}")
        return data, self.flag_final

url = "https://offenedaten-konstanz.de/sites/default/files/Wahlbezirke-OB-Wahl-2020.json"


dsf_json = jsonFetcher()
result, flag = dsf_json.load_data(url)
print(flag)
print(result)


