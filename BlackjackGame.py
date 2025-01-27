from deck import Deck
from player import Player
from dealer import Dealer
from constants import *


class BlackjackGame():
    def __init__(self, starting_balance= 1000):
        self.deck = Deck()
        self.player = Player(starting_balance)
        self.dealer = Dealer()
        self.game_state = STATE_MENU
        self.outcome = None # lose, win or draw

    def start_game(self, bet_amount):

        self.player.place_bet(bet_amount)
        self.player.reset_hand()
        self.dealer.reset_hand()


        #Each is being delt two cards
        self.player.hit(self.deck.deal_card())
        self.dealer.hit(self.deck.deal_card())
        self.player.hit(self.deck.deal_card())
        self.dealer.hit(self.deck.deal_card())

        self.game_state = STATE_PLAYING
        self.outcome = None


    def player_hit(self):
        self.player.hit(self.deck.deal_card())
        if self.player.hand.is_bust():
            self.game_state = STATE_GAME_OVER
            self.outcome = "LOSE"

    def player_stand(self):
        while self.dealer.should_hit():
            self.dealer.hit(self.deck.deal_card())


        self.determine_result()


    def determine_result(self):
        player_value = self.player.hand.calculate_score()
        dealer_value = self.dealer.hand.calculate_score()

        if self.dealer.hand.is_bust():
            self.outcome = "WIN"
            self.player.winning()

        elif self.player.hand.is_bust():
            self.outcome = "LOSE"
            self.player.lose()

        elif dealer_value < player_value:
            self.outcome = "WIN"
            self.player.winning()

        elif dealer_value > player_value:
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
        self.game_state = STATE_MENU
        self.outcome = None