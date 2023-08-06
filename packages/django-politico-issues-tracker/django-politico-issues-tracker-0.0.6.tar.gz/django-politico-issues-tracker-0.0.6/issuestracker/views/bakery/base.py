from rest_framework.views import APIView
from issuestracker.utils.api_auth import TokenAPIAuthentication
from issuestracker.models import Candidate
from issuestracker.serializers.Candidate import CandidateSerializer


class BakeryBase(APIView):
    authentication_classes = (TokenAPIAuthentication,)
    permission_classes = []

    def get_all_candidates(self):
        output = {}
        for candidate in Candidate.objects.all():
            output[candidate.slug] = CandidateSerializer(candidate).data
        return output
