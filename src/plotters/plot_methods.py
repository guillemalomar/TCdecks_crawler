import matplotlib.pyplot as plt

from src.data.data_processing import normalize_cards, clean_dict


def plot_average_when_played(cards_for_average):
    cards_for_average = normalize_cards(cards_for_average)
    sorted_cards = \
        [(k, cards_for_average[k]) for k in sorted(cards_for_average, key=cards_for_average.get, reverse=True)]
    print(sorted_cards[0:100])
    names = [x[0] for x in sorted_cards][0:100]
    values = [x[1] for x in sorted_cards][0:100]
    plt.figure(figsize=(40, 20))
    plt.xticks(rotation='vertical')
    plt.bar(range(len(names)), values, tick_label=names)
    plt.title('Average per deck when played')
    plt.savefig('../plots/result_average.png', dpi=200)
    plt.show()


def plot_total_played(cards_for_total):
    cards_for_total = clean_dict(cards_for_total)
    sorted_cards = \
        [(k, cards_for_total[k]) for k in sorted(cards_for_total, key=cards_for_total.get, reverse=True)]
    print(sorted_cards[0:100])
    names = [x[0] for x in sorted_cards][0:100]
    values = [x[1] for x in sorted_cards][0:100]
    plt.figure(figsize=(40, 20))
    plt.xticks(rotation='vertical')
    plt.bar(range(len(names)), values, tick_label=names)
    plt.title('Total played in all decks')
    plt.savefig('../plots/result_total.png', dpi=200)
    plt.show()
