from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse 
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import AskQuestionForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import Group
# Create your views here.

def home(request):
    message = 'Hello from home'
    courses = Group.objects.all()
    context = {'message': message,
                'title' : 'home',
                'courses' : courses
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about_us.html', {'title': 'About'})
    # return HttpResponse('<p>about page</p>')

def course_detail(request, pk):
    course = get_object_or_404(Group, pk=pk)
    modules = course.modules.all()
    # Get description from profile if exists, else placeholder
    description = course.profile.description if hasattr(course, 'profile') else "Lorem ipsum dolor sit amet, consectetur adipiscing elit. This is a placeholder description for the course."
    return render(request, 'core/course_detail.html', {'course': course, 'modules': modules, 'description': description})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        email_address = request.POST.get('email')
        phone_number = request.POST.get('phone_number')  
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')
        role = request.POST.get('role')

        # Build the message
        message = f"""
        Name: {name}
        Email: {email_address}
        Phone: {phone_number if phone_number else 'N/A'}
        Role: {role if role else 'N/A'}

        Message:
        {message_body}
        """

        email = EmailMessage(
            subject=f"Contact form submission: {subject}",
            body=message,
            from_email=email_address,
            to=['adoranaw.nhw@gmail.com'],  # your email
        )
        email.send()

        messages.success(request, "Your message has been sent successfully.")
        return redirect('core:core-contact')

    return render(request, 'core/contact_us.html', {
        'title': 'Contact',
    })