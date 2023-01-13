from rest_framework import serializers

from task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    complete = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'date', 'name', 'complete', 'created_by', 'repeated']


class TaskUpdateNameSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    complete = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'date', 'name', 'complete', 'created_by', 'repeated']


class TaskUpdateDateSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    complete = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'date', 'name', 'complete', 'created_by', 'repeated']