import pandas as pd

import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.preprocessing import OneHotEncoder, LabelEncoder, MinMaxScaler

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/content/drive/MyDrive/DA DS/Modeled_mobile.csv')

df.shape

df.columns

df.info()

df.describe(include='all')

# Visualizing the Count of Mobile Phones by Brand

brand_counts = df['Brand'].value_counts().reset_index()
brand_counts.columns = ['Brand', 'Count']
fig = px.bar(brand_counts, x='Brand', y='Count', title='Mobile Phone Count by Brand')
fig.update_xaxes(categoryorder='total descending')
fig.update_layout(xaxis_title='Brand', yaxis_title='Count')
fig.show()

# Visualizing Brand Popularity Based on Popularity Score

df['PopularityScore'] = df['ProductRating'] * df['Num_Ratings'] * df['Num_Reviews']
brand_popularity = df.groupby('Brand')['PopularityScore'].sum().reset_index()
fig = px.bar(brand_popularity, x='Brand', y='PopularityScore', title='Brand Popularity based on PopularityScore')
fig.update_xaxes(categoryorder='total descending')
fig.update_layout(xaxis_title='Brand', yaxis_title='Popularity Score')
fig.show()

# Visualizing the Most Expensive Phones in Each Brand

most_expensive_phones = df.groupby('Brand')['DiscountPrice'].max().reset_index()
most_expensive_phones = df.merge(most_expensive_phones, on=['Brand', 'DiscountPrice'])
fig = px.bar(most_expensive_phones, x='Brand', y='DiscountPrice',
             title='Most Expensive Phones in Every Brand',
             labels={'DiscountPrice': 'Discounted Price'},
             text='PhoneModel')
fig.update_xaxes(categoryorder='total descending')  # Order brands by price
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.show()

# Visualizing the Most Cheapest Phones in Each Brand

cheapest_phones = df.groupby('Brand')['DiscountPrice'].min().reset_index()
cheapest_phones = df.merge(cheapest_phones, on=['Brand', 'DiscountPrice'])
fig = px.bar(cheapest_phones, x='Brand', y='DiscountPrice',
             title='Most Cheapest Phones in Every Brand',
             labels={'DiscountPrice': 'Discounted Price'},
             text='PhoneModel')
fig.update_xaxes(categoryorder='total ascending')  # Order brands by price in ascending order
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.show()

# Identifying and printing Categorical and Numeric columns in a DataFrame

categorical_columns = df.select_dtypes(include=['object']).columns
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

print("Categorical columns:")
print(categorical_columns)

print("\nNumeric columns:")
print(numeric_columns)

# Transform the availability column from categorical columns to numerical columns using OneHotEncoder

onehot_encoder = OneHotEncoder()
availability = onehot_encoder.fit_transform(df[['availability']])

onehot_df = pd.DataFrame(availability.toarray(), columns=onehot_encoder.get_feature_names_out(['availability']))

df = pd.concat([df, onehot_df], axis=1)

df.drop('availability', axis=1, inplace=True)

# Transform the categorical columns to numerical columns using LabelEncoder

categorical_col = ['Brand', 'PhoneModel', 'PhoneColor', 'Display', 'Camera', 'Battery', 'Processor']

label_encoder = LabelEncoder()
for column in categorical_col:
    df[column] = label_encoder.fit_transform(df[column])

# Feature Scaling using MinMaxScaler

columns_to_scale = ['NetworkType', 'ProductRating', 'DiscountPrice', 'OriginalPrice', 'Discount', 'Num_Ratings', 'Num_Reviews', 'RAM', 'ROM', 'Expandable']
scaler = MinMaxScaler()
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
