from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address', help_text='Your email address.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    phone = forms.CharField(max_length=15)
    address = forms.CharField(max_length=255, required=False)
    student_id = forms.CharField(max_length=50, required=False, label='Student ID', help_text='Your student ID number.')
    city = forms.CharField(max_length=100, required=False, label='City/Town')
    country = forms.CharField(max_length=100, required=False)
    course = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label='Course',
        help_text='Select your course.',
        empty_label='Select a course'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'phone', 'address', 'student_id', 'city', 'country', 'course', 'password1', 'password2']
        help_texts = {
            'username': 'Enter your desired username (letters, digits, and @/./+/-/_ only).',
            'email': 'Your email address.',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Assign the selected course (group) to the user
            course = self.cleaned_data.get('course')
            if course:
                user.groups.add(course)
            # Create or update the Profile
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'date_of_birth': self.cleaned_data['date_of_birth'],
                    'gender': self.cleaned_data['gender'],
                    'phone': self.cleaned_data['phone'],
                    'address': self.cleaned_data['address'],
                    'student_id': self.cleaned_data['student_id'],
                    'city': self.cleaned_data['city'],
                    'country': self.cleaned_data['country']
                }
            )
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)
    student_id = forms.CharField(max_length=50, required=False, label='Student ID')
    city = forms.CharField(max_length=100, required=False, label='City/Town')
    country = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'gender', 'phone', 'address', 'student_id', 'city', 'country', 'image']
        labels = {
            'image': 'Photo of student'
        }