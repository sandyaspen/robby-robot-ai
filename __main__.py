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
        self.options['7'] = "Quit"

    def use_graphics(self):
        answer = 0
        while answer not in ['y', 'n']:
            print("Display every 500 episodes? [y/N]")
            answer = input().lower()
        if answer == 'y':
            return True
        return False

    def start_test(self, test):

        if test == '1':
            graphics = False
            q = None

            print("Basic training - 5000 Episodes, 200 Steps, E=0.1, LR=0.2, D=0.9")
            print("Epsilon decay: -0.001 per 50 Episodes\n")
            graphics = self.use_graphics()
            robby = Robby(q)
            print("Training Robby...")
            q, train_rewards = robby.train(
                5000, 200, 0.2, 0.9, 0.1, graphics)
            print("Testing - 5000 Episodes, 200 Steps, E=0.1")
            print("Epsilon and Q-Matrix Stable")
            print("Testing Robby...")
            test_rewards = robby.test(5000, 200, 0.1, graphics)
            avg_rewards = sum(test_rewards) / 5000
            print("Average Reward: {}   Standard Deviation: {}\n\n".format(
                avg_rewards, statistics.pstdev(test_rewards)))
            plot_list = []
            p_sum = 0
            for i in range(len(train_rewards)):
                p_sum += train_rewards[i]
                if i % 100 == 99:
                    plot_list.append(p_sum)
                    p_sum = 0
            plt.plot(plot_list)
            plt.figure()
            plt.show()

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
                print("Average Reward: {}   Standard Deviation: {}\n\n".format(
                    avg_rewards, statistics.pstdev(test_rewards)))
                plot_list = []
                p_sum = 0
                for i in range(len(train_rewards)):
                    p_sum += train_rewards[i]
                    if i % 100 == 99:
                        plot_list.append(p_sum)
                        p_sum = 0
                plt.plot(plot_list)
                plt.figure()
                plt.show()
                trial += 1

    def print_menu(self):
        for line in self.options.items():
            print("[{}] - {}".format(line[0], line[1]))

    def run(self):
        done = False

        while not done:
            selection = None
            while not selection:
                self.print_menu()
                selection = input()
                if selection not in self.options.keys():
                    print("\n*--- Invalid input, select again ---*\n\n ")
                    selection = None
                elif selection == '7':
                    done = True
                else:
                    self.start_test(selection)


if __name__ == "__main__":
    Menu().run()
    quit()
