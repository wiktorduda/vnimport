class ErogetrailersResourceMapper:
	def __init__(self, playnite):
		self.playnite = playnite
		
	def map(self, response):
		results = []
		if response['items']:
			for item in response['items']:
				results.append({
					'kanji_name': item['title'],
					'roman_name': item['romanTitle'],
					'developers': [item['brand']],
					'release_date': item['releaseDayNumber'],
					'links': self._map_item_to_links(item),
					'platform': item['platform'],
					'getchu_id': item['getchu']
				})
		return results

	def _map_item_to_links(self, item):
		getchu_url = 'http://www.getchu.com/soft.phtml?id={}'
		erogamescape_url = 'https://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/game.php?game={}'
		getchu_id = item['getchu']
		erogamescape_id = item['erogamescape']
		links = []
		if item['getchu']:
			links.append(self.playnite.SDK.Models.Link('Getchu', getchu_url.format(getchu_id)))
		if item['erogamescape']:
			links.append(self.playnite.SDK.Models.Link('ErogameScape', erogamescape_url.format(erogamescape_id)))
		return links