from client import Client

class Operation:

    @staticmethod
    def create(url,data,token=None):
        return Client(
            url= url,
            method = "POST", 
            data = data,
            token =  token
        ).to_json()
    
    @staticmethod
    def get(url,id,token=None):
        return Client(
            url = url + id,
            method = "GET",
            token = token
        ).to_json()

class BaseResource():

    @classmethod
    def create(cls,data,token=None):
        return Operation.create(cls.URL,data,token)

    @classmethod
    def get(cls,id,toke=None):
        return Operation.get(cls.URL,id,token)


class AuthJwt(BaseResource):
    URL = "/gateway-ecommerce/v1/auth/login"

class TokenCard(BaseResource):
    URL = "/gateway-ecommerce/v1/token-card"

class CustomerTokens(BaseResource):
    URL = "/gateway-ecommerce/v1/token-card/customer-tokens"

class RiskManager(BaseResource):
    URL = "/gateway-ecommerce/v1/risk-manager/token-card"

class StoreApiKey(BaseResource):
    URL = "/gateway-ecommerce/v1/store/store-api-key"

class WebAuthorizer(BaseResource):
    URL = "/gateway-ecommerce/v2/checkout"

class Transaction(BaseResource):
    URL = "/gateway-ecommerce/v1/transaction/charge"

class TransactionRefund(BaseResource):
    URL = "/gateway-ecommerce/v1/transaction/refund"

class TokenCardDelete(BaseResource):
    URL = "/gateway-ecommerce/v1/token-card/delete"



    
