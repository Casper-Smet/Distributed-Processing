import requests
from functools import reduce
import pandas as pd


def get_holiday_range(region: str = "noord", selected_years: list = ["2019 - 2020", "2020 - 2021"]):
    """[summary]
    
    :param region: [description], defaults to "noord"
    :type region: str, optional
    :param selected_years: Note that after "2020 - 2021" there are no spaces between the years, defaults to ["2019 - 2020", "2020 - 2021"]
    :type selected_years: list, optional
    :return: [description]
    :rtype: [type]
    """
    parameters = {"output": "JSON"}

    url = r"https://opendata.rijksoverheid.nl/v1/sources/rijksoverheid/infotypes/schoolholidays"
    r = requests.get(url, params=parameters)

    # Note that after "2020 - 2021" there are no spaces between the years
    years = filter(lambda x: x.get("content")[0].get(
        "schoolyear").strip() in selected_years, r.json())

    vacations = map(lambda x: x.get("content")[0].get("vacations"), years)

    comp_regions = map(lambda y: [(x.get("compulsorydates"), filter(lambda z: z.get(
        "region") == region or z.get("region") == "heel Nederland", x.get("regions"))) for x in y], vacations)

    dates = map(lambda x: ([(compulsory == "true", [(date.get("startdate"), date.get(
        "enddate")) for date in dates][0]) for compulsory, dates in x]), comp_regions)
    dates3d = reduce(lambda x, y: x + y, dates)
    dates2d = [(x, y, z) for x, (y, z) in dates3d]

    df = pd.DataFrame(dates2d, columns=[
                      "Compulsory", "Start date", "End date"])

    df["Start date"] = pd.to_datetime(df["Start date"])
    df["End date"] = pd.to_datetime(df["End date"])

    iterator = df.iterrows()
    i, row = next(iterator)
    full_range = pd.date_range(start=row["Start date"], end=row["End date"]).to_series().append(
        [pd.date_range(start=row["Start date"], end=row["End date"]).to_series() for i, row in iterator])

    full_range = full_range.dt.date
    return full_range


def main():
    series = get_holiday_range()
    print(series)


if __name__ == "__main__":
    main()
