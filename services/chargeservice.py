import imp

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import*
from decimal import*

import services.constants as CONSTANTS

class CreditCard:

    def charge_credit_card(self, amount):
        """
        Charge a credit card
        """
        self.amount = amount 

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = CONSTANTS.api_login_name
        merchantAuth.transactionKey = CONSTANTS.transaction_key

        # figure out how to make teh credit card info secure. for now hardcode the variables needed
        # creditCard = apicontractsv1.creditCardType()
        # creditCard.cardNumber = self.card_number 
        # creditCard.expirationDate = self.expiration_date
        # creditCard.cardCode = self.card_code

        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = "4111111111111111"
        creditCard.expirationDate = "2035-12"
        creditCard.cardCode = "123"

        
        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        order = apicontractsv1.orderType()
        order.invoiceNumber = "10101"
        order.description = "Golf Shirts"

        customerAddress = apicontractsv1.customerAddressType()
        customerAddress.firstName = "Ellen"
        customerAddress.lastName = "Johnson"
        customerAddress.company = "Souveniropolis"
        customerAddress.address = "14 Main Street"
        customerAddress.city = "Pecan Springs"
        customerAddress.state = "TX"
        customerAddress.zip = "44628"
        customerAddress.country = "USA"

        customerData = apicontractsv1.customerDataType()
        customerData.type = "individual"
        customerData.id = "99999456654"
        customerData.email = "EllenJohnson@example.com"

        duplicateWindowSetting = apicontractsv1.settingType()
        duplicateWindowSetting.settingName = "duplicateWindow"
        duplicateWindowSetting.settingValue = "600"
        settings = apicontractsv1.ArrayOfSetting()
        settings.setting.append(duplicateWindowSetting)

        line_item_1 = apicontractsv1.lineItemType()
        line_item_1.itemId = "12345"
        line_item_1.name = "first"
        line_item_1.description = "Here's the first line item"
        line_item_1.quantity = "2"
        line_item_1.unitPrice = "12.95"
        line_item_2 = apicontractsv1.lineItemType()
        line_item_2.itemId = "67890"
        line_item_2.name = "second"
        line_item_2.description = "Here's the second line item"
        line_item_2.quantity = "3"
        line_item_2.unitPrice = "7.95"

        line_items = apicontractsv1.ArrayOfLineItem()
        line_items.lineItem.append(line_item_1)
        line_items.lineItem.append(line_item_2)

        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authCaptureTransaction"
        transactionrequest.amount = self.amount
        transactionrequest.payment = payment
        transactionrequest.order = order
        transactionrequest.billTo = customerAddress
        transactionrequest.customer = customerData
        transactionrequest.transactionSettings = settings
        transactionrequest.lineItems = line_items

        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId = "MerchantID-0001"
        createtransactionrequest.transactionRequest = transactionrequest

        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()
        
        response = createtransactioncontroller.getresponse()

        if response is not None:
        # Check to see if the API request was successfully received and acted upon
            if response.messages.resultCode == "Ok":
        # Since the API request was successful, look for a transaction response
        # and parse it to display the results of authorizing the card
                if hasattr(response.transactionResponse, 'messages') is True:
                    print('Successfully created transaction with Transaction ID: {}'.format(response.transactionResponse.transId))
                    print('Transaction Response Code: {}'.format(response.transactionResponse.responseCode))
                    print('Message Code: {}'.format(response.transactionResponse.messages.message[0].code))
                    print('Description: {}'.format(response.transactionResponse.messages.message[0].description))
                else:
                    print('Failed Transaction.')
                    if hasattr(response.transactionResponse, 'errors') is True:
                        print('Error Code:  {}'.format(response.transactionResponse.errors.error[0].errorCode))
                        print(
                            'Error message: {}'.format(response.transactionResponse.errors.error[0].errorText))
            # Or, print errors if the API request wasn't successful
            else:
                print('Failed Transaction.')
                if hasattr(response, 'transactionResponse') is True and hasattr(
                        response.transactionResponse, 'errors') is True:
                    print('Error Code: {}'.format(response.transactionResponse.errors.error[0].errorCode))
                    print('Error message: {}'.format(response.transactionResponse.errors.error[0].errorText))
                else:
                    print('Error Code: {}'.format(response.messages.message[0]['code'].text))
                    print('Error message: {}'.format(response.messages.message[0]['text'].text))
        else:
            print('Null Response.')

        return response

        # if (os.path.basename(__file__) == os.path.basename(sys.argv[0])):
        # charge_credit_card(CONSTANTS.amount)
        
        # if (response.messages.resultCode=="Ok"):
        #     print('Transaction ID : {}'.format(response.transactionResponse.transId))
        # else:
        #     print('response code: {}'.format(response.messages.resultCode))

class MomoPay:

    def charge_momo_account(self, momoName, momoNumber):
        self.momo_name = momoName
        self.momo_number = momoNumber

# card_number = "4111111111111111"
# expiration_date = "2020-12"
# amount = Decimal('13.37') 
# merchant_id = "Pied-Piper"

def generateTransactionId():
    pass 
