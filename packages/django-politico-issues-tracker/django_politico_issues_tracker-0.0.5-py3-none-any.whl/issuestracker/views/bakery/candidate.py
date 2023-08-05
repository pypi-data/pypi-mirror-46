from .base import BakeryBase
from rest_framework.response import Response
from issuestracker.models import Category
from issuestracker.serializers.bakery.CandidatePage import CategorySerializer


class BakeryCandidate(BakeryBase):
    def get(self, request, candidate=None):
        issues = CategorySerializer(
            Category.live.all(), context={"slug": candidate}, many=True
        ).data

        for category in issues:
            category["issue_set"] = [
                issue
                for issue in category["issue_set"]
                if issue["position"] is not None
            ]

        return Response(
            {
                "slug": candidate,
                "categories": [
                    category
                    for category in issues
                    if len(category["issue_set"]) > 0
                ],
            }
        )
