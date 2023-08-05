from .base import BakeryBase
from rest_framework.response import Response
from issuestracker.models import Category
from issuestracker.serializers.bakery.HomePage import CategorySerializer


class BakeryHome(BakeryBase):
    def get(self, request, format=None):
        return Response(
            CategorySerializer(Category.live.all(), many=True).data
        )
