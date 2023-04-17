import scrapy
import re
import datetime
from scraper.items import ProductItem


class CompelZeroDaysSpider(scrapy.Spider):
    name = 'ic_compel'
    custom_settings = {'ITEM_PIPELINES': {'scraper.pipelines.SqliteCompelPipeline': 300}}
    allowed_domains = ['www.electronshik.ru']
    #start_urls = ['https://www.electronshik.ru/catalog/mikrokontrollery/L1J4']
    start_urls = ['https://www.electronshik.ru/catalog/operatsionnye-usiliteli/KXhN',
                  'https://www.electronshik.ru/catalog/komparatory/KXhX',
                  'https://www.electronshik.ru/catalog/usiliteli-moshchnosti-zch/KXhd',
                  'https://www.electronshik.ru/catalog/preobrazovateli-multimedia/KXhf',
                  'https://www.electronshik.ru/catalog/analogovye-klyuchi/KXhh',
                  'https://www.electronshik.ru/catalog/analogo-tsifrovye-preobrazovateli/KXhj',
                  'https://www.electronshik.ru/catalog/tsifro-analogovye-preobrazovateli/Kpfa',
                  'https://www.electronshik.ru/catalog/istochniki-opornogo-napryazheniya/KXht',
                  'https://www.electronshik.ru/catalog/preobrazovateli-elektricheskih-velichin/KXi7',
                  'https://www.electronshik.ru/catalog/tokovye-monitory/KXiB',
                  'https://www.electronshik.ru/catalog/mikrokontrollery/KXiF',
                  'https://www.electronshik.ru/catalog/signalnye-protsessory/KXiM',
                  'https://www.electronshik.ru/catalog/energonezavisimaya-pamyat/KXiR',
                  'https://www.electronshik.ru/catalog/chasy-realnogo-vremeni-rtc/KXiV',
                  'https://www.electronshik.ru/catalog/taymery-integralnye/KXia',
                  'https://www.electronshik.ru/catalog/interfeysy-rs-485-rs-422/KXio',
                  'https://www.electronshik.ru/catalog/interfeysy-can/KXir',
                  'https://www.electronshik.ru/catalog/interfeysy-rs-232/KXiv',
                  'https://www.electronshik.ru/catalog/interfeysy-usb/KXix',
                  'https://www.electronshik.ru/catalog/interfeysy-ethernet/KXjB',
                  'https://www.electronshik.ru/catalog/transivery-lin/KXjH',
                  'https://www.electronshik.ru/catalog/diody-zashchitnye/KXk3',
                  'https://www.electronshik.ru/catalog/polevye-tranzistory/KXkJ',
                  'https://www.electronshik.ru/catalog/bipolyarnye-tranzistory/KXka',
                  'https://www.electronshik.ru/catalog/igbt-tranzistory/LAEH',
                  'https://www.electronshik.ru/catalog/moduli-silovye-mosfet/KXkl',
                  'https://www.electronshik.ru/catalog/moduli-silovye-igbt/KXkn',
                  'https://www.electronshik.ru/catalog/klyuchi-intellektualnye/KXku',
                  'https://www.electronshik.ru/catalog/rf-svch-tranzistory/KXkz',
                  'https://www.electronshik.ru/catalog/optogalvanicheskie-drayvery/KXlB',
                  'https://www.electronshik.ru/catalog/optopary/KXlF',
                  'https://www.electronshik.ru/catalog/fotopriemniki-integralnye/KXlH',
                  'https://www.electronshik.ru/catalog/opticheskie-transivery/KXlJ',
                  'https://www.electronshik.ru/catalog/akselerometry/KXlW',
                  'https://www.electronshik.ru/catalog/integralnye-datchiki-temperatury/KXlk',
                  'https://www.electronshik.ru/catalog/termopary/KXlp',
                  'https://www.electronshik.ru/catalog/datchiki-davleniya/KXlw',
                  'https://www.electronshik.ru/catalog/datchiki-toka-aktivnye/KXmN',
                  'https://www.electronshik.ru/catalog/fototranzistory/KXmb',
                  'https://www.electronshik.ru/catalog/fotodiody/KXmo',
                  'https://www.electronshik.ru/catalog/dc-dc-istochniki-pitaniya/KXo1',
                  'https://www.electronshik.ru/catalog/transivery-lin/KXpF',
                  'https://www.electronshik.ru/catalog/interfeysy-lvds/KXpY',
                  'https://www.electronshik.ru/catalog/interfeys-modemy-plc/KXpZ',
                  'https://www.electronshik.ru/catalog/preobrazovateli-interfeysov/KXpd',
                  'https://www.electronshik.ru/catalog/tsifrovye-izolyatory/KXpr',
                  'https://www.electronshik.ru/catalog/drayvery-rasshiriteli/KXpt',
                  'https://www.electronshik.ru/catalog/mikroshemy-zashchity/KXq1',
                  'https://www.electronshik.ru/catalog/mikroshemy-prostoy-logiki/KXq7',
                  'https://www.electronshik.ru/catalog/preobrazovateli-logicheskogo-urovnya/KXqB',
                  'https://www.electronshik.ru/catalog/formirovateli-impulsa-sbrosa/KXqP',
                  'https://www.electronshik.ru/catalog/izmeriteli-rashoda-elektroenergii/KXqV',
                  'https://www.electronshik.ru/catalog/kontrollery-sensornoy-klaviatury/KXqY',
                  'https://www.electronshik.ru/catalog/kontrollery-ac-dvigateley/KXqZ',
                  'https://www.electronshik.ru/catalog/kontrollery-dc-dvigateley/KXqd',
                  'https://www.electronshik.ru/catalog/regulyatory-lineynye/KXql',
                  'https://www.electronshik.ru/catalog/regulyatory-dlya-ac-dc/KXqn',
                  'https://www.electronshik.ru/catalog/kontrollery-dlya-ac-dc/KXqr',
                  'https://www.electronshik.ru/catalog/drayvery-igbt-i-mosfet/KXqu',
                  'https://www.electronshik.ru/catalog/kontrollery-dlya-dc-dc/KXr7',
                  'https://www.electronshik.ru/catalog/kontrollery-kkm/KXrD',
                  'https://www.electronshik.ru/catalog/kontrollery-sinhronnyh-vypryamiteley/KXrI',
                  'https://www.electronshik.ru/catalog/regulyatory-dlya-svetodiodnyh-lamp/KXrL',
                  'https://www.electronshik.ru/catalog/mikroshemy-zaryada-akkumulyatorov/KXrN',
                  'https://www.electronshik.ru/catalog/dopolnitelnye-kontrollery-pitaniya/KXrV',
                  'https://www.electronshik.ru/catalog/diody-vypryamitelnye/KXjr',]

    def parse(self, response):
        product_urls = response.css('a.part-name::attr(href)').getall()

        for product_url in product_urls:
            yield scrapy.Request(response.urljoin(product_url), callback=self.parse_product)

        next_page_url = response.css('div#paginator > div > div:nth-child(3) > a::attr(href)').get()

        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_product(self, response):
        special_mark_hit = response.css('span.part_special_mark_hit::text').get(default='')
        category = response.css('div#breadcrumbs nav.breadcrumbs ul li span[itemprop="name"]::text')[-2].get()
        item_offers = response.xpath('//table[@id="item_offers"]')
        item_id_search = item_offers.xpath('@data-item_id_search').get()
        query_string = item_offers.xpath('@data-query_string').get()
        search_brend = item_offers.xpath('@data-search_brend').get()
        weight = item_offers.xpath('@data-weight').get()
        deleted = item_offers.xpath('@data-deleted').get()

        #cookies = response.headers.getlist('Set-Cookie')

        cookies = {
            'ELECTRO': 'ph1q1pfe869irt5nqh3kp27jq4',
            'dimension7': 'ax1',
            '_ym_uid': '1679378866694971231',
            '_ym_d': '1679378866',
            '_ym_isad': '2',
            '_gcl_au': '1.1.970854413.1679378868',
            '_ga': 'GA1.2.1647783015.1679378868',
            '_gid': 'GA1.2.855640701.1679378868',
            '_ym_visorc': 'w',
        }

        headers = {
            'authority': 'www.electronshik.ru',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.electronshik.ru',
            'referer': response.url,  # Use the current response URL instead of a hardcoded one
            'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        # make the second request
        xhr_url = 'https://www.electronshik.ru/items_storage/getOffers_v2'
        xhr_data = {
            'storage': 'center',
            'item_id_search': item_id_search,
            'query_string': query_string,
            'search_brend': search_brend,
            'weight': weight,
            'deleted': deleted,
            'changed': 'true'
        }

        yield scrapy.FormRequest(
            xhr_url,
            formdata=xhr_data,
            headers=headers,
            cookies=cookies,
            callback=self.parse_price_table,
            meta={'query_string': query_string, 'search_brend': search_brend, 'prod_url': response.url,
                  'category': category, 'special_mark_hit': special_mark_hit}
        )

    def parse_price_table(self, response):
        def collect_fraction(price_element):
            fraction_element = price_element.xpath('./following-sibling::span[@class="fraction"]/text()').get()
            if fraction_element is not None:
                return fraction_element.replace(',', '')
            else:
                return 0

        dms_offers = response.css('tr.dms_offer')

        # Инициализация переменных для минимальной цены, количества товара и времени до отгрузки
        lowest_price = None
        lowest_price_qty = None
        lowest_days_until_shipment = None

        # Обход элементов с информацией о продуктах
        for offer in dms_offers:
            # Извлечение информации о времени до отгрузки
            days_until_shipment_element = offer.css('td.offer-header-dt::text').get()
            days_until_shipment = int(re.sub(r'\D', '', days_until_shipment_element))

            # Извлечение информации о цене
            price_elements = offer.css('span.integer')
            for price_element in price_elements:
                if price_element is not None:
                    price = re.sub(r'\D', '', price_element.get())
                    fraction = collect_fraction(price_element)
                    price = float(price + '.' + fraction)
                    qty_td = offer.css('td.offer-header-avail::attr(data-qty)').get()

                    # Проверка, что время до отгрузки равно нулю
                    if days_until_shipment == 0:
                        # Проверка, что цена меньше текущей минимальной цены
                        if lowest_price is None or price < lowest_price:
                            lowest_price = price
                            lowest_price_qty = int(qty_td)
                            lowest_days_until_shipment = days_until_shipment
                    # Если время до отгрузки не равно нулю
                    else:
                        # Проверяем, что временя до отгрузки меньше текущего минимального времени до отгрузки
                        if lowest_days_until_shipment is None or days_until_shipment < lowest_days_until_shipment:
                            lowest_days_until_shipment = days_until_shipment
                            lowest_price = price
                            lowest_price_qty = int(qty_td)
                        # Если время до отгрузки равно текущему минимальному времени до отгрузки, то проверяем цену
                        elif days_until_shipment == lowest_days_until_shipment:
                            # Проверяем, что цена меньше текущей минимальной цены
                            if lowest_price is None or price < lowest_price:
                                lowest_price = price
                                lowest_price_qty = int(qty_td)

        product_item = ProductItem()

        product_item['category'] = response.meta['category'].split('\n')[1].strip()
        product_item['name'] = response.meta['query_string']
        product_item['brand'] = response.meta['search_brend']
        product_item['price'] = lowest_price
        product_item['quantity'] = lowest_price_qty
        product_item['days_until_shipment'] = lowest_days_until_shipment
        product_item['special_mark_hit'] = response.meta['special_mark_hit']
        product_item['url'] = response.meta['prod_url']
        product_item['date'] = datetime.date.today()

        yield product_item
