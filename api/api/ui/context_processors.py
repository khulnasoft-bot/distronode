import base64
import os

from api.main.utils import get_api_version


def csp(request):
    return {'csp_nonce': base64.encodebytes(os.urandom(32)).decode().rstrip()}


def version(request):
    context = getattr(request, 'parser_context', {})
    return {
        'version': get_api_version(),
        'tower_version': get_api_version(),
        'short_tower_version': get_api_version().split('-')[0],
        'deprecated': getattr(context.get('view'), 'deprecated', False),
    }
