#from PIL import Image
from functions import load_data, get_df, get_month,get_day,get_percentage,get_df_pv

import streamlit as st
import plotly.express as px

def main():

  # load data
  df = load_data()
  # obtain objects from data
  cc_names, df_minmax, col_pv = get_df(df)
  
  # Streamlit web
  st.set_page_config(layout='wide')

  # # Cryptocurrency image
  # row_0_spacer_1, row_0, row_0_spacer_2 = st.columns((0.1,1,0.1))
  # cc_image = Image.open('bitcoin.jpg')
  # with row_0:
  #     st.image(cc_image)
  # #''' image here'''

  # ROW 1: introduction
  row_1_spacer_1, row_1, row_1_spacer_2 = st.columns((0.1,1,0.1))

  row_1.title(":currency_exchange:Data Analysis: Historical Price of 23 Crypto-currencies")

  row_1.subheader(
      '''This App aims to provide various form of visualization, charts, graphs, and tables for you to analyze 23 crypto-currencies on the market. Some are well known to all, such as Bitcoin and Dogecoin, some are only popular among enthusiasts. Whether you are familiar with crypto-currencies or not, have fun with this simple dashboard!''')

  row_1.markdown(''':star2: For all charts, you are able to zoom in/out, and focus on a range of dates of your interest:star2:''')

  row_1.write(''':chart: Check the data source [here](https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory):chart:''')
  row_1.write(''':notebook_with_decorative_cover: Check Data Wrangling Notebook [here](https://nbviewer.org/github/honghusldl/cryptocurrency-dashboard/blob/main/preprocessing/data_wrangling.ipynb):notebook_with_decorative_cover:''')
  # divider
  row_1.markdown('---')

  # ROW 2: Life span table
  row_2_spacer_1, row_2_1,row_2_2, row_2_spacer_2 = st.columns((0.3,1.7,1.3,0.3))

  with row_2_1:
    st.subheader('Life Span')

    st.write(':bar_chart:Each crypto-currency has distinct life span. Here you can discover the life span for each currency')
    
    fig_bar_lifespan = st.plotly_chart(
      px.bar(data_frame=df_minmax,x=df_minmax.index,y='Duration', color=df_minmax.index,
      title='Duration on Market by Currency',hover_data=['First Day','Last Day'],height = 600,width=800,
      labels={'Duration':'Duration on Market in Days'}, text = 'Duration'
      ).update_traces(textposition = 'outside').update_layout(showlegend=False)
    )

  with row_2_2:
    st.write('')
    st.dataframe(data = df_minmax,height = 1000)
    st.write(':warning:The data source was update on 2021-7-6')

  st.write('---')

  # ROW 3: overview line chart market cap
  
  row_3_spacer_1, row_3_1,row_3_2, row_3_spacer_2 = st.columns((0.5,4,1,0.5))
  with row_3_2:
    st.subheader(':book:Capitalpedia')
    st.markdown(":ledger:***Market Capitalization*** is the total market value of the shares outstanding of a publicly traded cryptocurrency.")
    st.markdown(":ledger:It is equal to **share price** times **number of shares outstanding**.")
    st.markdown(":ledger:Market capitalization is one of the metrics to reflect the value of a cryptocurrency. It is even more useful for investors to understand the whole picture of a specific cryptocurrency since it leverages both volume and price. ")
    st.markdown(":ledger:Cryptocurrencies are categorized into three classes based on their market capitalization")
    st.markdown(":one:Large-cap cryptocurrencies: with over $10 billion market cap. Lower risks for investors.")
    st.markdown(":two:Mid-cap cryptocurrencies: with $1 to $10 billion market cap. Great growth potential but high risks.")
    st.markdown(":three:Small-cap cryptocurrencies: with less than $1 billion market cap. High risks due to massive volatility.([Reference](https://www.coinbase.com/learn/crypto-basics/what-is-market-cap))")

  with row_3_1:
    st.subheader('Overview: Market Capitalization')
    fig_line_cap = st.plotly_chart(
      px.line(data_frame=df, x='Date',y='Market_Capitalization',
      color='Name', width=1000, height=600,
      labels= {'Market_Capitalization':'Market Cap in USD','Volume':'Traded Volume'},template='seaborn'
      ).add_vline(x='2017-01-01',line_width = 3, line_dash = 'dot',line_color = 'red'
      ).add_annotation(x='2017-01-01',y=max(df['Market_Capitalization'])*0.85,text="'Cryptocurrency Fever' Began"
      ).update_layout(showlegend = False))

    st.markdown(''':bookmark:**PC Component Market**:bookmark:''')
    st.markdown('''After cryptocurrency went in vogue in the middle of 2017, well-prepared mining companies and the enthusiasm among the general public causes destructive fluctuation on market. 
      People have been forced to pay more than twice amount of money to hunt for a GPU. Majority of PC components rises in price due to shortage in supply. Used mining GPU are placed on market with a unresonable price.
      There are more and more disturbing the PC component market, especially GPU. ''')
   
  st.markdown('---')
  row_4_spacer_1, row_4_1,row_4_2, row_4_3, row_4_spacer_2 = st.columns((0.5,1,3,1,0.5))
  with row_4_1:
    st.markdown(':point_down:Choose Your Day of Interest')
    # get year, month, day for pie chart
    y = list(range(2017,2022))
    year = st.selectbox('Select Year', options=y)
    m = get_month(year)
    month = st.selectbox('Select Month',options=m)
    d = get_day(year,month)
    day = st.selectbox('Select Day',options=d)

    st.write(':bookmark:Dates range from 2017-1-1 to 2021-7-6.')

  with row_4_2:
    st.write('Due to limit of space, full information about percentages of market cap are showed via table :point_right: ')
    st.write("Percentage of Market Capitalization by Currency on a specific date after 2017 when the 'Fever' begun")
    target_date = f'{year}-{month}-{day}'
    fig_pie_cap = st.plotly_chart(
      px.pie(data_frame=df.query(f"Date == '{target_date}'"),values='Market_Capitalization',names='Name',height = 550
      ).update_traces(textposition='inside', textinfo='percent+label')
    )

    st.markdown("Higher percentage indicates that a cryptocurrency has higher total market value and stand strong in the crypto market. **However, as the line graph shown, market capitalization of a cryptocurrency could evaporate drastically due to market sentiment, societal responses and even governmental intervention.**")

  with row_4_3:
    df_percentage = df.query(f"Date == '{target_date}'")
    df_cap_percentage = get_percentage(df_percentage)
    st.dataframe(data = df_cap_percentage,height = 1000)

  st.write('---')

  row_5_spacer_1, row_5_1,row_5_spacer_2 = st.columns((0.2,1,0.2))
  # get df for analyzing price and volume
  df_pv = get_df_pv(df)

  with row_5_1:
    st.subheader('Price & Volume')
    st.write('Price and volume are two important metrics reflecting the value of a cryptocurrency. Compared to market capitalization, they depict a cryptocurrency from different angles.')
    st.markdown(':chart_with_upwards_trend:**Explore Opening price, Closing Price, Daily Highest and Lowest Price by selecting name of your interest.**')
  
  row_6_spacer_1, box1,box2,box3,row_6_spacer_2 = st.columns((0.6,1,1,1,0.6))
  with box1:
    currency_name = st.selectbox('Select Cryptocurrency',options=cc_names)
  with box2:
    price_type_line = st.selectbox('Select type of price (Line)',options = col_pv)
  with box3:
    price_type_bar = st.selectbox('Select type of price (Bar)',options = col_pv)
  
  row_7_spacer_1, row_7_1,row_7_spacer_2 = st.columns((0.2,1,0.2))
  with row_7_1:
    df_query = df_pv.query("Name == @currency_name")
    fig_line_price = st.plotly_chart(
      px.line(data_frame=df_pv.query("Name == @currency_name"),x='Date',y= price_type_line,
      labels={'High':'Highest Price in USD',
      'Low':'Lowest Price in USD',
      'Open':'Opening Price in USD',
      'Close':'Closing Price in USD'},
      height=500,width=1050
      ).add_bar(x=df_query['Date'],y=df_query[price_type_bar],name=price_type_bar
      ).update_layout(showlegend = False)
    )
    st.markdown(':chart_with_upwards_trend:**Explore Volume by specifiying the date.**')
  
  row_8_spacer_1, box4,box5,box6,row_8_spacer_2 = st.columns((0.6,1,1,1,0.6))
  with box4:
    y2 = list(range(2017,2022))
    year2 = st.selectbox('Select Year:', options=y2)
  with box5:
    m2 = get_month(year2)
    month2 = st.selectbox('Select Month:',options=m2)
  with box6:
    d2 = get_day(year2,month2)
    day2 = st.selectbox('Select Day:',options=d2)
  row_8_spacer_1, row_8_1,row_8_2,row_8_spacer_2 = st.columns((0.6,2,1,0.6))
  with row_8_1:
    target_date2 = f'{year2}-{month2}-{day2}'
    fig_bubble_volume = st.plotly_chart(
      px.scatter(data_frame = df_pv.query(f"Date == '{target_date2}'"),x='Close',y='Market_Capitalization',
      labels={'Close':'Closing Price','Market_Capitalization':'Market Capitalization'},
      size='Volume',color='Name',log_x=True,log_y=True,width=700,height=500)
    )
  with row_8_2:
    st.markdown(":warning:Note: The chart is applied with log transformation on both X and Y axis.")
    st.markdown(":books:Volume reflects activity or intensity of a cryptocurrency. In general, large volume indicates large number of participants in trading.")
    st.markdown(":books:Since volume reflects activity, it might reveal the characteristics of a cryptocurrency. For instance, Bitcoin requires high-end PC specification to solve math problems in blockchain, which makes Bitcoin finite in amount and time-comsuming. Thus, Bitcoin has higher value and attracts more participants on the market, resulting in larger volume.")
    st.markdown(":books:Volume fluctuates at various stages, and it is not necessarily correlated with price.")
    st.markdown(":books:As mentioned earlier, volume and price together are able to reveal the market's trend, hotspot and so on. Let's discover more about volume and price below!")
  
  row_9_spacer_1, row_9_1,row_9_2,row_9_3,row_9_spacer_2 = st.columns((0.6,1,1,1,0.6))
  with row_9_1:
    st.markdown(":chart_with_upwards_trend:**Explore Closing price and Volume Trend.**")
    currency_name_pv = st.selectbox('Select Cryptocurrency:',options = cc_names)
  
  row_10_spacer_1, row_10_1,row_10_2,row_10_spacer_2 = st.columns((0.8,3,1,0.8))
  with row_10_1:
    df_query2 = df_pv.query("Name == @currency_name_pv")
    fig_line_volume_price = st.plotly_chart(
      px.line(data_frame=df_query2.melt(id_vars=['Name','Date','High','Open','Low']),x='Date',y='value',color='variable',
      height=500,width=700,log_y=True)
    )






if __name__ == "__main__":
  main()
