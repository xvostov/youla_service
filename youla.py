import re
import pprint

from loguru import logger
from loader import chrome, db_handler
from utils import stopwatch
from offer import Offer
from exceptions import UnsuitableProductError
from bs4 import BeautifulSoup


class Youla:
    def __init__(self):
        self.chrome = chrome

    @stopwatch
    def get_urls(self, url):
        logger.debug(f'Collecting urls from the category - {url}')
        soup = BeautifulSoup(self.chrome.get_html(url), 'lxml')
        ads_containers = soup.find_all('div', {'data-test-component': 'ProductOrAdCard'})

        ads_urls = []
        for ad_cont in ads_containers:
            try:
                ad_url = ad_cont.find_all('a')[0].get('href')
                if ad_url.startswith('/'):
                    ad_url = 'https://youla.ru' + ad_url
                    ads_urls.append(ad_url)

                else:
                    continue

            except IndexError:
                pass
            else:
                print(ad_url)
                ads_urls.append(ad_url)
        ads_urls = list(set(ads_urls))

        viewed_links = db_handler.get_viewed_links()

        for url in viewed_links:
            try:
                ads_urls.remove(url)
            except ValueError:
                pass
            else:
                logger.debug(f'Offer was found in db, will be skipped - {url}')

        logger.debug(f'Urls from the category are collected. New urls found: {len(ads_urls)}')
        return ads_urls

    @stopwatch
    def get_offer(self, url):
        logger.debug(f'Parsing offer - {url}')
        content = self.chrome.get_html(url)
        soup = BeautifulSoup(content, 'lxml')
        offer = Offer(url)

        offer.title = soup.find_all('h2', {'data-test-block': 'ProductCaption'})[0].text
        logger.debug(f'Title was found - {offer.title}')

        try:
            offer.description = soup.find_all('li', {'data-test-block': 'Description'})[0].text.replace('Описание', '', 1)
        except IndexError:
            logger.warning('Description was not found')
        else:
            logger.debug(f'Description was found')

        offer.price = soup.find_all('span', {'data-test-component': 'Price'})[0].text
        logger.debug(f'Price was found - {offer.price}')

        try:
            offer.photo = soup.find_all('div', {'data-test-component': 'ProductGallery'})[0].find_all('img')[0].get('src')
        except Exception:
            raise UnsuitableProductError
        else:
            logger.debug(f'Price was found - {offer.photo}')

        logger.debug(f'The offer was parsed - {url}')
        return offer


def main():
    app = Youla()
    # urls = app.get_urls('https://youla.ru/moskva/muzhskaya-odezhda/aksessuary?attributes[term_of_placement][from]=-1%20day&attributes[term_of_placement][to]=now&attributes[sort_field]=date_published&attributes[muzhskaya_odezhda_aksessuary_tip][0]=8415&attributes[price][from]=5000000')
    #
    # for url in urls:
    app.get_offer('https://youla.ru/moskva/muzhskaya-odezhda/aksessuary/novyie-muzhskiie-chasy-frederique-constant-horological-60e2f5cdcd9e613538566ccb')

if __name__ == '__main__':
    main()