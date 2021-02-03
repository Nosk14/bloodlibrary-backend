from lxml import html
import requests

SETS_URL = 'http://vtes.pl/cards'
CARDS_URL = 'http://vtes.pl/cards/set/{0}'


def get_sets():
    page = requests.get(SETS_URL)
    tree = html.fromstring(page.content)
    node_sets = tree.xpath('//table[@class="listtable"]/child::*')

    ret = []
    for node in node_sets[1:]:
        a_node = node.getchildren()[0].getchildren()[0]
        name = a_node.text
        id = a_node.attrib['href'].rsplit('/')[-1]
        ret.append((name, id))
    return ret


def get_cards(set_id):
    page = requests.get(CARDS_URL.format(set_id))
    tree = html.fromstring(page.content)
    node_cards = tree.xpath('//table[@class="listtable"]/child::*')

    ret = []
    for node in node_cards[1:]:
        name = node.getchildren()[1].getchildren()[0].text
        img = node.getchildren()[0].getchildren()[0].attrib['src'].replace('/_mini', '')
        ret.append((name, img))
    return ret


if __name__ == '__main__':
    sets_info = get_sets()
    with open("data/cards_pl.csv", 'w') as outfile:
        for zet in sets_info:
            print(zet[0])
            cards_info = get_cards(zet[1])
            for card in cards_info:
                outfile.write("{0};{1};{2};{3}\n".format(zet[0], zet[1], card[0], card[1]))
