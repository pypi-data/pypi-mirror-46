#!/usr/bin/env python3

import os, sys, argparse, logging
import requests

def single(domain, rrtype):
	if not rrtype.upper() in ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT']:
		return "You provided an invalid rrtype: {}".format(rrtype)

	try:
		data = requests.get("https://dnsjson.com/{}/{}.json".format(domain, rrtype.upper()))
		if data.status_code in [200]:
			data = data.json()
			if data['success']:
				return data['results']['records']
	except:
		return None

def main():

	parser = argparse.ArgumentParser()

	# IO
	parser.add_argument("--input", '-i', help="path to list of domains (in plain text)")
	parser.add_argument("--output", '-o', help="path to output")

	# Records
	parser.add_argument("--rrtype", "-r", help="rrtype to collate", default="AAAA")

	# Modes
	parser.add_argument("--single", "-s", help="single domain mode", action="store_true")

	# Domain (in single mode)
	parser.add_argument("domain", help="domain name (single mode only)", default="", nargs="?")
	
	# Verbose mode
	parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)
	log = logging.getLogger(__name__)

	if args.single:
		print("\n".join(single(args.domain, args.rrtype)))
	
if __name__ == '__main__':
	main()
