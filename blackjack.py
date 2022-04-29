""" 
Blackjack Simulator
Author: Brandon Jenkins

"""

import random
from time import sleep
from os import linesep


def create_standard_deck():
    """ Creates a deck of cards where:
        The deck is a list, 
        The cards are tuples of the form (suit, number),
        The number represents the card's identity
        Jack = 11, Queen = 12, King = 13, and Ace = 14 """

    return [
        ('clubs', 2), ('clubs', 3), ('clubs', 4), ('clubs', 5), ('clubs', 6), ('clubs', 7),
        ('clubs', 8), ('clubs', 9), ('clubs', 10), ('clubs', 'Jack'), ('clubs', 'Queen'), ('clubs', 'King'),
        ('clubs', 'Ace'), ('diamonds', 2), ('diamonds', 3), ('diamonds', 4), ('diamonds', 5), ('diamonds', 6),
        ('diamonds', 7), ('diamonds', 8), ('diamonds', 9), ('diamonds', 10), ('diamonds', 'Jack'),
        ('diamonds', 'Queen'), ('diamonds', 'King'), ('diamonds', 'Ace'), ('hearts', 2), ('hearts', 3), ('hearts', 4),
        ('hearts', 5), ('hearts', 6), ('hearts', 7), ('hearts', 8), ('hearts', 9), ('hearts', 10), ('hearts', 'Jack'),
        ('hearts', 'Queen'), ('hearts', 'King'), ('hearts', 'Ace'), ('spades', 2), ('spades', 3), ('spades', 4),
        ('spades', 5), ('spades', 6), ('spades', 7), ('spades', 8), ('spades', 9), ('spades', 10), ('spades', 'Jack'),
        ('spades', 'Queen'), ('spades', 'King'), ('spades', 'Ace')
    ]


def remove_card_from_deck(deck, card):
    """ Removes a drawn card from the deck """
    deck.remove(card)
    return deck


def draw_card(deck):
    """ Takes a deck of cards as the input
        Randomly selects a card from the deck and then
        Removes the card from the deck
        Returns the card that was selected. """

    random_card = random.choice(deck)
    remove_card_from_deck(deck, random_card)
    return random_card


def display_dealer(opponent, start=False):
    """ Displays the dealer's hand """

    sleep(1)
    print('Dealer:')
    if start:  # only display before dealer plays
        output = [opponent[0], ('?', '?')]  # second card is hidden
        print(f"{output}\n")
    else:
        print(f"{opponent}\n")


def display_player(player):
    """ Displays the player's hand """

    sleep(1)
    print('Player:')
    print(f"{player}\n")


def get_count(player):
    """ Takes a player’s hand, which is a list of tuples
        Converts 'Jack', 'Queen', 'King', 'Ace' into values
        Calculates and returns the value of the player’s hand """

    card_amount = len(player)
    hand_count = 0
    iterate_count = 0
    ace_in_hand = 0

    for i in range(card_amount):
        # Tallies total aces in hand
        if player[iterate_count][1] == 'Ace':
            ace_in_hand += 1

        elif player[iterate_count][1] == 'King' \
                or player[iterate_count][1] == 'Queen' or player[iterate_count][1] == 'Jack':
            hand_count += 10

        else:
            hand_count += player[iterate_count][1]

        iterate_count += 1

    for ace in range(ace_in_hand):
        # Represents ace as 1 or 11 depending on current hand value
        if hand_count < 11:
            hand_count += 11
        else:
            hand_count += 1

    return hand_count


def check_cards(player):
    """ Takes a player’s hand as input
        Returns ‘WIN’ if the input player has exactly a count of 21.
        If they have a count that is greater than 21, then it returns ‘BUST’;
        otherwise, it returns ‘OK’ """

    hand_count = get_count(player)

    if hand_count == 21:
        return 'WIN'

    elif hand_count > 21:
        return 'BUST'

    else:
        return 'OK'


def decipher_winner(player, dealer, double_down=False):
    """ When both player and dealer stands, this function deciphers the winner """

    player_count = get_count(player)
    dealer_count = get_count(dealer)

    if player_count > dealer_count:
        sleep(.5)
        print("Player wins.\n")
        sleep(.5)
        if double_down:
            return 2
        return 1
    elif player_count < dealer_count:
        sleep(.5)
        print("Dealer wins.\n")
        sleep(.5)
        if double_down:
            return -2
        return -1
    else:
        sleep(.5)
        print("It's a draw.\n")
        sleep(.5)
        return 0


