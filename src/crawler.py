import string
import urllib.request
from bs4 import BeautifulSoup

main_url = 'http://tcdecks.net/'


def obtain_page(url):
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response)
    return soup


def obtain_archetypes(my_soup):
    fieldset_tags = my_soup.findAll('fieldset')
    archetypes = []
    printable = set(string.printable)
    for field_set in fieldset_tags:
        if field_set.find('legend').get_text() == 'Archetypes':
            archetypes_tags = field_set.findAll('a', {'class': 'btn btn-1'})
            for enum, archetype_tag in enumerate(archetypes_tags):
                arch_name_all = ''.join(filter(lambda x: x in printable,
                                        archetype_tag.get_text().strip()))
                arch_name = clean_name(arch_name_all)
                archetypes.append((arch_name,
                                   '{}{}'.format(main_url, archetype_tag['href'])))
    return archetypes


def clean_name(full_name):
    arch_name = ''
    for ind, letter in enumerate(full_name):
        try:
            if ind == 0:
                arch_name += letter
            else:
                _ = int(letter)
        except:
            arch_name += letter
    return arch_name


def obtain_decks(archetypes_list):
    for archetype in archetypes_list:
        print(archetype[1])
        archetype_page = obtain_page(archetype[1])
        print(archetype_page)
        break


main_page = obtain_page('{}{}'.format(main_url, 'format.php?format=Vintage%20Old%20School'))
archetypes = obtain_archetypes(main_page)
print(archetypes)
obtain_decks(archetypes)

