from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework.views import APIView

from accounts.functions import (
    apply_stage,
    check_petshop_register_stage,
    get_user_data,
)
from accounts.models import PetshopProfile
from accounts.views.permissions import IsPetShop
from config.responses import bad_request, ok


class RegisterPetshop(APIView):
    permission_classes = [IsPetShop]

    @transaction.atomic
    def patch(self, *args, **kwargs):
        try:
            data = self.request.data
            files = self.request.FILES
            user = self.request.user
            try:
                stage = int(self.request.query_params.get("stage", 0))
            except ValueError:
                return bad_request({"stage": _("invalid stage")})
            profile = getattr(user, "petshop_profile", PetshopProfile())
            if (user.is_registered and stage < 3) or profile.is_approved:
                return bad_request({"stage": _("user is already registered")})
            if stage < 0 or stage > 3:
                return bad_request({"stage": _("invalid stage")})
            check, min_stage = check_petshop_register_stage(user, stage)
            if not check:
                return bad_request(
                    {
                        "stage": _("stage ")
                        + str(min_stage)
                        + _(" is not completed")
                    }
                )
            applying_func = apply_stage[stage]
            success, errors = applying_func(user, data=data, files=files)
            if not success:
                return bad_request(errors)
            user_data = {}
            if stage == 3:
                user.refresh_from_db()
                user_data = get_user_data(user)
            return ok({"user_data": user_data})
        except Exception as e:
            print(e)
            return bad_request()
