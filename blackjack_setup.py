from constants import *
import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.calculate_value()

    def calculate_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_score(self):
        value = 0
        aces = 0
        for card in self.cards:
            value += card.value
            if card.rank == 'A':
                aces += 1
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value

    def is_bust(self):
        return self.calculate_score() > 21

    def is_blackjack(self):
        return len(self.cards) == 2 and self.calculate_score() == 21

    def reset(self):
        self.cards = []

class Player:
    def __init__(self, starting_balance=1000):
        self.hand = Hand()
        self.balance = starting_balance
        self.bet = 0

    def place_bet(self, amount):
        self.bet = amount
        self.balance -= amount

    def winning(self):
        prize = self.bet * 2
        self.balance += prize
        self.bet = 0

    def lose(self):
        self.bet = 0

    def draw(self):
        self.balance += self.bet
        self.bet = 0

    def hit(self, card):
        self.hand.add_card(card)

    def stand(self):
        pass

    def reset_hand(self):
        self.hand.reset()
        self.bet = 0

class Dealer:
    def __init__(self):
        self.hand = Hand()

    def hit(self, card):
        self.hand.add_card(card)

    def should_hit(self):
        return self.hand.calculate_score() < 17

    def reset_hand(self):
        self.hand.reset()

class BlackjackGame:
    def __init__(self, starting_balance=1000):
        self.deck = Deck()
        self.player = Player(starting_balance)
        self.dealer = Dealer()
        self.game_state = STATE_MENU

        self.outcome = None
        self.error_message = ""

    def player_wins_blackjack(self):
        # Blackjack usually pays 3:2
        prize = int(self.player.bet * 2.5)
        self.player.balance += prize
        self.player.bet = 0

    def start_game(self, bet_amount):
        if bet_amount <= 0:
            self.outcome = "INVALID_BET"
            self.error_message = "Bet must be greater than 0."
            return
        if bet_amount > self.player.balance:
            self.outcome = "INVALID_BET"
            self.error_message = "Not enough balance."
            return

        self.player.reset_hand()
        self.dealer.reset_hand()
        self.player.place_bet(bet_amount)

        self.player.hit(self.deck.deal_card())
        self.dealer.hit(self.deck.deal_card())
        self.player.hit(self.deck.deal_card())
        self.dealer.hit(self.deck.deal_card())

        p_bj = self.player.hand.is_blackjack()
        d_bj = self.dealer.hand.is_blackjack()

        if p_bj and d_bj:
            self.outcome = "DRAW"
            self.player.draw()
            self.game_state = STATE_GAME_OVER
        elif p_bj:
            self.outcome = "BLACKJACK"
            self.player_wins_blackjack()
            self.game_state = STATE_GAME_OVER
        elif d_bj:
            self.outcome = "LOSE"
            self.player.lose()
            self.game_state = STATE_GAME_OVER
        else:
            self.outcome = None
            self.error_message = ""
            self.game_state = STATE_PLAYING

    def player_hit(self):
        self.player.hit(self.deck.deal_card())
        if self.player.hand.is_bust():
            self.outcome = "LOSE"
            self.game_state = STATE_GAME_OVER

    def player_stand(self):
        # Dealer hits until at least 17
        while self.dealer.should_hit():
            self.dealer.hit(self.deck.deal_card())
        self.determine_result()

    def determine_result(self):
        p_val = self.player.hand.calculate_score()
        d_val = self.dealer.hand.calculate_score()

        if self.dealer.hand.is_bust():
            self.outcome = "WIN"
            self.player.winning()
        elif self.player.hand.is_bust():
            self.outcome = "LOSE"
            self.player.lose()
        elif d_val < p_val:
            self.outcome = "WIN"
            self.player.winning()
        elif d_val > p_val:
            self.outcome = "LOSE"
            self.player.lose()
        else:
            self.outcome = "DRAW"
            self.player.draw()

        self.game_state = STATE_GAME_OVER

    def reset_game(self):
        self.deck = Deck()
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.outcome = None
        self.error_message = ""
        self.game_state = STATE_MENU
