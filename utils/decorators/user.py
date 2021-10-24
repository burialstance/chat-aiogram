def user_required(func):
    setattr(func, 'userdata_required', True)
    return func
