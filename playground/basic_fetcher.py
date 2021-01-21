
import requests

class BasicFetcher:
    """
    BasicFetcher: functions as a parent class for
    all file-specific fetcher
    """

    def __init__(self):
        self.PACKAGE_BASE_URL = "https://offenedaten-konstanz.de/api/3/action/package_show?id="
        self.headers = {
            "User-Agent": "PythonOpenDataPackage/1.0"
        }

    def fetch_resource_urls(self, p_id):
        """
        yield
        """
        resp = requests.get(self.PACKAGE_BASE_URL + p_id, headers=self.headers)
        if resp.status_code == 200:
            resources = resp.json()["result"][0]["resources"]
            for resource in resources:
                yield resource["url"], resource["name"], resource["format"]
        return resp.status_code

    def get_file_ending(self, url):
        """
        extract file ending from an url
        """
        return url.split(".")[::-1][0].lower()
