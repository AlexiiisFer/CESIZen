from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Create your views here.

def home(request):
    activity_limit = 8
    activities = Activity.objects.filter(is_active=True).order_by('-created_at')[:activity_limit]
    return render(request, 'home.html', {'activities': activities})

def signUp(request):
    if request.user.is_authenticated:
        messages.error(request, "Vous êtes déjà connecté.")
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('signUp')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Le nom d'utilisateur est déjà pris.")
            return redirect('signUp')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('signUp')

        # Créer l'utilisateur
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        UserProfile.objects.create(user=user)

        login(request, user)
        messages.success(request, "Votre compte a été créé avec succès!")
        return redirect('home')

    return render(request, 'signUp.html')

def custom_login(request):
    if request.user.is_authenticated:
        messages.error(request, "Vous êtes déjà connecté.")
        return redirect('home')

    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        user = None

        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                pass

        # Vérification du mot de passe ET statut actif
        if user and user.check_password(password):
            if user.is_active:
                login(request, user)
                messages.success(request, "Connexion réussie !")
                return redirect('home')
            else:
                messages.error(request, "Ce compte est désactivé. Veuillez contacter un administrateur.")
        else:
            messages.error(request, "Nom d'utilisateur, email ou mot de passe incorrect.")

    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('home') 

def settings(request):
    return render(request, 'settings.html')

@login_required
def profile_update(request):
    user = request.user
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=user)
        user_profile.save()

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('settings')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if password and confirm_password and password == confirm_password:
            user.set_password(password)
            user.save()
            messages.success(request, "Votre mot de passe a été mis à jour avec succès ! Veuillez vous reconnecter.")
            return redirect('login')

        if form.is_valid():
            form.save()

        user.save()
        messages.success(request, "Votre profil a été mis à jour avec succès !")
        return redirect('settings')

    form = ProfilePictureForm(instance=user_profile)
    return render(request, 'settings.html', {'user_profile': user_profile, 'form': form}) 


def activity_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    favorites_only = request.GET.get('favorites') == '1'

    activities = Activity.objects.filter(is_active=True)
    categories = Category.objects.all()

    favorite_activities = []
    if request.user.is_authenticated:
        favorite_activities = FavoriteActivity.objects.filter(user=request.user).values_list('activity_id', flat=True)


    if query:
        activities = activities.filter(title__icontains=query)

    if category_id:
        activities = activities.filter(category_id=category_id)

    if favorites_only and request.user.is_authenticated:
        favorite_ids = FavoriteActivity.objects.filter(user=request.user).values_list('activity_id', flat=True)
        activities = activities.filter(id__in=favorite_ids)

    paginator = Paginator(activities, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'activities.html', {
        'activities': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_query': query,
        'favorites_only': favorites_only,
        'page_obj': page_obj,
        'favorite_activities': favorite_activities,
    })

def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)

    if activity.is_active is False:
        messages.error(request, "Cette activité n'est pas disponible.")
        return redirect('activities')

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteActivity.objects.filter(user=request.user, activity=activity).exists()
    return render(request, 'activity_detail.html', {'activity': activity, 'is_favorite': is_favorite})


def toggle_favorite(request, pk):
    activity = get_object_or_404(Activity, pk=pk)

    if request.user.is_authenticated:
        favorite, created = FavoriteActivity.objects.get_or_create(user=request.user, activity=activity)
        if not created:
            favorite.delete()

    return redirect(request.META.get('HTTP_REFERER', 'activities'))


def information_list(request):
    if request.user.is_superuser or request.user.groups.filter(name="Moderator").exists():
        informations = Information.objects.order_by('-created_at')
    else:
        informations = Information.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'informations.html', {'informations': informations})

def information_detail(request, info_id):
    info = get_object_or_404(Information, id=info_id)

    if request.method == 'POST':
        info.title = request.POST.get('title')
        info.content = request.POST.get('content')
        info.save()
        return redirect('information_detail', info_id=info.id)

    return render(request, 'information_detail.html', {
        'info': info,
    })



# A Partir d'ici c'est coté admin et modo


#  On gere les utilisateurs

@login_required
def admin_user(request):
    if not request.user.is_superuser and not request.user.groups.filter(name="Moderator").exists():
        messages.error(request, "Accès non autorisé.")
        return redirect('home')

    if request.user.is_superuser or request.user.groups.filter(name="Moderator").exists():
        search = request.GET.get('search', '')
        sort = request.GET.get('sort', 'username')
        direction = request.GET.get('dir', 'asc')

        users = User.objects.all()

        if search:
            users = users.filter(Q(username__icontains=search))

        sort_expr = f"-{sort}" if direction == 'desc' else sort
        users = users.order_by(sort_expr)

        paginator = Paginator(users, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'administrator_user.html', {
            'page_obj': page_obj,
            'search': search,
            'sort': sort,
            'direction': direction,
        })
    else:
        messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('home')

