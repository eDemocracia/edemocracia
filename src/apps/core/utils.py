

def get_user_data(user):
    user_data = {
        'name': user.get_full_name(),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'is_active': user.is_active,
        'email': user.email,
    }

    if hasattr(user, 'profile'):
        user_data['country'] = user.profile.country
        user_data['gender'] = user.profile.gender
        user_data['uf'] = user.profile.uf

        if user.profile.birthdate:
            user_data['birthdate'] = user.profile.birthdate.strftime("%x")
        else:
            user_data['birthdate'] = None

        if user.profile.avatar:
            user_data['avatar'] = user.profile.avatar.url
        else:
            user_data['avatar'] = None

    return user_data
