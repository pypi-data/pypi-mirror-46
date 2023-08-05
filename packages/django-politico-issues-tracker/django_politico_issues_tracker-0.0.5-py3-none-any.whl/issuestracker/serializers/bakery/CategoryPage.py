from rest_framework import serializers
from issuestracker.models import Category, Issue, Candidate


class IssueSerializer(serializers.ModelSerializer):
    position_count = serializers.SerializerMethodField()
    candidates_with_position_count = serializers.SerializerMethodField()

    def get_position_count(self, obj):
        return obj.position_set.all().count()

    def get_candidates_with_position_count(self, obj):
        count = 0
        for position in obj.position_set.all():
            count += position.candidates.count()

        return count

    class Meta:
        model = Issue
        fields = (
            "name",
            "slug",
            "dek",
            "position_count",
            "candidates_with_position_count",
        )


class CategorySerializer(serializers.ModelSerializer):
    issue_set = IssueSerializer(many=True, read_only=True)
    candidates_count = serializers.SerializerMethodField()

    def get_candidates_count(self, obj):
        return Candidate.objects.all().count()

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
            "icon",
            "summary",
            "candidates_count",
            "issue_set",
        )
