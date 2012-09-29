from .base import AbstractRAuth


class GithubOAuth(AbstractRAuth):

    name = 'github'
    options = dict(
        base_url='https://api.github.com/',
        authorize_url='https://github.com/login/oauth/authorize',
        access_token_url='https://github.com/login/oauth/access_token',
    )

    @classmethod
    def get_credentials(cls, response, oauth_token):
        me = cls.client.get('/user', access_token=oauth_token)
        return dict(
            username=me.content['login'],
            access_token=oauth_token,
            service_id=me.content['id'],
        )
