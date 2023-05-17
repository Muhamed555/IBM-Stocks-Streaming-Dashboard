python3 -m pip install plotly

import streamlit as st
import plotly
import plotly.graph_objs as go
import requests
import pandas as pd

def get_data():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame(data['Time Series (5min)']).T
    df = df.apply(pd.to_numeric)
    df = df.reset_index()
    df.columns = ['Time Series (5min)', 'open', 'high', 'low', 'close', 'volume']

    # Splitting the dictionary values in each row into separate columns
    df = pd.concat([df.drop(['Time Series (5min)'], axis=1), df['Time Series (5min)'].apply(pd.Series)], axis=1)
    df['time'] = df[0]
    df.drop(0, inplace=True, axis=1)

    # set the 'name' column as the index
    df['time2'] = df['time']
    df = df.set_index('time')

    return df

def plot_volume(df):
    st.bar_chart(df['volume'])

def plot_open_stocks(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time2'], y=df['open'], mode='lines', name='open'))
    fig.update_layout(title='IBM Open Stocks', xaxis_title='Time', yaxis_title='Open Stocks')

    st.plotly_chart(fig, width='50%')

def plot_close_stocks(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time2'], y=df['close'], mode='lines', name='Close'))
    fig.update_layout(title='IBM Close Stocks', xaxis_title='Time', yaxis_title='Close Stocks')

    st.plotly_chart(fig, width = '50%')

def plot_low_stocks(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time2'], y=df['low'], mode='lines', name='Low'))
    fig.update_layout(title='IBM Low Stocks', xaxis_title='Time', yaxis_title='Low Stocks')

    st.plotly_chart(fig, width = '50%')

def plot_high_stocks(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time2'], y=df['high'], mode='lines', name='high'))
    fig.update_layout(title='IBM High Stocks', xaxis_title='Time', yaxis_title='High Stocks')

    st.plotly_chart(fig, width = '50%')


st.set_page_config(
 layout='wide',
 page_title='Real time dashboard',
 page_icon='&'
)

st.title("IBM Stocks Real Time Dashboard")

df = get_data()


col1, col2 = st.columns(2)

with col1:
 delta = df['high'].pct_change() * 100
 st.metric(label="High", value=df['high'].iloc[-1], delta=delta.iloc[-1])

 delta = df['low'].pct_change() * 100
 st.metric(label="Low", value=df['low'].iloc[-1], delta=delta.iloc[-1])

with col2:
 delta = df['open'].pct_change() * 100
 st.metric(label="Open", value=df['open'].iloc[-1], delta=delta.iloc[-1])

 delta = df['close'].pct_change() * 100
 st.metric(label="Close", value=df['close'].iloc[-1], delta=delta.iloc[-1])


st.write(" ")
st.write(" ")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
with col1:
 plot_open_stocks(df)

with col2:
 plot_close_stocks(df)

with col3:
 plot_low_stocks(df)

with col4:
 plot_high_stocks(df)

st.bar_chart(df["volume"])
