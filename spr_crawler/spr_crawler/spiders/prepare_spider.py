import re

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "institution"
    filename = "urls.txt"

    institutions = set()

    def start_requests(self):
        with open('institutions.txt', 'r') as inst:
            i = 0
            for line in inst:
                i += 1
                self.institutions.add(line.strip())

        print(self.institutions)

        f = open(self.filename, 'w')
        f.write("")
        for institution in self.institutions:
            request = scrapy.Request(url=institution, callback=self.get_reviews_urls)
            request.meta['file'] = f
            yield request

    @staticmethod
    def generate_url(url_type, ins_id, total, pos_neg):
        urls = []
        if url_type == 1:
            i = 0
            while i < int(total):
                urls.append("https://www.spr.ru/js/zzz_next.php?id_top=%s&id_firm=%s&view11=%s&all11=%s"
                            % (pos_neg, ins_id, i, total))
                i += 20
        elif url_type == 2:
            i = 0
            while i < int(total):
                urls.append("https://www.spr.ru/js/zzz_next.php?id_top=%s&id_net=%s&view11=%s&all11=%s&setevie=1"
                            % (pos_neg, ins_id, i, total))
                i += 20
        return urls

    def get_reviews_urls(self, response):
        html = response.body.decode('windows-1251')
        urls = []

        file = response.meta['file']

        # searching urls in page html
        m = re.search("next11\(\d+.+,11\);'", html)
        inst_id_net = 0
        if m:
            params = m.group()[7:-3].split(",")
            # print("==== 1  1 ====")
            # print(params)
            total = params[0]
            inst_id = params[2]
            inst_id_net = inst_id
            # print("total %s" % total)
            # print("ins_id %s\n" % inst_id)
            urls.extend(self.generate_url(1, inst_id, total, "11"))
        else:
            m = re.search("next11\(\d+.+,11\)'", html)
            if m:
                params = m.group()[7:-2].split(",")
                # print("==== 1  2 ====")
                # print(params)
                total = params[0]
                inst_id = params[2]
                inst_id_net = inst_id
                # print("total %s" % total)
                # print("ins_id %s\n" % inst_id)
                urls.extend(self.generate_url(2, inst_id, total, "11"))
            else:
                m = re.search("id_firm_forum=\d+'", html)
                if m:
                    inst_id = m.group()[14:-1]
                    inst_id_net = inst_id
                    # print("==== 1  3 ====")
                    # print("ins_id %s\n" % inst_id)
                    urls.extend(self.generate_url(1, inst_id, 20, "11"))
                else:
                    m = re.search("/\d+.png'", html)
                    # print("==== 1  4 ====")
                    # print("ins_id %s\n" % inst_id)
                    if m:
                        inst_id = m.group()[1:-5]
                        inst_id_net = inst_id
                        urls.extend(self.generate_url(2, inst_id, 20, "11"))
                    else:
                        urls.extend(self.generate_url(2, inst_id_net, 20, "11"))

        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        m = re.search("next11\(\d+.+,1\);'", html)
        if m:
            # 11 with certain id
            params = m.group()[7:-3].split(",")
            # print("==== 2  1 ====")
            # print(params)
            total = params[0]
            inst_id = params[2]
            inst_id_net = inst_id
            # print("total %s" % total)
            # print("ins_id %s\n" % inst_id)
            urls.extend(self.generate_url(1, inst_id, total, "1"))
        else:
            m = re.search("next11\(\d+.+,1\)'", html)
            if m:
                params = m.group()[7:-2].split(",")
                # print("==== 2  2 ====")
                # print(params)
                total = params[0]
                inst_id = params[2]
                inst_id_net = inst_id
                # print("total %s" % total)
                # print("ins_id %s\n" % inst_id)
                urls.extend(self.generate_url(2, inst_id, total, "1"))
            else:
                m = re.search("id_firm_forum=\d+'", html)
                if m:
                    inst_id = m.group()[14:-1]
                    inst_id_net = inst_id
                    # print("==== 2  3 ====")
                    # print("ins_id %s\n" % inst_id)
                    urls.extend(self.generate_url(1, inst_id, 20, "1"))
                else:
                    m = re.search("/\d+.png'", html)
                    # print("==== 2  4 ====")
                    # print("ins_id %s\n" % inst_id)
                    if m:
                        inst_id = m.group()[1:-5]
                        inst_id_net = inst_id
                        urls.extend(self.generate_url(2, inst_id, 20, "1"))
                    else:
                        urls.extend(self.generate_url(2, inst_id_net, 20, "1"))

        for url in urls:
            file.write(url + '\n')

    def get_reviews_links(self, response):
        page = response.url.split("/")[-1]
        filename = 'reviews/review-%s.html' % page
        html = response.body.decode('windows-1251')
        with open(filename, 'w') as f:
            f.write(html)
        f.close()

        urls = re.findall('www.spr.ru/forum_vyvod.php\?id_tema=\d+\\\\', html)
        # print(urls)

    def parse(self, response):
        pass
