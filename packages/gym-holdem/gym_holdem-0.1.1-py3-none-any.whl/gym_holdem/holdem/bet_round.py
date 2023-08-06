from enum import Enum


class BetRound(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4
    GAME_OVER = 5


def bet_round_to_str(bet_round):
    if bet_round == BetRound.PREFLOP:
        return "Preflop"
    elif bet_round == BetRound.FLOP:
        return "Flop"
    elif bet_round == BetRound.TURN:
        return "Turn"
    elif bet_round == BetRound.RIVER:
        return "River"
    elif bet_round == BetRound.SHOWDOWN:
        return "Showdown"
    else:
        raise Exception("No valid bet round")
