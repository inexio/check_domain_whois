#! /usr/bin/env python

"""
Nagios Plugin to check whether whois returns the expected registrar or (and) the expected name servers
"""

import whois
import argparse

__author__  = 'Inexio'
__version__ = 0.1


def parse_args():
    parser = argparse.ArgumentParser(description="Nagios Plugin to check whether whois returns the expected registrar or (and) the expected name servers")
    parser.add_argument("-H", "--Host", type=str, help="Domain to check")
    parser.add_argument("-n", "--nameserver", type=str, help="Expected nameservers")
    parser.add_argument("-r", "--registrar", type=str, help="Expected registrar")
    return parser.parse_args()


def main():
    args = parse_args().__dict__
    host = args["Host"]
    expected_ns = args["nameserver"].replace(" ", "").split(",")
    expected_registrar = args["registrar"]

    if host is None:
        print("UNKNOWN - No host is given. Use -H <Host>")
        exit(3)

    if expected_ns is None and expected_registrar is None:
        print("UNKNOWN - Please use -r to give the expected registrar or/and -n to give the expected nameservers")
        exit(3)

    w = whois.whois(host)
    registrar = None
    if "registrar" in w.keys():
        registrar = w["registrar"]
    ns = None
    if "name_servers" in w.keys():
        ns = w["name_servers"]

    if registrar is None and ns is None:
        print("UNKNOWN - whois did not deliver any nameservers or the registrar for %s" % host)
        exit(3)

    # Check Registrars
    if registrar is not None and expected_registrar is not None:
        if registrar.upper() != expected_registrar.upper():
            print("CRITICAL - Registrar was changed for %s, it doesn't meet the expectations: Expected %s, Actual: %s" % (host, expected_registrar, registrar))
            exit(2)

    # Check Nameservers
    wrong_ns = []
    if ns is not None and expected_ns is not None:
        for i in range(len(ns)):
            ns[i] = ns[i].upper()
        for nameserver in expected_ns:
            if nameserver.upper() not in ns:
                wrong_ns.append(nameserver)
    if len(wrong_ns) != 0:
        print("CRITICAL - Nameservers were changed for %s, they don't meet the expectations: Expected: %s, Actual: %s" % (host, expected_ns, ns))
        exit(2)

    print("OK - The values for %s were like expected" % host)
    exit(0)


if __name__ == "__main__":
    main()
