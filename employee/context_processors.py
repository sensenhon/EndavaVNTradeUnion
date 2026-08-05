from .models import TUCommittee

def role_flags(request):
    is_president = False
    if request.user.is_authenticated:
        if request.user.is_superuser:
            is_president = True
        else:
            is_president = TUCommittee.objects.filter(user=request.user, position='President').exists()
    return {
        'is_president': is_president,
    }
