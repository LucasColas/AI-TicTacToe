import random

class QLearning():
    def __init__(self, board, lr, gamma, episodes, Epsilon, Min_Epsilon, Decay):
        self.board = board
        self.lr = lr
        self.gamma = gamma
        self.episodes = episodes
        self.Epsilon = Epsilon
        self.Min_Epsilon = Min_Epsilon
        self.Decay = Decay
        self.Q_Table = self.Q_Table()
        self.pos = self.possible_actions()

    def Q_Table(self):
        Q_Table = [0 for i in range(9)]
        return Q_Table

    def possible_actions(self):
        empty_cells = []
        for y,row in enumerate(self.board):
            for x,case in enumerate(row):
                if case == 0:
                    empty_cells.append([x,y])
        return empty_cells

    def choose_action(self):

        if random.random() < self.Epsilon:
            #take random action
            i = random.randint(0, len(self.possible_actions(self.board))-1)
            pos = self.pos[i]
            x,y = pos[0], pos[1]


        else:
            #exploitation
            #take biggest value
            action = max(self.Q_Table)
