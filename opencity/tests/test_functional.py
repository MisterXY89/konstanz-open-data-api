from opencity import opencity as oc
from opencity import config as conf 


def test_functional_smoke(tmpdir):
    """Smoke Test

    Doesn't  actually test anything but
    catches errors including package setup errors.
    Requires the API to be available.
    """
    cf = conf.Config(PKG_FOLDER=str(tmpdir))
    open_city = oc.OpenCity(cf = cf,interactive=False)
    open_city.get_data(["radverkehr_stadtradeln"])
    
