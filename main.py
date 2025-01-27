import sys
from constants import *
from blackjack_setup import BlackjackGame

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

clock = pygame.time.Clock()


# BACKGROUND + CARDS + BACK
background_img = load_background()
card_images = load_card(scale_width=70, scale_height=100)
back_image = pygame.image.load("img/back.png").convert_alpha()
back_image = pygame.transform.scale(back_image, (70, 100))

# STARTING GAME
game = BlackjackGame(starting_balance=1000)

# FONTS
font_small = pygame.font.SysFont("arial", 20)
font_medium = pygame.font.SysFont("arial", 26)
font_large = pygame.font.SysFont("arial", 36)

# ALL NEEDED BUTTONS
plus_button_rect = pygame.Rect(500, 180, 60, 60)
minus_button_rect = pygame.Rect(240, 180, 60, 60)
deal_button_rect = pygame.Rect(350, 250, 100, 50)
hit_button_rect = pygame.Rect(250, 500, 120, 50)
stand_button_rect = pygame.Rect(430, 500, 120, 50)
play_again_rect = pygame.Rect(350, 530, 150, 50)

# START BET
current_bet = 100

###############################################################################
# DRAW / HELPER FUNCTIONS
###############################################################################

# FUNCTION FOR TEXTING
def draw_text(surface, text, x, y, font, color=WHITE, center=False):
    img = font.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)
    else:
        surface.blit(img, (x, y))

# DRAWING BUTTONS
def draw_button(surface, text, rect, font, bg_color, text_color=WHITE):
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, BLACK, rect, 2)
    text_img = font.render(text, True, text_color)
    text_rect = text_img.get_rect(center=rect.center)
    surface.blit(text_img, text_rect)

# DRAWING CARDS
def draw_cards(surface, hand, start_x, start_y, hide_first_card=False):
    offset = 25
    for i, card in enumerate(hand.cards):
        x = start_x + i * offset
        y = start_y
        if hide_first_card and i == 0:
            surface.blit(back_image, (x, y))
        else:
            img = card_images.get((card.rank, card.suit))
            if img:
                surface.blit(img, (x, y))
            else:
                surface.blit(back_image, (x, y))

# IN-GAME SITUATIONS

def handle_menu_events(event):
    global current_bet
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = event.pos

        if plus_button_rect.collidepoint(mouse_pos):
            current_bet += 10
            if current_bet > game.player.balance:
                current_bet = game.player.balance

        elif minus_button_rect.collidepoint(mouse_pos):
            current_bet -= 10
            if current_bet < 10:
                current_bet = 10

        elif deal_button_rect.collidepoint(mouse_pos):
            game.start_game(current_bet)

def handle_playing_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = event.pos
        if hit_button_rect.collidepoint(mouse_pos):
            game.player_hit()
        elif stand_button_rect.collidepoint(mouse_pos):
            game.player_stand()

def handle_game_over_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = event.pos
        if play_again_rect.collidepoint(mouse_pos):
            game.reset_game()

# DRAWING STATES

def draw_menu_state(surface):
    surface.blit(background_img, (0, 0))

    # Title
    draw_text(surface, "Blackjack", SCREEN_WIDTH // 2, 80, font_large, YELLOW, center=True)

    # Current Bet
    draw_text(surface, f"Current Bet: ${current_bet}", SCREEN_WIDTH // 2, 150, font_medium, WHITE, center=True)

    # +/- Buttons
    draw_button(surface, "+", plus_button_rect, font_large, GREEN, WHITE)
    draw_button(surface, "-", minus_button_rect, font_large, RED, WHITE)

    # Deal Button
    draw_button(surface, "Deal", deal_button_rect, font_medium, BLUE, WHITE)

    # Player balance
    draw_text(surface, f"Balance: ${game.player.balance}", 10, 10, font_small, YELLOW)



def draw_playing_state(surface):
    surface.blit(background_img, (0, 0))

    draw_text(surface, f"Balance: ${game.player.balance}", 10, 10, font_small, YELLOW)
    draw_text(surface, f"Current Bet: ${game.player.bet}", 10, 30, font_small, YELLOW)

    # Dealer
    draw_text(surface, "Dealer's Hand:", 50, 80, font_medium, WHITE)
    draw_cards(surface, game.dealer.hand, 50, 110, hide_first_card=True)

    # Player
    draw_text(surface, "Your Hand:", 50, 300, font_medium, WHITE)
    draw_cards(surface, game.player.hand, 50, 330)

    # Hit / Stand
    draw_button(surface, "Hit", hit_button_rect, font_medium, GREEN, WHITE)
    draw_button(surface, "Stand", stand_button_rect, font_medium, GREEN, WHITE)

def draw_game_over_state(surface):
    surface.blit(background_img, (0, 0))

    # Outcome
    if game.outcome == "BLACKJACK":
        outcome_text = "Blackjack! You Win!"
    elif game.outcome == "WIN":
        outcome_text = "You Win!"
    elif game.outcome == "LOSE":
        outcome_text = "You Lose!"
    elif game.outcome == "DRAW":
        outcome_text = "It's a Draw!"
    else:
        outcome_text = "Game Over"

    # Final state
    draw_text(surface, f"Balance: ${game.player.balance}", 10, 10, font_small, YELLOW)
    draw_text(surface, outcome_text, SCREEN_WIDTH // 2, 50, font_large, YELLOW, center=True)

    # Dealer
    draw_text(surface, "Dealer's Hand:", 50, 120, font_medium, WHITE)
    draw_cards(surface, game.dealer.hand, 50, 150, hide_first_card=False)
    dealer_score = game.dealer.hand.calculate_score()
    draw_text(surface, f"Dealer's Score: {dealer_score}", 50, 280, font_small, WHITE)

    # Player
    draw_text(surface, "Your Hand:", 50, 320, font_medium, WHITE)
    draw_cards(surface, game.player.hand, 50, 350, hide_first_card=False)
    player_score = game.player.hand.calculate_score()
    draw_text(surface, f"Your Score: {player_score}", 50, 480, font_small, WHITE)

    # Play Again
    draw_button(surface, "Play Again", play_again_rect, font_medium, BLUE, WHITE)

def main_loop():
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game.game_state == STATE_MENU:
                handle_menu_events(event)
            elif game.game_state == STATE_PLAYING:
                handle_playing_events(event)
            elif game.game_state == STATE_GAME_OVER:
                handle_game_over_events(event)

        # Draw
        if game.game_state == STATE_MENU:
            draw_menu_state(screen)
        elif game.game_state == STATE_PLAYING:
            draw_playing_state(screen)
        elif game.game_state == STATE_GAME_OVER:
            draw_game_over_state(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()
