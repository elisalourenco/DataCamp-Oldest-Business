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


all_businesses = pd.concat([businesses, new_businesses], ignore_index=True)
print(len(businesses) + len(new_businesses) == len(all_businesses))

businesses_countries = all_businesses.merge(countries, on='country_code', how='left')
businesses_countries.head()

df = businesses_countries.merge(categories, on='category_code', how='left')
df.head()

#question 1
df_small_reordered = df[['continent', 'country', 'business', 'year_founded']]
oldest_business_continent = df_small_reordered.loc[df_small_reordered.groupby('continent')['year_founded'].idxmin()]
print(oldest_business_continent)

#question 2
business_country = businesses.merge(countries, on= 'country_code', how = 'outer', indicator=True)
count_not_in_both = business_country[business_country['_merge'] != 'both']
count_missing_pre = pd.DataFrame(count_not_in_both.groupby('continent').agg({'country': 'count'}))
count_missing_pre.columns = ['count_missing']
print(count_missing_pre)

all_business_country = all_businesses.merge(countries, on= 'country_code', how = 'outer', indicator=True)
all_count_not_in_both = all_business_country[all_business_country['_merge'] != 'both']
count_missing = pd.DataFrame(all_count_not_in_both.groupby('continent').agg({'country': 'count'}))
count_missing.columns = ['count_missing']
print(count_missing)
print(count_missing == count_missing_pre)

print(count_missing)

#question 3
bus_count_cat = business_country.merge(categories, on='category_code', how='left')
oldest_by_continent_category = bus_count_cat.groupby(['continent', 'category']).agg({'year_founded': 'min'})
print(oldest_by_continent_category)
print(oldest_by_continent_category.shape)
