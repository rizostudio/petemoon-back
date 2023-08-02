import requests
from django.contrib.auth import get_user_model
import json
from django.conf import settings
from payment.models import Transaction


User = get_user_model()

# def create_transaction(
#     user: User,
#     amount: int,
#     transaction_type: str,
#     description: str | None = None,
#     order: str | None = None,
# ) -> str:

#     """
#     create transaction
#         user: user object
#         amount: amount of transaction
#         transaction_type: type of transaction
#             order or wallet or vet
#         description: description of transaction optional
#         order: order object needed for transaction_type order
#     return: link to zarrinpal payment gateway
#     """
    
#     if transaction_type == "order":
#         assert (
#             order is not None
#         ), "order is required for transaction_type order"
#     else:
#         order = None
#     assert transaction_type in [
#         x[0] for x in Transaction.transaction_type_choices
#     ], "transaction_type must be one of these choices: " + str(
#         [x[0] for x in Transaction.transaction_type_choices]
#     )
#     transaction = Transaction.objects.create(
#         user=user,
#         amount=amount,
#         transaction_type=transaction_type,
#         description=description,
#         order=order,
#     )
#     response = requests.post(
#         f"{settings.ZARRINPAL_URL}v4/payment/request.json",
#         json={
#             "merchant_id": settings.ZARRINPAL_MERCHANT_ID,
#             "amount": amount,
#             "callback_url": "http:/127.0.0.1/payment/verify/"
#             + str(transaction.id)
#             + "/",
#             "description": description,
#             "metadata": {"mobile": user.phone_number},
#         },
#     )
#     data = json.dumps(response.content)

#     data = response.json()
#     status = data["errors"]["code"]
#     if status != 100:
#         raise Exception("error in zarrinpal gateway")
#     transaction.authority = data["data"]["authority"]
#     transaction.save()
#     return f"{settings.ZARRINPAL_URL}StartPay/{transaction.authority}"




def create_transaction(
    user: User,
    amount: int,
    transaction_type: str,
    description: str | None = None,
    order: str | None = None,
    #description: str = None,
    #order: str = None,
) -> str:

    transaction = Transaction.objects.create(
        user=user,
        amount=amount,
        transaction_type=transaction_type,
        description=description,
        order=order,
    )
    data = {
        "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
        "Amount": amount,
        "Description": description,
        "Phone": user.phone_number,
        "CallbackURL": settings.ZARIN_CALL_BACK
            + str(transaction.id)
            + "/",
        }

    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    try:
        response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                transaction.authority = response['Authority']
                transaction.save()
                data = { 'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']),'transaction': transaction.id, 'authority': response['Authority'] }
                return data
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


