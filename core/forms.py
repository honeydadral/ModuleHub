# core/form.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

# core/form.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class AskQuestionForm(forms.Form):
    email = forms.EmailField(label="Your E-Mail Address", required=True)
    name = forms.CharField(label="Full Name", required=True)
    subject = forms.CharField(required=True)
    question = forms.CharField(widget=forms.Textarea, required=True)

    role = forms.ChoiceField(
        choices=[
            ("", "No value"),
            ("current student", "Current Student"),
            ("staff", "Staff"),
            ("prospective student", "Prospective Student"),
            ("alumni", "Alumni"),
            ("other", "Other")
        ],
        required=False,
        label="I am"
    )


    identifier = forms.CharField(
        required=False,
        label="If applicable: student number / preregistration / application number"
    )
