import pandas as pd
from urllib.request import urlopen
import re

class txt(object):
    """
    docstring tba
    """
    def __init__(self):
        self.encoding_type = "utf-8"  # default encoding

    def get_data(self, url):

        file = urlopen(url)
        lines_list = []

        first_line = file.readline().decode(self.encoding_type)  # TO DO: idiotensicher machen bzgl encoding
        if re.findall("encoding", first_line):
            for i in re.finditer("encoding", first_line):
                text = first_line[i.end():]
                self.encoding_type = str(re.findall('"([^"]*)"', text)).strip('[]')
                #self.encoding_type = str(self.encoding_type).strip('[]')
        else:
            for quoted_part in re.findall(r'\"(.+?)\"', first_line):
                first_line = first_line.replace(quoted_part, quoted_part.replace(" ", "@"))
            split_lines = first_line.split(' ')
            lines_list.append(split_lines)

        for line in file:  # starts at second line
            decoded_line = line.decode(self.encoding_type)
            for quoted_part in re.findall(r'\"(.*?)\"', decoded_line):  # replace 'space' in quotes with '@'
                decoded_line = decoded_line.replace(quoted_part, quoted_part.replace(" ", "@"))
            split_lines = decoded_line.split(' ')
            for i in range(len(split_lines)):
                for quoted_part in re.findall(r'\"(.*?)\"', split_lines[i]):  # replace '@' in quotes with 'space'
                    split_lines[i] = split_lines[i].replace(quoted_part, quoted_part.replace("@", " "))
            lines_list.append(split_lines)

        return lines_list

    def convert_df(self, data):

        #data = self.get_data(url)
        df = pd.DataFrame(data)
        df = df.drop(df.columns[0], axis=1)  # drop first column
        row, col = df.shape
        col_name_ref = ''  # default value
        col_names = []

        for j in range(col):  # get col names and extract values

            for i in range(row):

                if i == 0:
                    col_name_ref = df.iloc[i, j].split("=")[0]

                split_element = df.iloc[i, j].split("=")
                col_name = split_element[0]

                if j == (col - 1):
                    value = split_element[1].split("/>")[0][1:-1]
                else:
                    value = split_element[1][1:-1]

                if col_name_ref != col_name:
                    print("ERROR: COLS")  # TO DO: Throw Error as col names do mismatch

                if value == "":
                    df.iloc[i, j] = "NaN"
                else:
                    df.iloc[i, j] = value

            col_names.append(col_name_ref)

        df.columns = col_names

        return df

    def load_data(self, url):

        data = self.get_data(url)
        return self.convert_df(data)

url = "https://offenedaten-konstanz.de/sites/default/files/FAHRPLAENE.txt"
#url = "https://offenedaten-konstanz.de/sites/default/files/FAHRTEN.Txt" # dauert ca 1 min
#url = "https://offenedaten-konstanz.de/sites/default/files/FAHRTHALTEZEITEN.txt"
#url = "https://offenedaten-konstanz.de/sites/default/files/FAHRWEGE.txt"
#url = "https://offenedaten-konstanz.de/sites/default/files/FAHRZEITEN.txt"
#url = "https://offenedaten-konstanz.de/sites/default/files/FIRMENKALENDER.txt"
#url = "https://offenedaten-konstanz.de/sites/default/files/LINIEN.txt"
#url = "https://offenedaten-konstanz.de/sites/default/files/ORTE.txt"
#url = "https://offenedaten-konstanz.de/sites/default/files/VERBINDUNGEN.txt"

dsf_txt = txt()
end_product = dsf_txt.load_data(url)
print(end_product)