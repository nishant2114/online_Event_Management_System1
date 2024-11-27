from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.mail import send_mail  # Importing for email notifications
from .models import CustomUser  # Assuming you're using CustomUser
from accounts.utils.notifications import send_sms


def home(request):
    return render(request, 'home.html')


def profile(request):
    if request.method == 'POST':
        # Update profile details
        phone_number = request.POST.get('phone_number')
        description = request.POST.get('description')
        address = request.POST.get('address')

        # Update the current user profile
        user = request.user
        validated_phone_number = validate_phone_number(phone_number)
        if not validated_phone_number:
            messages.error(request, "Invalid phone number format.")
            return redirect('profile')
        
        user.phone_number = validated_phone_number
        user.description = description
        user.address = address
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    
    return render(request, 'profile.html')


def logout(request):
    auth_logout(request)
    return redirect('/')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(username=username).exists():
            messages.info(request, "Username does not exist.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # if CustomUser.objects.filter(email=email).exists():
        #     messages.error(request, "Email is already registered.")
        #     return redirect('register')

        # Email validation
        try:
            EmailValidator()(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect('register')

        # Validate phone number
        validated_phone_number = validate_phone_number(phone_number)
        if not validated_phone_number:
            messages.error(request, "Invalid phone number format.")
            return redirect('register')

        # Create and save the user
        user = CustomUser.objects.create_user(
            username=username,
            password=password1,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.save()

        # Send SMS notification (optional)
        # try:
        #     send_sms(
        #         to=validated_phone_number,
        #         message="Welcome to the Event Management System! Thank you for registering."
        #     )
        # except Exception as e:
        #     messages.error(request, f"Error sending SMS: {e}")
        #     return redirect('register')

        # Send email notification
        try:
            send_mail(
                'Welcome to Event Management System',
                'Thank you for registering with us. We are excited to have you on board.',
                'no-reply@eventmanagement.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")
            return redirect('register')

        messages.success(request, "Registration successful! Check your email and SMS for confirmation.")
        return redirect('login')
    return render(request, 'registration.html')


# Utility function to validate and format phone number
def validate_phone_number(phone_number):
    try:
        # Parse the phone number
        parsed_number = parse(phone_number, None)
        # Check if the number is valid
        if is_valid_number(parsed_number):
            return format_number(parsed_number, PhoneNumberFormat.E164)
        else:
            return None
    except Exception:
        return None
    
# def provider_registration_view(request):
#     return render(request, 'provider_registration.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.db import transaction
from hall.models import Hall
from accounts.utils.notifications import send_sms

# Dynamically get the custom user model
User = get_user_model()

def provider_registration(request):
    if request.method == 'POST':
        # Personal Details
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Username and Email Uniqueness Check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('provider_registration')

        # if User.objects.filter(email=email).exists():
        #     messages.error(request, "Email already registered.")
        #     return redirect('provider_registration')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('provider_registration')

        # Hall Details
        hall_name = request.POST.get('hall_name')
        location = request.POST.get('location')
        address = request.POST.get('address')
        price = request.POST.get('price')
        capacity = request.POST.get('capacity')
        amenities = request.POST.get('amenities')
        photo = request.FILES.get('photo')

        # Bank Details (Optional)
        bank_name = request.POST.get('bank_name', '')
        account_number = request.POST.get('account_number', '')
        ifsc_code = request.POST.get('ifsc_code', '')

        try:
            with transaction.atomic():
                # Create User
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1,
                )
                user.save()

                # Create Hall
                hall = Hall.objects.create(
                    user=user,
                    name=hall_name,
                    location=location,
                    address=address,
                    price=float(price),
                    capacity=int(capacity),
                    amenities=amenities,
                    images=photo,
                    bank_name=bank_name,
                    account_number=account_number,
                    ifsc_code=ifsc_code
                )
                hall.save()

                # Send Email Notification
                send_mail(
                    subject='Welcome to Event Management System',
                    message='Thank you for registering as a provider. Your hall has been successfully listed.',
                    from_email='no-reply@eventmanagement.com',
                    recipient_list=[email],
                    fail_silently=False,
                )

                # Optional: Send SMS Notification
                # send_sms(phone_number, 'Your registration was successful!')

                messages.success(request, "Registration successful!")
                return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('provider_registration')

    return render(request, 'provider_registration.html')





# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.contrib.auth.models import User
# from django.db import transaction
# from hall.models import Hall
# from accounts.utils.notifications import send_sms


# def provider_registration(request):
#     if request.method == 'POST':
#         # Personal Details
#         username = request.POST.get('username')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number')
#         password1 = request.POST.get('password')
#         password2 = request.POST.get('confirm-password')

        
       
#         # Username and Email Uniqueness Check
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return redirect('provider_registration')
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered.")
#             return redirect('provider_registration')

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect('provider_registration')

#         # Hall Details
#         hall_name = request.POST.get('hall-name')
#         location = request.POST.get('location')
#         address = request.POST.get('address')
#         price = request.POST.get('price')
#         capacity = request.POST.get('capacity')
#         amenities = request.POST.get('amenities')
#         photo = request.FILES.get('photo')

#         # Bank Details (Optional)
#         bank_name = request.POST.get('bank_name', '')
#         account_number = request.POST.get('account_number', '')
#         ifsc_code = request.POST.get('ifsc_code', '')

#         # try:
#         #     with transaction.atomic():
#                 # Create User
#         user = User.objects.create_user(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password=password1,
#         )
#         user.save()

#         # Create Hall
#         hall = Hall.objects.create(
#             user=user,
#             name=hall_name,
#             location=location,
#             address=address,
#             price=float(price),
#             capacity=int(capacity),
#             amenities=amenities,
#             images=photo,
#             bank_name=bank_name,
#             account_number=account_number,
#             ifsc_code=ifsc_code
#         )
#         hall.save()

#                 # Send Email Notification
#                 # send_mail(
#                 #     subject='Welcome to Event Management System',
#                 #     message='Thank you for registering as a provider. Your hall has been successfully listed.',
#                 #     from_email='no-reply@eventmanagement.com',
#                 #     recipient_list=[email],
#                 #     fail_silently=False,
#                 # )

#                 # Optional: Send SMS Notification
#                 # send_sms(phone_number, 'Your registration was successful!')

#                 # messages.success(request, "Registration successful!")
#                 # return redirect('login')

#         # except Exception as e:
#         #     messages.error(request, f"An error occurred: {str(e)}")
#         #     return redirect('provider_registration')
#         messages.success(request, "Registration successful! Check your email and SMS for confirmation.")
#         return redirect('login')

#     return render(request, 'provider_registration.html')
