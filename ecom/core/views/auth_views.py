from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from ..models import MyUser
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        errors = {}
        # 1. Get data from the form
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phonenumber')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        street = request.POST.get('address') # This is the 'address' input from your HTML
        city = request.POST.get('city')

        # 2.Check for empty fields and validate inputs
        if not fullname:
            errors['fullname'] = "Full name is required."

        if not email:
            errors['email'] = "Email is required."

        if not phone:
            errors['phonenumber'] = "Phone number is required."

        if not street:
            errors['address'] = "Address is required."

        if not city:
            errors['city'] = "City is required."

        if not password:
            errors['password'] = "Password is required."

        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."

        if not confirm_password:
            errors['confirm_password'] = "Please confirm your password."

        # 3. Validation: Check if passwords match
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match!"

        # 4. THE FIX: Combine Street and City into one string
        combined_address = f"{street}, {city}"
        

        # 5. If there are errors, re-render the form with error messages
        if errors:
            return render(request, 'auth/signup.html', {'errors': errors, 'data': request.POST})
        
        # 6. If no errors, create the user
        try:
            user = MyUser.objects.create_user(
                email=email,
                fullname=fullname,
                phonenumber=phone,
                password=password,
                address=combined_address
            )
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')  # Redirect to login page after successful signup
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'auth/signup.html', {'data': request.POST})
    else:
        return render(request, 'auth/signup.html')

def login_view(request):
    if request.method == 'POST':
        errors = {}
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email:
            errors['email'] = "Email is required."

        if not password:
            errors['password'] = "Password is required."

        if errors:
            return render(request, 'auth/login.html', {'errors': errors, 'data': request.POST})
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'auth/login.html', {'data': request.POST})
    else:
        return render(request, 'auth/login.html')