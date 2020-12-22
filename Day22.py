import collections
import os
import sys


class DisablePrints() :
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout



def play_combat(player1_cards, player2_cards) :
    player1_cards = player1_cards[:]
    player2_cards = player2_cards[:]

    turn = 0
    while player1_cards and player2_cards :
        turn += 1
        print('-- Round {} --'.format(turn) )
        print('Player 1: {}'.format(player1_cards))
        print('Player 2: {}'.format(player2_cards))
        drawn_cards = [ player1_cards.pop(0), player2_cards.pop(0) ]
        print('Player 1 plays: {}'.format(drawn_cards[0]))
        print('Player 2 plays: {}'.format(drawn_cards[1]))
        print('Player {} wins the round'.format(1 if drawn_cards[0] > drawn_cards[1] else 2))
        print()
        if drawn_cards[0] > drawn_cards[1] :
            player1_cards.extend(drawn_cards)
        else :
            player2_cards.extend(drawn_cards[::-1])

    winner = 1 if player1_cards else 2
    winning_deck = player1_cards if winner == 1 else player2_cards
    score = sum([(n+1) * v for n, v in enumerate(winning_deck[::-1])])

    return winner, score


def play_recursive_combat(player1_cards, player2_cards) :
    global next_game
    game = next_game
    next_game += 1

    print('=== Game {} ==='.format(game))

    player1_cards = player1_cards[:]
    player2_cards = player2_cards[:]
    previous_hands = []

    turn = 0
    while player1_cards and player2_cards :
        if (tuple(player1_cards), tuple(player2_cards)) in previous_hands :
            break
        previous_hands.append((tuple(player1_cards), tuple(player2_cards)))
        turn += 1
        print('-- Round {} (Game {}) --'.format(turn, game) )
        print('Player 1: {}'.format(player1_cards))
        print('Player 2: {}'.format(player2_cards))
        drawn_cards = [ player1_cards.pop(0), player2_cards.pop(0) ]
        print('Player 1 plays: {}'.format(drawn_cards[0]))
        print('Player 2 plays: {}'.format(drawn_cards[1]))
        if len(player1_cards) >= drawn_cards[0] and len(player2_cards) >= drawn_cards[1] :
            print('Playing a sub-game to determine the winner...')
            print()
            winner, _ = play_recursive_combat(player1_cards[:drawn_cards[0]], player2_cards[:drawn_cards[1]])
            print('... anyway, back to game {}'.format(game))
        else :
            winner = 1 if drawn_cards[0] > drawn_cards[1] else 2
        print('Player {} wins round {} of game {}'.format(winner, turn, game))
        print()
        if winner == 1:
            player1_cards.extend(drawn_cards)
        else :
            player2_cards.extend(drawn_cards[::-1])

    winner = 1 if player1_cards else 2
    winning_deck = player1_cards if winner == 1 else player2_cards
    score = sum([(n+1) * v for n, v in enumerate(winning_deck[::-1])])

    print('The winner of game {} is player {}'.format(game, winner))
    return winner, score


with open('data/input-day22.txt', 'r') as fp :
    player = 0
    cards = collections.defaultdict(list)

    for line in [ line.strip() for line in fp ] :
        if not line :
            continue
        if line[:6] == 'Player' :
            player = int(line[7:].rstrip(':')) - 1
        else :
            cards[player].append(int(line))



with DisablePrints() :
    result = play_combat(cards[0], cards[1])
print(result)


with DisablePrints() :
    next_game = 1
    result = play_recursive_combat(cards[0], cards[1])
print(result)