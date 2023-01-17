from rest_framework import serializers

from diary.models import Diary, Comment


class DiaryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id', 'date', 'context', 'created_by']


class DiaryCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Diary
        fields = ['id', 'date', 'context', 'created_by']


class DiaryRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Diary
        fields = ['id', 'date', 'context',  'created_by']


class CommentListCreateSerializer(serializers.ModelSerializer):
    diary = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.PrimaryKeyRelatedField(read_only=True)
    updated_at = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'context', 'diary', 'created_at', 'updated_at', 'created_by']


class CommentRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    diary = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.PrimaryKeyRelatedField(read_only=True)
    updated_at = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'context', 'diary', 'created_at', 'updated_at', 'created_by']