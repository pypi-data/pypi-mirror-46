from rest_framework import serializers
from issuestracker.models import Category, Issue


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("slug",)


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ("slug",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("slug",)
