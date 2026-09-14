import os
from dotenv import load_dotenv
from app import App

load_dotenv()

host = os.getenv('HOST')
port = os.getenv('PORT')
token = os.getenv('TOKEN')
webhookUrl = os.getenv('WEBHOOK_URL')
baseApiUrl = os.getenv('API_BASE_URL')

if __name__ == '__main__':
    app = App(token=token, webhook_url=webhookUrl, base_api_url=baseApiUrl)

    if host:
        app.host = host
    if port:
        app.port = port

    app.run()
