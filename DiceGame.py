from random import randint, shuffle
from collections import defaultdict, OrderedDict
from argparse import ArgumentParser
import argparse


class DiceGame:
    REPEAT_AGAIN_VALUE = 6  # the dice value against which the player is allowed to roll again
    USER_NAME = "PLAYERS-{user_no}"  # user name format
    DICE_RANGE = {'from': 1, 'to': 6}  # the dice range , b/w which random values to be calculated
    PENALIZED_VALUE = 1  # the penalized value , if this value comes twice then we are not suppose to allow the player to roll for 1 time

    def __init__(self, number_of_users, points_to_win):
        self.number_of_users = number_of_users
        self.points_to_win = points_to_win
        self.winning_list = []
        print(f"Total number of Players --> {number_of_users}")
        print(f"Points to win --> {points_to_win}")


    def start_game(self):
        """
            The Entry of the Game...
        :return:
        """

        players = self.__get_players()
        players_ordered_dict = self.__get_player_dict(players)
        while True:  # condition to check winner list , if winnerlist < total_participants
            for player, player_details in players_ordered_dict.items():
                if self.verify_if_player_in_winning_list(player):
                    continue
                print("\n")
                input_value = input(f"{player} its your turn !! Press 'r' to continue : ")
                if input_value != 'r':
                    continue
                self.__roll_dice(player=player, players_dict=players_ordered_dict)
            if not self.__check_winner_list_count():
                break

        self.__append_last_user(players_ordered_dict)
        self.log_final_result()

    def __append_last_user(self, player_dict):
        for player, details in player_dict.items():
            if not self.verify_if_player_in_winning_list(player):
                self.winning_list.append({player: details})



    def log_final_result(self):
        print("********Annoucing the final result********")
        for index, obj in enumerate(self.winning_list, start=1):
            for player, player_details in obj.items():
                print(f"{index}. {player}")

    def __roll_dice(self, player, players_dict):
        if not self.__check_if_player_allowed_to_roll(player=player, player_dict=players_dict):
            print(f'{player} is Penalized as it rolled {self.PENALIZED_VALUE} twice')
            return
        rolled_value = randint(self.DICE_RANGE['from'], self.DICE_RANGE['to'])

        while True:
            if rolled_value == self.REPEAT_AGAIN_VALUE:
                print(f"Hurrayy !!!, {player} rolled {rolled_value} hence giving another changes to roll ")
                if self.__check_if_player_won(player=player, players_dict=players_dict, rolled_value=rolled_value):
                    break
                rolled_value = randint(self.DICE_RANGE['from'], self.DICE_RANGE['to'])
            else:
                print(f"{player} rolled {rolled_value}  ")
                break

        with open("just_check.txt", "w") as fp:
            fp.write(str(rolled_value))
        if self.__check_if_player_won(player=player, players_dict=players_dict, rolled_value=rolled_value):
            return

    def __check_if_player_won(self, player, players_dict, rolled_value):
        if self.verify_if_player_in_winning_list(player):
            return True
        players_dict[player]['points'].append(rolled_value)
        total_points = sum(players_dict[player]['points'])
        players_dict[player]['total_points'] = total_points
        self.log_player_rank(players_dict)
        print(f"Total score for {player} is {total_points}")

        if total_points >= self.points_to_win:
            self.winning_list.append({player: players_dict[player]})
            print(f"Inserting {player} into winners list")
            return True
        return False

    def log_player_rank(self, players_dict):
        print("******** LOGGING PLAYER RANK ***********")
        sorted_by_total_points = OrderedDict(
            sorted(players_dict.items(), key=lambda item: item[1]['total_points'], reverse=True))
        for player, details in sorted_by_total_points.items():
            print(f"{player} has scored --> {details['total_points']}")
        print("*******************", end="\n")

    def verify_if_player_in_winning_list(self, player):
        for plyr in self.winning_list:
            if player in plyr.keys():
                print(f"{player} in winning list")
                return True

        return False

    def __check_winner_list_count(self):

        if len(self.winning_list) >= (self.number_of_users - 1):
            print("Winner list found reached the hit ---> ", len(self.winning_list))
            return False
        return True

    def __check_if_player_allowed_to_roll(self, player, player_dict):
        player_obj = player_dict[player]
        try:
            if player_obj['points'][-1] >= self.PENALIZED_VALUE and player_obj['points'][
                -2] == self.PENALIZED_VALUE and not player_obj['penalized']:
                player_obj['penalized'] = True
                return False
            return True
        except IndexError:
            print()
            return True

    def __get_player_dict(self, players: list):
        players_ordered_dict = OrderedDict()
        for player in players:
            players_ordered_dict[player] = {
                "total_points": 0,
                "points": [],
                "penalized": False
            }
        return players_ordered_dict

    def __get_players(self) -> list:
        players_list = []
        for user_no in range(self.number_of_users):
            user_name = self.USER_NAME.format(user_no=user_no + 1)
            players_list.append(user_name)
        shuffle(players_list)
        return players_list  # shuffling the user order


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def get_argument_parser():
    arg_parse = ArgumentParser(description="Provide dice game params")
    arg_parse.add_argument('-UserCount', type=check_positive, help="Provide the total number of users")
    arg_parse.add_argument('-PointsToWin', type=check_positive, help="Provide the total number of users")
    return arg_parse.parse_args()


if __name__ == "__main__":
    args = get_argument_parser()
    dcgm_obj = DiceGame(number_of_users=args.UserCount, points_to_win=args.PointsToWin)
    dcgm_obj.start_game()
