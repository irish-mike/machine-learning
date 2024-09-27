import numpy as np
from numpy.ma.extras import average

from num_py.config.bike_constants import *
from num_py.config.common_constants import MONTH
from utils.utils import normalize, denormalize


class BikeRentalAnalysis:
    def __init__(self):
        self.data = np.genfromtxt('data/bike.csv', delimiter=',')
        pass

    def run_all(self):
        self.average_temperature()
        self.average_users()
        self.monthly_casual_users()
        self.average_users_for_temperature_range()

    def average_temperature(self):
        avg = denormalize(np.mean(self.data[:, TEMP_COL]), MAX_TEMP)
        print(f"(i) The average temperature is {avg:.2f}°C\n")

    def average_users(self):
        holiday_mask = self.data[:, HOLIDAY_COL] == 1
        non_holiday_mask = self.data[:, HOLIDAY_COL] == 0

        avg_holiday_users = int(np.mean(self.data[holiday_mask, TOTAL_COUNT_COL]))
        avg_non_holiday_users = int(np.mean(self.data[non_holiday_mask, TOTAL_COUNT_COL]))

        print(f"(ii) A: The average number of holiday users is {avg_holiday_users}\n")
        print(f"(ii) B: The average number of non-holiday users is {avg_non_holiday_users}\n")

    def monthly_casual_users(self):
        print(f"(iii) The total number of casual users monthly:\n")
        print(f"{'Month':<10} {'Casual Users':>15}")  # Header
        print("-" * 30)  # Separator

        # Loop through each month from January (1) to December (12)
        for i in range(1, 13):
            month_mask = self.data[:, MONTH_COL] == i
            total_casual_users = np.sum(self.data[month_mask, CASUAL_USERS_COL])

            # Print the month and the total casual users, formatted to ensure alignment
            print(f"{MONTH[i]:<10} {int(total_casual_users):>15}")

    def average_users_for_temperature_range(self):
        increment = 5
        print(f"{'\nTemperature Range':<20} {'Average Users':>15}")
        print("-" * 35)

        for i in range(1, 40, increment):
            upper = i + increment
            avg_users = self.__get_avg_users_for_temperature_range(i, upper)
            print(f"{i:2} °C - {upper:2}°C {avg_users:15.2f}")

    def __get_avg_users_for_temperature_range(self, lower, upper):
        lower = self.data[:, TEMP_COL] >= normalize(lower, MAX_TEMP)
        upper = self.data[:, TEMP_COL] <= normalize(upper, MAX_TEMP)
        return np.mean(self.data[lower & upper, TOTAL_COUNT_COL])