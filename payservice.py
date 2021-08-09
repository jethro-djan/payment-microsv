from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_restful import Resource, Api
from decimal import *
from importlib import import_module

from models import Transaction, TransactionSchema
from services import chargeservice as cs

app = Flask(__name__)
sqldatabase = 'mysql://admin@localhost:3306/main'
# sqldatabase = 'sqlite:///tmp/main.db'
app.config.update(
    SQLALCHEMY_DATABASE_URI=sqldatabase,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy(app)
payservice = Api(app)

class Home(Resource):
    def __index(self):
        return 'index'

    def get(self):
        return self.__index()
    
class Payment(Resource):
    def __pay(self):
        credit_card = cs.CreditCard()
        CONSTANTS = import_module('services.constants')
        return credit_card.charge_credit_card(CONSTANTS.amount)

    def get(self):
        receipt = self.__pay()
        return receipt
        
class TransactionList(Resource):
    def __output(self):
        # initialize_database()
        transaction1 = Transaction(transaction_id='2321112', payment_amt='300')
        transaction2 = Transaction(transaction_id='1326792', payment_amt='422')
        transactions = [transaction1, transaction2]
        transactions_schema = TransactionSchema(many=True)
        json_result = transactions_schema.dumps(transactions)
        return json_result

    def get(self):
        return self.__output()

class PaymentBalance(Resource):
    def __get_balance(self):
        return 'Your balance is hehe' 

    def get(self):
        return self.__get_balance()

# Requested endpoints
payservice.add_resource(Home, '/')
payservice.add_resource(Payment, '/pay')
payservice.add_resource(TransactionList, '/transactions')
payservice.add_resource(PaymentBalance, '/balance')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)