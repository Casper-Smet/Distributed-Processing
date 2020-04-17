import requests
from io import StringIO
import pandas as pd
from typing import List

YYYYMMDDHH = str
YY = str
MM = str
DD = str
HH = str


def data_dictionary():
    text = """DD	Windrichting (in graden) gemiddeld over de laatste 10 minuten van het afgelopen uur (360=noord, 90=oost, 180=zuid, 270=west, 0=windstil 990=veranderlijk. Zie http://www.knmi.nl/kennis-en-datacentrum/achtergrond/klimatologische-brochures-en-boeken
    FH	Uurgemiddelde windsnelheid (in 0.1 m/s). Zie http://www.knmi.nl/kennis-en-datacentrum/achtergrond/klimatologische-brochures-en-boeken
    FF	Windsnelheid (in 0.1 m/s) gemiddeld over de laatste 10 minuten van het afgelopen uur
    FX	Hoogste windstoot (in 0.1 m/s) over het afgelopen uurvak
    T	Temperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming
    T10N	Minimumtemperatuur (in 0.1 graden Celsius) op 10 cm hoogte in de afgelopen 6 uur
    TD	Dauwpuntstemperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming
    SQ	Duur van de zonneschijn (in 0.1 uren) per uurvak, berekend uit globale straling (-1 for <0.05 uur)
    Q	Globale straling (in J/cm2) per uurvak
    DR	Duur van de neerslag (in 0.1 uur) per uurvak
    RH	Uursom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm)
    P	Luchtdruk (in 0.1 hPa) herleid naar zeeniveau, tijdens de waarneming
    VV	Horizontaal zicht tijdens de waarneming (0=minder dan 100m, 1=100-200m, 2=200-300m,..., 49=4900-5000m, 50=5-6km, 56=6-7km, 57=7-8km, ..., 79=29-30km, 80=30-35km, 81=35-40km,..., 89=meer dan 70km)
    N	Bewolking (bedekkingsgraad van de bovenlucht in achtsten), tijdens de waarneming (9=bovenlucht onzichtbaar)
    U	Relatieve vochtigheid (in procenten) op 1.50 m hoogte tijdens de waarneming
    WW	Weercode (00-99), visueel(WW) of automatisch(WaWa) waargenomen, voor het actuele weer of het weer in het afgelopen uur. Zie http://bibliotheek.knmi.nl/scholierenpdf/weercodes_Nederland
    IX	Weercode indicator voor de wijze van waarnemen op een bemand of automatisch station (1=bemand gebruikmakend van code uit visuele waarnemingen, 2,3=bemand en weggelaten (geen belangrijk weersverschijnsel, geen gegevens), 4=automatisch en opgenomen (gebruikmakend van code uit visuele waarnemingen), 5,6=automatisch en weggelaten (geen belangrijk weersverschijnsel, geen gegevens), 7=automatisch gebruikmakend van code uit automatische waarnemingen)
    M	Mist 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming
    R	Regen 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming
    S	Sneeuw 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming
    O	Onweer 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming
    Y	IJsvorming 0=niet voorgekomen, 1=wel voorgekomen in het voorgaande uur en/of tijdens de waarneming
    WIND\t = DD:FH:FF:FX Wind
    TEMP\t = T:T10N:TD Temperatuur
    SUNR\t = SQ:Q Zonneschijnduur en globale straling
    PRCP\t = DR:RH Neerslag en potentiële verdamping
    VICL\t = VV:N:U Zicht, bewolking en relatieve vochtigheid
    WEER\t = M:R:S:O:Y:WW Weerverschijnselen, weertypen
    ALL\t alle variabelen"""

    data_dict = dict()
    for line in text.split("\n"):
        code, description, = line.split("\t")
        data_dict[code] = description

    return data_dict


def get_KNMI_HH(stations: List[str] = ["240"], vars_: List[str] = ["T", "R", "O", "S", "VV", "RH"], start: YYYYMMDDHH = None,
                end: YYYYMMDDHH = None, inseason: bool = False):
    """[summary]
    
    :param stations: [description], defaults to ["240"]
    :type stations: List[str], optional
    :param vars_: [description], defaults to ["T", "R", "O", "S", "VV", "RH"]
    :type vars_: List[str], optional
    :param start: [description], defaults to None
    :type start: YYYYMMDDHH, optional
    :param end: [description], defaults to None
    :type end: YYYYMMDDHH, optional
    :param inseason: [description], defaults to False
    :type inseason: bool, optional
    :return: [description]
    :rtype: [type]
    """

    parameters = dict()
    parameters["stns"] = ":".join(stations)
    parameters["vars"] = ":".join(vars_)

    if inseason and (start or end):
        parameters["inseason"] = "y"
        if start:
            byear, bmonth, bday = start[:4], start[4:6], start[6:8]
            parameters["byear"] = byear
            parameters["bmonth"] = bmonth
            parameters["bday"] = bday
        if end:
            eyear, emonth, eday = end[:4], end[4:6], end[6:8]
            parameters["eyear"] = eyear
            parameters["emonth"] = emonth
            parameters["eday"] = eday
    else:
        if start:
            parameters["start"] = start
        if end:
            parameters["end"] = end

    headers = ["Station", "Date", "Hour"] + vars_
    dtypes = {"Station": str, "Date": str, "Hour": int}

    url = r"http://projects.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi"
    response = requests.get(url, params=parameters)
    response.url
    output = StringIO(response.text)
    df = pd.read_csv(output, comment="#", names=headers, dtype=dtypes)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")

    return df


def main():
    df = get_KNMI_HH(inseason=True, start="2000050200", end="2002060123")
    print(df)
    print(data_dictionary)


data_dictionary = data_dictionary()

if __name__ == "__main__":
    main()
