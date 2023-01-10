import factory

from product.models import Comment


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    title = factory.Faker("name")
    text = factory.Faker("text")
    rate = factory.Faker("pyint", min_value=1, max_value=5)
    user = factory.SubFactory("accounts.tests.fakers.user.UserFactory")
    product = factory.SubFactory("product.tests.fakers.product.ProductFactory")
