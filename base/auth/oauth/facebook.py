from .base import AbstractRAuth


class FacebookOAuth(AbstractRAuth):

    name = 'facebook'
    options = dict(
        base_url='https://graph.facebook.com',
        authorize_url='https://www.facebook.com/dialog/oauth',
        access_token_url='https://graph.facebook.com/oauth/access_token',
    )

    @classmethod
    def get_credentials(cls, response, oauth_token):
        me = cls.client.get('/me', access_token=oauth_token)
        return dict(
            username=me.content['username'],
            access_token=oauth_token,
            expires=response.content['expires'],
            service_id=me.content['id'],
        )
