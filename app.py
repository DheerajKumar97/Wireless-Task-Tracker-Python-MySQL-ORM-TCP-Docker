from flask import Flask
from flask_cors import CORS
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='wtt_logs.log',
                    filemode='a')

app = Flask(__name__)
from auth import route as auth_route
from card import route as card_route

CORS(app)
app.register_blueprint(auth_route.AUTH_BP)
app.register_blueprint(card_route.CARD_BP)



if __name__ == '__main__':
    app.run(port=8080,debug=True)
