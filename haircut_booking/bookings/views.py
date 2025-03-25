from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.conf import settings
from datetime import datetime
import razorpay
import logging
import cv2
import numpy as np

from .forms import UserRegisterForm, AppointmentForm
from .models import Appointment, Service, Payment

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'bookings/register.html', {'form': form})


# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_appointment')  # Redirect to booking page after login
    else:
        form = AuthenticationForm()
    return render(request, 'bookings/login.html', {'form': form})


# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

from .face_shape_ai import detect_face_and_recommend 
# Appointment Booking View

def recommendation(request):
    if request.method == 'POST':
        # Check if a file was uploaded
        face_image = request.FILES.get('face_image')
        if not face_image:
            return HttpResponseBadRequest("No face image uploaded. Please upload a valid image.")

        try:
            # Convert the uploaded file to a numpy array for OpenCV
            np_image = cv2.imdecode(np.frombuffer(face_image.read(), np.uint8), cv2.IMREAD_COLOR)

            # Detect face shape and get recommendations
            shape, recommendations = detect_face_and_recommend(np_image)

        except Exception as e:
            return HttpResponseBadRequest(f"Error processing face image: {e}")

        return render(request, 'bookings/recommendation_result.html', {
            'face_shape': shape,
            'recommendations': recommendations
        })

    return render(request, 'bookings/recommendation.html')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']

            # Redirect to confirmation page with details
            return render(request, 'bookings/confirm_appointment.html', {
                'service': service,
                'appointment_date': appointment_date,
                'appointment_time': appointment_time
            })
    else:
        form = AppointmentForm()
    return render(request, 'bookings/book_appointment.html', {'form': form})



# Confirm Appointment and Proceed to Payment
@login_required
def finalize_appointment(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        appointment_date = request.POST.get('appointment_date')  # Now a string
        appointment_time = request.POST.get('appointment_time')

        try:
            # Create Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

            # Calculate amount
            service = Service.objects.get(id=service_id)
            amount = float(service.price) * 100  # Razorpay expects amount in paise

            # Create Razorpay order
            razorpay_order = client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': '1'
            })

            # Save the Payment record in the database
            Payment.objects.create(
                user=request.user,
                razorpay_order_id=razorpay_order['id'],
                amount=service.price,
                is_paid=False  # Initially unpaid
            )

            # Render payment page
            return render(request, 'bookings/payment.html', {
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_api_key': settings.RAZORPAY_API_KEY,
                'amount': service.price,
                'appointment_date': appointment_date,  # No parsing required
                'appointment_time': appointment_time,
                'service': service
            })

        except Service.DoesNotExist:
            return HttpResponse("Invalid service selected.", status=404)

    else:
        return redirect('my_appointments')




# Payment Verification View
@login_required
def payment_verification(request):
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            appointment_date = request.POST.get('appointment_date')  # Already a string
            appointment_time = request.POST.get('appointment_time')

            # Verify Razorpay payment
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Update payment record
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.is_paid = True
            payment.save()

            # Create the appointment
            service = Service.objects.get(id=request.POST.get('service_id'))
            Appointment.objects.create(
                user=request.user,
                service=service,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status='confirmed'
            )

            return JsonResponse({"message": "Payment Successful! Appointment confirmed."}, status=200)

        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment matching query does not exist."}, status=404)

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "Payment verification failed."}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request."}, status=400)




# View Appointments for Logged-in User
@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('appointment_date', 'appointment_time')
    return render(request, 'bookings/my_appointments.html', {'appointments': appointments})
