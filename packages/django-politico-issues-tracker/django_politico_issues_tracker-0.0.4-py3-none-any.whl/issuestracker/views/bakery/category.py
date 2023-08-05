from .base import BakeryBase
from rest_framework.response import Response
from issuestracker.models import Category
from issuestracker.serializers.bakery.CategoryPage import CategorySerializer


class BakeryCategory(BakeryBase):
    def get(self, request, category=None):
        return Response(
            CategorySerializer(
                Category.live.get(slug=self.kwargs["category"])
            ).data
        )
