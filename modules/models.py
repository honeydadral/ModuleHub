from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse

class Module(models.Model):
    QUALIFICATION_TYPES = [
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
    ]
    MODE_OF_STUDY = [
        ('Part time', 'Part time'),
        ('Full time', 'Full time')
    ]
    MODE_OF_DELIVERY = [
        ('Online', 'Online'),
        ('On Campus', 'On Campus')
    ]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=50)
    qualification_type = models.CharField(max_length=2, choices=QUALIFICATION_TYPES, default='UG', help_text="Qualification level of the module")
    mode_of_study = models.CharField(max_length=10, choices=MODE_OF_STUDY, default='Full time', help_text="Mode of study")
    mode_of_delivery = models.CharField(max_length=10, choices=MODE_OF_DELIVERY, default='On Campus', help_text="Mode of delivery")
    description = models.TextField()
    availability = models.BooleanField(default=True)
    credits = models.IntegerField(default=15)
    courses = models.ManyToManyField(Group, related_name='modules')
    image = models.ImageField(upload_to='module_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse('modules:module_detail', args=[self.id])

    class Meta:
        ordering = ['name']

class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'module')

    def __str__(self):
        return f"{self.student.username} - {self.module.name}"

class CourseProfile(models.Model):
    course = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(blank=True, help_text="Detailed description of the course.")
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.course.name}"

    def get_image_url(self):
        return self.image.url if self.image and hasattr(self.image, 'url') else 'img/default_img.jpg'