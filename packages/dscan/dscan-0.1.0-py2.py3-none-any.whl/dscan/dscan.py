#!/usr/bin/env python3

import requests

class dscan:
	def __init__(self, provider='cloudflare'):
		self.provider = provider
		self.headers = {
			'Accept': 'application/dns-json'
		}

		if not self.provider in ["cloudflare", "google", "quad9"]:
			self.provider = "cloudflare"
		
		providers = {
			'cloudflare': "https://cloudflare-dns.com/dns-query",
			'google': 'https://dns.google.com/resolve',
			'quad9': 'https://dns.quad9.net/dns-query'
		}
		self.base = providers[self.provider]

	def single(self, domain, rrtype='AAAA'):
		if not rrtype.upper() in ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT']:
			return "You provided an invalid rrtype: {}".format(rrtype)

		try:
			data = requests.get(
				"{}?name={}&type={}".format(self.base, domain, rrtype),
				headers=self.headers
			)
			if data.status_code == 200:
				data = data.json()
				if data['Status'] == 0:
					results = []
					try:
						for answer in data['Answer']:
							results.append(answer['data'])
						return results
					except:
						return []
			return []
		except:
			return []