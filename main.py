from send_email import send_mail
from fetch_stock_info import fetch_stock_info, process_data
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    data_price, data_PER = fetch_stock_info()
    html_content = process_data(data_price=data_price, data_PER=data_PER, years_duration=3)
    html_content += process_data(data_price=data_price, data_PER=data_PER, years_duration=5)

    send_mail(html_content=html_content)
