import functools
from urllib.parse import urlencode
import urllib.parse as urlparse
from .error_exception import ERROR
from . import access_token
from tornado import gen


def authenticated(method):
    """modified from web.authenticated
    """

    @functools.wraps(method)
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        is_valid = yield verify_access_token(self)
        if is_valid:
            if gen.is_coroutine_function(method):
                yield method(self, *args, **kwargs)
            else:
                method(self, *args, **kwargs)
        else:
            if self.is_api_mode():
                err = ERROR.E40301
                self.write_error(err.code(), err.message())
            else:
                if self.request.method in ("GET", "HEAD"):
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            # if login url is absolute, make next absolute too
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urlencode(dict(next=next_url))
                    self.redirect(url)

    return wrapper


@gen.coroutine
def verify_access_token(self):
    remote_ip = self.request.remote_ip

    if self.is_api_mode():
        # API模式
        user_id = self.request.headers.get("x-user-id")
        token = self.request.headers.get("x-access-token")
        # 判断是否为合法token
        valid = yield access_token.verify_access_token(user_id, token, remote_ip)
        if not valid:
            return False
    else:
        # 网页模式
        user_id = self.get_secure_cookie("user-id")
        if user_id is None:
            return False
        user_id = user_id.decode()

        token = self.get_secure_cookie("access-token")
        if token is None:
            return False
        token = token.decode()

        # 判断是否为合法token
        valid = yield access_token.verify_access_token(user_id, token, remote_ip)
        if not valid:
            return False

    return True


