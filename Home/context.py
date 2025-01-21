def auth(request):
    if request.user.is_authenticated:
        admin = request.user.is_admin
    else:
        admin = False
    return {'admin':admin}