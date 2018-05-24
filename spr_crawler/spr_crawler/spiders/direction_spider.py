import re

import scrapy


class QuotesSpider(scrapy.Spider):
    """
    Returns urls of institutions by given direction url
    """
    name = "direction"
    filename = "institutions.txt"

    direction = 'https://www.spr.ru/all/medtsentri/'

    # direction = 'https://www.spr.ru/all/dispanseri-vrachebno-fizkulturnie/'  # Диспансеры врачебно-физкультурные'
    # direction = 'https://www.spr.ru/all/dispanseri-kozhno-venerologicheskie/'  # Диспансеры кожно-венерологические'
    # direction = 'https://www.spr.ru/all/dispanseri-mammologicheskie/'  # Диспансеры маммологические'
    # direction = 'https://www.spr.ru/all/dispanseri-narkologicheskie/'  # Диспансеры наркологические'
    # direction = 'https://www.spr.ru/all/dispanseri-onkologicheskie/'  # Диспансеры онкологические'
    # direction = 'https://www.spr.ru/all/dispanseri-protivotuberkuleznie/'  # Диспансеры противотуберкулезные'
    # direction = 'https://www.spr.ru/all/dispanseri-psihonevrologicheskie/'  # Диспансеры психоневрологические'
    # direction = 'https://www.spr.ru/all/dispanseri-endokrinologicheskie/'  # Диспансеры эндокринологические'
    # direction = 'https://www.spr.ru/all/zhenskie-konsultatsii/'  # Женские консультации'
    # direction = 'https://www.spr.ru/all/mediko-sotsialnaya-ekspertiza-mse/'  # Медико-социальная экспертиза, МСЭ'
    # direction = 'https://www.spr.ru/all/polikliniki-detskie/'  # Поликлиники детские'
    # direction = 'https://www.spr.ru/all/polikliniki-gorodskie/'  # Поликлиники'
    # direction = 'https://www.spr.ru/all/travmpunkti/'  # Травмпункты'
    # direction = 'https://www.spr.ru/all/ginekologicheskie-kliniki-eko-tsentri/'  # Гинекологические клиники, ЭКО, центры репродукции'
    # direction = 'https://www.spr.ru/all/detskie-meditsinskie-tsentri/'  # Детские медицинские центры'
    # direction = 'https://www.spr.ru/all/kliniki-i-lechebnie-tsentri-pri-meditsinskih-nii/'  # Клиники и лечебные центры при медицинских НИИ'
    # direction = 'https://www.spr.ru/all/lechebno-ozdorovitelnie-tsentri/'  # Лечебно-оздоровительные центры'
    # direction = 'https://www.spr.ru/all/lechenie-za-rubezhom/'  # Лечение за рубежом'
    # direction = 'https://www.spr.ru/all/meditsinskie-laboratorii-analizi/'  # Медицинские лаборатории, анализы'
    # direction = 'https://www.spr.ru/all/ortopedicheskie-tsentri-lechenie-pozvonochnika-i/'  # Ортопедические центры, лечение позвоночника и суставов'
    # direction = 'https://www.spr.ru/all/oftalmologicheskie-kliniki/'  # Офтальмологические клиники'
    # direction = 'https://www.spr.ru/all/tsentri-plasticheskoy-hirurgii/'  # Центры пластической хирургии'
    # direction = 'https://www.spr.ru/all/tsentri-magnitno-rezonansnoy-tomografii/'  # МРТ'
    # direction = 'https://www.spr.ru/all/narkologicheskie-kliniki-lechenie-alkogolizma/'  # Наркологические клиники'
    # direction = 'https://www.spr.ru/all/vedomstvennie-bolnitsi-polikliniki-medsanchasti/'  # Ведомственные больницы, поликлиники, медсанчасти, военные госпитали'
    # direction = 'https://www.spr.ru/all/molochnie-kuhni-i-molochno-razdatochnie-punkti/'  # Молочные кухни и молочно-раздаточные пункты'
    # direction = 'https://www.spr.ru/all/morgi-patologo-anatomicheskie-otdeleniya/'  # Морги, патолого-анатомические отделения'
    # direction = 'https://www.spr.ru/all/patronazh-patronazhnie-uslugi/'  # Патронаж, патронажные услуги'
    # direction = 'https://www.spr.ru/all/perelivanie-krovi-sdacha-krovi/'  # Переливание крови, сдача крови'
    # direction = 'https://www.spr.ru/all/sanatorii-reabilitatsionnie-tsentri/'  # Санатории, реабилитационные центры'
    # direction = 'https://www.spr.ru/all/skoraya-meditsinskaya-pomosch/'  # Скорая медицинская помощь'
    # direction = 'https://www.spr.ru/all/bolnitsi-gorodskie/'  # Больницы'
    # direction = 'https://www.spr.ru/all/rodilnie-doma-perinatalnie-tsentri/'  # Роддома'
    # direction = 'https://www.spr.ru/all/internet-apteki-internet-magazini-meditsinskih/'  # Интернет-аптеки, интернет-магазины медицинских товаров'
    # direction = 'https://www.spr.ru/all/ortopedicheskie-izdeliya-protezi-badi-i-pischevie/'  # Ортопедические изделия, протезы, бады и пищевые добавки, медицинские товары'
    # direction = 'https://www.spr.ru/all/sluhovie-apparati-tsentri-sluhoprotezirovaniya/'  # Слуховые аппараты, центры слухопротезирования'
    # direction = 'https://www.spr.ru/all/apteki/'  # Аптеки'
    # direction = 'https://www.spr.ru/all/saloni-i-magazini-ochkov-optiki-kontaktnih-linz/'  # Оптики'
    # direction = 'https://www.spr.ru/all/polikliniki-stomatologicheskie/'  # Поликлиники стоматологические'
    # direction = 'https://www.spr.ru/all/stomatologicheskie-kliniki/'  # Стоматологии'

    def start_requests(self):
        f = open(self.filename, 'w')
        f.write("")
        request = scrapy.Request(url=self.direction, callback=self.parse)
        request.meta['file'] = f
        yield request

    def parse(self, response):
        f = response.meta['file']

        html = response.body.decode('windows-1251')
        matches = re.findall("(a href='//www.spr.ru/otzyvy/.*?(\.html)?'>Отзывы)", html)

        url = ""
        for m in matches:
            print(m)
            m = str(m)
            start = m.index("'//") + 3
            if ' title=' in m:
                end = m.index("' title='", start)
                url = "https://" + m[start:end]
            else:
                end = m.index("'>", start)
                url = "https://" + m[start:end]
            f.write(url + "\n")
