
import pandas as pd
from csv_fetcher import csvFetcher

dsf = csvFetcher()

ids = [
    "https://offenedaten-konstanz.de/sites/default/files/Stromverbrauch%20Entsorgungsbetriebe%20Konstanz.csv",
    "https://offenedaten-konstanz.de/sites/default/files/FAHRPLAENE.csv",
    "https://offenedaten-konstanz.de/sites/default/files/FAHRTEN.csv",
    "https://offenedaten-konstanz.de/sites/default/files/Abfallplaner_M%C3%BCllabfuhrtermine_2020.csv",
    "https://offenedaten-konstanz.de/sites/default/files/FAHRWEGE.csv",
    "https://offenedaten-konstanz.de/sites/default/files/FIRMENKALENDER.csv",
    "https://opendata.arcgis.com/datasets/1697f3e6a9274f4db25de63f0e5444f3_1.csv",
    "https://opendata.arcgis.com/datasets/d6f1ebede298432ba7cee60946eef94c_1.csv",
    "https://offenedaten-konstanz.de/sites/default/files/VERBINDUNGEN_0.csv",
    "https://offenedaten-konstanz.de/sites/default/files/ORTE_0.csv",
    "https://offenedaten-konstanz.de/sites/default/files/Kl%C3%A4ranlage%20Konstanz%20und%20Umgebung_0.csv",
    "https://offenedaten-konstanz.de/sites/default/files/Gesamtnutzung%20Fahrrad-Mietsystem%20in%20den%20Jahren%202018%20und%202019.csv",
    "https://offenedaten-konstanz.de/sites/default/files/Anmietungen%20Fahrrad-Mietsystem%20konrad%20im%20Jahr%202018.csv",
    "https://offenedaten-konstanz.de/sites/default/files/Anmietungen%20Fahrrad-Mietsystem%20TINK%20im%20Jahr%202018.xlsx",
    "https://offenedaten-konstanz.de/sites/default/files/R%C3%BCckgaben%20Fahrrad-Mietsystem%20konrad%20im%20Jahr%202018.xlsx",
    "https://offenedaten-konstanz.de/sites/default/files/R%C3%BCckgaben%20Fahrrad-Mietsystem%20TINK%20im%20Jahr%202018.xlsx",
    "https://offenedaten-konstanz.de/sites/default/files/Fahrradabstellanlagen%202020_0.csv",
    "https://opendata.arcgis.com/datasets/6cbcc86045de4756a2de89f1c5736086_0.csv"


    # "dc37dce2-1550-4257-a896-e1056062b37c",
    # "b5ddf98d-52bc-4677-ad72-939192a5d5a9",
    # "67e37de3-ba6e-44fc-8e07-0884b1b4d61c",
    # "a47fac75-1d4d-4dc4-9b76-b400d483f73f",
    # "db8d5dc2-b740-45cf-9c42-c0fa8e271051",
    # "8743fd11-8f6b-46cb-8815-d942b9a45653"
]

for dataset_id in ids:
    # print(dataset_id)
    # print(50*"%")
    d,flag = dsf.load_data(dataset_id)
    print(f"{flag=}")
