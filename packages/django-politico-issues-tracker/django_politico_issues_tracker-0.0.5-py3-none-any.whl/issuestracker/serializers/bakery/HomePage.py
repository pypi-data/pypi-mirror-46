from rest_framework import serializers
from issuestracker.models import Category, Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ("name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    issue_set = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("name", "slug", "issue_set")
