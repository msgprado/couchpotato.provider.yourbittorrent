from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.helpers.variable import tryInt, getImdb
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
from bs4 import BeautifulSoup

import traceback
#import requests

log = CPLog(__name__)

class YourBitTorrent(TorrentProvider, MovieProvider):

    urls = {
        'test': 'http://yourbittorrent.com',
        'login': '',
        'login_check': '',
        'detail': 'http://yourbittorrent.com%s',
        'search': 'http://yourbittorrent.com/?q=%s&c=1',
        'download': 'http://yourbittorrent.com/down/%s.torrent',
    }
    

    http_time_between_calls = 1 #seconds
	
#    def search(self, movie, quality):
#
#        if not quality.get('hd', False):
#            return []
#
#        return super(ExtraTorrent, self).search(movie, quality)

    def _searchOnTitle(self, title, movie, quality, results):
	
        #returnResponse = requests.get(self.urls['test'], verify=False)

        #url = self.urls['search'] % tryUrlencode('%s' % (title.replace(':', '')))
        url = self.urls['search'] % tryUrlencode('%s %s' % (title.replace(':', ''), movie['info']['year']))
        log.debug('>>>> yourbittorrent url %s', (url))		
        #print url

        data = self.getHTMLData(url)
        if data:
            html = BeautifulSoup(data)
            try:
                resultsTable = html.find_all('table', attrs = {'class' : 'bordered'})[1]
                if resultsTable is None:
                   log.debug('>>>> yourbittorrent EMPTY RESULT')
                   return

                #log.debug('result table %s', (resultsTable) )
                entries = resultsTable.find_all('tr')[1:-1]
                #log.debug('>>> result %s', (entries))
                
                for result in entries:
                    if result.find('td', attrs = {'class' : 'v'}) is None:
                        log.debug('>>> retornado')
                        continue
                    #log.debug('for result %s', result)
                    torrent_details = result.find_all('td')[0].find('a')['href']
                    torrent_split = result.find_all('td')[0].find('a')['href'].split('/')
                    torrent_id = torrent_split[2] 
                    torrent_title = result.find_all('td')[0].find('a').get_text()                                     
					
                    log.debug('>>>torrent_t %s', (torrent_title))
                    #torrent_title = [x.extract() for x in a.findAll('script')]	
                    torrent_seeders = tryInt(result.find('td', attrs = {'class' : 'u'}).string)
                    torrent_leechers = tryInt(result.find('td', attrs = {'class' : 'd'}).string)
                    torrent_size = self.parseSize(result.find('td', attrs = {'class' : 's'}).contents[0])                    
                    imdb_id = getImdb(torrent_title, check_inside = True)
					
					#get .torrent file
                    #down_url = self.urls['detail'] % torrent_details
                    #down_data = self.getHTMLData(down_url)
					
                    #if down_data:
					
                        #down_html = BeautifulSoup(down_data)
                        #results_down = down_html.find('ul', attrs = {'class' : 'download_links'})
						
                        #if results_down is None:
                        #    log.debug('>>>> yourbittorrent EMPTY RESULT', (url))
                        #    return;
							
                        #entries = resultsTable.find_all('li')[1]
						
                        #torrent_download = entries.find('a')['href']
					    ##################
                    #log.debug('>>>id %s', (torrent_id))
                    #log.debug('>>>title %s', (torrent_title))
                    #log.debug('>>> size %s', (torrent_size))
                    log.debug('>>> torrent_download %s', (self.urls['download'] % torrent_id))
					

                    results.append({
                       'id': torrent_id,
                       'name': torrent_title,
                       'url': self.urls['download'] % torrent_id,
                       'detail_url': self.urls['detail'] % torrent_details,
                       'size': torrent_size,
                       'seeders': torrent_seeders if torrent_seeders else 0,
                       'leechers': torrent_leechers if torrent_leechers else 0,
                       'description': imdb_id if imdb_id else '',
                    })

            except:
                log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))

#    def getLoginParams(self):
#        return tryUrlencode({
#            'user': self.conf('username'),
#            'pass': self.conf('password'),
#        })
#
#    def loginSuccess(self, output):
#        return '{"kod":1,"msg":"0"}' in output.lower()
#
#    loginCheckSuccess = loginSuccess
