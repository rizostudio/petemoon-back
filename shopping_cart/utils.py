import secrets
import string

from django.core.cache import cache
from django.db import transaction
from django.db.models import F
from config.exceptions import CustomException

def add_to_cart(user_id, cart):

    cache.set(f"cart-{user_id}", cart)


def get_cart(user_id):
    return cache.get(f"cart-{user_id}")


@transaction.atomic
def order_completion(total_price,user):
    if user.profile.wallet.credit < total_price:
        raise CustomException(detail=("total price is greater that wallet please charge it first")) 
    else:
        user.profile.wallet.credit = F('user.profile.wallet.credit') - F('total_price')
        cache.delete(f"cart-{user.id}")



def random_N_chars_str(n: int) -> string:
    return (''.join(secrets.choice(string.ascii_uppercase + string.digits + string.digits) for _ in range(n)))

