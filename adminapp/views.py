# from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .models import RecipePost
from .tockens import generate_token


# Create your views here.
def admin_das(request):
    return render(request, 'adminapp/admin_index.html')


def admin_read_more(request, id):
    read = RecipePost.objects.filter(id=id)
    return render(request, 'adminapp/admin_readmore.html', {'read': read})


def admin_dashboard(request):
    context = RecipePost.objects.all()
    return render(request, 'adminapp/admin_posts.html', {'context': context})


def admin_login_page(request):
    return render(request, 'adminapp/registration/admin_register+login.html')


def admin_registration(request):
    # collect data from form
    if request.method == 'POST':
        admin_username = request.POST['admin_username']
        admin_email = request.POST['admin_email']
        admin_password = request.POST['admin_password']
        admin_confirm_password = request.POST['admin_confirm_password']
        # admin_pic = request.FILES.get('admin_pic')

        # conditions on registration
        if User.objects.filter(username=admin_username).exists():
            messages.error(request, 'Username already exist! please try some other username')
            return render(request, 'adminapp/registration/admin_register+login.html')

        if User.objects.filter(email=admin_email):
            messages.error(request, 'Email already registered')
            return render(request, 'adminapp/registration/admin_register+login.html')

        if admin_password != admin_confirm_password:
            messages.error(request, 'passwords are not matching!!')

        if len(admin_username) > 10 or len(admin_username) < 3:
            messages.error(request, 'Username should not be more than 10 Characters or less than 3 Characters!!')
        # save admin with username+email+password
        new_admin = User.objects.create_superuser(admin_username, admin_email, admin_password)
        # block activation until email confirmation
        new_admin.is_active = False
        # save entries
        new_admin.save()

        # asking user to confirm
        messages.success(request, 'Account has been created successfully,\n We have send you a confirmation email,'
                                  'please confirm inorder to activate your account')

        # Welcome email
        subject = "Welcome to God's Own Recipe.."
        message = "Hello " + new_admin.username + " \n " + "Thankyou for visiting our website, Please confirm " \
                                                           "your email address "
        from_email = settings.EMAIL_HOST_USER
        to_list = [new_admin.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ God's own recipe login"
        message2 = render_to_string('adminapp/registration/admin_email_confirmation.html', {
            'name': admin_username,
            'domain': current_site.domain,
            'userid': urlsafe_base64_encode(force_bytes(new_admin.pk)),
            'token': generate_token.make_token(new_admin),
        })
        # create email object
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [new_admin.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('admin_login_page')

    return render(request, 'adminapp/registration/admin_register+login.html')


def admin_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_admin = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_admin = None

    if new_admin and generate_token.check_token(new_admin, token):
        new_admin.is_active = True
        new_admin.save()
        messages.add_message(request, messages.SUCCESS, 'Email verified, you can now login')
        return redirect(reverse('admin_login'))
    else:
        return render(request, 'adminapp/registration/activation_failed.html', {'appadmin': new_admin})


@ensure_csrf_cookie
@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        admin_username = request.POST.get('admin_username')
        admin_password = request.POST.get('admin_password')

        admin_user = authenticate(username=admin_username, password=admin_password)
        if admin_user is not None:
            login(request, admin_user)
            admin_username = admin_username
            return render(request, 'adminapp/admin_index.html', {'admin_username': admin_username})
        else:
            messages.error(request, 'Bad Credentials!!!')
            return redirect('admin_login_page')
    return render(request, 'adminapp/registration/admin_register+login.html')


def admin_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'logged out successfully...')
    return redirect('admin_login_page')


@login_required
def recipe_db_rend(request):
    return render(request, 'adminapp/admin_add_recipe1.html')


@login_required
def recipe_db(request):
    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        short_description = request.POST.get('short_description')
        ingredients = request.POST.get('ingredients')
        directions = request.POST.get('directions')
        tips = request.POST.get('tips')
        cooking_time = request.POST.get('cooking_time')
        preparation_time = request.POST.get('preparation_time')
        image = request.FILES['image']
        author = request.session.get('author', 'user_username')
        db = RecipePost(
            recipe_name=recipe_name, short_description=short_description, ingredients=ingredients,
            cooking_directions=directions, cooking_tips=tips,
            cooking_time=cooking_time, preparation_time=preparation_time,
            recipe_images=image, author=author)

        db.save()
        return redirect('add_recipe')
    else:
        return HttpResponse('Complete the form and try again...')


def users_list(request):
    users_list = User.objects.all()
    return render(request,'adminapp/users_list.html',{'users_list':users_list})