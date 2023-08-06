# sipwhitelist
Python library that interacts with SIP to build an indicator whitelist system.

## Requirements
    https://pypi.org/project/tld/ 0.9+
    https://github.com/IntegralDefense/pysip
    https://github.com/IntegralDefense/urltools
    
## SIPWhitelist parameters
    whitelist_tags: Required. List of indicator tags to build your whitelist.
    sip: Required. PySIP connection.
    
## Example Usage
Creating a SIPWhitelist object will look something like this:

    import pysip
    from sipwhitelist import SIPWhitelist

    sip = pysip.Client('localhost:4443', '11111111-1111-1111-1111-111111111111', verify=False)
    w = SIPWhitelist(['whitelist:e2w'], sip)
    
## Functionality
When you create the SIPWhitelist object, you must specify the "whitelist_tags" attribute. This is a list of tags you want include when searching the Deprecated indicators in SIP to build the whitelist.

For example, if you want the domain "google.com" to be whitelisted, two conditions must be met in SIP:

1. The indicator must be set to Deprecated in SIP.
2. The indicator must have one of the tags you specified in the "whitelist_tags" attribute when you created the SIPWhitelist object. The example above uses the "whitelist:e2w" tag.

When these two criteria are met, SIPWhitelist will include that indicator in its whitelist.

### value_in_indicator vs. indicator_in_value
Most of the public functions available in the SIPWhitelist class provide both a "value_in_indicator" and an "indicator_in_value" boolean parameter. These parameters allow you to mirror the functionality of how SIP indicator matching is performed as though they are wildcard/substring values.

If you are checking if "thing" is whitelisted, these parameters mean:
* **value_in_indicator**: If the "thing" string exists in a whitelisted indicator, "thing" is considered to be whitelisted.
    
    * This is set to **True** when we want the whitelisted indicators to match against less specific "thing" values. Think file paths, for example. If we whitelisted the path "C:\Users\Administrator\AppData\Roaming\Microsoft\Office\something.tmp", and one of the sandbox reports showed a dropped file but listed the path as "AppData\Roaming\Microsoft\Office\something.tmp", then presumably we would want to consider this path whitelisted as well.

* **indicator_in_value**: If a whitelisted indicator exists in "thing", then "thing" is considered to be whitelisted.

    * This is set to **True** when we want less specific whitelisted indicators to match against "thing" values. Again, think about file paths. We can't realistically whitelist every combination of file paths, but we know that certain paths are almost always benign, such as any path containing the whitelisted string "Microsoft\CryptnetUrlCache\".

