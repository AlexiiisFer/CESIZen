from django.contrib.auth.models import Group

def moderator_status(request):
    if request.user.is_authenticated:
        is_moderator = request.user.groups.filter(name='Moderator').exists()
    else:
        is_moderator = False
    return {'is_moderator': is_moderator}
