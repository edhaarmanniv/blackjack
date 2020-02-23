from blackjack import *
from cards import *
from game_funcs import *

cards = []
for _, suit in suits["solid"].items():
    for face, face_value in faces.items():
        cards.append(Card(face, face_value, suit))

deck = Deck(cards)
deck.shuffle()

players = create_gamblers()
dealer = Dealer()
table = Table(players, dealer)

nother_hand = True
while nother_hand and deck.num_cards > (2 * len(players) + 1):
    game(deck, table, players, dealer)
    nother_hand = bool(input("'nother hand?"))
    reset_hands(players, dealer)
else:
    print(
        """No more cards! Thank you for playing.
        Stay Tuned for multi-deck play!"""
    )
