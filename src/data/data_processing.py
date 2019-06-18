import re

from src.data.data_gathering import obtain_page
from src.mtg_info import archetypes, card_types

main_url = 'http://tcdecks.net/'
archetypes_url = 'http://tcdecks.net/archetype.php?archetype={}&format=Vintage%20Old%20School'


def normalize_cards(cards_to_normalize):
    print(cards_to_normalize)
    normalized_cards = {}
    for k, v in cards_to_normalize.items():
        normalized_cards[k] = v[0] / v[1]
    cards_to_normalize = normalized_cards
    return cards_to_normalize


def clean_dict(cards_to_clean):
    print(cards_to_clean)
    cleaned_cards = {}
    for k, v in cards_to_clean.items():
        cleaned_cards[k] = v[0]
    cards_to_clean = cleaned_cards
    return cards_to_clean


def process_deck(deck_page, cards):
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
    return cards


def obtain_decks():
    num_decks = 0
    cards = {}
    for ind, archetype in enumerate(archetypes):
        page = 0
        deck_urls = []
        while len(deck_urls) % 30 == 0:
            page += 1
            archetype_page = obtain_page(archetypes_url.format(archetype.replace(' ', '%20')) + '&page=' + str(page))
            if archetype_page:
                deck_urls = archetype_page.findAll('td', {'data-th': 'Deck Name'})
                for deck_url in deck_urls:
                    num_decks += 1
                    url = '{}{}'.format(main_url, deck_url.find('a')['href'])
                    deck = obtain_page(url)
                    if deck:
                        cards = process_deck(deck, cards)
                        print(url)
                        print('{}%'.format((num_decks/644)*100))
            else:
                deck_urls = ['bla']
    print('Total number of decks analyzed: {}'.format(num_decks))
    return cards
