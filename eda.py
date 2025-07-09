# # IMPORTING THE LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
#warnings.filterwarnings('ignore')

# Set plot style
sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

# LOADING THE DATASET 
df = pd.read_excel("Global YouTube Statistics.xlsx")  # replace with your filename

# PRINTING THE HEAD OF THE DATA
print(df.head())

# PRINTING THE STATS OF THE DATA
print("Shape:", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())
print("\nDescriptive Stats:\n", df.describe(include='all'))

# REMOVE COMMAS AND CONVERT NUMERIC COLUMNS TO APPROPRIATE DTYPES
num_cols = ['subscribers', 'video views', 'uploads', 'video_views_for_the_last_30_days',
            'lowest_monthly_earnings', 'highest_monthly_earnings',
            'lowest_yearly_earnings', 'highest_yearly_earnings',
            'subscribers_for_last_30_days', 'Population', 
            'Gross tertiary education enrollment (%)', 'Unemployment rate', 'Urban_population']

for col in num_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '').str.replace('$', '').str.replace('M', 'e6').str.replace('K', 'e3')
        df[col] = pd.to_numeric(df[col], errors='coerce')

# CONVERTING THE DATE FIELDS
df['created_date'] = pd.to_datetime(dict(year=df['created_year'], month=df['created_month'], day=1))

# TOP 10 YOUTUBERS BY SUBSCRIBERS
top_subs = df.sort_values(by='subscribers', ascending=False).head(10)
plt.figure()
sns.barplot(x='subscribers', y='Youtuber', data=top_subs, palette='viridis')
plt.title('Top 10 YouTubers by Subscribers')
plt.xlabel('Subscribers')
plt.ylabel('Youtuber')
plt.show()

# DISTRIBUTION PLOTS 
colors = ['#F60000', '#E80EB9', '#9E01E5']  # Custom Red, Pink, Purple
columns = ['subscribers', 'video views', 'uploads']

for i, col in enumerate(columns):
    if col in df.columns:
        sns.histplot(
            df[col].dropna(),
            kde=True,
            bins=30,
            color=colors[i],
            alpha=1.0,              # Full opacity
            edgecolor=colors[i],    # Match edge with fill for bold bars
            linewidth=1             # Optional: makes edges clear
        )
        plt.title(f'Distribution of {col}', fontsize=14)
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.show()

# COUNT OF YOUTUBERS PER CATEGORY with chocolate color
plt.figure(figsize=(10, 6))
sns.countplot(data=df, y='category', order=df['category'].value_counts().index, color='#6C4040')
plt.title('YouTubers per Category', fontsize=14)
plt.xlabel('Count')
plt.ylabel('Category')
plt.show()

# COUNTRY-WISE YOUTUBERS with RGB(255, 0, 102)
top_countries = df['Country'].value_counts().head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, color='#FF0066')  # Bright pinkish-red
plt.title('Top Countries by Number of YouTubers', fontsize=14)
plt.xlabel('Count')
plt.ylabel('Country')
plt.show()

# CORRELATION ANALYSIS
corr = df[num_cols].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

# TIME-BASED ANALYSIS
df['year'] = df['created_date'].dt.year
yearly_counts = df['year'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
plt.plot(
    yearly_counts.index,
    yearly_counts.values,
    marker='o',
    color='#00118E',   # Custom RGB color
    linewidth=2,
    markerfacecolor='#00118E'
)
plt.title('Number of Channels Created per Year', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Number of Channels')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# EARNINGS VS SUBSCRIBERS/VIEWS
sns.scatterplot(data=df, x='subscribers', y='highest_yearly_earnings', hue='category')
plt.title('Subscribers vs. Highest Yearly Earnings')
plt.xscale('log')
plt.yscale('log')
plt.show()

sns.scatterplot(data=df, x='video views', y='highest_monthly_earnings', hue='category')
plt.title('Views vs. Monthly Earnings')
plt.xscale('log')
plt.yscale('log')
plt.show()

# GEO PLOT (USING PLOTLY)
import plotly.express as px

fig = px.scatter_geo(df,
                     lat='Latitude',
                     lon='Longitude',
                     hover_name='Youtuber',
                     size='subscribers',
                     color='Country',
                     title='YouTubers Around the World')
fig.show()