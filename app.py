from flask import Flask, render_template, request
import random
import numpy as np

app = Flask(__name__)

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    return [(value, suit) for suit in suits for value in values]

def card_value(card):
    value, _ = card
    if value in ['Jack', 'Queen', 'King']:
        return 10
    elif value == 'Ace':
        return 11
    else:
        return int(value)


def calculate_hand(hand):
    total = sum(card_value(card) for card in hand)
    aces = sum(card[0] == 'Ace' for card in hand)

    while total > 21 and aces:
        total -= 10
        aces -= 1

    return total

def simulate_hand(deck, player_hand, dealer_card, action):
    if action == 'hit':
        player_hand.append(deck.pop())

    player_total = calculate_hand(player_hand)
    if player_total > 21:
        return 'lose'

    dealer_hand = [dealer_card, deck.pop()]
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

    dealer_total = calculate_hand(dealer_hand)
    if dealer_total > 21 or player_total > dealer_total:
        return 'win'
    elif player_total < dealer_total:
        return 'lose'
    else:
        return 'draw'

def simulate_blackjack(player_hand, dealer_card, action, simulations=1000):
    wins = 0
    losses = 0
    draws = 0

    for _ in range(simulations):
        deck = create_deck()
        random.shuffle(deck)

        initial_cards = player_hand + [dealer_card]
        deck = [card for card in deck if card not in initial_cards]

        result = simulate_hand(deck, list(player_hand), dealer_card, action)
        if result == 'win':
            wins += 1
        elif result == 'lose':
            losses += 1
        else:
            draws += 1

    win_percentage = (wins / simulations) * 100
    loss_percentage = (losses / simulations) * 100
    draw_percentage = (draws / simulations) * 100

    return win_percentage, loss_percentage, draw_percentage

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_hand = [
            (request.form['player_card1_value'], request.form['player_card1_suit']),
            (request.form['player_card2_value'], request.form['player_card2_suit'])
        ]
        dealer_card = (request.form['dealer_card_value'], request.form['dealer_card_suit'])
        action = request.form['action']
        simulations = int(request.form['simulations'])

        win_percentage, loss_percentage, draw_percentage = simulate_blackjack(
            player_hand, dealer_card, action, simulations)
        
        return render_template('results.html', 
                               win_percentage=win_percentage, 
                               loss_percentage=loss_percentage, 
                               draw_percentage=draw_percentage, 
                               action=action)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
