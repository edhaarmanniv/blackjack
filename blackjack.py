from random import shuffle as rshuffle
from terminaltables import SingleTable


class Card:
    def __init__(self, face, value, suit):
        self.face = face
        self.value = value
        self.suit = suit
        self.card = face + suit
        self.front = f"[{self.card}]"
        self.back = "[**]"
        self.facedown = False
        return

    def __str__(self):
        return self.show()

    def flip(self):
        self.facedown = not self.facedown
        return

    def show(self):
        display = None
        if self.facedown:
            display = self.back
        else:
            display = self.front
        return display

    def flip_show(self):
        self.flip()
        return self.show()


class Deck:
    def __init__(self, cards, num_cards=52):
        self.cards = cards
        self.num_cards = len(cards)
        return

    def shuffle(self):
        rshuffle(self.cards)
        return

    def draw(self):
        top_card = None
        if len(self.cards) > 0:
            top_card = self.cards.pop()
        else:
            print("NO MORE CARDS")
            top_card = 0
        return top_card

    def cards_left(self):
        print([card.card for card in self.cards])


class Player:
    def __init__(self, name="Player"):
        self.hand = []
        self.name = name
        self.blackjack = False
        self.bust = False
        self.keep_playing = True
        self.num_wins = 0
        return

    def __str__(self):
        return f"{self.name} || {self.score()} || {self.show_hand()}"

    def add_card(self, card):
        self.hand.append(card)
        if self.score() == 21:
            self.blackjack = True
            self.keep_playing = False
        return

    def hit(self, card):
        self.add_card(card)
        if self.score() > 21:
            self.bust = True
        if self.score() == 21:
            self.blackjack = True
        return

    def stay(self):
        self.keep_playing = False
        return

    def score(self):
        score = 0
        hand = self.hand.copy()
        for card in hand:
            if card.face == "A":
                hand.append(hand.pop(hand.index(card)))

        for card in hand:
            if card.face == "A":
                values = [score + value for value in card.value]
                score += max(card.value) if max(values) <= 21 else min(card.value)
            else:
                score += card.value
        return score

    def play(self, deck):
        if not self.blackjack:
            while self.keep_playing and not self.bust and not self.blackjack:
                choice = input(f"Player {self.name}:\n(H)it or (S)tay: ")
                if choice in {"H", "h", "Hit", "hit"}:
                    self.hit(deck.draw())
                    print(self)
                elif choice in {"S", "s", "Stay", "stay"}:
                    self.stay()
                # elif split:
                # elif double:
                else:
                    print("Invalid Selection! Select Again")

                if self.blackjack:
                    print("21!")
                    self.keep_playing = False

                if self.bust:
                    print("Busted!")
                    self.keep_playing = False
        return

    def show_hand(self):
        hand_str = ""
        for card in self.hand:
            if card.facedown == True:
                hand_str += card.back
            else:
                hand_str += card.front
        return hand_str

    def reset_hand(self):
        self.hand = []
        self.blackjack = False
        self.bust = False
        self.keep_playing = True

    def show_blackjack(self):
        bj = ""
        if self.blackjack:
            bj = "\u2605"
        return bj


class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")
        return

    def show_hidden(self):
        for card in self.hand:
            if card.facedown == True:
                card.flip()

    def play(self, deck):
        print("Dealer's Turn:")
        if self.score() > 21:
            bust = True
        elif self.score() < 16:
            while self.score() < 17:
                self.hit(deck.draw())
        else:
            self.stay()
        self.show_hidden()
        return


class Table:
    def __init__(self, players, dealer):
        self.table = self.create_table(players, dealer)
        return

    def __str__(self):
        return self.show_table()

    def create_table(self, players, dealer):
        column_headers = ["Player", "Score", "Hand", "Blackjack", "Wins"]
        table_data = [column_headers]
        players_done_playing = {player.keep_playing for player in players}
        if len(players_done_playing) == 1 and False in players_done_playing:
            table_data.append(
                [
                    dealer.name,
                    dealer.score(),
                    dealer.show_hand(),
                    dealer.show_blackjack(),
                    dealer.num_wins,
                ]
            )
        else:
            table_data.append(
                [
                    dealer.name,
                    "??",
                    dealer.show_hand(),
                    dealer.show_blackjack(),
                    dealer.num_wins,
                ]
            )
        table_data.extend(
            [
                [
                    player.name,
                    player.score(),
                    player.show_hand(),
                    player.show_blackjack(),
                    player.num_wins,
                ]
                for player in players
            ]
        )

        single_table = SingleTable(table_data, title="Blackjack")
        for column in range(len(column_headers)):
            single_table.justify_columns[column] = "center"
        return single_table.table

    def show_table(self):
        return self.table
