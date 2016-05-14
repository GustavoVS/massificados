from allauth.account.adapter import DefaultAccountAdapter

class NoSignUp(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        # Disable new users registration
        return False