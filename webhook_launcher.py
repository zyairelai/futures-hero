import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = 'xxxxxxxxxxxxxxx'
    bot_chatID = 'xxxxxxxxxxxxx'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=html&text=' + bot_message
    response = requests.get(send_text)
    return response.json()
 
 


