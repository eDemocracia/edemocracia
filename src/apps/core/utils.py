

def get_user_data(user):
    user_data = {
        'name': user.first_name,
        'email': user.email,
        'country': user.profile.country,
        'gender': user.profile.gender,
        'uf': user.profile.uf,
    }

    if user.profile.birthdate:
        user_data['birthdate'] = user.profile.birthdate.strftime("%x")
    else:
        user_data['birthdate'] = None

    if user.profile.avatar:
        user_data['avatar'] = user.profile.avatar.url
    else:
        user_data['avatar'] = None

    return user_data