def add_user(request):
    if not request.user.is_superuser and not request.user.groups.filter(name="Moderator").exists():
        messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        is_moderator = 'is_moderator' in request.POST

        if User.objects.filter(username=username).exists():
            messages.error(request, "Le nom d'utilisateur est déjà pris.")
            return redirect('administrator_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('administrator_user')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        UserProfile.objects.create(user=user)

        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            user_profile = UserProfile(user=user, profile_picture=profile_picture)
            user_profile.save()

        if is_moderator:
            moderator_group = Group.objects.get(name='Moderator')
            user.groups.add(moderator_group)

        messages.success(request, "L'utilisateur a été ajouté avec succès.")
        return redirect('administrator_user')  

    return redirect('administrator_user')

@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser and not request.user.groups.filter(name="Moderator").exists():
        messages.error(request, "Accès refusé.")
        return redirect('home')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        password = request.POST.get('password')
        if password:
            user.set_password(password)

        user.save()

        moderator_group, created = Group.objects.get_or_create(name='Moderator')
        if 'is_moderator' in request.POST:
            user.groups.add(moderator_group)
        else:
            user.groups.remove(moderator_group)

        messages.success(request, "Utilisateur mis à jour avec succès.")
        return redirect('administrator_user')

    return redirect('administrator_user')

def delete_user(request, user_id):
    if not request.user.is_superuser and not request.user.groups.filter(name="Moderator").exists():
        messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('home')
    
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "Utilisateur supprimé avec succès !")
    return redirect('administrator_user')

@login_required
def toggle_user_active(request, user_id):
    if not request.user.is_superuser and not request.user.groups.filter(name="Moderator").exists():
        messages.error(request, "Accès non autorisé.")
        return redirect('home')

    user = get_object_or_404(User, id=user_id)
    if request.user.is_superuser or request.user.groups.filter(name="Moderator").exists():
        user.is_active = not user.is_active
        user.save()
    return redirect('administrator_user')


# A partir d'ici c'est pour les activités


@login_required
def administrator_activities(request):
    if not request.user.is_superuser and not request.user.groups.filter(name="Moderator").exists():
        messages.error(request, "Accès non autorisé.")
        return redirect('home')


    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Activité ajoutée avec succès.")
            return redirect('administrator_activities')
    else:
        form = ActivityForm()

    search_query = request.GET.get('search', '')
    activities = Activity.objects.all().order_by('-created_at')
    if search_query:
        activities = activities.filter(title__icontains=search_query)
    paginator = Paginator(activities, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'administrator_activities.html', {
        'form': form,
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
    })

@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Activité ajoutée avec succès.")
    return redirect('administrator_activities')

@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if request.method == 'POST':
        original_status = activity.is_active 
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.is_active = original_status
            activity.save()
            messages.success(request, "Activité modifiée avec succès.")
    return redirect('administrator_activities')

@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    activity.delete()
    messages.success(request, "Activité supprimée.")
    return redirect('administrator_activities')

@login_required
def toggle_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    activity.is_active = not activity.is_active
    activity.save()
    return redirect('administrator_activities')


# A partir d'ici c'est pour les informations

@login_required
def add_information(request):
    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Information ajoutée avec succès.")
            return redirect('informations')  
    else:
        form = InformationForm()
    return render(request, 'informations.html', {'form': form})

@login_required
def edit_information(request, pk):
    info = get_object_or_404(Information, pk=pk)
    if request.method == 'POST':
        form = InformationForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect('information')
    else:
        form = InformationForm(instance=info)
    return render(request, 'informations.html', {'form': form})

@login_required
def delete_information(request, info_id):
    if not request.user.is_superuser and not request.user.groups.filter(name="Moderator").exists():
        messages.error(request, "Accès non autorisé.")
        return redirect('home')

    info = get_object_or_404(Information, id=info_id)
    if request.method == 'POST':
        info.delete()
        messages.success(request, "Information supprimée avec succès.")
    return redirect('informations')

@login_required
def toggle_information(request, info_id):
    if not request.user.is_superuser and not request.user.groups.filter(name="Moderator").exists():
        messages.error(request, "Accès non autorisé.")
        return redirect('home')

    info = get_object_or_404(Information, id=info_id)
    info.is_active = not info.is_active
    info.save()
    messages.success(request, "Statut de l'information mis à jour.")
    return redirect('informations')
