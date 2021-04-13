import requests
import schedule
from bs4 import BeautifulSoup


def bot_send_text(bot_message):
    
    bot_token = '1740159617:AAF54njX4q8X7wXAA-stvcHmp_XL8-vq0L0'
    bot_chatID = '146321299'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response


def btc_scraping():
    url = requests.get('https://awebanalysis.com/es/coin-details/bitcoin/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('td', {'class': 'wbreak_word align-middle coin_price'})
    format_result = result.text

    return format_result


def report():
    btc_price = f'El precio de Bitcoin es de {btc_scraping()}'

    bot_send_text(btc_price)

if __name__ == '__main__':
        
    # schedule.every().day.at("11:27").do(report)
    schedule.every(1).minutes.do(report)

    while True:
        schedule.run_pending()