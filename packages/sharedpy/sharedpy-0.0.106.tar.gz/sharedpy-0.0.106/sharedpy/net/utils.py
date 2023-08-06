import ipaddress
import re
import requests
import string
import urllib.request
from io import BytesIO
from numbers import Number
from posixpath import basename, dirname
from urllib.parse import urlparse
from socket import gaierror, gethostbyaddr, gethostbyname

from requests.exceptions import HTTPError
from requests_ntlm.requests_ntlm import HttpNtlmAuth

from ..text.utils import contains, remove_extended_characters, get_string_bytes_size, sanitise_hex_string
from ..misc.utils import get_object_sha1, run_cmd, is_windows
from ..number.utils import is_valid_latitude, is_valid_longitude, is_decimal




def get_elevation(latitude, longitude):
    '''
    Provides elevation data for all locations on the surface of the earth excluding the ocean
    Originally used Google Elevation, but that was converted to a paid service
    Converted to use https://github.com/Jorl17/open-elevation/blob/master/docs/api.md (e.g. https://api.open-elevation.com/api/v1/lookup?locations=40.161758,-8.583933) however the service is extremely unreliable
    Now uses https://github.com/racemap/elevation-service (e.g. https://elevation.racemap.com/api?lat=41.161758&lng=-8.183939)
    '''
    if not isinstance(latitude, Number):
        raise TypeError("Invalid latitude type")

    if not isinstance(longitude, Number):
        raise TypeError("Invalid longitude type")

    if not is_valid_latitude(latitude):
        raise ValueError("Invalid latitude value")

    if not is_valid_longitude(longitude):
        raise ValueError("Invalid longitude value")

    url = 'https://elevation.racemap.com/api?lat={}&lng={}'.format(latitude, longitude)

    req = requests.get(url, timeout=30)

    if req.status_code != 200:
        raise HTTPError(req.reason)

    data = req.text
    
    if not data or not is_decimal(data):
        raise ValueError("Invalid data returned: {}".format(data))
        
    return float(data)


def webpage_exists(url, verify=True, headers={'User-Agent': 'My User Agent 1.0'}):
    '''
    Attempts to download the supplied URL.
    Returns True if the status code is less than 400, False if above.
    Note: Does not handle any exceptions
    http://stackoverflow.com/a/16778749
    '''
    request = requests.get(url, verify=verify, headers=headers)
    return request.status_code < 400


def resolve_ip(ip):
    '''
    Attempts to resolve a hostname for the supplied IP address
    If several hostnames are found only the first is returned
    '''
    try:
        return gethostbyaddr(ip)[0]
    except gaierror:
        return None


def resolve_host(host):
    '''
    Attempts to resolve an IP address for the supplied hostname
    If several IP are found only the first is returned
    '''
    try:
        return gethostbyname(host)
    except gaierror:
        return None


def is_valid_v4_or_v6_ip(ip):
    '''
    Returns true if argument is a valid IPv4 or IPv6 address
    '''
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_v4_ip(ip):
    '''
    Returns true if argument is a valid IPv4 address
    https://docs.djangoproject.com/en/1.11/_modules/django/core/validators/#validate_ipv46_address
    '''
    if ip and ip[:1] == '0': # Workaround because '0.107.72.58' is considered valid by the following regex
        return False
    return bool(re.search(r'^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])){3}\Z', ip))



def is_valid_hostname(value):
    '''
    Returns True if all characters are valid for a hostname, and is less than maximum length
    Does not validate a hostname in any other way!
    https://stackoverflow.com/a/3523068/1095373
    '''
    if not value:
        return False

    return contains(value, string.digits + string.ascii_letters + "_-. ") and len(value) <= 253


def get_projecthoneypot_ip_lookup_url(ip):
    '''
    Returns the ProjectHoneyPot.org URL to lookup information relating to an IP
    '''
    return 'https://www.projecthoneypot.org/ip_{0}'.format(ip)


def get_badips_ip_lookup_url(ip):
    '''
    Returns the BadIps.com URL to lookup information relating to an IP
    '''
    return 'https://www.badips.com/info/{0}'.format(ip)


def get_iplookup_url(ip):
    '''
    Returns the Ip-Lookup.net URL to lookup information about the specified IP address 
    '''
    return 'https://ip-lookup.net/index.php?ip={0}'.format(ip)


def get_google_images_search_url(term):
    '''
    Returns the Google Images search URL for the specified term
    Note that no escaping or character cleansing is performed
    '''
    return "https://www.google.com/search?q={0}&tbm=isch".format(term)


def get_wikipedia_search_url(term):
    '''
    Returns the Wikipedia search URL for the specified term
    Note that no escaping or character cleansing is performed
    '''
    return 'https://en.wikipedia.org/wiki/Special:Search/{0}'.format(term)


def get_google_search_url(term):
    '''
    Returns the Google search URL for the specified term
    Note that no escaping or character cleansing is performed
    '''
    return 'https://www.google.com/search?as_epq={0}&num=100'.format(term)


def is_valid_mac(value):
    '''
    Returns true if the supplied string consists of only valid MAC address characters and is 12 characters in length
    '''
    return contains(value, string.hexdigits) and len(value) == 12


def ipv4_is_within_range(ip, start, end):
    '''
    Returns True if the specified IP address falls within the range
    Start and end range values are treated as inclusive of the range definition
    Expects all arguments to be strings
    '''
    return int(ipaddress.IPv4Address(ip)) >= int(ipaddress.IPv4Address(start)) and int(ipaddress.IPv4Address(ip)) <= int(ipaddress.IPv4Address(end))


