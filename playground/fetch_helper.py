
from config import PACKAGE_BASE_URL

class FetchHelper:
    def __init__(self):
        pass

    def fetch_dataset_urls(id):
        response = requests.get(PACKAGE_BASE_URL + id)
        if response.status_code == 200:
            resources = response.json()["result"][0]["resources"]
            for resource in resources:
                yield resource["url"], resource["format"], resource["name"]
        return response.status_code

    def get_url_ending(url):
        return url.split(".")[::-1][0].lower()

    def verify_url(self, url):
        """
        check if an url belongs to offenedaten-konstanz.de
        """
        return "offenedaten-konstanz.de" in url.lower()
