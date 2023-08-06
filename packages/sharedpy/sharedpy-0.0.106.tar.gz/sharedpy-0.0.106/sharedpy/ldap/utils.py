from ldap3 import Server, Connection, BASE, ALL




def create_connection(server, user, password):
    '''
    Creates and returns a bound LDAP connection
    '''
    server = Server(server)
    c = Connection(server, user=user, password=password, auto_bind=True)
    return c


def get_root_domain_naming_context(server, username, password):
    server = Server(server, get_info=ALL)
    c = Connection(server, user=username, password=password, auto_bind=True)
    rdnc = server.info.other['rootDomainNamingContext'][0]
    c.unbind()
    return rdnc


def get_domain_controller_dns_host_names(connection, root_domain_naming_context):
    mb = connection.extend.standard.paged_search(
            search_base=root_domain_naming_context,
            attributes=['masteredBy',],
            search_filter='(&(objectClass=top)(objectClass=domain)(objectClass=domainDNS))',
            search_scope=BASE,
            paged_size=100,
            generator=False)
    if mb[0]['dn'] != root_domain_naming_context:
        raise Exception('Unexpected masteredBy response')
    ntds_settings_dns = [x for x in mb[0]['attributes']['masteredBy']]

    server_dns = []
    for dn in ntds_settings_dns:
        if not dn.startswith('CN=NTDS Settings,'):
            raise Exception('Unexpected masteredBy distinguished name value')
        server_dns.append(dn[17:])

    dns = []
    for dn in server_dns:
        server = connection.extend.standard.paged_search(
            search_base=dn,
            attributes=['dNSHostName',],
            search_filter='(objectClass=server)',
            search_scope=BASE,
            paged_size=100,
            generator=False)

        if server[0]['dn'] != dn:
            raise Exception('Unexpected domain controller search response')
    
        dns.append(server[0]['attributes']['dNSHostName'])
    return dns


def get_value_or_first_list_value(value):
    '''
    Intended to be used with Active Directory attributes that may be returned as a single value or as a list of one or more values
    '''
    if isinstance(value, list):
        if len(value) > 0:
            return value[0]
        else:
            return None
    else:
        return value


class UserAccountControl():
    '''
    Flags that control the behavior of the user account.
    This attribute value can be zero or a combination of one or more values.
    https://msdn.microsoft.com/en-us/library/ms680832.aspx
    http://www.selfadsi.org/ads-attributes/user-userAccountControl.htm
    https://stackoverflow.com/a/1888133
    '''

    ADS_UF_SCRIPT = 0x00000001
    ADS_UF_ACCOUNTDISABLE = 0x00000002
    ADS_UF_HOMEDIR_REQUIRED = 0x00000008
    ADS_UF_LOCKOUT = 0x00000010
    ADS_UF_PASSWD_NOTREQD = 0x00000020
    ADS_UF_PASSWD_CANT_CHANGE = 0x00000040
    ADS_UF_ENCRYPTED_TEXT_PASSWORD_ALLOWED = 0x00000080
    ADS_UF_TEMP_DUPLICATE_ACCOUNT = 0x00000100
    ADS_UF_NORMAL_ACCOUNT = 0x00000200
    ADS_UF_INTERDOMAIN_TRUST_ACCOUNT = 0x00000800
    ADS_UF_WORKSTATION_TRUST_ACCOUNT = 0x00001000
    ADS_UF_SERVER_TRUST_ACCOUNT = 0x00002000
    ADS_UF_DONT_EXPIRE_PASSWD = 0x00010000
    ADS_UF_MNS_LOGON_ACCOUNT = 0x00020000
    ADS_UF_SMARTCARD_REQUIRED = 0x00040000
    ADS_UF_TRUSTED_FOR_DELEGATION = 0x00080000
    ADS_UF_NOT_DELEGATED = 0x00100000
    ADS_UF_USE_DES_KEY_ONLY = 0x00200000
    ADS_UF_DONT_REQUIRE_PREAUTH = 0x00400000
    ADS_UF_PASSWORD_EXPIRED = 0x00800000
    ADS_UF_TRUSTED_TO_AUTHENTICATE_FOR_DELEGATION = 0x01000000

    def __init__(self, user_account_control_value):
        self.user_account_control_value = user_account_control_value

    @property
    def script(self):
        ''' The logon script is executed. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_SCRIPT)

    @property
    def accountdisable(self):
        ''' The user account is disabled. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_ACCOUNTDISABLE)

    @property
    def homedir_required(self):
        ''' The home directory is required. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_HOMEDIR_REQUIRED)

    @property
    def lockout(self):
        ''' The account is currently locked out. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_LOCKOUT)

    @property
    def passwd_notreqd(self):
        ''' No password is required. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_PASSWD_NOTREQD)

    @property
    def passwd_cant_change(self):
        ''' The user cannot change the password. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_PASSWD_CANT_CHANGE)

    @property
    def encrypted_text_password_allowed(self):
        ''' The user can send an encrypted password. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_ENCRYPTED_TEXT_PASSWORD_ALLOWED)

    @property
    def temp_duplicate_account(self):
        ''' This is an account for users whose primary account is in another domain. This account provides user access to this domain, but not to any domain that trusts this domain. Also known as a local user account. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_TEMP_DUPLICATE_ACCOUNT)

    @property
    def normal_account(self):
        ''' This is a default account type that represents a typical user. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_NORMAL_ACCOUNT)

    @property
    def interdomain_trust_account(self):
        ''' This is a permit to trust account for a system domain that trusts other domains. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_INTERDOMAIN_TRUST_ACCOUNT)

    @property
    def workstation_trust_account(self):
        ''' This is a computer account for a computer that is a member of this domain. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_WORKSTATION_TRUST_ACCOUNT)

    @property
    def server_trust_account(self):
        ''' This is a computer account for a system backup domain controller that is a member of this domain. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_SERVER_TRUST_ACCOUNT)

    @property
    def dont_expire_passwd(self):
        ''' The password for this account will never expire. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_DONT_EXPIRE_PASSWD)

    @property
    def mns_logon_account(self):
        ''' This is an MNS logon account. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_MNS_LOGON_ACCOUNT)

    @property
    def smartcard_required(self):
        ''' The user must log on using a smart card. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_SMARTCARD_REQUIRED)

    @property
    def trusted_for_delegation(self):
        ''' The service account (user or computer account), under which a service runs, is trusted for Kerberos delegation. Any such service can impersonate a client requesting the service. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_TRUSTED_FOR_DELEGATION)

    @property
    def not_delegated(self):
        ''' The security context of the user will not be delegated to a service even if the service account is set as trusted for Kerberos delegation. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_NOT_DELEGATED)

    @property
    def use_des_key_only(self):
        ''' Restrict this principal to use only Data Encryption Standard (DES) encryption types for keys. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_USE_DES_KEY_ONLY)

    @property
    def dont_require_preauth(self):
        ''' This account does not require Kerberos pre-authentication for logon. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_DONT_REQUIRE_PREAUTH)

    @property
    def password_expired(self):
        ''' The user password has expired. This flag is created by the system using data from the Pwd-Last-Set attribute and the domain policy. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_PASSWORD_EXPIRED)

    @property
    def trusted_to_authenticate_for_delegation(self):
        ''' The account is enabled for delegation. This is a security-sensitive setting; accounts with this option enabled should be strictly controlled. This setting enables a service running under the account to assume a client identity and authenticate as that user to other remote servers on the network. '''
        return bool(self.user_account_control_value & UserAccountControl.ADS_UF_TRUSTED_TO_AUTHENTICATE_FOR_DELEGATION)
