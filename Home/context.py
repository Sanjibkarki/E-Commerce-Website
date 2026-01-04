def auth(request):
    return {
        'is_authenticated': request.user.is_authenticated,
        'user': request.user,
    }
