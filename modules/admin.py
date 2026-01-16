from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import Module, Registration, CourseProfile

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'qualification_type', 'get_mode_of_study_display', 'get_mode_of_delivery_display', 'availability', 'credits', 'course_list')
    list_filter = ('category', 'qualification_type', 'mode_of_study', 'mode_of_delivery', 'availability')
    search_fields = ('name', 'code', 'description')
    list_editable = ('availability',)
    filter_horizontal = ('courses',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'description', 'image')
        }),
        ('Details', {
            'fields': ('category', 'qualification_type', 'mode_of_study', 'mode_of_delivery', 'credits', 'availability', 'courses')
        }),
    )
    actions = ['make_unavailable', 'make_available']

    def course_list(self, obj):
        return ", ".join([course.name for course in obj.courses.all()])
    course_list.short_description = 'Courses'

    def make_unavailable(self, request, queryset):
        queryset.update(availability=False)
        self.message_user(request, "Selected modules marked as unavailable.")
    make_unavailable.short_description = "Mark selected modules as unavailable"

    def make_available(self, request, queryset):
        queryset.update(availability=True)
        self.message_user(request, "Selected modules marked as available.")
    make_available.short_description = "Mark selected modules as available"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('courses')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'registration_date')
    list_filter = ('module__category', 'module__qualification_type', 'module__mode_of_study', 'module__mode_of_delivery', 'registration_date')
    search_fields = ('student__username', 'module__name', 'module__code')
    autocomplete_fields = ('student', 'module')
    ordering = ('-registration_date',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'module')

@admin.register(CourseProfile)
class CourseProfileAdmin(admin.ModelAdmin):
    list_display = ('course', 'get_image_url')
    search_fields = ('course__name', 'description')
    list_filter = ('course',)

    def get_image_url(self, obj):
        return obj.get_image_url()
    get_image_url.short_description = 'Image URL'

admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)