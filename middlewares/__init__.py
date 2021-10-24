from loader import dp

from .userdata import UserMiddleware


if __name__ == 'middlewares':
    dp.middleware.setup(UserMiddleware())