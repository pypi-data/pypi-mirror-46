from urllib.parse import urlparse

import collections
import logging
import requests
import validators

from nameko.dependency_providers import Config
from nameko.events import event_handler, EventDispatcher

from .logger import LoggingDependency
from .storages import RedisStorage

HEAD_TIMEOUT = 10  # in seconds
GET_TIMEOUT = 3 * 60  # in seconds

log = logging.info
FakeResponse = collections.namedtuple('Response', ['status_code', 'headers',
                                                   'url', 'history'])
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=50)
session.mount('http://', adapter)


class CrawlerService(object):
    name = 'url_crawler'
    storage = RedisStorage()
    logger = LoggingDependency()
    dispatch = EventDispatcher()
    config = Config()

    @event_handler('http_server', 'url_to_check')
    @event_handler('timer', 'url_to_check')
    def check_url(self, url_group_frequency):
        url, group, frequency = url_group_frequency
        log(('Checking {url} for group {group} and frequency "{frequency}"'
             .format(url=url, group=group, frequency=frequency)))
        if not validators.url(url):
            logging.error('Error with {url}: not a URL'.format(url=url))
            return
        self.storage.store_url(url)
        if group:
            self.storage.store_group(url, group)
            if frequency:
                self.storage.store_frequency(url, group, frequency)
        head_timeout = self.config.get('CRAWLER_HEAD_TIMEOUT', HEAD_TIMEOUT)
        get_timeout = self.config.get('CRAWLER_GET_TIMEOUT', GET_TIMEOUT)
        no_head_domains = self.config.get('HEAD_DOMAINS_BLACKLIST', [])
        try:
            domain = urlparse(url).netloc
            head_offend = domain in no_head_domains
            if not head_offend:
                try:
                    response = session.head(url, allow_redirects=True,
                                            timeout=head_timeout)
                except requests.exceptions.ReadTimeout:
                    # simulate 404 to trigger GET request below
                    log('Timeout on %s', url)
                    response = FakeResponse(status_code=404, headers={},
                                            url=url, history=[])
            # Double check for servers not dealing properly with HEAD.
            if head_offend or response.status_code in (404, 405):
                log('Checking {url} with a GET'.format(url=url))
                response = session.get(url, allow_redirects=True,
                                       timeout=get_timeout, stream=True)
                response.close()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout):
            response = FakeResponse(status_code=503, headers={}, url=url,
                                    history=[])
        except Exception as e:
            logging.error('Error with {url}: {e}'.format(url=url, e=e))
            return
        finally:
            self.storage.remove_check_flag(url)
        metadata = self.storage.store_metadata(url, response)
        self.dispatch('url_crawled', metadata)
