import re
import matplotlib.pyplot as plt
from urllib import request
from bs4 import BeautifulSoup
from mtg_info import archetypes, card_types

main_url = 'http://tcdecks.net/'
archetypes_url = 'http://tcdecks.net/archetype.php?archetype={}&format=Vintage%20Old%20School'
decks = []
cards = {}


def obtain_page(url):

    from http.cookiejar import CookieJar
    cj = CookieJar()
    cp = request.HTTPCookieProcessor(cj)
    opener = request.build_opener(cp)
    with opener.open(url, timeout=1000) as response:
        soup = BeautifulSoup(response.read())
    return soup


def process_deck(deck_page):
    found_deck = {}
    deck_table = deck_page.find('table', {'class': 'table_deck'})
    all_data = ''
    all_tables = deck_table.findAll('td')
    for table in all_tables:
        if (table.has_attr('scope') and table['scope'] != "side_movil") or not table.has_attr('scope'):
            all_data += table.get_text().strip().replace('\n', '').replace('\r', '')
    for card_type in card_types:
        all_data = all_data.replace(card_type + ' ', '')
    all_data = re.sub(r"\[[0-9]*\]", "", all_data)
    card_num = 0
    card_name = ''
    for ind, letter in enumerate(all_data):
        if ind == 0:
            card_num = letter
        else:
            try:
                new_card_num = int(letter)
                if card_name != '':
                    prev = cards.get(card_name, (0, 0))
                    cards[card_name] = (prev[0] + int(card_num)), (prev[1] + 1)
                    found_deck[card_name] = card_num
                card_num = new_card_num
                card_name = ''
            except ValueError:
                card_name += letter
    decks.append(found_deck)


def obtain_decks():
    num_decks = 0
    for ind, archetype in enumerate(archetypes):
        archetype_page = obtain_page(archetypes_url.format(archetype))
        deck_urls = archetype_page.findAll('td', {'data-th': 'Deck Name'})
        for deck_url in deck_urls:
            num_decks += 1
            url = '{}{}'.format(main_url, deck_url.find('a')['href'])
            deck = obtain_page(url)
            process_deck(deck)
            print('{}%'.format((num_decks/644)*100))

    print('Total number of decks analyzed: {}'.format(num_decks))


def normalize_cards(cards):
    print(cards)
    normalized_cards = {}
    for k, v in cards.items():
        normalized_cards[k] = v[0] / v[1]
    cards = normalized_cards
    return cards


def plot_cards(cards):
    sorted_cards = [(k, cards[k]) for k in sorted(cards, key=cards.get, reverse=True)]
    print(sorted_cards[0:100])
    names = [x[0] for x in sorted_cards][0:100]
    values = [x[1] for x in sorted_cards][0:100]
    plt.figure(figsize=(40, 20))
    plt.xticks(rotation='vertical')
    plt.bar(range(len(names)), values, tick_label=names)
    plt.savefig('result.png', dpi=200)
    plt.show()


def _main():

    obtain_decks()
    plot_cards(normalize_cards(cards))


if __name__ == '__main__':
    _main()
