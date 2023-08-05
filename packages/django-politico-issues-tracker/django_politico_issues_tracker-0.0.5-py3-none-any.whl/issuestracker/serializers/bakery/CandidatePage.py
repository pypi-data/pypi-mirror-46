from rest_framework import serializers
from issuestracker.models import Category, Issue, Candidate, Position


def get_position(obj, slug):
    candidate_slug = slug
    c = Candidate.objects.get(slug=candidate_slug)
    return c.position_set.get(issue=obj.id)


def get_candidates_with_position_count(obj):
    count = 0
    for position in obj.position_set.all():
        count += position.candidates.count()

    return count


class IssueSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    explanation = serializers.SerializerMethodField()
    like_candidates = serializers.SerializerMethodField()
    other_candidates_with_positions = serializers.SerializerMethodField()

    def get_position(self, obj):
        try:
            return get_position(obj, self.context["slug"]).name
        except Position.DoesNotExist:
            return None

    def get_explanation(self, obj):
        try:
            return get_position(obj, self.context["slug"]).explanation
        except Position.DoesNotExist:
            return None

    def get_like_candidates(self, obj):
        candidate_slug = self.context["slug"]
        try:
            position = get_position(obj, self.context["slug"])
            return [
                cand.slug
                for cand in position.candidates.all()
                if cand.slug != candidate_slug
            ]
        except Position.DoesNotExist:
            return []

    def get_other_candidates_with_positions(self, obj):
        like_candidates = self.get_like_candidates(obj)
        candididates_with_positions = get_candidates_with_position_count(obj)
        return candididates_with_positions - len(like_candidates) - 1

    class Meta:
        model = Issue
        fields = (
            "name",
            "slug",
            "position",
            "explanation",
            "like_candidates",
            "other_candidates_with_positions",
        )


class CategorySerializer(serializers.ModelSerializer):
    issue_set = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("name", "slug", "icon", "issue_set")
