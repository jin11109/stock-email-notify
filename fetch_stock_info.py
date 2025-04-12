import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from scipy.stats import percentileofscore
from dotenv import load_dotenv
import numpy as np

def fetch_stock_info(years_duration):
    api_token = os.environ.get('FINMIND_API_TOKEN')

    days_duration = years_duration * 365
    stock_id = '2330'
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=days_duration)).strftime('%Y-%m-%d')

    print(f'Request params : \n',
          f'    stock_id : {stock_id} \n' 
          f'    start_date : {start_date}, end_date : {end_date} \n', sep='')

    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanStockPrice",
        "data_id": stock_id,
        "start_date": start_date,
        "end_date": end_date,
        "token": api_token
    }
    data_price = requests.get(url, params=parameter)
    data_price = data_price.json()
    print(f'Fetch price info : {data_price["msg"]}, {data_price["status"]}')
    data_price = pd.DataFrame(data_price['data'])
    data_price['date'] = pd.to_datetime(data_price['date'])
    # print(data_price)

    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanStockPER",
        "data_id": stock_id,
        "start_date": start_date,
        "end_date": end_date,
        "token": api_token
    }
    data_PER = requests.get(url, params=parameter)
    data_PER = data_PER.json()
    print(f'Fetch PER info : {data_PER["msg"]}, {data_PER["status"]}')
    data_PER = pd.DataFrame(data_PER['data'])
    data_PER['date'] = pd.to_datetime(data_PER['date'])
    # print(data_PER)

    return data_price, data_PER

def process_data(data_price, data_PER, years_duration):
    latest_price = data_price.loc[data_price['date'].idxmax()]
    latest_PER = data_PER.loc[data_PER['date'].idxmax()]
    if latest_price['date'] != latest_PER['date']:
        print(f'Latest data ERROR : {latest_price["date"]} and {latest_PER["date"]}')
        os._exit(0)

    latest_EPS = float(latest_price['close']) / float(latest_PER['PER'])
    latest_close_price = float(latest_price['close'])
    PER_values = data_PER["PER"].dropna().to_list()

    lower_limit = round(latest_close_price * 0.9, 2)
    upper_limit = round(latest_close_price * 1.1, 2)

    prices = np.linspace(lower_limit, upper_limit, 20)
    prices = np.append(prices, latest_close_price)
    prices = np.sort(prices)

    html_output = f"""
    <div style="font-family: 'Noto Sans TC'; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
        <h2 style="color: #333;">📊 價格 vs PER 本益比位階</h2>
        <h3 style="color: #233;">    {years_duration} 年</h3>
        <div style="display: flex; flex-direction: row; flex-wrap: wrap; gap: 2px;">
    """

    for price in prices:
        per = price / latest_EPS
        percentile = percentileofscore(PER_values, per, kind='rank')

        r = int(255 * (percentile / 100))
        g = int(255 * (1 - percentile / 100))
        color = f"rgb({r},{g},80)"
        bar_height = percentile

        is_close = price == latest_close_price
        border = "3px solid #007bff" if is_close else "1px solid #ccc"
        background = "#e7f1ff" if is_close else "#fff"

        html_output += f"""
            <div style="background:{background}; border:{border}; border-radius:6px; padding:2px; width:40px; margin-right: 1px;">
                <div style="margin-bottom:4px;">
                    <strong style="color:#555; font-size: 12px; text-align:center;">
                        價：{price:.2f}<br>PER：{per:.2f}
                    </strong>
                </div>
                <div style="background:#eee; border-radius:4px; width:100%; height:150px; position:relative;">
                    <div style="height:{bar_height}%; background:{color}; width:100%; position:absolute; bottom:0; text-align:center; color:white; font-weight:bold; line-height:20px;">
                        {percentile:.1f}
                    </div>
                </div>
            </div>
        """

    html_output += "</div>"

    # print(html_output)
    return html_output

if __name__ == '__main__':
    load_dotenv()
    # data_price, data_PER = fetch_stock_info(years_duration=3)
    # print(process_data(data_price, data_PER, 3))
    data_price, data_PER = fetch_stock_info(years_duration=5)
    print(process_data(data_price, data_PER, 5))