import urllib.request
from bs4 import BeautifulSoup
import time

class Helper:

    def __init__(self):
        print("init")

    # Получаем исходный код страницы
    def get_html(self, url):
        response = urllib.request.urlopen(url)
        return response.read()

    # Парсим секреты с одной страницы в список.
    def scraping_secrets_from_page(self, html, number):
        soup = BeautifulSoup(html)
        counter = 0
        secrets = []
        div = soup.find_all('div', class_='shortContent')
        for secret in div:
            if counter < number:
                secrets.append(secret.text)
                counter += 1
            else:
                break
        return secrets

    # Переходим на следующую страницу.
    def paginate(self, url):
        if "page" in url:
            cols = url.split('/')
            cols[-1] = str(int(cols[-1]) + 15)
            return "/".join(cols)
        else:
            return url + "/page/15"

    # Парсим все секреты из категории в список списков (потому что иногда полезно
    # было бы вытащить секреты с одной страницы, а не со всех разом).
    def scraping_all_secrets_from_category(self, url, number):
        secrets = []
        while 'В данную категорию пока не добавлено ни одного секрета.' not in BeautifulSoup(Helper.get_html(self, url)).text:
            if len(secrets) < number:
                secrets += Helper.scraping_secrets_from_page(self, Helper.get_html(self, url), number - len(secrets))
                url = Helper.paginate(self, url)
            else:
                break
        return secrets

    # Парсим ссылки на стихи с детского сайта.
    def scraping_links(self, url):
        soup = BeautifulSoup(Helper.get_html(self, url))
        links = []
        trs = soup.table.find_all('a', href=True)
        for tr in trs:
            links.append(tr['href'])
        return links

    # Парсим все стихи от одного автора.
    def scraping_all_verse_from_category(self, url, number):
        links = Helper.scraping_links(self, url)
        tales = []
        counter = 0
        for link in links:
            if counter < number:
                tales.append(Helper.scraping_verse(self, 'https://deti-online.com' + link))
                counter += 1
            else:
                break
        return tales

    # Парсим один стих.
    def scraping_verse(self, url):
        soup = BeautifulSoup(Helper.get_html(self, url))
        verse = ""
        tags = soup.find('div', class_='r').find_all('p')
        for tag in tags:
            for string in tag.contents:
                try:
                    verse += string + ' '
                except:
                    continue
        return verse

    # Парсим стихи из других категорий, тк сайт размечен по-разному.
    def scraping_other_verses(self, url, number):
        counter = 0
        soup = BeautifulSoup(Helper.get_html(self, url))
        divs = soup.find_all('div', class_='txt')
        verses = []
        for verse in divs:
            if counter < number:
                verse_global = ""
                for tag in verse.contents:
                    for string in tag.contents:
                        try:
                            verse_global += string + ' '
                        except:
                            continue
                verses.append(verse_global)
                counter += 1
            else:
                break
        return verses

    # Парсим хорошие рассказы.
    def scraping_good_tales(self, good_categories, number):
        tales = []
        for category in good_categories:
            try:
                if len(tales) < number:
                    tales = tales + Helper.scraping_all_verse_from_category(self, category, number - len(tales))
                else:
                    break
            except:
                time.sleep(1)
                continue

        return tales

    # Парсим хорошие рассказы (страниы сайта с другой разметкой).
    def scraping_good_other_tales(self, good_categories, number):
        tales = []
        for category in good_categories:
            if len(tales) < number:
                tales = tales + Helper.scraping_other_verses(self, category, number - len(tales))
            else:
                break
        return tales

    # Ссылки на стихи.
    def get_good_categories(self):
        barto = 'https://deti-online.com/stihi/stihi-agnii-barto/'
        zahoder = 'https://deti-online.com/stihi/stihi-zahodera/'
        mihalkov = 'https://deti-online.com/stihi/stihi-mihalkova/'
        berestov = 'https://deti-online.com/stihi/stihi-berestova/'
        sapgir = 'https://deti-online.com/stihi/stihi-sapgira/'
        blaginina = 'https://deti-online.com/stihi/stihi-blaginina/'
        surikov = 'https://deti-online.com/stihi/stihi-surikova/'
        shemyakina = 'https://deti-online.com/stihi/stihi-shemyakina/'
        gusarova = 'https://deti-online.com/stihi/stihi-gusarova/'
        uspenskyi = 'https://deti-online.com/stihi/stihi-uspenskogo/'
        mecgera = 'https://deti-online.com/stihi/stihi-mecgera/'

        good_tales = [barto, zahoder, mihalkov, berestov, sapgir, blaginina, surikov, shemyakina, gusarova, uspenskyi,
                      mecgera]

        return good_tales

    # Ссылки на стихи.
    def get_good_categories_other(self):
        animals = 'https://deti-online.com/stihi/stihi-pro-zhivotnyh/'
        birds = 'https://deti-online.com/stihi/stihi-pro-ptic/'
        fishes = 'https://deti-online.com/stihi/stihi-pro-ryb/'
        nasekomye = 'https://deti-online.com/stihi/stihi-pro-nasekomyh/'
        winter = 'https://deti-online.com/stihi/zima/'
        osen = 'https://deti-online.com/stihi/osen/'
        fruits = 'https://deti-online.com/stihi/ovoschi-i-frukty/'
        sea = 'https://deti-online.com/stihi/stihi-pro-more/'
        mushrooms = 'https://deti-online.com/stihi/griby/'
        "help me pls"
        flowers = 'https://deti-online.com/stihi/cvety/'
        spring = 'https://deti-online.com/stihi/vesna/'
        summer = 'https://deti-online.com/stihi/leto/'
        stValentine = 'https://deti-online.com/stihi/stihi-valentina/'
        fevral = 'https://deti-online.com/stihi/stihi-23-fevralya/'
        mart = 'https://deti-online.com/stihi/stihi-8-marta/'
        masl = 'https://deti-online.com/stihi/stihi-maslenica/'
        easter = 'https://deti-online.com/stihi/stihi-pasha/'
        fstsept = 'https://deti-online.com/stihi/stihi-1-sentyabrya/'
        teacher = 'https://deti-online.com/stihi/stihi-den-uchitelya/'
        motherDay = 'https://deti-online.com/stihi/stihi-den-materi/'
        xmas = 'https://deti-online.com/stihi/stihi-rozhdestvo/'
        newyear = 'https://deti-online.com/stihi/stihi-pro-novyy-god/'
        tree = 'https://deti-online.com/stihi/stihi-pro-novogodnyuyu-elku/'
        forlittle = 'https://deti-online.com/stihi/novogodnie-stihi-dlya-malenkih/'
        moroz = 'https://deti-online.com/stihi/stihi-pro-deda-moroza/'
        snegurochka = 'https://deti-online.com/stihi/stihi-pro-snegurochku/'
        sneg = 'https://deti-online.com/stihi/stihi-pro-snezhinki/'
        snowman = 'https://deti-online.com/stihi/stihi-pro-snegovika/'
        "zaebalsya"
        good_tales_other = [snowman, sneg, snegurochka, moroz, forlittle, tree, newyear, xmas, motherDay, teacher, fstsept,
                            easter, masl, mart, fevral, stValentine, summer, spring, flowers, mushrooms, sea, fruits, osen,
                            animals, birds, fishes, winter, nasekomye]

        return good_tales_other


