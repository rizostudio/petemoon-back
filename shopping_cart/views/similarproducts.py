from product.selectors.recommended import get_top_sales
from django.contrib.auth import get_user_model
from django.db.models import Count
from product.models import Product
from shopping_cart.models import Order
from rest_framework.views import APIView
from config.responses import ok
from product.serializers import ProductListSerializer

User = get_user_model()



def get_similar_products(user: User) -> list:
    if user is None or user.is_anonymous:
        return get_top_sales()

    orders_pet_type = Order.objects.filter(user=user).values_list("products__product__pet_type",flat=True).distinct()

    user_bought_products = (
        Order.objects.filter(user=user)
        .values("products__product")
        .annotate(sell_count=Count("products__product"))
        .distinct()
        .order_by("-sell_count")
    )
    user_bought_products_id = []
    for product_id in user_bought_products:
        user_bought_products_id.append(product_id['products__product'])

    bought_product_categories = (Product.objects.filter(id__in=user_bought_products_id).values_list("category", flat=True).distinct())

    user_last_order_products = ( Order.objects.filter(user=user).order_by("-created_at").values_list("products__product", flat=True))

    recommended_products = (Product.objects.filter(pet_type__pet_type__in=orders_pet_type,
                                                   category__in=bought_product_categories, ).exclude(
        id__in=user_last_order_products).distinct())

    if recommended_products.count() == 0:
        return Product.objects.all()[0:20]
    elif recommended_products.count() < 20:
        remaining = 20 - recommended_products.count()
        return recommended_products | get_top_sales()[0:remaining]
    return recommended_products[0:20]





class SimilarProducts(APIView):
    def get(self, *args, **kwargs):
        user = self.request.user
        products = get_similar_products(user)
        return ok(data=ProductListSerializer(products, many=True).data)





