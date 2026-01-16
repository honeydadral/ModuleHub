from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'course', 'date_of_birth', 'gender', 'phone')
    search_fields = ('user__username', 'student_id', 'city', 'country')
    list_filter = ('gender', 'city', 'country')

    def course(self, obj):
        return obj.user.groups.first().name if obj.user.groups.exists() else 'No course'
    course.short_description = 'Course'