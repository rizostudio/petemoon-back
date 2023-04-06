from django.db import transaction
from slugify import slugify

from accounts.models import PetshopProfile, User

from product.models import Petshop


def check_petshop_register_stage(user: User, stage: int = 0):
    if not hasattr(user, "petshop_profile"):
        return stage == 0, 0
    profile: PetshopProfile = user.petshop_profile
    if not (
        user.first_name
        and user.last_name
        and profile.gender
        and profile.national_id
    ):
        return stage == 0, 0
    if not hasattr(profile, "shops"):
        return stage <= 1, 1
    shop: Petshop = profile.shops
    if not (
        profile.city
        and profile.postal_region
        and profile.address
        and shop.name
    ):
        return stage <= 1, 1
    if not (profile.sheba_number and profile.estimated_item_count):
        return stage <= 2, 2
    if not (profile.national_card):
        return stage <= 3, 3
    return False, -1


@transaction.atomic
def apply_stage_0(user: User, data, **kw):
    profile, _ = PetshopProfile.objects.get_or_create(user=user)
    serializer = Stage0PetShopSerializer(data=data)
    if not serializer.is_valid():
        return False, serializer.errors
    data = serializer.data
    user.first_name = data.get("first_name")
    user.last_name = data.get("last_name")
    user.save()
    profile.gender = data.get("gender")
    profile.national_id = data.get("national_id")
    profile.save()
    return True, None


@transaction.atomic
def apply_stage_1(user: User, data, **kw):
    profile = PetshopProfile.objects.get(user=user)
    if Petshop.objects.filter(owner=profile).exists():
        shop = Petshop.objects.get(owner=profile)
    else:
        shop = Petshop(owner=profile)
    serializer = Stage1PetShopSerializer(data=data)
    if not serializer.is_valid():
        return False, serializer.errors
    data = serializer.data
    profile.city = data.get("city")
    profile.postal_region = data.get("postal_region")
    profile.address = data.get("address")
    profile.save()
    shop.name = data.get("store_name")
    shop.slug = slugify(data.get("store_name"))
    if Petshop.objects.filter(slug=shop.slug).exists():
        shop.slug += profile.id
    shop.save()
    return True, None


@transaction.atomic
def apply_stage_2(user: User, data, **kw):
    profile = PetshopProfile.objects.get(user=user)
    serializer = Stage2PetShopSerializer(data=data)
    if not serializer.is_valid():
        return False, serializer.errors
    data = serializer.data
    profile.sheba_number = data.get("sheba_number")
    profile.estimated_item_count = data.get("estimated_item_count")
    profile.save()
    return True, None


@transaction.atomic
def apply_stage_3(user: User, files, **kw):
    profile = PetshopProfile.objects.get(user=user)
    if "national_card" not in files:
        return False, {"national_card": ["This field is required."]}
    try:
        profile.national_card = files["national_card"]
        profile.save()
        return True, None
    except Exception:
        return False, {"national_card": ["file is not valid"]}
