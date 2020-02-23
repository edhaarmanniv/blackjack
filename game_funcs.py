from blackjack import *


def game(deck, table, players, dealer):
    for round in range(2):
        for i, player in enumerate(players):
            player.add_card(deck.draw())
            if i == 0:
                if round == 1:
                    dealer.add_card(deck.draw())
                    dealer.hand[0].flip()
                else:
                    dealer.add_card(deck.draw())
    print(table.create_table(players, dealer))

    for player in players:
        while player.keep_playing:
            player.play(deck)
            print(table.create_table(players, dealer))

    dealer.play(deck)
    print(table.create_table(players, dealer))
    display_winners(players, dealer)
    return


def player_names():
    names = []
    more_players = True
    print("Add players by name. Type '0' to Stop Entering")
    while more_players:
        name = input("Player Name: ")
        if name == str(0):
            more_players = False
        else:
            names.append(name)
    return names


def create_gamblers():
    names = player_names()
    gamblers = [Player(name) for name in names]
    return gamblers


def calc_winners(players, dealer):
    winners = []
    scores = [
        {"score": player.score(), "bust": player.bust, "blackjack": player.blackjack}
        for player in players
    ]

    if (
        (dealer.blackjack)
        or (
            all(
                dealer.score() >= score["score"]
                for score in scores
                if not score["bust"]
            )
            and not dealer.bust
        )
        or all(score["bust"] for score in scores)
    ):
        winners.append(dealer)
    elif any(score["blackjack"] for score in scores):
        winners = [player for player in players if player.blackjack]
    else:
        winners = [
            player
            for player in players
            if (not player.bust and player.score() > dealer.score())
        ]

    for winner in winners:
        winner.num_wins += 1

    return winners


def display_winners(players, dealer):
    winners = calc_winners(players, dealer)
    winner_names = [winner.name for winner in winners]
    win = "Winners:" if len(winner_names) > 1 else "Winner:"
    if len(winner_names) == 1 and winner_names[0] == "Dealer":
        print("Dealer Wins! :(")
    else:
        print(win)
        print(*winner_names, sep=", ")


def reset_hands(players, dealer):
    dealer.reset_hand()
    for player in players:
        player.reset_hand()
    return
