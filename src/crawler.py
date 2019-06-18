from src.data.data_processing import obtain_decks
from src.plotters.plot_methods import plot_total_played, plot_average_when_played


def _main():

    cards = obtain_decks()
    plot_average_when_played(cards)
    plot_total_played(cards)


if __name__ == '__main__':
    _main()
