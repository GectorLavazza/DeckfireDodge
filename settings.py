from itertools import product

SW, SH = 1280, 720
CENTER = SW // 2, SH // 2

COLORS = {
    'Diamonds': 'red',
    'Hearts': 'red',
    'Spears': 'black',
    'Clubs': 'black'
}

SUITS = ('Diamonds', 'Hearts', 'Spears', 'Clubs')
CARDS = ('6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
VARIANTS = list(product(SUITS, CARDS))

PLAYER_ABILITIES = ('dash', 'sprint', 'shield',
                    'heal', '- bullets speed', '- bullets frequency',
                    'small bullets', 'small player')

BULLET_ABILITIES = ('random speed', 'targets player',
                    '+ bullets speed', '2x damage', '+ bullets frequency',
                    'big bullets', 'shield breaking')

CARD_W, CARD_H = 200, 280
CARDS_AMOUNT = 4

EDGE_OFFSET = 200
OFFSET = (SW - EDGE_OFFSET * 2 - CARD_W * CARDS_AMOUNT) // (CARDS_AMOUNT - 1)
