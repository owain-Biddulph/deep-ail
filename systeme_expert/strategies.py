import utils
from alphabeta import possible_target_squares
import math
import time

class Strategy:

    def play(self, state):
        pass


class AttackFirst(Strategy):

    def play(self, state):
        distance_min, groups = utils.distance_min(state)
        print("distance_min:", distance_min)
        if distance_min == 1:
            moves = [[groups[0][0], groups[0][1], state.board[groups[0][0], groups[0][1], 1],groups[1][0], groups[1][1]]]

        elif distance_min == 2:
            possible_squares = possible_target_squares(state.nb_rows, state.nb_columns, groups[0][0], groups[0][1])
            for square in possible_squares:
                new_distance = utils.distance(square, groups[1])
                moves = [[groups[0][0], groups[0][1], state.board[groups[0][0], groups[0][1], 1], square[0], square[1]]]
                if new_distance == 2:
                    print("move choisi", move)
                    break

        else:
            possible_squares = possible_target_squares(state.nb_rows, state.nb_columns, groups[0][0], groups[0][1])
            min_distances = math.inf
            for square in possible_squares:
                new_distance = utils.distance(square, groups[1])

                if new_distance < min_distances:
                    move = [
                        [groups[0][0], groups[0][1], state.board[groups[0][0], groups[0][1], 1], square[0], square[1]]]
                    min_distances = new_distance
        time.sleep(0.3)
        return move


class StraightAttack(Strategy):

    def play(self, state):

        distance_min, groups = utils.distance_min(state)
        possible_squares = possible_target_squares(state.nb_rows, state.nb_columns, groups[0][0], groups[0][1])

        for square in possible_squares:
            new_distance = utils.distance(square, groups[1])
            move = [[groups[0][0], groups[0][1], state.board[groups[0][0], groups[0][1], 1], square[0], square[1]]]
            if new_distance == distance_min - 1:
                print("move choisi", move)
                break
        return move






