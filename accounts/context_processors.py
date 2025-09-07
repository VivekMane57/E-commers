from .models import UserProfile

def user_profile(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        return {'user_profile': profile}
    return {}