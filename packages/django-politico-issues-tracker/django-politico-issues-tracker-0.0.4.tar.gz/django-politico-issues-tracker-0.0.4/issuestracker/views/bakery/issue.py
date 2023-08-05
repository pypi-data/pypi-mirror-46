from .base import BakeryBase
from rest_framework.response import Response
from issuestracker.models import Issue
from issuestracker.serializers.bakery.IssuePage import IssueSerializer


class BakeryIssue(BakeryBase):
    def get(self, request, issue=None):
        return Response(
            IssueSerializer(Issue.live.get(slug=self.kwargs["issue"])).data
        )