class Scraper:

    def __init__(self):
        print("init")

    # Финальный метод получения хороших рассказов.
    @staticmethod
    def get_good_tales(x):
        helper = Helper()
        if x % 2 == 0:
            y = x / 2
        else:
            y = (x + 1)/2

        good = helper.scraping_good_other_tales(helper.get_good_categories_other(), (x+1)/2 - 1) \
               + helper.scraping_good_tales(helper.get_good_categories(), y)

        return good

    # Финальный метод получения плохих рассказов.
    @staticmethod
    def get_bad_tales(bad_categories, number):
        helper = Helper()
        secrets = []
        for category in bad_categories:
            if len(secrets) < number:
                secrets += (helper.scraping_all_secrets_from_category(category, number - len(secrets)))
            else:
                break
        return secrets

    # Ссылки на категории в подслушано.
    @staticmethod
    def get_bad_categories():
        vulgar = 'https://ideer.ru/secrets/vulgar'
        angry = 'https://ideer.ru/secrets/angry'
        pizdec = 'https://ideer.ru/secrets/pizdec'
        lust = 'https://ideer.ru/secrets/lust'
        cherhuha = 'https://ideer.ru/secrets/cherhuha'
        cruelty = 'https://ideer.ru/secrets/cruelty'
        ebanko = 'https://ideer.ru/secrets/ebanko'
        fuuu = 'https://ideer.ru/secrets/fuuu'
        betrayal = 'https://ideer.ru/secrets/betrayal'
        alco = 'https://ideer.ru/secrets/alco'
        boom = 'https://ideer.ru/secrets/boom'
        envy = 'https://ideer.ru/secrets/envy'
        enrage = 'https://ideer.ru/secrets/enrage'

        bad_categories = [vulgar, angry, pizdec, lust, cherhuha, cruelty, ebanko, fuuu, betrayal, alco, boom, envy,
                          enrage]

        return bad_categories