### Default Behavior
The behavior of the following public functions in the SIPWhitelist class have been customized to the best default behavior for our events and [Event Sentry](https://github.com/IntegralDefense/eventsentry).

Most of the functions outlined below check to see if the given value is invalid.
* **Example**: If you check if the domain name "google.local" is whitelisted, it will return True since ".local" is not a valid top-level domain.

There is a caching system built-in, so if you check the same value twice, it will return faster whether it was cached as whitelisted or non-whitelisted.

**is_md5_whitelisted(md5)**

    Checks whitelisted indicators: Hash - MD5
    Returns: True/False if the "md5" string is whitelisted or the md5 is invalid
    
**is_sha1_whitelisted(sha1)**

    Checks whitelisted indicators: Hash - SHA1
    Returns: True/False if the "sha1" string is whitelisted or the sha1 is invalid
    
**is_sha256_whitelisted(sha256)**

    Checks whitelisted indicators: Hash - SHA256
    Returns: True/False if the "sha256" string is whitelisted or the sha256 is invalid
    
**is_sha512_whitelisted(sha512)**

    Checks whitelisted indicators: Hash - SHA512
    Returns: True/False if the "sha512" string is whitelisted or the sha512 is invalid
    
**is_ssdeep_whitelisted(ssdeep)**

    Checks whitelisted indicators: Hash - SSDEEP
    Returns: True/False if the "ssdeep" string is whitelisted
    
**is_file_name_whitelisted(name, value_in_indicator=False, indicator_in_value=True)**

    Checks whitelisted indicators: Windows - FileName
    Returns: True/False if the "name" string is whitelisted

Example: If "~WRS" is whitelisted, then:
* "~WRS{ab90d-fade840abc-9e9da}" is whitelisted.
* "WRS" is NOT whitelisted.

**is_file_path_whitelisted(path, value_in_indicator=True, indicator_in_value=True)**

    Checks whitelisted indicators: Windows - FilePath
    Returns: True/False if the "path" string is whitelisted

Example: If "AppData/Local/Microsoft" is whitelisted, then:

* "Local/Microsoft" is whitelisted (even though this is not a valid path)
* "C:/Users/Dude/AppData/Local/Microsoft/something.tmp" is whitelisted.
* "C:/Users/Dude/AppData/Local/malicious.exe" is NOT whitelisted.

**is_email_subject_whitelisted(subject, value_in_indicator=True, indicator_in_value=False)**

    Checks whitelisted indicators: Email - Subject
    Returns: True/False if the "subject" string is whitelisted

Example: If "Hi There" is whitelisted, then:

* "Hi" is whitelisted.
* "Hi There friend" is NOT whitelisted.

**is_email_address_whitelisted(address, value_in_indicator=True, indicator_in_value=False)**

    Checks whitelisted indicators: Email - Address, WHOIS Registrant Email Address, Email Address From, Email Address Sender
    Returns: True/False if the "address" string is whitelisted or the domain is invalid

Example: If "noreply@microsoft.com" is whitelisted, then:

* "reply@microsoft.com" is whitelisted.
* "bad-noreply@microsoft.com" is NOT whitelisted.

**is_url_whitelisted(u, value_in_indicator=False, indicator_in_value=False)**

    Checks whitelisted indicators: URI - URL, Address - ipv4-net, Address - ipv4-addr, URI - Domain Name, URI - Path
    Returns: True/False if the "u" string/domain/IP/path is whitelisted or the domain/IP is invalid

Example: If "http://www.google.com/" is whitelisted, then:

* "http://www.google.com/" is whitelisted.
* "http://www.google.com/something.html" is NOT whitelisted.

**NOTE:** is_url_whitelisted also calls the functions is_uri_path_whitelisted, is_domain_whitelisted, and is_ip_whitelisted.

**is_uri_path_whitelisted(path, relationships=None, value_in_indicator=True, indicator_in_value=True)**

    Checks whitelisted indicators: URI - Path, Address - ipv4-addr, URI - Domain Name
    Returns: True/False if the "path" string is whitelisted OR if any of the relationships are whitelisted

"relationships" is an optional list of values the URI path is related to. For example, if you know the URI path you are checking came from the URL "http://google.com/index.html", then one of the relationships might be "google.com". In this case, if the URI - Domain Name indicator "google.com" was whitelisted, then this URI - Path indicator would also be whitelisted.

Example: If ".css" is whitelisted, then:

* "https://randomsite.com/style.css" is whitelisted.

Example: If "/social/signin/" is whitelisted, then:

* "/social" is whitelisted.

**is_domain_whitelisted(domain, value_in_indicator=False, indicator_in_value=True)**

    Checks whitelisted indicators: URI - Domain Name
    Returns: True/False if the "domain" string is whitelisted or the domain is invalid

Example: If "blog.google.com" is whitelisted, then:

* "http://blog.google.com" is whitelisted.
* "google.com" is NOT whitelisted.

**is_ip_whitelisted(ip, value_in_indicator=False, indicator_in_value=False)**

    Checks whitelisted indicators: Address - ipv4-net, Address - ipv4-addr, Email Originating IP, Email X-Originating IP
    Returns: True/False if the "ip" string is whitelisted or the ip is invalid (including private addresses)

Example: If "100.0.0.0/8" is whitelisted, then:

* "100.1.8.37" is whitelisted.
