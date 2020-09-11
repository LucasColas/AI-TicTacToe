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

    def choose_action(self):

        if random.random() < self.Epsilon:
            #take random action
            pass

        else:
            #exploitation
            #take biggest value
            action = max(self.Q_Table)
            pass
