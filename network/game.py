class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]

    def get_player_move(self, p):
        # p must be 0 or 1
        return self.moves[p]

    def player(self, player, move):
        self.moves[player] = move
        if player == 0:
            p1Went = True
        else:
            p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1  # tie

        if p1 == "R" and p2 == "S":
            winner = 0  # p1 wins
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def reset_went(self):
        self.p1Went = False
        self.p2Went = False