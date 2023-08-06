from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from dashboard.serializers import UserProfileSerializer
from dashboard.models import Pet
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException



class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
           
        result = self.serializer_class(self.request.user).data
        return SuccessResponse(data=result)

    def patch(self, request):
        serialized_data = self.serializer_class(request.user,data=request.data, partial=True)

        try:
            if serialized_data.is_valid(raise_exception=True):


                user_profile = serialized_data.update(
                    instance=request.user,validated_data=serialized_data.validated_data)

                return SuccessResponse(data=UserProfileSerializer(user_profile).data)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)     

