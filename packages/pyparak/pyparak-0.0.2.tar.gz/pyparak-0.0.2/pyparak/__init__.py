from zeep import Client

zarinpal_client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
zarinpal_merchant = 'Your Zarinpal Merchant'


class BaseGateway(object):
    def send(self):
        raise NotImplementedError()

    def verify(self):
        raise NotImplementedError()


class ZarinpalGateway(BaseGateway):
    def send(user, pk):
        result = zarinpal_client.service.PaymentRequest(
            zarinpal_merchant, user['amount'], user['description'], user['email'], user['mobile'],
            user['CallbackURL'] + str(pk))

        if result.Status == 100:
            return ('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return ('Error code: ' + str(result.Status))

    def verify(self, user):
        result = zarinpal_client.service.PaymentVerificationWithExtra(
            user['MERCHANT'], user['Authority'], user['amount'])

        if result.Status == 100:
            return True
        elif result.Status == 101:
            return ('Transaction submitted : ' + str(result.Status))
        else:
            return ('Transaction failed.\nStatus: ' + str(result.Status))
