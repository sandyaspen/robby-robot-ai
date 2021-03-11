from collections import OrderedDict
from robby import Robby
import matplotlib.pyplot as plt
import statistics


class Menu():

    def __init__(self):
        # Create dict of options
        self.options = OrderedDict()
        self.options['1'] = "Run 1 Standard Training + 1 Test"
        self.options['2'] = "Run 4 Training/Tests with different Learning Rates"
        self.options['3'] = "Run Training/Test with no Epsilon decay"
        self.options['4'] = "Run Training/Test with -0.5 action tax"
        self.options['0'] = "Quit"

    def use_graphics(self):
        answer = 0
        while answer not in ['y', 'n', '']:
            print("Display every 500 episodes? [y/N]")
            answer = input().lower()
        if answer == 'y':
            return True
        return False

    def plot_training(self, data, title):
        fig, ax = plt.subplots()
        ax.plot(range(99, 5000, 100), data)
        ax.set(xlabel='Episode Number', ylabel='Cumulative Rewards over Previous 100 Episodes',
            title=title)
        ax.grid()
        fig.savefig("{}.png".format(title))
        plt.show()

    def start_test(self, test):

        if test == '1':
            graphics = False
            q = None

            print("Training - 5000 Episodes, 200 Steps, E=0.1, LR=0.2, D=0.9")
            print("Epsilon decay: -0.001 per 50 Episodes\n")
            graphics = self.use_graphics()
            robby = Robby(q)
            print("Training Robby...")
            q, train_rewards = robby.train(
                5000, 200, 0.2, 0.9, 0.1, graphics)
            print("\n\nTesting - 5000 Episodes, 200 Steps, E=0.1")
            print("Epsilon and Q-Matrix Stable")
            print("Testing Robby...")
            test_rewards = robby.test(5000, 200, 0.1, graphics)
            avg_rewards = sum(test_rewards) / 5000
            print("\n\nTest-Average: {}   Test-Standard-Deviation: {}\n\n".format(
                avg_rewards, statistics.pstdev(test_rewards)))
            plot_list = []
            p_sum = 0
            for i in range(len(train_rewards)):
                p_sum += train_rewards[i]
                if i % 100 == 99:
                    plot_list.append(p_sum)
                    p_sum = 0
            self.plot_training(plot_list, "StandardTraining")

        if test == '2':
            graphics = False
            q = None
            trial = 1
            learning_rates = [0.2, 0.4, 0.6, 0.8]

            print("===Learning Rate Tests===\n")
            for lr in learning_rates:
                print("Learning Rate Test {}: LR={}\n".format(trial, lr))
                print(
                    "Training - 5000 Episodes, 200 Steps, E=0.1, LR={}, D=0.9".format(lr))
                print("Epsilon decay: -0.001 per 50 Episodes")
                robby = Robby(q)
                print("Training Robby...")
                q, train_rewards = robby.train(
                    5000, 200, lr, 0.9, 0.1, graphics)
                print("\n\nTesting - 5000 Episodes, 200 Steps, E=0.1")
                print("Epsilon and Q-Matrix Stable")
                print("Testing Robby...")
                test_rewards = robby.test(5000, 200, 0.1, graphics)
                avg_rewards = sum(test_rewards) / 5000
                print("\n\nTest-Average: {}   Test-Standard-Deviation: {}\n\n".format(
                    avg_rewards, statistics.pstdev(test_rewards)))
                plot_list = []
                p_sum = 0
                for i in range(len(train_rewards)):
                    p_sum += train_rewards[i]
                    if i % 100 == 99:
                        plot_list.append(p_sum)
                        p_sum = 0
                self.plot_training(plot_list, "LearningRate{}".format(trial))
                trial += 1

        if test == '3':
            graphics = False
            q = None
            print("===No Epsilon Decay Test===\n")
            print("Training - 5000 Episodes, 200 Steps, E=0.1, LR=0.2, D=0.9")
            print("Epsilon decay: None\n")
            graphics = self.use_graphics()
            robby = Robby(q)
            print("Training Robby...")
            q, train_rewards = robby.train(
                5000, 200, 0.2, 0.9, 0.1, graphics, decay=False)
            print("\n\nTesting - 5000 Episodes, 200 Steps, E=0.1")
            print("Epsilon and Q-Matrix Stable")
            print("Testing Robby...")
            test_rewards = robby.test(5000, 200, 0.1, graphics)
            avg_rewards = sum(test_rewards) / 5000
            print("\n\nTest-Average: {}   Test-Standard-Deviation: {}\n\n".format(
                avg_rewards, statistics.pstdev(test_rewards)))
            plot_list = []
            p_sum = 0
            for i in range(len(train_rewards)):
                p_sum += train_rewards[i]
                if i % 100 == 99:
                    plot_list.append(p_sum)
                    p_sum = 0
            self.plot_training(plot_list, "NoEpsilonDecay")

        if test == '4':
            graphics = False
            q = None
            print("===Action Tax Test===\n")
            print("Training - 5000 Episodes, 200 Steps, E=0.1, LR=0.2, D=0.9")
            print("Epsilon decay: -0.001 per 50 Episodes")
            print("Each action taxed -0.5 reward")
            graphics = self.use_graphics()
            robby = Robby(q)
            print("Training Robby...")
            q, train_rewards = robby.train(
                5000, 200, 0.2, 0.9, 0.1, graphics, decay=True, tax=True)
            print("\n\nTesting - 5000 Episodes, 200 Steps, E=0.1")
            print("Epsilon and Q-Matrix Stable")
            print("Testing Robby...")
            test_rewards = robby.test(5000, 200, 0.1, graphics)
            avg_rewards = sum(test_rewards) / 5000
            print("\n\nTest-Average: {}   Test-Standard-Deviation: {}\n\n".format(
                avg_rewards, statistics.pstdev(test_rewards)))
            plot_list = []
            p_sum = 0
            for i in range(len(train_rewards)):
                p_sum += train_rewards[i]
                if i % 100 == 99:
                    plot_list.append(p_sum)
                    p_sum = 0
            self.plot_training(plot_list, "ActionTax")



    def print_menu(self):
        for line in self.options.items():
            print("[{}] - {}".format(line[0], line[1]))

    def run(self):
        done = False
        print("Sandy Wood - 2021")

        while not done:
            selection = None
            print("\n")
            print("-"*30)
            print("| Robby the Clever Can Robot |")
            print("-"*30)
            print("How can Robby be of service today?\n")
            while not selection:
                self.print_menu()
                selection = input()
                if selection not in self.options.keys():
                    print("\n*--- Invalid input, select again ---*\n\n ")
                    selection = None
                elif selection == '0':
                    done = True
                else:
                    self.start_test(selection)


if __name__ == "__main__":
    Menu().run()
    quit()
