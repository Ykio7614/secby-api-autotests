

from api.routes import ProfileRoutes


class UserApi:
    def __init__(self, client):
        self.client = client

    def get_my_profile(self):
        return self.client.get(ProfileRoutes.ME)