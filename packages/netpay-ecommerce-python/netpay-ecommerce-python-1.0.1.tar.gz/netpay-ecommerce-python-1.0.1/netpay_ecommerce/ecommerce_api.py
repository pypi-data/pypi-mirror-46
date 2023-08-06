from services.ecommerce import Service


class EcommerceApi(Service):

    def __init__(self, _user, _pass):
        print("user"+_user)
        Service.__init__(self, _user, _pass)

    def send(self):
        self._test()
        print('oli');
        return 'oli';