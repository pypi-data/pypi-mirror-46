from zeep import Client

zarinpal_client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')


class BaseGateway(object):
    def send(self):
        raise NotImplementedError()

    def verify(self):
        raise NotImplementedError()


class ZarinpalGateway(BaseGateway):
    def send(user, pk):
        result = zarinpal_client.service.PaymentRequest(
            user['merchant'], user['amount'], user['description'], user['email'], user['mobile'],
            user['CallbackURL'] + str(pk))

        if result.Status == 100:
            return ('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return ('Error code: ' + str(result.Status))

    def verify(user):
        result = zarinpal_client.service.PaymentVerificationWithExtra(user['merchant'], user['authority'],
                                                                      user['amount'])

        if result.Status == 100:
            return True
        elif result.Status == 101:
            return ('Transaction submitted : ' + str(result.Status))
        else:
            return ('Transaction failed.\nStatus: ' + str(result.Status))
