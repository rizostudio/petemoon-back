import factory

from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    password = "foo"
    set_password = factory.PostGenerationMethodCall("set_password", "foo")
    phone_number = factory.Faker("numerify", text="09#########")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birth_date = factory.Faker(
        "date_time_between", start_date="-18y", end_date="-99y"
    )
