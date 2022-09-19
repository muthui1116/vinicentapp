
from ast import keyword
from unicodedata import category

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from ksgposts.models import Post, ReviewRating
from category.models import Category
from accounts.models import Account, UserProfile


from accounts.forms import RegistrationForm, UserProfileForm, UserForm, UserProfile
from ksgposts.forms import ReviewForm


# Create your views here.


def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'ksghome/home.html', context)


def posts(request, category_slug=None):
    categories = None
    posts = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=categories)
        paginator = Paginator(posts, 9)
        page = request.GET.get('page')
        paged_posts = paginator.get_page(page)
        posts_count = posts.count()
    else:
        posts = Post.objects.all().order_by('id')
        paginator = Paginator(posts, 9)
        page = request.GET.get('page')
        paged_posts = paginator.get_page(page)
        posts_count = posts.count()
    
    context = {
        'posts': paged_posts,
        'posts_count': posts_count, 
    }
    return render(request, 'ksghome/posts.html', context)


def post_detail(request, category_slug, post_slug):
    try:
        single_post = Post.objects.get(category__slug=category_slug, slug=post_slug)
    except Exception as e:
        raise e

    # get the reviews
    reviews = ReviewRating.objects.filter(post_id=single_post.id) 

    context = {
        'single_post': single_post,
        'reviews':  reviews,
    }
    return render(request, 'ksghome/post_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            posts = Post.objects.order_by('-created_date').filter(Q(body__icontains=keyword) | Q(topic__icontains=keyword) | Q(sub_topic__icontains=keyword))
            posts_count = posts.count()    
    context = {
        'posts':  posts,
        'posts_count': posts_count, 
    }
    return render(request, 'ksghome/posts.html', context) 


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registration Successful!')
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')
            
    return render(request, 'accounts/login.html')
 

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def submit_review(request, post_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, post__id=post_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data =  ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = post_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submited')
                return redirect(url)

def dashboard(request):
    posts = Post.objects.order_by('-created_at')
    posts_count = posts.count()
    context = {
        'posts_count': posts_count 
    }
    return render(request, 'ksghome/dashboard.html', context)

def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile':  userprofile,

    }      
    return render(request, 'ksghome/edit_profile.html', context)