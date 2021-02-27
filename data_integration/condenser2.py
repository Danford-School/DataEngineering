import pandas as pd
import csv


data = pd.read_csv("acs2017_census_tract_data.csv")

state = None
county_compare = None
sum_totalpop = 0
sum_men = 0
sum_women = 0
sum_hispanic = 0
sum_white = 0
sum_black = 0
sum_native = 0
sum_asian = 0
sum_pacific = 0
sum_income = 0
sum_incomeErr = 0
sum_incomePerCap = 0
sum_incomePerCapErr = 0
sum_poverty = 0

once = False

for rows in data:
    county = data['County'].values
    for count in county:
        with open("condensed_data.csv", mode="a") as output:
            writer = csv.writer(output)
            if not once:
                writer.writerow(['county', 'total_population', 'men', 'women', 'hispanic', 'white', 'black', 'native', 'asian', 'pacific', 'income', 'incomeErr', 'incomePerCap', 'incomePerCapErr', 'poverty'])
                once = True
                continue

    sum_totalpop = data["TotalPop"].groupby(data["County"]).sum()
    sum_men = data(["Men"]).groupby(data["County"]).sum()
    sum_women = data["Women"].groupby(data["County"]).sum()
    sum_hispanic += data["Hispanic"].groupby(data["County"]).sum()
    sum_white += data["White"].groupby(data["County"]).sum()
    sum_black += data["Black"].groupby(data["County"]).sum()
    sum_native += data["Native"].groupby(data["County"]).sum()
    sum_asian += data["Asian"].groupby(data["County"]).sum()
    sum_pacific += data["Pacific"].groupby(data["County"]).sum()
    sum_income += data["Income"].groupby(data["County"]).sum()
    sum_incomeErr += data["IncomeErr"].groupby(data["County"]).sum()
    sum_incomePerCap += data["IncomePerCap"].groupby(data["County"]).sum()
    sum_incomePerCapErr += data["IncomePerCapErr"].groupby(data["County"]).sum()
    sum_poverty += data["Poverty"].groupby(data["County"]).sum()

    with open("condensed_data.csv", mode="a") as output:
        writer = csv.writer(output)
        writer.writerow([county_compare, sum_totalpop, sum_men, sum_women, sum_hispanic, sum_white, sum_black, sum_native, sum_asian, sum_pacific, sum_income, sum_incomeErr, sum_incomePerCap, sum_incomePerCapErr, sum_poverty])
