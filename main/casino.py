from main.player import Player
from poker.start_poker import Poker_Game
from races.races import Races
import os
from blackjack.start_blackjack import Strat_blackjack
from bingo.bingo import Bingo
from roulette.roulette import Roulette


LIST_OF_GAMES = ["Races", "Poker", "Blackjack", "Roulette", "Bingo"] 

def get_pass():
    import tkinter
    import tkinter.simpledialog
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    return tkinter.simpledialog.askstring('Password','Password:', show='*')

class Casino():
    def __init__(self, players_file) -> None:
        self.file = players_file

    def create_player(self, name, money):
        return Player(name, money)

    def login(self):
        print("Welcome to AH Casino!")
        first_time = input("Are you visiting us for the first time? (Y/N) ")
        if first_time in "Yesyes":
            while True:
                name = input("Give us your name: ")
                with open(self.file, 'r') as players:
                    for line in players:
                        line = line.strip('\n')
                        login, password, money = line.split(';')
                        if name == login:
                            print("Sorry this login is already taken"
                                  "Please choose another one.")
                            break
                    else:
                        break
            password = input("Password: ")
            with open(self.file, 'a') as players:
                players.write(name + ";" + password + ";" + "1000\n")

            player = self.create_player(name, 1000)
            return player

        elif first_time in "Nono":
            player_login = input("Login: ")
            while True:
                with open(self.file, 'r') as players:
                    for line in players:
                        line = line.strip('\n')
                        login, password, money = line.split(';')
                        if player_login == login:
                            player_password = get_pass()
                            while player_password != password:
                                print("Invalid password.")
                                player_password = get_pass()
                            money = int(money)
                            player = self.create_player(login, money)
                            return player
                print("Sorry I couldn't find that login.")
                player_login = input("Login: ")
        
        else:
            print("Are you dumb? YES or NO")
            return None


    def start(self):
        player = self.login()
        
        while True:
            print("Please choose a game from the list below:")
            for index, game in enumerate(LIST_OF_GAMES):
                print(f"{index + 1}: {game}")
            print("Type 'b' if you want to check your balance")
            print("Type 'q' if you want to quit")

            choice = input("Type a number of a game: ")

            if choice == "1":
                races = Races(player)
                races.make_race()
                os.system('cls')

            elif choice == "2":
                if player.get_tokens() < 10:
                    print("In order to play poker you need to bet 10 tokens, "
                          "please come back later with the money")
                else:
                    
                    player.spend_tokens(10)
                    print("Poker is starting")
                    game = Poker_Game(player)
                    
                    game.start_game()
                    game.end_game()

                    os.system('cls')
                

            elif choice == "3":
                bet = player.get_tokens() + 1
                while bet > player.get_tokens():
                    bet = int(input("Place your bet: "))
                    if bet > player.get_tokens():
                        print("You don't have enough tokens")

                player.spend_tokens(bet)
                game = Strat_blackjack(player, bet)
                game.start_game()

                os.system('cls')

            elif choice == "4":
                print("Roulette is starting")
                r = Roulette(player)
                r.start_roulette()

            elif choice == "5":
                print("Bingo is starting")
                b = Bingo(player)
                b.start_game()


            elif choice == "q":
                print("Thank you for playing, hope to see you soon!")
                self.logout(player)
                break

            elif choice == "b":
                print(f"You have {player.get_tokens()} tokens")

    def logout(self, player: Player):
        players = open(self.file, "r")
        replaced_content = ""

        for line in players:
            line = line.strip()
            login, password, money = line.split(';')
            if player.get_name() == login:
                new_line = line.replace(money, str(player.get_tokens()))
            else:
                new_line = line
            replaced_content = replaced_content + new_line + "\n"
    
        players.close()
        new_players = open(self.file, "w")
        new_players.write(replaced_content)
        new_players.close()
        
    