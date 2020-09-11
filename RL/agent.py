import random

class QLearning():
    def __init__(self, lr, gamma, episodes, Epsilon, Min_Epsilon, Decay):
        self.lr = lr
        self.gamma = gamma
        self.episodes = episodes
        self.Epsilon = Epsilon
        self.Min_Epsilon = Min_Epsilon
        self.Decay = Decay
        self.Q_Table = self.Q_Table()

    def Q_Table(self):
        Q_Table = [0 for i in range(9)]
        return Q_Table

    def possible_actions(self, board):
        empty_cells = []
        for y,row in enumerate(board):
            for x,case in enumerate(row):
                if case == 0:
                    empty_cells.append([x,y])
        return empty_cells

    def choose_action(self, board):


        if random.random() < self.Epsilon:
            #take random action

            i = random.randint(len(self.possible_actions(board)))
            

        else:
            #exploitation
            #take biggest value
            action = max(self.Q_Table)
