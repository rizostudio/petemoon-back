from rest_framework.permissions import IsAuthenticated


class IsPetShop(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.user_type == "petshop"
        )