def is_valid_url(url, attributes_to_validate=None):
    '''
    Returns True if the url is valid
    All attributes that can be validated: scheme, netloc, path, params, query, fragment
    E.g. <scheme>://<netloc>/<path>;<parameters>?<query>#<fragment>
    If no attributes are specified then only 'scheme' and 'netloc' are validated
    https://stackoverflow.com/a/36283503
    https://docs.python.org/3/library/urllib.parse.html
    '''
    minimum_attributes = ('scheme', 'netloc')
    attributes_to_validate = minimum_attributes if attributes_to_validate is None else attributes_to_validate
    tokens = urlparse(url)
    return all([getattr(tokens, qualifying_attr) for qualifying_attr in attributes_to_validate])


def filter_oui_data(raw_oui_data):
    '''
    Filters http://standards-oui.ieee.org/oui/oui.txt (Organization Unique Identifiers)
    Does not download the OUI data - OUI data must be passed in via argument
    Returns [{prefix: vendorname}, ...]
    '''
    r = re.compile('^[0-9A-Fa-f]{6}\s+\(base 16\)\s+')
    data = []
    for line in raw_oui_data.splitlines():
        if r.match(line):
            line = remove_extended_characters(line).replace('(base 16)', '')
            prefix = line[:6]
            vendor = line[6:].strip()
            data.append({prefix: vendor})
    return data


def download(url, timeout=30, proxy=None): # TODO: Tests
    '''
    Proxy must be in format: {'http/https/ftp': 'server:port'}
    '''
    if proxy:
        handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read()


def disable_urllib_warnings(): # TODO: Tests
    requests.packages.urllib3.disable_warnings()


def download_with_ntlm_auth(url, timeout=30, verify=False, ntlm_user=None, ntlm_password=None, disable_warnings=True):  #TODO: Tests
    '''
    https://stackoverflow.com/questions/10115126/python-requests-close-http-connection
    '''
    if disable_warnings:
        disable_urllib_warnings()
    auth = HttpNtlmAuth(ntlm_user, ntlm_password) if ntlm_user and ntlm_password else None
    response = requests.get(url, headers={'Connection':'close'}, timeout=timeout, verify=verify, auth=auth)
    if response.status_code >= 400:
        raise Exception("Invalid status response: {0}".format(response.status_code))
    content = response.content
    text = response.text
    size = get_string_bytes_size(text)
    sha1 = get_object_sha1(content)
    response.connection.close()
    return content, text, size, sha1


def strip_dns_suffix(hostname):
    '''
    Returns the first segment of a hostname (e.g. returns 'google' for the value 'google.com.au')
    Not intended to be used with hostnames beginning with www - will return 'www'
    '''
    return hostname.split('.')[0] if '.' in hostname else hostname


def sanitise_mac(value):
    '''
    Returns a 'clean' MAC address if 12 characters remain after removing all non-hexidecimal characters (not 0-9 A-F a-f).
    '''
    sanitised = sanitise_hex_string(value) if value else None
    return sanitised if sanitised and len(sanitised) == 12 else None


def strip_domain_prefix_from_username(username):
    '''
    Removes the preceeding domain name, if present, from a username
    Domain and user name are expected to be separated by either a forward or backslash
    Returns the username component
    '''
    username_parts = [x for x in username.replace('/', '\\').split('\\') if x]
    return username_parts[len(username_parts) -1]


regex = re.compile(r'\b0+\B')
def strip_leading_zero_ipv4_octets(ip):
    '''
    Removes leading otet zeros from IPv4 addresses.
    Some leading octet zeros appear to be handled and some throw exceptions when parsed with the ipAddress module: https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address
    Examples:
    010.1.0.001 --> 10.1.0.1
    010.064.214.210  --> 10.64.214.210
    010.064.000.150  --> 10.64.0.150
    '''
    return regex.sub('', ip)


def disect_url(url):
    '''
    Disects the supplied URL
    returns: scheme, server, path, file, dirs
    '''
    parser = urlparse(url)
    scheme = parser.scheme
    server = parser.netloc
    path = parser.path
    file = basename(path)
    dirs = dirname(path)
    return scheme, server, path, file, dirs


def download_ftp_file(ftp_client, remote_ftp_file_path):
    '''
    Downloads the FTP file to memory and returns the byte object
    Client must already be created and connected via ftplib
    Based on https://stackoverflow.com/a/18773444
    '''
    sio = BytesIO()
    def handle_binary(more_data):
        sio.write(more_data)
    resp = ftp_client.retrbinary("RETR {0}".format(remote_ftp_file_path), callback=handle_binary)
    sio.seek(0)
    return sio.read()


def get_network_boundaries(network):
    '''
    Determines the first and last IPs given an ipaddress network object
    Returns: First IP, Last IP
    https://stackoverflow.com/a/9717242
    https://stackoverflow.com/a/1942848
    '''
    count = 0
    for ip in network: # len() not implemented, only __iter__()
        count += 1
    return network[0], network[count-1]


def ping(target, max_ping_count, packet_size, timeout): # TODO: tests
    '''
    Pings a host or IP
    If a successful response is not received then ping attempts will continue up to the value of max_pings
    '''
    # Count argument:
    # -n Windows
    # -c Linux

    # Size argument:
    # -l Windows
    # -s Linux

    for _ in range(max_ping_count):
        if is_windows():
            cmd = 'ping.exe -n 1 -l {0} -w {1} {2}'.format(str(packet_size), str(timeout), target)
        else:
            cmd = r'/bin/ping -c 1 -s {0} -w {1} {2}'.format(str(packet_size), str(int(timeout / 1000)), target)
            cmd = cmd.split(' ')

        output, success, error = run_cmd(cmd)
        if success:
            return True
        if error:
            if '100% loss' not in output and '100% packet loss' not in output:
                raise Exception(str(output) + ' : ' + str(cmd))
        # non-responsive ping - allow to retry next loop iteration
    return False
