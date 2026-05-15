

from api.routes import ProfileRoutes


class UserApi:
    def __init__(self, client):
        self.client = client

    def get_my_profile(self):
        return self.client.get(ProfileRoutes.ME)

    def get_profile_by_account_id(self, account_id):
        return self.client.get(ProfileRoutes.profile_by_account_id(account_id))

    def list_profiles(self, limit=1000, offset=0):
        return self.client.get(
            ProfileRoutes.LIST,
            params={"limit": limit, "offset": offset},
        )

    def update_account_role(self, account_id, role_name):
        return self.client.put(
            ProfileRoutes.role_by_account_id(account_id),
            params={"role_name": role_name},
        )
