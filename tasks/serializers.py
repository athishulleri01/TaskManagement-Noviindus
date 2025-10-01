from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['assigned_to', 'created_at', 'updated_at']

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        if data.get('status') == 'completed':
            if not data.get('completion_report') or not data.get('worked_hours'):
                raise serializers.ValidationError("Completion report and worked hours are required when marking task as completed.")
        return data
