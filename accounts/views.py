from django.shortcuts import render, redirect, reverse
from .models import Account, UserProfile
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserForm, UserProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages, auth
from cart.views import _cart_id
from cart.models import Cart, CartItem
# Create your views here.

def Log_In(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('store:Home')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user is not None:

                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                except:
                    cart = Cart.objects.create(cart_id=_cart_id(request))
                
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()

                auth.login(request, user)
                messages.success(request, 'Logged in succesfully.')
                
                return redirect('store:Home')

    return render(request, 'accounts/login.html')


@login_required(login_url='accounts:login')
def Log_Out(request):
	if request.user.is_authenticated:
		auth.logout(request)
		messages.success(request, 'You are now logged out.')
	else:
		messages.warning(request, 'You are already logged out.')
		return redirect('accounts:login')
	return redirect('accounts:login')


def Sign_Up(request):
    form = RegistrationForm()
    if request.user.is_authenticated != True:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']

                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
                user.save()

                to_mail = email
                current_site = get_current_site(request)
                mail_subject = 'Please active your account'
                mail_messages = render_to_string('accounts/accounts_verification_email.html', {

				'user':user,
				'domain':current_site,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),
				'token':default_token_generator.make_token(user),

				})

                email_send = EmailMessage(mail_subject, mail_messages, settings.EMAIL_HOST_USER, to=[to_mail])
                email_send.fail_silently = False
                email_send.send()
                
                url = reverse('accounts:login') + f'?command=verification&email={email}'
                return redirect(url)
  
    else:
        return redirect('accounts:login')
    
    context = {'form':form}
    return render(request, 'accounts/register.html', context)



def Activate(request, uidb64, token):
	
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = Account._default_manager.get(pk=uid)
	except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
		user = None

	if user is not None and default_token_generator.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, 'Congratulations! Your account is activated.')
		return redirect('accounts:login')

	else:
		messages.error(request, 'Invalid activation link.')
		return redirect('accounts:register')

def Reset_Password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email__iexact=email).exists():
            user  = Account.objects.filter(email__iexact=email)[0]
            current_site = get_current_site(request)
            to_mail = email
            mail_subject = 'Reset your password.'
            mail_messages = render_to_string('accounts/reset_password_email.html', {

			'user':user,
			'domain':current_site,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':default_token_generator.make_token(user),

			})

            send_mail = EmailMessage(mail_subject, mail_messages, to=[to_mail])
            send_mail.fail_silently = False
            send_mail.send()
            messages.success(request, 'Password reset email has been send to your email address.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'No account associated with this email.')
            return redirect('accounts:login')
    
    return render(request, 'accounts/reset_password.html')


def Reset_Password_Validate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
        
    except(ValueError, TypeError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('accounts:reset_password_process')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('accounts:log_in')

def Reset_Password_Process(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            messages.error('Password did not match.')
            return redirect('accounts:reset_password')

    return render(request, 'accounts/new_password.html')

@login_required(login_url='accounts:login')
def DashBoard(request):
    current_user = request.user
    userprofile = UserProfile.objects.get(user=current_user)
    context = {'current_user':current_user, 'userprofile':userprofile}
    return render(request, 'accounts/profle.html', context)

@login_required(login_url='accounts:login')
def Update_Profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    userform = UserForm(instance=request.user)
    userprofileform = UserProfileForm(instance=userprofile)
    if request.method == 'POST':

        try:
            userform = UserForm(request.POST, instance=request.user)
            userprofileform = UserProfileForm(request.POST, request.FILES, instance=userprofile)
            if userform.is_valid() & userprofileform.is_valid():
                userform.save()
                userprofileform.save()
                messages.success(request, 'Profile information has been updated.')
                return redirect('accounts:dashboard')
        except:
            userform = UserForm(instance=request.user)
            userprofileform = UserProfileForm(instane=userprofile)

    context = {'userform':userform, 'userprofileform':userprofileform}

    return render(request, 'accounts/update_profile.html', context)

@login_required(login_url='accounts:login')
def Change_Password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email=request.user.email)
        if new_password == confirm_password:
            authorized = user.check_password(current_password)
            if authorized:
                user.set_password(new_password)
                user.save()
                auth.logout(request)
                messages.success(request, 'Your password has been updated, login to continue!')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Your current password does not match.')
                return redirect('accounts:change_password')


        else:
            messages.error(request, 'Confirm password does not match.')
            return redirect('accounts:change_password')
    return render(request, 'accounts/change_password.html')