def create_blackjack_game(user_input):
    """ Create a list for the player called ‘player’, 
        which will hold the cards in the player’s hand,
        and then create another list for the dealer called ‘dealer’,
        which will hold the cards in the dealer’s hand. """

    double_down = False  # declaring this variable here makes my IDE happy. double down hit variable
    player = []
    dealer = []

    # Create a new deck of cards using the create_standard_deck() function.

    deck = create_standard_deck()

    # Draw two cards for each player and add them to the respective player’s hands.

    player.append(draw_card(deck))
    player.append(draw_card(deck))
    dealer.append(draw_card(deck))
    dealer.append(draw_card(deck))

    # Display the cards

    display_player(player)
    display_dealer(dealer, start=True)

    # The dealer must first check for blackjack
    # Insurance is offered to the player

    dealer_count = get_count(dealer)
    if dealer[0][1] == 'Ace':
        print("Dealer displays an Ace.")
        print(f"Purchase insurance for ${bet / 2}?")
        insurance = input("Enter 'y' or 'n': ")

        if dealer_count == 21 and insurance == 'y':
            sleep(1)
            print("Dealer blackjack! Dealer wins.\n")
            return -3
        elif dealer_count == 21:
            sleep(1)
            print("Dealer blackjack! Dealer wins.\n")
            return -1
        else:
            sleep(1)
            print("No dealer blackjack.\n")

    if not user_input:
        player_action = input('press h to hit, s to stand, d to double down, q to quit.\n').lower().strip(linesep)
        while player_action not in ('s', 'h', 'q', 'd'):
            player_action = input('press h to hit, s to stand, d to double down, q to quit.\n').lower().strip(linesep)

    else:
        player_action = user_input.pop(0)

    if player_action == 'q':
        return 0

    while player_action != 'q':

        if player_action == 'h':
            # Hit. Draw card.

            player.append(draw_card(deck))
            print("Player hits.\n")

            display_player(player)
            display_dealer(dealer, start=True)

            # After each card is drawn, the player’s hand needs to be checked to see whether they have won,
            # they bust, or whether everything is ok.

            check = check_cards(player)

            if check == 'WIN':
                print("Player blackjack! Player wins.\n")
                return 3
            elif check == 'BUST':
                print("Player busts.\n")
                return -1
            else:
                print(check)

        else:
            if player_action == 'd':  # begin double down cascade
                double_down = True
                print("Player doubles down on a hit.\n")

                player.append(draw_card(deck))

                display_player(player)
                display_dealer(dealer, start=True)

                check = check_cards(player)

                if check == 'WIN':
                    sleep(1)
                    print("Player blackjack! Player wins.\n")
                    return 4
                elif check == 'BUST':
                    sleep(1)
                    print("Player busts.\n")
                    return -2

            elif player_action == 's':  # player stands, check for blackjack before dealer plays
                print("Player stands.\n")

                check = check_cards(player)
                if check == 'WIN':
                    sleep(1)
                    print("Player blackjack! Player wins.\n")
                    return 1

            while True:
                # Dealer logic:
                # The dealer displays hidden card
                # The dealer will continue to ‘hit’ if the total count in their hand is lower than 17.
                # There is a check whether the dealer has won, is bust, or is in the range from 17 to 20.
                # If the dealer has a total value in the range from 17 to 20, then the dealer must stop drawing cards.
                # The winner is then deciphered and returned

                check = check_cards(dealer)

                if check == 'WIN':
                    display_player(player)
                    display_dealer(dealer)
                    print("Dealer blackjack! Dealer wins.\n")

                    if double_down:
                        return -2
                    return -1

                else:
                    while dealer_count < 17:
                        display_player(player)
                        display_dealer(dealer)
                        print("Dealer hits.\n")
                        dealer.append(draw_card(deck))
                        check = check_cards(dealer)

                        if check == 'WIN':
                            display_player(player)
                            display_dealer(dealer)
                            print("Dealer blackjack! Dealer wins.\n")
                            if double_down:
                                return -2
                            return -1

                        elif check == 'BUST':
                            display_player(player)
                            display_dealer(dealer)
                            print("Dealer busts.\n")
                            if double_down:
                                return 2
                            return 1

                        dealer_count = get_count(dealer)

                    display_player(player)
                    display_dealer(dealer)
                    return decipher_winner(player, dealer, double_down)

        if not user_input:
            player_action = input('press h to hit, s to stand, q to quit.\n').lower().strip(linesep)
            while player_action not in ('s', 'h', 'q'):
                player_action = input('press h to hit, s to stand, q to quit.\n').lower().strip(linesep)
            if player_action == 'q':
                return 0
        else:
            player_action = user_input.pop(0)


# Game begins here
print("Welcome to blackjack.\n")
print("How much are you entering the table with?")
pot = 0
bet = 0

while True:
    try:
        pot = int(input("Enter pot amount: "))
    except ValueError:
        print("Enter a valid number.")
        continue

    if pot < 1:
        print("Enter a valid number.")
        continue
    break

while True:
    print(f"\nPot: {pot}\n")
    print("Game is about to begin.")

    while True:
        try:
            bet = int(input("Enter bet amount: "))
        except ValueError:
            print("Enter a valid number.")
            continue

        if bet > pot:
            print("Bet cannot be greater than your pot.\n")
            continue
        elif bet < 1:
            print("Bet minimum is $1.\n")
            continue
        break

    print("")
    result = create_blackjack_game(False)

    # Win or Loss currency results
    if result == 1:  # normal hand winning
        pot += bet
    elif result == -1:  # normal hand losing
        pot -= bet
    elif result == 2:  # double down winning
        pot += bet * 2
    elif result == 3:  # blackjack winning
        pot += bet * 1.5
    elif result == 4:  # blackjack & double down winning
        pot += (bet * 2) * 1.5
    elif result == -2:  # double down losing
        pot -= bet * 2
    elif result == -3:  # insurance losing
        pot -= bet / 2

    print(f"Pot: {pot}\n")
    if pot == 0:
        sleep(1)
        print("Unfortunately you are out of funds. Go get some more and come back.")
        print("Thanks for playing.")
        break

    elif pot < 0:  # honestly gibberish
        print("You double downed when you don't have the money.")
        print("I will now hack your device. Stand by.\n")
        sleep(1)
        print("....")
        print("Exit()")
        break

    play = input("Play again? (enter 'y' or 'n'): ")

    if play == 'n':
        print("\nThanks for playing.")
        break
