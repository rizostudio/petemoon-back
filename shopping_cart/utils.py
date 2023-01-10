from django.core.cache import cache


def add_to_cart(user_id,product_id,product_count):
    cart = cache.get(f"cart-{user_id}")
    if cart != None:
        new_cart = cache.get(f"cart-{user_id}")
        if new_cart[product_id]!= None:
            new_cart[product_id] += product_count
            
        #cache[product_id] = product_count 
        cache.set(f"cart-{user_id}",new_cart)
        print(cache.get(f"cart-{user_id}"))

    else:
        cart = {}
        cart[product_id] = product_count
        cache.set(f"cart-{user_id}",cart)
