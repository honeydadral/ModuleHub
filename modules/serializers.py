from rest_framework import serializers
from .models import Module, Registration
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    module = serializers.SlugRelatedField(slug_field='code', queryset=Module.objects.all())

    class Meta:
        model = Registration
        fields = ['id', 'student', 'module', 'registration_date']
        read_only_fields = ['registration_date']

    def validate(self, data):
        student = data['student']
        module = data['module']
        if not module.availability:
            raise serializers.ValidationError("This module is not available for registration.")
        student_course = student.groups.first()
        if not student_course:
            raise serializers.ValidationError(f"No course assigned to user {student.username}.")
        if student_course not in module.courses.all():
            raise serializers.ValidationError(f"This module is not available for your course ({student_course.name}). Available courses: {', '.join([course.name for course in module.courses.all()])}.")
        return data