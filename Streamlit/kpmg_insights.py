import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as pxl
import plotly.express as px
import seaborn as sns
from ydata_profiling import ProfileReport
# %matplotlib inline

from matplotlib import pyplot as plt

import matplotlib.style as style




import requests
from matplotlib.figure import Figure


#sns.set_style('whitegrid')
style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1
dpi = 1000
plt.rcParams['font.size'] = 13
#plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
plt.rcParams['axes.titlesize'] = plt.rcParams['font.size']
plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['figure.figsize'] = 8, 8

# Use the non-interactive Agg backend, which is recommended as a
# thread-safe backend.
# See https://matplotlib.org/3.3.2/faq/howto_faq.html#working-with-threads.
import matplotlib as mpl
mpl.use("agg")

##############################################################################
# Workaround for the limited multi-threading support in matplotlib.
# Per the docs, we will avoid using `matplotlib.pyplot` for figures:
# https://matplotlib.org/3.3.2/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server.
# Moreover, we will guard all operations on the figure instances by the
# class-level lock in the Agg backend.
##############################################################################
from matplotlib.backends.backend_agg import RendererAgg
_lock = RendererAgg.lock


#st.beta_set_page_config(page_title="COVID19: EpiCenter for Disease Dynamics", 
#                    page_icon="signal",
#                    layout='centered',
#                    initial_sidebar_state='auto')
#@st.cache(suppress_st_warning=True)

st.title("KPMG - Reports and Insights")



# Load data
tra_df = pd.read_excel('kpmg_cleaned_dataset.xlsx',sheet_name="transactions")
cdg_df = pd.read_excel('kpmg_cleaned_dataset.xlsx',sheet_name="customer_demographic")
cad_df = pd.read_excel('kpmg_cleaned_dataset.xlsx',sheet_name="customer_address")


tra_df["profit"] = tra_df['list_price'] - tra_df['standard_cost']


# tra_df analysis
# Revenue Vs Product_size & Product line
fig = px.histogram(tra_df, x="product_line", y="list_price",
            color = 'product_size', barmode='group',
            labels=dict(list_price ="Revenue ($)"),
            height=500,
            title = "Revenue Vs Product line & product size"
            )

st.plotly_chart(fig)
st.markdown("\nThe graph shows revenue is distributed among the different product sizes. The sales of Standard bikes are high compared to other categories. The medium size bikes often popular in standard sozes bikes. The sales of large size bikes are high in Touring bikes compared to medium size bikes.Overall, this graph provides valuable insights into the sales performance of different product lines and the impact of product size on revenue.")

# Profit Vs Product_size & Product line
fig = px.histogram(tra_df, x="product_line", y="profit",
            color = 'product_size', barmode='group',
            labels=dict(profit ="Profit ($)"),
            height=500,
            title = "Profit Vs Product line & product size")

st.plotly_chart(fig)
st.markdown("\nThe graph is a representation of the relationship between the profit and the product line and product size of a certain company, wherein the profit from standard bikes is high than other category bikes. Standard medium size and large touring bikes makes profit in bikes categories")

# Profit Vs Product_size & Product line
fig = px.histogram(tra_df, x='online_order', y=["profit","list_price"],
                barmode='group',height=500, title = "Online_order Vs Revenue & Profit")

st.plotly_chart(fig)
st.markdown("This histogram compares the online_order/offline order and revenue (represented by list_price) and profit of a company, where 0 is offline order and 1 is online order")




# cdg_df analysis
# Last_3_years_purchase VS Wealth_segment & Gender
fig = px.histogram(cdg_df, x="wealth_segment", y="past_3_years_bike_related_purchases",
            color = "gender",
            barmode='group',
            height=500,
            title = "No of purchases in last 3 years Vs Gender & Wealth Segment "
            )
st.plotly_chart(fig)
st.markdown("\n This histogram represents the relationship between the number of bike-related purchases made in the last 3 years, wealth segment and gender. This graph provides an insight into how the number of bike-related purchases in the last 3 years is related to wealth segment and gender. It allows the user to see patterns and trends in the data and gain a better understanding of customer behavior.")


# cad_df Analysis
# Revenue Vs count customer_id & state
fig = px.histogram(cad_df, x="customer_id", y="state",
                
            labels=dict(x = "number of customers"),
            height=500,
            title = "Number of customers living in each state",
            histfunc = "count"
            )
st.plotly_chart(fig)
st.markdown("\nThe graph indicates that, customers from NSW(New South wales) state pourchase more bikes followed by VIC and QLD (Queensland) states.")


tra_cdg_df = pd.merge(tra_df, cdg_df, on='customer_id', how='inner')


# profit VS job_industry_category & wealth_segment
fig = px.box(tra_cdg_df, x="job_industry_category", y="profit", color="wealth_segment",
            title="profit VS job_industry_category & wealth_segment")
st.plotly_chart(fig)
st.markdown("\nhis graph shows profit and customer job categories with different wealth segment. By comparing the box plots for different job industry categories and wealth segment, we can make inferences about which job industries tend to be more profitable and which wealth segments tend to have higher profits.In this case, high net worth customer in Telecommunications category results to make more profit.")


# Revenue VS job_industry_category & wealth_segment
fig = px.box(tra_cdg_df, x="job_industry_category", y="list_price", color="wealth_segment",
            title="Revenue VS job_industry_category & wealth_segment")
st.plotly_chart(fig)
st.markdown("\nThe above graph indicates the revenue (List Price) segment and customer wealth segment with different job category, purchasing the bikes with listed price. In this case Affluent customer tends to purchase more bikes followed by Mass customer in Financial services and Affluent customer in Agriculture job categories.")


# profits by product line pie chart
fig = px.pie(tra_cdg_df, values='profit', names='wealth_segment', title="profit % by wealth_segment")
st.plotly_chart(fig)
st.markdown("\n Pie charts shows profit made by Mass customer is higher than Affluent and High net worth customer, resulting in half (50.1%) of the overall profit.")




# tra_df & cdg_df & cad_df merged
tra_cdg_df = pd.merge(tra_df, cdg_df, on='customer_id', how='inner')
tra_cdg_cad_df = pd.merge(tra_cdg_df, cad_df, on='customer_id', how='inner')
tra_cdg_cad_df = tra_cdg_cad_df.dropna()





# list_price vs standard_cost & product_line

fig = px.scatter(tra_cdg_cad_df, y="list_price", x="standard_cost", color = "product_line", title="list_price vs standard_cost & product_line")
st.plotly_chart(fig)
st.markdown("\nThe Scatter plot represents the list price of the product line bikes. The list prices of Standard bikes and road bikes ranges between low to very high prices. The Touring bikes and mountain bikes price ranges between average to very high.")


    

