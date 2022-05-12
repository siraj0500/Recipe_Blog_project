from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tockens import generate_token
from django.utils.encoding import force_bytes, force_str
from RecipeProject import settings
from .models import User_Message
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from adminapp.models import RecipePost


def read_more(request, id):
    more = RecipePost.objects.filter(id=id)
    return render(request, 'userapp/readmore.html', {'more': more})


def user_home(request):
    context = RecipePost.objects.all()
    return render(request, 'userapp/user_index.html', {'context': context})


def user_index(request):
    return render(request, 'userapp/user_profile.html')


@login_required
def user_profile_return_home(request):
    return render(request, 'userapp/user_profile.html')


def user_contact_form(request):
    return render(request, 'userapp/user-message.html')


def user_contact(request):
    if request.method == 'POST':
        sender_name = request.POST.get('sender_name')
        sender_email = request.POST.get('sender_email')
        sender_message = request.POST.get('sender_message')
        register = User_Message(sender_name=sender_name, sender_email=sender_email, sender_message=sender_message)
        register.save()
        return redirect('user_contact_form')
    else:
        return HttpResponse('Complete the form....')


def user_login_reg(request):
    return render(request, 'userapp/user_sign-in+registration.html')


@ensure_csrf_cookie
@csrf_exempt
def user_signin(request):
    if request.method == 'POST':
        user_username = request.POST.get('user_username')
        user_password = request.POST.get('user_password')

        user = authenticate(username=user_username, password=user_password)
        if user is not None:
            login(request, user)
            user_username = user_username
            return render(request, 'userapp/user_profile.html', {'user_username': user_username})
        else:
            messages.error(request, 'Bad Credentials!!!')
            return redirect('user_login_reg')
    return render(request, 'userapp/user_sign-in+registration.html')


def user_register(request):
    # collecting data
    if request.method == 'POST':
        user_username = request.POST['user_username']
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']
        confirm_password = request.POST['confirm_password']

        # conditions

        if User.objects.filter(username=user_username).exists():
            messages.error(request, 'Username already exist! please try some other username')
            return render(request, 'userapp/user_sign-in+registration.html')

        if User.objects.filter(email=user_email):
            messages.error(request, 'Email already registered')
            return render(request, 'userapp/user_sign-in+registration.html')

        if user_password != confirm_password:
            messages.error(request, 'passwords are not matching!!')

        if len(user_username) > 10 or len(user_username) < 3:
            messages.error(request, 'Username should not be more than 10 Characters or less than 3 Characters!!')

            # saving
        new_user = User.objects.create_user(user_username, user_email, user_password)

        # user active only after confirmation
        new_user.is_active = False

        new_user.save()
        messages.success(request, 'Account has been created successfully,\n We have send you a confirmation email,'
                                  'please confirm inorder to activate your account')

        # Welcome email
        subject = "Welcome to God's Own Recipe.."
        message = "Hello " + new_user.username + "!! \n " + "Thankyou for visiting our website, Please confirm " \
                                                            "your email address "
        from_email = settings.EMAIL_HOST_USER
        to_list = [new_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ God's own recipe login"
        message2 = render_to_string('userapp/user_email_confirmation.html', {
            'name': user_username,
            'domain': current_site.domain,
            'userid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'token': generate_token.make_token(new_user),
        })
        # create email object
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [new_user.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('user_login_reg')

    return render(request, 'userapp/user_sign-in+registration.html')


def user_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None

    if new_user and generate_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        messages.add_message(request, messages.SUCCESS, 'Email verified, you can now login')
        return redirect(reverse('user_sign_in'))
    else:
        return render(request, 'userapp/activation_failed.html', {'user': new_user})


def user_forgot_password(request):
    return render(request, 'registration/password_reset_form.html')


# password reset class
class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('custom_auth:password_reset_done')
    subject_template_name = 'password_reset_subject.txt'
    email_template_name = 'password_reset_email.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('user_login_reg')
    form_valid_message = "Your password was changed!"


def user_update_prof(request):
    return render(request, 'userapp/user_update_profile.html')


def user_sign_out(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'logged out successfully...')
    return redirect('user_login_reg')


def blog_about(request):
    return render(request, 'about/about_developer.html')


def show(request):
    show = RecipePost.objects.all()
    context = {'show': show}
    return render(request, 'adminapp/admin_index.html', context)
