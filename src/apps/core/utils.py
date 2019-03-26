from datetime import datetime
import pytz


def str_to_date(value):
    final_value = None
    date_formats = {
        '%d/%m/%Y': 'date',
        '%d/%m/%Y %H:%M:%S': None,
        '%d/%m/%Y %H:%M': None,
        '%H:%M': 'time',
        '%H:%M:%S': 'time',
        '%Y-%m-%dT%H:%M:%S.%fZ': 'date',
    }
    for date_format in date_formats.keys():
        try:
            final_value = datetime.strptime(value, date_format)
            tz = pytz.timezone('America/Sao_Paulo')
            final_value = tz.localize(final_value)
            if date_formats[date_format]:
                get_date_type = getattr(final_value,
                                        date_formats[date_format])
                final_value = get_date_type()
            break
        except (ValueError, TypeError):
            final_value = value.strip() if value else None
    return final_value


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
            user_data['birthdate'] = user.profile.birthdate.strftime(
                "%Y-%m-%d")
        else:
            user_data['birthdate'] = None

        if user.profile.avatar:
            user_data['avatar'] = user.profile.avatar.url
        else:
            user_data['avatar'] = None

    return user_data
