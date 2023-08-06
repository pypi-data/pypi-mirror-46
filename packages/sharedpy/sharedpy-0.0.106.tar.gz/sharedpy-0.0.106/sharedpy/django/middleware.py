from django.utils.cache import add_never_cache_headers




class DisableClientCachingMiddleware(object):
    '''
    Prevents caching on the client side
    This middleware must be called before all other middleware
    http://stackoverflow.com/a/5882033
    '''
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response
