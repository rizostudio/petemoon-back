import requests
from django.contrib.auth import get_user_model

from config.settings import ZARRINPAL_MERCHANT_ID, ZARRINPAL_URL
from payment.models import Transaction

User = get_user_model()


def create_transaction(
    user: User,
    amount: int,
    transaction_type: str,
    description: str | None = None,
    order: str | None = None,
) -> str:

    """
    create transaction
        user: user object
        amount: amount of transaction
        transaction_type: type of transaction
            order or wallet or vet
        description: description of transaction optional
        order: order object needed for transaction_type order
    return: link to zarrinpal payment gateway
    """
    if transaction_type == "order":
        assert (
            order is not None
        ), "order is required for transaction_type order"
    else:
        order = None
    assert transaction_type in [
        x[0] for x in Transaction.transaction_type_choices
    ], "transaction_type must be one of these choices: " + str(
        [x[0] for x in Transaction.transaction_type_choices]
    )
    transaction = Transaction.objects.create(
        user=user,
        amount=amount,
        transaction_type=transaction_type,
        description=description,
        order=order,
    )
    response = requests.post(
        f"{ZARRINPAL_URL}v4/payment/request.json",
        json={
            "merchant_id": ZARRINPAL_MERCHANT_ID,
            "amount": amount,
            "callback_url": "https://api.petemoon.com/payment/verify/"
            + str(transaction.id)
            + "/",
            "description": description,
            "metadata": {"mobile": user.phone_number},
        },
    )
    data = response.json()
    status = data["errors"]["code"]
    if status != 100:
        raise Exception("error in zarrinpal gateway")
    transaction.authority = data["data"]["authority"]
    transaction.save()
    return f"{ZARRINPAL_URL}StartPay/{transaction.authority}"
