from urllib.parse import urlencode




def build_href_tag(url, display_text, new_window=False, title=None):
    '''
    Returns the HTML to build an <a href...> tag string from values supplied
    WARNING: There is NO filtering or escaping of ANY characters.
    Character cleansing must be performed prior to calling this method.
    '''
    target = "target='_blank' " if new_window else ''    
    return "<a {0}href='{1}'{2}>{3}</a>".format(target, url, 'title="{0}"'.format(title) if title else '', display_text)
    
    
def url_with_querystring(path, **kwargs):
    '''
    Constructs a URL with query parameters
    Does NOT preserve kwarg order
    '''
    return '{0}?{1}'.format(path, urlencode(kwargs))


def build_img_tag(src, height, width, alt):
    '''
    Constructs an IMG tag
    WARNING: There is NO filtering or escaping of ANY characters.
    '''
    return '<img height="{0}" width="{1}" src="{2}" alt="{3}"/>'.format(height, width, src, alt)
