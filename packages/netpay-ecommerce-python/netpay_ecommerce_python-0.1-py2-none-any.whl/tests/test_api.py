import unittest
import netpay_ecommerce

class BaseSetupTest(unittest.TestCase):

    client = netpay_ecommerce
    

    login_object = {
        'security': {
            "userName": "adrian@netpay.com",
            "password": "adm0n2"
        }
    }

    token_card_object = {
        "username": "adrian@netpay.com",
        "storeApiKey": "6kQui=_ZJ4r15GRT5ix7Pot_sCObk1WG",
        "customerCard": {
            "cardNumber": "4000000000000004",
            "expirationMonth": "01",
            "expirationYear":  "24",
            "cvv": "123",
            "cardType": "001",
            "cardHolderName": "John Doe"
        }
    }

    risk_manager_object = {  
        "storeApiKey":"6kQui=_ZJ4r15GRT5ix7Pot_sCObk1WG",
        "riskManager":{
            "promotion":"000000",
            "requestFraudService":{  
                "merchantReferenceCode":"14500049450000",
                "deviceFingerprintID":"086e46a7d7b0d22a8966feed39eefd1c881507939638",
                "bill":{  
                "city":"city",
                "country":"MX",
                "firstName":"mailto",
                "lastName":"mailto",
                "email":"accept@netpay.com.mx",
                "phoneNumber":"8110000011",
                "postalCode":"12345",
                "state":"state",
                "street1":"street 1",
                "street2":"street 2",
                "ipAddress":"10.0.0.1"
                },
                "ship":{  
                "city":"city ship",
                "country":"MX",
                "firstName":"mailto",
                "lastName":"mailto",
                "phoneNumber":"8110111111",
                "postalCode":"12345",
                "state":"state",
                "street1":"street 1",
                "street2":"street 2",
                "shippingMethod":"flatrate_flatrate"
                },
                "itemList":[{  
                    "id":"421",
                    "productSKU":"wbk012c-Royal Blue-S",
                    "unitPrice":"1.0000",
                    "productName":"Elizabeth Knit Top",
                    "quantity":1,
                    "productCode":"Tops & Blouses"
                }
                ],
                "card":{  
                "cardToken":"VW2FdHVU6BXGoiR99teVRKnuvIE897u7AMlh8MVHprBr4/LHIv6r7Nn0SwNEfsEfx8i7ngLOZyEL+eLsKoZCGg=="
                },
                "purchaseTotals":{  
                "grandTotalAmount":"6",
                "currency":"MXN"
                },
                "merchanDefinedDataList":[{  
                    "id":2,
                    "value":"Web"
                },{  
                    "id":4,
                    "value":"515"
                },{  
                    "id":5,
                    "value":"0"
                },{  
                    "id":6,
                    "value":"0"
                },{ 
                    "id":7,
                    "value":"0"
                },{  
                    "id":9,
                    "value":"Retail"
                },{  
                    "id":10,
                    "value":"3D"
                },{  
                    "id":11,
                    "value":"flatrate_flatrate"
                },{  
                    "id":13,
                    "value":"N"
                },{  
                    "id":14,
                    "value":"Domicilio"
                },{  
                    "id":"16",
                    "value":"50000"
                }]
            }
        }   
    }

    def get_jwt_token(self):
        response = netpay_ecommerce.AuthJwt.create(self.login_object)
        return response["token"]

    


class LoginTestCase(BaseSetupTest):

    def test_do_logint(self):
        response = self.client.AuthJwt.create(self.login_object.copy())
        assert "token" in response

