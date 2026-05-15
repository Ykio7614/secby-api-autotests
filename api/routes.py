class AuthRoutes:
    LOGIN = "/api/auth/login"
    VERIFY = "/api/auth/verify"

class ProfileRoutes:
    LIST = "/api/profiles/"
    ME = "/api/profiles/me"

    @staticmethod
    def profile_by_account_id(account_id):
        return f"/api/profiles/{account_id}"

    @staticmethod
    def role_by_account_id(account_id):
        return f"/api/profiles/{account_id}/role"
