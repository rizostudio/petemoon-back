from django.core.cache import cache


def add_to_cart(user_id, product_id, product_count):
    cart = cache.get(f"cart-{user_id}")
    if cart != None:
        try:
            cart[product_id]
            cart[product_id] += product_count
        except KeyError:

            cart[product_id] = product_count
        cache.set(f"cart-{user_id}", cart)

    else:
        cart = {}
        cart[product_id] = product_count
        cache.set(f"cart-{user_id}", cart)


def get_cart(user_id):
    return cache.get(f"cart-{user_id}")
