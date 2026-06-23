# Import necessary libraries
import pandas as pd

# Load the data
businesses = pd.read_csv("Oldest Business/data/businesses.csv")
new_businesses = pd.read_csv("Oldest Business/data/new_businesses.csv")
countries = pd.read_csv("Oldest Business/data/countries.csv")
categories = pd.read_csv("Oldest Business/data/categories.csv")

print(businesses.head())
print(new_businesses.head())
print(countries.head())
print(categories.head())

#What is the oldest business on each continent? Save your answer as a DataFrame called oldest_business_continent with four columns: 
# continent, country, business, and year_founded in any order.
first_dataset= pd.merge(businesses,countries,on="country_code")
print(first_dataset.head())
print(first_dataset.groupby('continent')['year_founded'].min())
print(first_dataset.loc[first_dataset.groupby("continent")["year_founded"].idxmin(), ["continent", "country", "business", "year_founded"]])

oldest_business_continent= first_dataset.loc[first_dataset.groupby("continent")["year_founded"].idxmin(), ["continent", "country", "business", "year_founded"]]

#How many countries per continent lack data on the oldest businesses? Does including new_businesses change this? 
# Count the number of countries per continent missing business data, including new_businesses, and store the results in a DataFrame named 
# count_missing with columns for the continent and the count.
print(first_dataset.head())
print(first_dataset.loc[first_dataset["year_founded"].isna()])
print(first_dataset.loc[first_dataset["category_code"].isna()])
print(first_dataset.loc[first_dataset["business"].isna(), ["continent", "country", "business"]])

# Combine datasets
all_businesses = pd.concat([businesses, new_businesses], ignore_index=True)
countries_businesses = pd.merge(
    countries,
    all_businesses,
    on="country_code",
    how="left",
    indicator=True
)

print(all_businesses)

# Count missing business data by continent
count_missing = (
    countries_businesses.loc[
        countries_businesses["business"].isna()
    ]
    .groupby("continent")
    .size()
    .reset_index(name="count")
)

print(count_missing)


#Which business categories are best suited to last many years, and on what continent are they? Create a DataFrame called 
# oldest_by_continent_category that stores the oldest founding year for each continent and category combination. It should contain three columns:
# continent, category, and year_founded, in that order.
second_dataset = (
    pd.merge(all_businesses, countries, on="country_code")
      .merge(categories, on="category_code")
)
print(second_dataset)

print(second_dataset.loc[second_dataset.groupby(["continent","category"])["year_founded"].idxmin(), ["continent", "category", "year_founded"]])
oldest_by_continent_category = (
    second_dataset
    .groupby(["continent", "category"], as_index=False)["year_founded"]
    .min()
)

oldest_by_continent_category = (
    oldest_by_continent_category
    .sort_values(["continent", "year_founded"])
)