# check_domain_whois

check_domain_whois is a monitoring plugin that can be used to monitor your registered domains' values, using whois.
It returns CRITICAL if a value is different according to the given expected values.
Otherwise it returns OK if all checks succeeded or UNKNOWN if the checks could not be executed.

### Usage
Possible options:  

    -h:                            Help
    -H/--Host <Host>:              The host you want to check for security breaches
    -r/--registrar <registrar>:    The expected registrar for the given host
    -n/--nameserver "<ns1>, ...":  The expected nameservers for the given host
    -s/--status "<status1>, ...":  The expected domain status values

For the script to work, you have to at least give it a host and (a registrar or nameservers).
Otherwise the script will set the status of the check to UNKNOWN as it then cannot execute any checks.

A possible usage could look like this:

```shell
python check_domain_whois.py -H example.com -r "ExampleRegistrar" -n "ns1.example.com, ns2.example.com" -s "Connect, ClientTransferProhibited"
```

### Dependencies

To retrieve the whois data the [python-whois](https://github.com/richardpenman/whois) library was used.
To be able to execute the script you first need to install it:

```shell
python3 -m pip install python-whois
```