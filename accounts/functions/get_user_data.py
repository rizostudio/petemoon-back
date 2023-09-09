def get_normal_user_data(user):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "email": user.email,
    }


def get_petshop_user_data(user):

    if user.petshop_profile.national_card:
        national_card = user.petshop_profile.national_card.url
    else:
        national_card = None

    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "gender": user.petshop_profile.gender,
        "national_id": user.petshop_profile.national_id,
        "city": user.petshop_profile.city,
        "postal_region": user.petshop_profile.postal_region,
        "address": user.petshop_profile.address,
        "sheba_number": user.petshop_profile.sheba_number,
        "estimated_item_count": user.petshop_profile.estimated_item_count,
        "national_card": national_card,
        "store_name": user.petshop_profile.shops.name,
        # "store_slug": user.petshop_profile.shops.slug,
    }


def get_user_data(user):
    if user.user_type == "normal":
        return get_normal_user_data(user)
    if user.user_type == "petshop":
        return get_petshop_user_data(user)
