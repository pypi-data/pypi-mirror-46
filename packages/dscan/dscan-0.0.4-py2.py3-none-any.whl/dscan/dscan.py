#!/usr/bin/env python3

import requests

class dscan:
	def __init__(self, provider='cloudflare'):
		self.provider = provider
		self.headers = {
			'Accept': 'application/dns-json'
		}

		if not self.provider in ["cloudflare", "google"]:
			self.provider = "cloudflare"
		
		if self.provider in ['cloudflare']:
			self.base = "https://cloudflare-dns.com/dns-query"
		if self.provider in ['google']:
			self.base = "https://dns.google.com/resolve"

	def single(self, domain, rrtype='AAAA'):
		if not rrtype.upper() in ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT']:
			return "You provided an invalid rrtype: {}".format(rrtype)

		data = requests.get(
			"{}?name={}&type={}".format(self.base, domain, rrtype),
			headers=self.headers
		)
		if data.status_code == 200:
			data = data.json()
			if data['Status'] == 0:
				results = []
				for answer in data['Answer']:
					results.append(answer['data'])
				return results
		return None
