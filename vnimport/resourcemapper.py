import datetime

class ErogetrailersResourceMapper:
    def map(self, response):
        results = []
        if response['items']:
            for item in response['items']:
                results.append({
                    'original_name': item['title'],
                    'roman_name': item['romanTitle'],
                    'developers': [item['brand']],
                    'release_date': self._map_release_date(item),
                    'links': self._map_item_to_links(item),
                    'platform': item['platform'],
                    'getchu_id': item['getchu']
                })
        return results

    def _map_release_date(self, item):
        release_date = None
        try:
            release_date = datetime.datetime.strptime(str(item['releaseDayNumber']), '%Y%m%d')
        except ValueError:
            pass
        return release_date

    def _map_item_to_links(self, item):
        getchu_url = 'http://www.getchu.com/soft.phtml?id={}'
        erogamescape_url = 'https://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/game.php?game={}'
        getchu_id = item['getchu']
        erogamescape_id = item['erogamescape']
        links = []
        if item['getchu']:
            links.append({
                    'name': 'Getchu', 
                    'url': getchu_url.format(getchu_id)
            })
        if item['erogamescape']:
            links.append({
                    'name': 'ErogameScape', 
                    'url': erogamescape_url.format(erogamescape_id)
            })
        return links