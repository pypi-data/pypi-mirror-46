from urllib import parse

from affiliate_deeplink.base import BaseDeeplinkGenerator
from affiliate_deeplink.config import NATURA_CONSULTORIA_NAME


class Natura(BaseDeeplinkGenerator):
    """
    https://www.natura.com.br/[...]?consultoria=NATURA_CONSULTORIA_NAME
    """

    @classmethod
    def get_tracking_url(cls, url):
        parsed_uri = parse.urlparse(url)
        query = 'consultoria={}&a=a'.format(NATURA_CONSULTORIA_NAME)
        url = '{scheme}://{netloc}{path}?{query}'.format(scheme=parsed_uri.scheme,
                                                         netloc=parsed_uri.netloc,
                                                         path=parsed_uri.path,
                                                         query=query)
        return url
