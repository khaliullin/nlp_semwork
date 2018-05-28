import re

import scrapy


class InstitutionSpider(scrapy.Spider):
    """
    Возвращает файл cо сгенерированными ссылками на получение отзывов для направлений из institutions.txt
    Запуск: scrapy crawl institution
    """
    name = "institution"
    filename = "urls.txt"

    # Set для уникальных ссылок на направления
    institutions = set()

    def start_requests(self):
        # Заполняем set с направлениями
        with open('institutions.txt', 'r') as inst:
            for line in inst:
                self.institutions.add(line.strip())

        print(self.institutions)

        # подготовка файла для ссылок
        f = open(self.filename, 'w')
        f.write("")
        for institution in self.institutions:
            # отправка запроса, вызов функции get_reviews_urls
            request = scrapy.Request(url=institution, callback=self.parse)
            request.meta['file'] = f
            yield request

    def parse(self, response):
        """
                Получение отзывов происходит по поиску JS функции next11(),
                в параметры которой передаются тип отзывов (+/-), id учреждения, общее количество отзывов
                """
        html = response.body.decode('windows-1251')
        urls = []

        file = response.meta['file']

        # поиск JavaScript функции для получения отзывов (применяется в пагинации)
        # ищем в положительных отзывах
        m = re.search("next11\(\d+.+,11\);'", html)

        inst_id_net = 0  # если id указан в неявном виде
        if m:
            params = m.group()[7:-3].split(",")
            total = params[0]
            inst_id = params[2]
            inst_id_net = inst_id
            urls.extend(self.generate_url(1, inst_id, total, "11"))
        else:
            m = re.search("next11\(\d+.+,11\)'", html)
            if m:
                params = m.group()[7:-2].split(",")
                total = params[0]
                inst_id = params[2]
                inst_id_net = inst_id
                urls.extend(self.generate_url(2, inst_id, total, "11"))
            else:
                m = re.search("id_firm_forum=\d+'", html)
                if m:
                    inst_id = m.group()[14:-1]
                    inst_id_net = inst_id
                    urls.extend(self.generate_url(1, inst_id, 20, "11"))
                else:
                    # если id учреждения нигде не указан, возможно, он есть в названии изображения учреждения
                    m = re.search("/\d+.png'", html)
                    if m:
                        inst_id = m.group()[1:-5]
                        inst_id_net = inst_id
                        urls.extend(self.generate_url(2, inst_id, 20, "11"))
                    else:
                        urls.extend(self.generate_url(2, inst_id_net, 20, "11"))

        # ищем в отрицательных отзывах
        m = re.search("next11\(\d+.+,1\);'", html)
        if m:
            params = m.group()[7:-3].split(",")
            total = params[0]
            inst_id = params[2]
            urls.extend(self.generate_url(1, inst_id, total, "1"))
        else:
            m = re.search("next11\(\d+.+,1\)'", html)
            if m:
                params = m.group()[7:-2].split(",")
                total = params[0]
                inst_id = params[2]
                urls.extend(self.generate_url(2, inst_id, total, "1"))
            else:
                m = re.search("id_firm_forum=\d+'", html)
                if m:
                    inst_id = m.group()[14:-1]
                    urls.extend(self.generate_url(1, inst_id, 20, "1"))
                else:
                    m = re.search("/\d+.png'", html)
                    if m:
                        inst_id = m.group()[1:-5]
                        urls.extend(self.generate_url(2, inst_id, 20, "1"))
                    else:
                        urls.extend(self.generate_url(2, inst_id_net, 20, "1"))

        # пишем ссылки на отзывы в файл
        for url in urls:
            file.write(url + '\n')

    @staticmethod
    def generate_url(url_type, ins_id, total, pos_neg):
        """
        Генерирует ссылки на получение отзывов
        :param url_type: тип ссылки (на сайте 2 разных вида ссылок)
        :param ins_id: id направления
        :param total: количество отзывов всего
        :param pos_neg: 11 - положительные отзывы, 1 - отрицательные
        :return: список со ссылками на получение отзывов
        """
        urls = []
        if url_type == 1:
            i = 0
            while i < int(total):
                urls.append("https://www.spr.ru/js/zzz_next.php?id_top=%s&id_firm=%s&view11=%s&all11=%s"
                            % (pos_neg, ins_id, i, total))
                i += 20  # шаг 20, так реализована пагинация на сайте spr.ru
        elif url_type == 2:
            i = 0
            while i < int(total):
                urls.append("https://www.spr.ru/js/zzz_next.php?id_top=%s&id_net=%s&view11=%s&all11=%s&setevie=1"
                            % (pos_neg, ins_id, i, total))
                i += 20
        return urls

