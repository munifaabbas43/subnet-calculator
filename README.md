# Subnet Calculator

Student: Munifa Abbas
Course: DACS Batch #56, PNY Trainings, Arfa Tower, Lahore

## About this project

This is a Python command line subnet calculator that I built for the networking
module of my DACS diploma. I got tired of doing subnetting by hand every time
I had to check my work for the wireless design and Samba labs, so I wrote this
small tool to speed things up and also to actually understand how the
calculations work under the hood instead of just using an online calculator.

Given an IP address with CIDR notation, it prints:

- Network address
- Broadcast address
- Subnet mask
- Wildcard mask
- Total addresses in the block
- Usable host range
- Whether the address is private or public

It can also split a network into a required number of equal sized subnets,
which I used a lot while planning VLANs for the enterprise wireless project.

## Requirements

- Python 3.8 or newer
- No external libraries needed, it only uses the built in `ipaddress` module

## How to run it

Clone the repo and run it directly:

```bash
git clone https://github.com/your-username/subnet-calculator.git
cd subnet-calculator
python3 subnet_calc.py 192.168.10.0/26
```

To split a network into subnets, for example splitting a /26 into 4 equal
subnets:

```bash
python3 subnet_calc.py 192.168.10.0/26 --split 4
```

## Example output

```
--------------------------------------------------
Input                : 192.168.10.0/26
Network Address      : 192.168.10.0
Broadcast Address    : 192.168.10.63
Subnet Mask          : 255.255.255.192
Wildcard Mask        : 0.0.0.63
Prefix Length        : /26
Total Addresses      : 64
Usable Hosts         : 62
First Usable Host    : 192.168.10.1
Last Usable Host     : 192.168.10.62
Private Address      : True
--------------------------------------------------

Base network 192.168.10.0/26 split into 4 subnets (new prefix /28):

Subnet 1: 192.168.10.0/28
Subnet 2: 192.168.10.16/28
Subnet 3: 192.168.10.32/28
Subnet 4: 192.168.10.48/28
```

## Running the tests

```bash
python3 -m unittest test_subnet_calc.py -v
```

## Project structure

```
subnet-calculator/
├── subnet_calc.py       # main script
├── test_subnet_calc.py  # unit tests
├── README.md
└── LICENSE
```

## What I learned

Writing this made the difference between a /24 and a /26 actually click for
me, since I had to build the host count and usable range logic myself instead
of memorizing a chart. The trickiest part was handling the /31 and /32 edge
cases correctly, since those do not follow the normal "subtract 2 for network
and broadcast" rule.

## Future improvements

- Add IPv6 support
- Add a simple web interface using Flask
- Export subnet plans to a CSV file for documentation purposes

