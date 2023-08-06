import ipaddress
import logging
import os
import re
from urllib.parse import urlsplit
from urlfinderlib import is_valid


class SIPWhitelist:
    def __init__(self, whitelist_tags, sip):
        """ Initiates the SIP whitelist system.

            whitelist_tags: A list of tags from Deprecated SIP indicators you want included in your whitelist.
            sip: A connected PySIP object (see https://github.com/integraldefense/pysip for details)
        """

        # Initiate logging.
        self.logger = logging.getLogger()

        # Set up the whitelist and cache.
        self.whitelist = {}
        self.cache_whitelisted = []
        self.cache_nonwhitelisted = []

        try:
            # Search for the whitelisted indicators with raw mongo because the API is slow.
            sip_result = sip.get('/api/indicators?status=Deprecated&tags={}&bulk=true'.format(','.join(whitelist_tags)))
            for r in sip_result:
                if not r['type'] in self.whitelist:
                    self.whitelist[r['type']] = []

                # If this indicator is an "Address - ipv4-net", make it an IPv4Network.
                if r['type'] == 'Address - ipv4-net':
                    try:
                        self.whitelist[r['type']].append(ipaddress.ip_network(r['value'], strict=False))
                    except:
                        pass
                # Otherwise just add the value to the whitelist.
                else:
                    self.whitelist[r['type']].append(r['value'])

            # Make sure the whitelist only contains unique entries.
            for indicator_type in self.whitelist:
                self.whitelist[indicator_type] = list(set(self.whitelist[indicator_type]))
        except:
            self.logger.exception('Error getting whitelisted indicators from SIP.')

    def _is_cached_whitelisted(self, thing):
        """ Checks if 'thing' has been added to the whitelisted cache. """

        if thing:
            if str(thing).lower() in self.cache_whitelisted:
                self.logger.debug('Cached whitelisted: {}'.format(thing))
                return True
        return False

    def _is_cached_nonwhitelisted(self, thing):
        """ Checks if 'thing' has been added to the nonwhitelisted cache. """

        if thing:
            if str(thing).lower() in self.cache_nonwhitelisted:
                self.logger.debug('Cached non-whitelisted: {}'.format(thing))
                return True
        return False

    def _add_whitelisted_cache(self, thing):
        """ Adds 'thing' to the whitelisted cache. Removes it from the nonwhitelisted cache if it exists. """

        try:
            self.cache_whitelisted.append(str(thing).lower())
        except:
            pass

        try:
            self._remove_nonwhitelisted_cache(str(thing).lower())
        except:
            pass

    def _remove_whitelisted_cache(self, thing):
        """ Removes 'thing' from the whitelisted cache. """

        try:
            self.cache_whitelisted.remove(str(thing).lower())
        except:
            pass

    def _add_nonwhitelisted_cache(self, thing):
        """ Adds 'thing' to the nonwhitelisted cache. Removes it from the whitelisted cache if it exists. """

        try:
            self.cache_nonwhitelisted.append(str(thing).lower())
        except:
            pass

        try:
            self._remove_whitelisted_cache(str(thing).lower())
        except:
            pass

    def _remove_nonwhitelisted_cache(self, thing):
        """ Removes 'thing' from the nonwhitelisted cache. """

        try:
            self.cache_nonwhitelisted.remove(str(thing).lower())
        except:
            pass

    def _is_whitelisted(self, thing, indicator_types, value_in_indicator=True, indicator_in_value=False):
        """ Check if 'thing' is whitelisted by the given indicator types. """

        # Make sure we actually have a "thing".
        if not thing:
            self.logger.debug('Given an invalid thing to check!')
            return True

        # First check if 'thing' was already cached.
        if self._is_cached_whitelisted(thing):
            return True
        if self._is_cached_nonwhitelisted(thing):
            return False

        try:
            for indicator_type in indicator_types:
                if indicator_type in self.whitelist:
                    for indicator in self.whitelist[indicator_type]:
                        # Return True if there is an exact match.
                        if thing.lower() == indicator.lower():
                            self._add_whitelisted_cache(thing)
                            self.logger.debug('Exact {} whitelist match: {}'.format(indicator_type, thing))
                            return True
                        # Check if we want to look for the value inside the indicator.
                        # This accounts for there already being a more specific version of
                        # "thing" already whitelisted in SIP.
                        if value_in_indicator:
                            if thing.lower() in indicator.lower():
                                self._add_whitelisted_cache(thing)
                                self.logger.debug('{} is in whitelisted {} indicator: {}'.format(thing, indicator_type, indicator))
                                return True
                        # Check if we want to look for the indicator inside the value.
                        # This accounts for things like file paths, where we want to
                        # whitelist a directory and everything inside of it.
                        if indicator_in_value:
                            if indicator.lower() in thing.lower():
                                self._add_whitelisted_cache(thing)
                                self.logger.debug('Whitelisted {} indicator {} is in: {}'.format(indicator_type, indicator, thing))
                                return True
        except:
            self.logger.exception('Could not check "{}" against whitelist types: {}'.format(thing, indicator_types))

        self._add_nonwhitelisted_cache(thing)
        return False

    """
    #
    # FILE WHITELIST
    #
    """
    def _is_hash_whitelisted(self, hash_value, hash_type):
        """ Returns True if the hash_value is invalid or whitelisted. """

        # First check if the hash_value was already cached.
        if self._is_cached_whitelisted(hash_value):
            return True
        if self._is_cached_nonwhitelisted(hash_value):
            return False

        # Check if the hash_value is valid.
        try:
            if hash_type == 'Hash - MD5':
                if not re.compile(r'^[a-fA-F0-9]{32}$').match((hash_value)):
                    self._add_whitelisted_cache(hash_value)
                    self.logger.debug('Invalid MD5 hash: {}'.format(hash_value))
                    return True
            if hash_type == 'Hash - SHA1':
                if not re.compile(r'^[a-fA-F0-9]{40}$').match((hash_value)):
                    self._add_whitelisted_cache(hash_value)
                    self.logger.debug('Invalid SHA1 hash: {}'.format(hash_value))
                    return True
            if hash_type == 'Hash - SHA256':
                if not re.compile(r'^[a-fA-F0-9]{64}$').match((hash_value)):
                    self._add_whitelisted_cache(hash_value)
                    self.logger.debug('Invalid SHA256 hash: {}'.format(hash_value))
                    return True
            if hash_type == 'Hash - SHA512':
                if not re.compile(r'^[a-fA-F0-9]{128}$').match((hash_value)):
                    self._add_whitelisted_cache(hash_value)
                    self.logger.debug('Invalid SHA512 hash: {}'.format(hash_value))
                    return True
        except:
            self._add_whitelisted_cache(hash_value)
            return True

        return self._is_whitelisted(hash_value, [hash_type], value_in_indicator=False)

    def is_md5_whitelisted(self, md5):
        """ Returns True if the MD5 is invalid or whitelisted. """

        return self._is_hash_whitelisted(md5, 'Hash - MD5')

    def is_sha1_whitelisted(self, sha1):
        """ Returns True if the SHA1 is invalid or whitelisted. """

        return self._is_hash_whitelisted(sha1, 'Hash - SHA1')

    def is_sha256_whitelisted(self, sha256):
        """ Returns True if the SHA256 is invalid or whitelisted. """

        return self._is_hash_whitelisted(sha256, 'Hash - SHA256')

    def is_sha512_whitelisted(self, sha512):
        """ Returns True if the SHA512 is invalid or whitelisted. """

        return self._is_hash_whitelisted(sha512, 'Hash - SHA512')

    def is_ssdeep_whitelisted(self, ssdeep):
        """ Returns True if the ssdeep is whitelisted. """

        return self._is_whitelisted(ssdeep, ['Hash - SSDEEP'])

    def is_file_name_whitelisted(self, name, value_in_indicator=False, indicator_in_value=True):
        """ Returns True if the file name is whitelisted. """

        return self._is_whitelisted(name, ['Windows - FileName'], value_in_indicator=value_in_indicator, indicator_in_value=indicator_in_value)

    def is_file_path_whitelisted(self, path, value_in_indicator=True, indicator_in_value=True):
        """ Returns True if the file path is whitelisted. """

        return self._is_whitelisted(path, ['Windows - FilePath'], value_in_indicator=value_in_indicator, indicator_in_value=indicator_in_value)

    """
    #
    # EMAIL WHITELIST
    #
    """
    def is_email_subject_whitelisted(self, subject, value_in_indicator=True, indicator_in_value=False):
        """ Returns True if the subject is whitelisted. """

        return self._is_whitelisted(subject, ['Email - Subject'], value_in_indicator=value_in_indicator, indicator_in_value=indicator_in_value)

    def is_email_address_whitelisted(self, address, value_in_indicator=True, indicator_in_value=False):
        """ Returns True if the email address is whitelisted. """

        # First check if the address was already cached.
        if self._is_cached_whitelisted(address):
            return True
        if self._is_cached_nonwhitelisted(address):
            return False

        # Check if the address is valid.
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}')
        try:
            if not email_pattern.match(address):
                self._add_whitelisted_cache(address)
                self.logger.debug('Invalid e-mail address: {}'.format(address))
                return True
        except:
            self._add_whitelisted_cache(address)
            return True

        # Check if the domain is valid.
        try:
            domain = address.split('@')[1]
            if not is_valid(domain):
                self._add_whitelisted_cache(address)
                self.logger.debug('Invalid e-mail address domain: {}'.format(address))
                return True
        except:
            self._add_whitelisted_cache(address)
            return True

        return self._is_whitelisted(address, ['Email - Address', 'WHOIS Registrant Email Address', 'Email Address From', 'Email Address Sender'], value_in_indicator=value_in_indicator, indicator_in_value=indicator_in_value)

    """
    #
    # NETWORK WHITELIST
    #
    """
    def is_url_whitelisted(self, u, value_in_indicator=False, indicator_in_value=False):
        """ Returns True if the URL is invalid or is whitelisted. """

        # First check if the URL was already cached.
        if self._is_cached_whitelisted(u):
            return True
        if self._is_cached_nonwhitelisted(u):
            return False

        # Check if the URL is valid.
        if not is_valid(u):
            self._add_whitelisted_cache(u)
            self.logger.debug('Invalid URL: {}'.format(u))
            return True

        # Split the URL and check each part against the whitelist.
        split_url = urlsplit(u)

        # First check if the netloc has a ':' in it, which indicates that
        # there is a port number specified. We need to remove that in order
        # to properly check it against the whitelists.
        if ':' in split_url.netloc:
            netloc = split_url.netloc.split(':')[0]
        else:
            netloc = split_url.netloc

        # Look for the edge case of the URL having a username:password notation.
        if ':' in split_url.netloc and '@' in split_url.netloc:
            user_pass = re.compile(r'(.*?:.*?@)').findall(split_url.netloc)[0]
            user_pass_url = u.replace(user_pass, '')
            split_url = urlsplit(user_pass_url)
            netloc = split_url.netloc

        # Check the netloc. Check if it is an IP address.
        try:
            ipaddress.ip_address(netloc)
            if self.is_ip_whitelisted(netloc):
                self._add_whitelisted_cache(u)
                self.logger.debug('URL whitelisted because of IP: {}'.format(u))
                return True
        # If we got an exception, it must be a domain name.
        except:
            if self.is_domain_whitelisted(netloc):
                self._add_whitelisted_cache(u)
                self.logger.debug('URL whitelisted because of domain: {}'.format(u))
                return True

        # Check the URI path if it exists.
        if split_url.path and split_url.path != '/':
            if self.is_uri_path_whitelisted(split_url.path):
                self._add_whitelisted_cache(u)
                self.logger.debug('URL whitelisted because of path: {}'.format(u))
                return True

        # Check the URI query if it exists.
        if split_url.query:
            if self.is_uri_path_whitelisted(split_url.query):
                self._add_whitelisted_cache(u)
                self.logger.debug('URL whitelisted because of query: {}'.format(u))
                return True

        # Finally check the entire URL.
        return self._is_whitelisted(u, ['URI - URL'], value_in_indicator=value_in_indicator, indicator_in_value=indicator_in_value)

    def is_uri_path_whitelisted(self, path, relationships=[], value_in_indicator=True, indicator_in_value=True):
        """ Returns True if the URI path is whitelisted. """

        # First check if the path was already cached.
        if self._is_cached_whitelisted(path):
            return True
        if self._is_cached_nonwhitelisted(path):
            return False

        # Check if any of the relationships (if we were given any) are whitelisted.
        for r in relationships:

            # Check if the relationship is a full URL by using urlsplit. If there is no
            # netloc attribute, then it is either an IP or a domain, not a full URL.
            split = urlsplit(r)
            if not split.netloc:

                # Check if the relationship is an IP address.
                try:
                    ipaddress.ip_address(r)
                    # If the IP is whitelisted, we should whitelist that path.
                    if self.is_ip_whitelisted(r):
                        self._add_whitelisted_cache(path)
                        self.logger.debug('{} URI - Path whitelisted because of relationship to IP address: {}'.format(path, r))
                        return True
                # If we got an exception, it must be a domain name.
                except:
                    # If the domain is whitelisted, we should whitelist the path.
                    if self.is_domain_whitelisted(r):
                        self._add_whitelisted_cache(path)
                        self.logger.debug('{} URI - Path whitelisted because of relationship to domain: {}'.format(path, r))
                        return True
            # Otherwise it must be a full URL.
            else:
                if self.is_url_whitelisted(r):
                    self._add_whitelisted_cache(path)
                    self.logger.debug('{} URI - Path whitelisted because of relationship to URL: {}'.format(path, r))
                    return True

        return self._is_whitelisted(path, ['URI - Path'], value_in_indicator=value_in_indicator, indicator_in_value=indicator_in_value)

    def is_domain_whitelisted(self, domain, value_in_indicator=False, indicator_in_value=True):
        """ Returns True if the domain has an invalid TLD or is whitelisted. """

        # First check if the domain was already cached.
        if self._is_cached_whitelisted(domain):
            return True
        if self._is_cached_nonwhitelisted(domain):
            return False

        # Check if the domain has a valid TLD.
        if not is_valid(domain):
            self._add_whitelisted_cache(domain)
            self.logger.debug('Invalid domain: {}'.format(domain))
            return True

        return self._is_whitelisted(domain, ['URI - Domain Name'], value_in_indicator=value_in_indicator, indicator_in_value=indicator_in_value)

    def is_ip_whitelisted(self, ip, value_in_indicator=False, indicator_in_value=False):
        """ Returns True if the IP is invalid, private, or whitelisted. """

        # First check if the IP was already cached.
        if self._is_cached_whitelisted(ip):
            return True
        if self._is_cached_nonwhitelisted(ip):
            return False

        # Check if the IP address is valid.
        try:
            ipaddress.ip_address(ip)
        except:
            self._add_whitelisted_cache(ip)
            self.logger.debug('Invalid IP address: {}'.format(ip))
            return True

        # Make sure this is a public IP address.
        # .is_global was added in Python 3.4
        try:
            if not ipaddress.ip_address(ip).is_global:
                self._add_whitelisted_cache(ip)
                self.logger.debug('IP {} whitelisted because it is not a global address'.format(ip))
                return True
        except:
            # Make sure this is a public IP address.
            if ipaddress.ip_address(ip).is_private:
                self._add_whitelisted_cache(ip)
                self.logger.debug('IP {} whitelisted because it is a private address'.format(ip))
                return True

        # Check if the IP address falls inside a whitelisted network.
        try:
            for network in self.whitelist['Address - ipv4-net']:
                if ipaddress.ip_address(ip) in network:
                    self._add_whitelisted_cache(ip)
                    self.logger.debug('IP {} whitelisted because it is in network {}'.format(ip, network))
                    return True
        except:
            self.logger.exception('Could not check IP "{}" against whitelisted networks'.format(ip))

        # Lastly check if the IP address itself is whitelisted.
        return self._is_whitelisted(ip, ['Address - ipv4-addr', 'Email Originating IP', 'Email X-Originating IP'], value_in_indicator=value_in_indicator, indicator_in_value=indicator_in_value)
