

from api.routes import AuthRoutes


class AuthApi:
    def __init__(self, client):
        self.client = client
    
    def login(self, login, password):
        data = {"login": login, "password": password}
        return self.client.post(AuthRoutes.LOGIN, json=data)
    
    def verify(self):
        return self.client.get(AuthRoutes.VERIFY)
    
