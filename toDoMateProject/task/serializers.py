from rest_framework import serializers

from task.models import Task#, Tag


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'date', 'name', 'complete', 'created_by', 'start_time', 'end_time']


class TaskListCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    complete = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'date', 'name', 'complete', 'created_by', 'start_time', 'end_time']

#commit
class TaskDetailDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'date', 'name', 'complete', 'created_by', 'start_time', 'end_time']


class TaskUpdateSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    complete = serializers.PrimaryKeyRelatedField(read_only=True)
    #tag = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'date', 'name', 'complete', 'created_by', 'start_time', 'end_time']
#
#
# class TagListCreateSerializer(serializers.ModelSerializer):
#     created_by = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Tag
#         fields = ['id', 'name', 'created_by']


# class TagDetailUpdateDestroySerializer(serializers.ModelSerializer):
#     created_by = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Tag
#         fields = ['id', 'name', 'created_by']


# class RepeatListCreateSerializer(serializers.ModelSerializer):
#     created_by = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Repeat
#         fields = ['id', 'name', 'created_by']