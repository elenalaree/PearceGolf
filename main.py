"""
PearceGolf
"""
import random
import arcade
from network import Network
import pickle
from player import Player


# Screen title and size
SCREEN_WIDTH = 1224
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Drag and Drop Cards"

# Constants for sizing
CARD_SCALE = 0.8

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.00
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# Card Back
# Face down image
FACE_DOWN_IMAGE = "images/card-back4.png"

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
DRAW_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT + 300

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT + 50
START_V = START_X + 750

DRAW_X =  MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT + 500

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT - 200

# The Y of the middle row (7 piles)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT 

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT 

# Card constants
SUITS = ["diamonds", "clubs", "hearts", "spades"]
VALUES = range(1, 14)
    # 11 = Jack, 12=Queen, 13=King, 14=Ace

# Constants that represent "what pile is what" for the game
PILE_COUNT = 15
DECK_PILE = 0
DISCARD_PILE = 1
DRAW_PILE = 2
PLAYER_1_PILE_1 = 3
PLAYER_1_PILE_2 = 4
PLAYER_1_PILE_3 = 5
PLAYER_1_PILE_4 = 6
PLAYER_1_PILE_5 = 7
PLAYER_1_PILE_6 = 8
PLAYER_2_PILE_1 = 9
PLAYER_2_PILE_2 = 10
PLAYER_2_PILE_3 = 11
PLAYER_2_PILE_4 = 12
PLAYER_2_PILE_5 = 13
PLAYER_2_PILE_6 = 14
 

PLAYER_1 = Player("Player 1", [])
PLAYER_2 = Player("Player 2", [])

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f"images/card-{self.suit}-{self.value}.png"
        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up




class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = None

        arcade.set_background_color(arcade.color.AMAZON)

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None
        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None
        self.piles = None


    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

    # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()
            # Create every card
        for card_suit in SUITS:
            for card_value in VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = DRAW_X, DRAW_Y
                self.card_list.append(card)
        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)     
        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for center cards
        # Deck
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_CYAN)
        pile.position = DRAW_X, DRAW_Y
        self.pile_mat_list.append(pile)
        # discard
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = DRAW_X + X_SPACING, DRAW_Y
        self.pile_mat_list.append(pile)
        #Drawn card Pile
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = (DRAW_X + X_SPACING) - 55, DRAW_Y + 175
        self.pile_mat_list.append(pile)
        
        # Create the six left piles
        # P1


        for i in range(3):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)
        for i in range(3):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Create the six right piles
        # P1
        for i in range(3):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_V + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        for i in range(3):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_V + i * X_SPACING, MIDDLE_Y 
            self.pile_mat_list.append(pile)


    # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]
        for card in self.card_list:
            self.piles[DECK_PILE].append(card)
        
        # Place one in the discard pile
        card = self.piles[DECK_PILE].pop()
        self.piles[DISCARD_PILE].append(card)
        card.face_up()
        card.position = self.pile_mat_list[DISCARD_PILE].position

        # loop through the piles and place one card each
        for i in range(PLAYER_1_PILE_1, PLAYER_2_PILE_6 + 1):
            card = self.piles[DECK_PILE].pop()
            # Put in the proper pile
            self.piles[i].append(card)

            # Move card to same position as pile we just put it in
            card.position = self.pile_mat_list[i].position
        self.check_hand()

    def check_hand(self):

        PLAYER_1.cards = [self.piles[PLAYER_1_PILE_1]]
        PLAYER_2.cards = []
        
    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_mouse_press(self, x, y, button, key_modifiers):
        
        """ Called when the user presses a mouse button. """
        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)
        
        # Have we clicked on a card?
        if len(cards) > 0:
            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            assert isinstance(primary_card, Card)

            # Figure out what pile the card is in
            pile_index = self.get_pile_for_card(primary_card)
            # Are we clicking on the draw deck?
            if pile_index == DECK_PILE:
                # Flip a card
                for i in range(1):
                    # If we ran out of cards, stop
                    if len(self.piles[DECK_PILE]) == 0:
                        break
                            # Get top card
                    card = self.piles[DECK_PILE][-1]
                        # Flip face up
                    card.face_up()
                        # Move card position to bottom-right face up pile
                    card.position = self.pile_mat_list[DRAW_PILE].position
                        # Remove card from face down pile
                    self.piles[DECK_PILE].remove(card)
                        # Move card to face up list
                    self.piles[DISCARD_PILE].append(card)
                        # Put on top draw-order wise
                    self.pull_to_top(card)
            elif primary_card.is_face_down:
                # Is the card face down? In one of those middle 7 piles? Then flip up
                primary_card.face_up()
            else:
            # All other cases, grab the face-up card we are clicking on
                self.held_cards = [primary_card]
                # Save the position
                self.held_cards_original_position = [self.held_cards[0].position]
                # Put on top in drawing order
                self.pull_to_top(self.held_cards[0])

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """
        # no cards, no care.
        if len(self.held_cards) == 0:
            return
        
        old_card = None     

        # Find the closest pile, in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True
        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):

            # What pile is it?
            pile_index = self.pile_mat_list.index(pile)

            if(pile_index == 0 or pile_index == 2):
                reset_position = True
            else:
                if pile_index in range(3, 15): 
                    old_card = self.piles[pile_index][0]
                # Place card on pile
                self.held_cards[0].position = pile.center_x, pile.center_y
                for card in self.held_cards:
                    self.move_card_to_new_pile(card, pile_index)

                # Success, don't reset position of cards
                reset_position = False

            # Release on top play pile? And only one card held?
        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            self.held_cards[0].position = self.held_cards_original_position[pile_index]
    # Access the value of the old card here
        if old_card:
            self.move_card_to_new_pile(old_card, DISCARD_PILE)

            self.piles[DISCARD_PILE][-1].position = DRAW_X + X_SPACING, DRAW_Y
            self.piles[DISCARD_PILE][-1].face_up()
            self.pull_to_top(self.piles[DISCARD_PILE][-1])
            print(f"discard array: {self.piles[DISCARD_PILE][0].value}")
        # We are no longer holding cards
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy
    
    def get_pile_for_card(self, card):
        """ What pile is this card in? """
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index
    
    def remove_card_from_pile(self, card):
        """ Remove card from whatever pile it was in. """
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break
    def move_card_to_new_pile(self, card, pile_index):
        """ Move the card to a new pile """
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)



def main():
    """ Main function """
    run = True
    n = Network()
    p = n.getP()
    while run:
        p2 = n.send(p)
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()