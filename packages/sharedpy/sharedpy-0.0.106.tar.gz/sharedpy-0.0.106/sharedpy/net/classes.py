import requests
from numbers import Number

from ..number.utils import is_valid_latitude, is_valid_longitude
from .utils import is_valid_v4_ip, resolve_host
from .random import find_all_valid_v4_ips




class BadIps(object):

    def __init__(self, ip):
        '''
        Queries Bad Ips API for the specified IP's threat level
        More info: https://www.badips.com/documentation
        '''
        self.ip = ip
        self.threat = None

        if not isinstance(ip, str):
            raise TypeError("Invalid IP data type")

        if not is_valid_v4_ip(ip):
            raise ValueError("Invalid IP")

        url = 'https://www.badips.com/get/info/{0}'.format(str(ip))
        response = requests.get(url, headers={'User-Agent': 'My User Agent 1.0'}) # Bad IPs requires a useragent, otherwise returns 403 access denied
        
        if response.status_code != 200:
            raise ValueError("Non-OK status returned: {0}".format(r.status))

        js = response.json()

        if 'err' in js:
            raise ValueError(js['err'])

        if not js['Score']:
            raise ValueError("Expected score element not found")

        # Not listed - IP is ok
        if not js['Listed']:
            return

        # Average out all threat scores for this IP
        self.threat = round(sum(js['Score'].values()), 1)


    def get_random_ip():
        '''
        Returns a random 'bad' ip address from the Bad IPs website
        '''
        url = 'https://www.badips.com/info'
        response = requests.get(url, headers={'User-Agent': 'My User Agent 1.0'}) # Bad IPs requires a useragent, otherwise returns 403 access denied

        if response.status_code != 200:
            raise ValueError("Non-OK status returned: {0}".format(response.reason))

        return find_all_valid_v4_ips(response.text)[0]




class Ip2Country(object):
    
    def __init__(self, ip):
        '''
        Attempts to return the country name for the IP.
        If country is unknown then returned value will be None
        Raises requests.ConnectionError exception on connection error
        https://about.ip2c.org/#outputs
        '''
        self.two_letter_country_code = None
        self.three_letter_country_code = None
        self.country = None

        if not isinstance(ip, str):
            raise TypeError("Invalid IP data type")

        if not is_valid_v4_ip(ip):
            raise ValueError("Invalid IP")

        r = requests.get('https://ip2c.org/?ip={0}'.format(ip), verify=False)

        if r.status_code != 200:
            raise ValueError("Non-OK status returned: {0}".format(r.status))

        self.two_letter_country_code, self.three_letter_country_code, self.country = Ip2Country._deconstruct_ip2c_response(r.text)

    def _deconstruct_ip2c_response(text):

        # Expected response example: # 1;AU;AUS;Australia
        if ';' not in text:
            raise ValueError("Expected delimiter not present in response")

        split_response = text.split(';')

        if split_response[0] == '0': # Bad response
            raise ValueError("Invalid server response")

        if split_response[0] == '1': # Good response
            two_letter_country_code = split_response[1].strip()
            three_letter_country_code = split_response[2].strip()
            country = split_response[3].strip()
            return two_letter_country_code, three_letter_country_code, country

        if split_response[0] == '2': # Country / IP not present in database
            raise Ip2Country.CountryNotPresentException()

        raise ValueError("Unexpected server response")

    class CountryNotPresentException(Exception):
        pass




