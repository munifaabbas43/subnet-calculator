#!/usr/bin/env python3
"""
Subnet Calculator
Author: Munifa Abbas
Course: DACS Batch #56, PNY Trainings, Arfa Tower, Lahore

A command line tool that takes an IPv4 address with CIDR notation
(for example 192.168.10.0/26) and prints the full subnet breakdown:
network address, broadcast address, first and last usable host,
total hosts, usable hosts, subnet mask and wildcard mask.

It also supports splitting a network into a required number of
equal sized subnets (VLSM style), which is the part I used the most
while practicing the wireless network design and Samba lab, since
both of those needed clean IP ranges to work with.
"""

import argparse
import ipaddress
import sys


def get_network_info(cidr):
    """Return a dictionary with all the relevant details for a given
    network in CIDR form, e.g. 192.168.1.0/24"""
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError as err:
        print(f"Error: {err}")
        sys.exit(1)

    total_hosts = network.num_addresses
    if network.prefixlen >= 31:
        usable_hosts = total_hosts
        first_host = network.network_address
        last_host = network.broadcast_address
    else:
        usable_hosts = total_hosts - 2
        hosts = list(network.hosts())
        first_host = hosts[0]
        last_host = hosts[-1]

    info = {
        "input": cidr,
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "netmask": str(network.netmask),
        "wildcard_mask": str(network.hostmask),
        "prefix_length": network.prefixlen,
        "total_addresses": total_hosts,
        "usable_hosts": usable_hosts,
        "first_usable_host": str(first_host),
        "last_usable_host": str(last_host),
        "is_private": network.is_private,
    }
    return info


def print_info(info):
    print("-" * 50)
    print(f"Input                : {info['input']}")
    print(f"Network Address      : {info['network_address']}")
    print(f"Broadcast Address    : {info['broadcast_address']}")
    print(f"Subnet Mask          : {info['netmask']}")
    print(f"Wildcard Mask        : {info['wildcard_mask']}")
    print(f"Prefix Length        : /{info['prefix_length']}")
    print(f"Total Addresses      : {info['total_addresses']}")
    print(f"Usable Hosts         : {info['usable_hosts']}")
    print(f"First Usable Host    : {info['first_usable_host']}")
    print(f"Last Usable Host     : {info['last_usable_host']}")
    print(f"Private Address      : {info['is_private']}")
    print("-" * 50)


def split_network(cidr, required_subnets):
    """Split a base network into equal sized subnets. Picks the smallest
    new prefix length that satisfies the requested number of subnets."""
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError as err:
        print(f"Error: {err}")
        sys.exit(1)

    new_prefix = network.prefixlen
    while (2 ** (new_prefix - network.prefixlen)) < required_subnets:
        new_prefix += 1
        if new_prefix > 32:
            print("Error: cannot fit that many subnets inside this network.")
            sys.exit(1)

    subnets = list(network.subnets(new_prefix=new_prefix))
    print(f"\nBase network {cidr} split into {len(subnets)} subnets "
          f"(new prefix /{new_prefix}):\n")
    for index, sub in enumerate(subnets[:required_subnets], start=1):
        print(f"Subnet {index}: {sub}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Subnet Calculator - DACS Batch 56 project by Munifa Abbas"
    )
    parser.add_argument(
        "cidr",
        help="Network in CIDR notation, e.g. 192.168.1.0/24"
    )
    parser.add_argument(
        "-s", "--split",
        type=int,
        help="Number of equal subnets to split the network into"
    )

    args = parser.parse_args()

    info = get_network_info(args.cidr)
    print_info(info)

    if args.split:
        split_network(args.cidr, args.split)


if __name__ == "__main__":
    main()
