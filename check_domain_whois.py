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
    parser.add_argument("-s", "--status", type=str, help="Expected status")
    return parser.parse_args()


def main():
    args = parse_args().__dict__
    host = args["Host"]
    expected_ns = None
    if args["nameserver"] is not None:
        expected_ns = args["nameserver"].replace(" ", "").split(",")
    expected_registrar = args["registrar"]
    expected_status = None
    if args["status"] is not None:
        expected_status = args["status"].replace(" ", "").split(",")

    if host is None:
        print("UNKNOWN - No host is given. Use -H <Host>")
        exit(3)

    if expected_ns is None and expected_registrar is None and expected_status is None:
        print("UNKNOWN - Please give at least one expected value with -n, -r or -s")
        exit(3)

    w = whois.whois(host)

    # Get whois results
    registrar = None
    if "registrar" in w.keys():
        registrar = w["registrar"]
    ns = None
    if "name_servers" in w.keys():
        ns = w["name_servers"]
    status = None
    if "status" in w.keys():
        status = w["status"]

    if registrar is None and ns is None and status is None:
        print("UNKNOWN - whois did not deliver any information to check the expected values for %s" % host)
        exit(3)

    # Check Registrars
    if registrar is not None and expected_registrar is not None:
        if registrar.upper() != expected_registrar.upper():
            print("CRITICAL - Registrar changed for %s, it doesn't meet the expectations: Expected %s, Actual: %s" % (host, expected_registrar, registrar))
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
        print("CRITICAL - Nameservers changed for %s, they don't meet the expectations: Expected: %s, Actual: %s" % (host, expected_ns, ns))
        exit(2)

    # Check Status
    wrong_status = []
    if status is not None and expected_status is not None:
        for i in range(len(expected_status)):
            expected_status[i] = expected_status[i].upper()
        for j in range(len(status)):
            status[j] = status[j].upper()
        for expected in expected_status:
            found = False
            for state in status:
                if expected in state:
                    found = True
                    break
            if not found:
                wrong_status.append(expected)
    if len(wrong_status) != 0:
        print("CRITICAL - Domain status changed for %s, it doesn't contain the expectations: Expected: %s, Actual: %s" % (host, expected_status, status))
        exit(2)

    print("OK - The values for %s were like expected" % host)
    exit(0)


if __name__ == "__main__":
    main()