class ProjectHoneyPot(object):

    def __init__(self, ip, key):
        '''
        Queries Project Honey Pot API for the specified IP
        https://www.projecthoneypot.org/httpbl_api.php
        '''
        self.ip = ip
        self.key = key
        self.days_since_last_active = None
        self.threat = None
        self.type = None

        self._query = ProjectHoneyPot._construct_php_query(ip, key)

        response = resolve_host(self._query)

        if not response:
            return

        self.days_since_last_active, self.threat, self.type = ProjectHoneyPot._deconstruct_php_response(response)


    def get_random_ip():
        '''
        Returns a random 'bad' ip address from the Project Honey Pot website
        '''
        response = requests.get("https://www.projecthoneypot.org/list_of_ips.php?rss=1")

        if response.status_code != 200:
            raise ValueError("Non-OK status returned: {0}".format(response.status))

        return find_all_valid_v4_ips(response.text)


    def _deconstruct_php_response(ip):
        '''
        Breaks-apart the IP response from PHP into its octets
        Returns: days_since_last_active, threat, type
        '''
        if not isinstance(ip, str):
            raise TypeError("Invalid IP data type")

        if not is_valid_v4_ip(ip):
            raise ValueError("Invalid IP")

        ip_reversed = ip.split('.')

        # The first octet is always 127 and is pre-defined to not have a
        # specified meaning related to the particular visitor.
        if ip_reversed[0] != "127":
            raise ValueError("Invalid PHP response")

        # The second octet represents the number of days since last activity.
        days_since_last_active = int(ip_reversed[1])

        # The third octet represents a threat score for IP.  This score is
        # assigned internally by Project Honey Pot based on a number of factors
        # including the number of honey pots the IP has been seen visiting, the
        # damage done during those visits (email addresses harvested or forms
        # posted to), etc.
        threat = int(ip_reversed[2])

        # The fourth octet represents the type of visitor.  Defined types
        # include: "search engine," "suspicious," "harvester," and "comment
        # spammer."
        # Because a visitor may belong to multiple types (e.g., a harvester
        # that is also a comment spammer) this octet is represented as a bitset
        # with an aggregate value from 0 to 255.
        type = int(ip_reversed[3])

        return days_since_last_active, threat, type


    def _construct_php_query(ip, key):
        '''
        Constructs the hostname to query the Project Honey Pot Ip blacklist (via DNS)
        Format: <Access Key>.<Octet-Reversed IP>.<List-Specific Domain>
        E.g. abcdefghijkl.2.1.9.127.dnsbl.httpbl.org
        https://www.projecthoneypot.org/httpbl_api.php
        '''
        if not isinstance(ip, str):
            raise TypeError("Invalid IP data type")

        if not isinstance(key, str):
            raise TypeError("Invalid key data type")

        if not is_valid_v4_ip(ip):
            raise ValueError("Invalid IP")

        iplist = str(ip).split('.')
        iplist.reverse()
        return '{0}.{1}.{2}'.format(key, '.'.join(iplist), 'dnsbl.httpbl.org')


    

class ReverseGeoCode(object):

    def __init__(self, latitude, longitude):
        '''
        Converts geographic coordinates into a human-readable address
        https://nominatim.org/release-docs/develop/api/Reverse/
        e.g. https://nominatim.openstreetmap.org/reverse?format=json&lat=52.5487429714954&lon=-1.91602098644987
        '''
        self.latitude = latitude
        self.longitude = longitude
        self.formatted_address = self.postcode = self.country = self.county = self.state = self.state_district = self.city = self.suburb = self.road = self.house_number = None
     
        if not isinstance(latitude, Number):
            raise TypeError("Invalid latitude type")

        if not isinstance(longitude, Number):
            raise TypeError("Invalid longitude type")

        if not is_valid_latitude(latitude):
            raise ValueError("Invalid latitude value")

        if not is_valid_longitude(longitude):
            raise ValueError("Invalid longitude value")

        url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}'.format(latitude, longitude)
        req = requests.get(url, timeout=30)

        if req.status_code != 200:
            raise HTTPError(req.reason)

        data = req.json()

        if data.get('error', None):
            if data['error'] == 'Unable to geocode':
                raise ReverseGeoCode.NoResolvedAddressException()
            else:
                raise Exception("Error: {}".format(data['error']))

        if not data.get("lat"):
            raise ValueError("Empty latitude response")

        if not is_valid_latitude(data['lat']):
            raise ValueError("Invalid latitude value returned: {}".format(data['lat']))

        if not data.get("lon"):
            raise ValueError("Empty longitude response")

        if not is_valid_longitude(data['lon']):
            raise ValueError("Invalid longitude value returned: {}".format(data['lon']))

        if not data.get("address"):
            raise ValueError("No address returned")

        if not data.get("display_name"):
            raise ValueError("No display name returned")

        self.formatted_address = data['display_name']

        address = data['address']

        if address.get('house_number'):
            self.house_number = str(address['house_number']).strip()

        if address.get('road'):
            self.road = str(address['road']).strip()

        if address.get('suburb'):
            self.suburb = str(address['suburb']).strip()

        if address.get('city'):
            self.city = str(address['city']).strip()

        if address.get('county'):
            self.county = str(address['county']).strip()
            
        if address.get('state_district'):
            self.state_district = str(address['state_district']).strip()
        
        if address.get('state'):
            self.state = str(address['state']).strip()
            
        if address.get('postcode'):
            self.postcode = str(address['postcode']).strip()
        
        if address.get('country'):
            self.country = str(address['country']).strip()

    class NoResolvedAddressException(Exception):
        pass
