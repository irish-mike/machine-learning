from contextlib import nullcontext

import numpy as np
from numpy.ma.extras import average

from num_py.config.common_constants import MONTH
from num_py.config.rainfall_constants import *
from utils.utils import print_rows


class RainfallAnalysis:

    def __init__(self):
        self.cork_data = np.genfromtxt("data/CorkRainfall.txt")
        self.dublin_data = np.genfromtxt("data/DublinRainfall.txt")

    def run_all(self):
        self.max_and_avg_rainfall()
        self.unique_years_and_rain_days()
        self.wettest_month()
        self.rain_days_threshold()
        self.average_seasonal_rainfall()
        self.total_average_rainfall()

    def max_and_avg_rainfall(self):
        max_rainfall_day_cork = np.max(self.cork_data[:, MOST_RAINFALL_DAY_COL])
        avg_rainfall_day_cork = np.average(self.cork_data[:, MOST_RAINFALL_DAY_COL])

        print(f"(i) A: Max rainfall in a day for Cork: {max_rainfall_day_cork:.2f}\n")
        print(f"(i) B: Average rainfall in a day for Cork: {avg_rainfall_day_cork:.2f}\n")

    def unique_years_and_rain_days(self):
        unique_years = np.unique(self.cork_data[:, YEAR_COL])
        print(f"(ii) A: Unique years for Cork:\n{unique_years}\n")

        year = int(input("Please input a year: "))
        matching_rows = self.cork_data[self.cork_data[:, YEAR_COL] == year]
        rain_days_for_year = int(np.sum(matching_rows[:, RAIN_DAYS_COL]))

        print(f"(ii) B: It rained {rain_days_for_year} days in {year}.\n")

    def wettest_month(self):
        # Get months as array
        months = self.cork_data[:, MONTH_COL].astype(int)

        # Get total rainfall as array
        total_rainfall = self.cork_data[:, TOTAL_RAINFALL_COL]

        # Map and sum them together
        total_rain_by_month = np.bincount(months, weights=total_rainfall)

        wettest_month = np.argmax(total_rain_by_month)
        most_rain = total_rain_by_month[wettest_month]

        print(f"(iii) The wettest month is {MONTH[wettest_month]} where it rained a total of {most_rain:.2f} ml\n")

    def rain_days_threshold(self):
        threshold = int(input("Please input a rain day threshold: "))

        # Get the rain days
        rain_days = self.cork_data[:, RAIN_DAYS_COL]

        # Get rows of rain days less than threshold
        rows_less_than_threshold = np.sum(rain_days < threshold)

        total_rows = self.cork_data.shape[0]
        percentage = (rows_less_than_threshold / total_rows) * 100

        print(f"(iv) The percentage of rows less than threshold is {percentage:.2f}%\n")

    def average_seasonal_rainfall(self):
        average_rainfall_summer = self.__average_rainfall_for_months(SUMMER_MONTHS)
        print(f"(v) A: The average rainfall for the Summer months is  {average_rainfall_summer:.2f} Ml\n")
        average_rainfall_autumn = self.__average_rainfall_for_months(AUTUMN_MONTHS)
        print(f"(v) B: The average rainfall for the Autumn months is  {average_rainfall_autumn:.2f} Ml\n")

    def total_average_rainfall(self):
        # Combine cork_data and dublin_data
        all_rainfall = np.concatenate((self.cork_data, self.dublin_data), axis=0)

        total_days = all_rainfall.shape[0]
        total_rain_days = np.sum(all_rainfall[:, RAIN_DAYS_COL])
        average_rain_days = total_rain_days / total_days

        print(f"(vi): The total average rain days is {average_rain_days:.2f}")

        np.savetxt(
            "data/all_rainfall.csv",
            all_rainfall,
            delimiter=",",
            fmt=['%d', '%d', '%.2f', '%.2f', '%d'],
        )

    def __average_rainfall_for_months(self, months):
        all_months = self.cork_data[:, MONTH_COL].astype(int)
        filtered = self.cork_data[np.isin(all_months, months)]
        total_rainfall = np.sum(filtered[:, TOTAL_RAINFALL_COL])
        matched_months_count = filtered.shape[0]
        return total_rainfall / matched_months_count

