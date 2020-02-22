from blackjack import *
from cards import *
from game_funcs import *

cards = []
for _, suit in suits["solid"].items():
    for face, face_value in faces.items():
        cards.append(Card(face, face_value, suit))

deck = Deck(cards)
deck.shuffle()

players = create_gamblers(deck)
dealer = Dealer(deck)
table = Table(players, dealer)
# ed = Player(deck, "Ed")
# table = Table([ed], dealer)
game(deck, table, players, dealer)
# print("starting game")
# game(deck, table, [ed], dealer)