

def get_user_data(user):
    data = user.__dict__.copy()
    data.pop('_state', None)
    data.pop('password', None)
    data.pop('last_login', None)
    data.pop('date_joined', None)
    data.pop('id', None)
    return data
