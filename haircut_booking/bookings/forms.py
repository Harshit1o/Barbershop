from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment, Service

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AppointmentForm(forms.ModelForm):
    # Allow manual input for date
    appointment_date = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter date (e.g., 2024-12-05)',
        }),
        label="Enter Appointment Date"
    )

    # Dropdown for predefined time slots
    appointment_time = forms.ChoiceField(
        choices=[
            ("09:00:00", "9:00 AM"),
            ("10:00:00", "10:00 AM"),
            ("11:00:00", "11:00 AM"),
            ("12:00:00", "12:00 PM"),
            ("13:00:00", "1:00 PM"),
            ("14:00:00", "2:00 PM"),
            ("15:00:00", "3:00 PM"),
            ("16:00:00", "4:00 PM"),
            ("17:00:00", "5:00 PM"),
        ],
        label="Select Time"
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        empty_label="Select a Service",
        label="Service"
    )

    class Meta:
        model = Appointment
        fields = ['service', 'appointment_date', 'appointment_time']
