# check_domain_whois

check_domain_whois is a Nagios plubin that can be used to monitor your registered domains for security breaches.
It returns CRITICAL if a possible security breach is detected according to the given expected values.
Otherwise it returns OK if all checks succeeded or UNKNOWN if the checks could not be executed.

### Usage
Possible options:  

    -h:             Help
    -H <Host>:      The host you want to check for security breaches
    -r <registrar>: The expected registrar for the given host
    -n <ns1, ...>:  The expected nameservers for the given host

To work you have to at least give the script a host and (a registrar or nameservers).
Otherwise the script will set the status of the check to UNKNOWN.

A possible usage could look like this:

```shell
python check_domain_whois.py -H example.com -r "ExampleUser" -n "ns1.example.com, ns2.example.com"
```
