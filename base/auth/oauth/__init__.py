from .twitter import TwitterOAuth
from .github import GithubOAuth
from .facebook import FacebookOAuth


PROVIDERS = [TwitterOAuth, FacebookOAuth, GithubOAuth]
