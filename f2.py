import re

f = '/Users/sagithaliullin/student/gitHub/nlp_semwork/spr_crawler/ip.txt'

with open (f, 'r') as file:
    content = file.read()

    m = re.findall('\d+\.\d+\.\d+\.\d+\t\d+', content)
    for n in m:
        print('http://' + n)