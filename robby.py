import random
random.seed()

import matplotlib.pyplot as plt
import numpy as np

import watchrobby
from grid import *


class Robby:

    def __init__(self, q=None) -> None:
        self.actions = [0,1,2,3,4] #Pickup, N, S, E, W
        if q:
            self.q = q
        else:
            self.q = {}

    def sense_state(self):
        grid = self.grid
        c = grid.sense_current()
        n = grid.sense_north()
        s = grid.sense_south()
        e = grid.sense_east()
        w = grid.sense_west()
        return c,n,s,e,w

    def set_state(self, c, n, s, e, w):
        self.state = c,n,s,e,w

    def pick_up_can(self):
        return self.grid.remove_can()
    
    def add_state_to_q(self, state):
        if state not in self.q:
            self.q[state] = np.zeros(5)

    def decide(self, epsilon = 0.1):
        #Choose Action
        if random.random() < epsilon:
            action = random.choice(self.actions)
        else:
            action = np.argmax(self.q[self.state])
        return action

    #Perform requested action, return reward
    def act(self, action):
        #Pick Up Can
        if action == 0:
            success = self.pick_up_can()
            if success:
                return 10 #Reward: Picked up can
            else:
                return -1 #Reward: Tried to pick up non-existant can
        #Move N
        elif action == 1:
            success = self.grid.move_robby_north()
            if success:
                return 0 #Reward: Successful Move
            else:
                return -5 #Reward: Crashed into wall
        #Move S
        elif action == 2:
            success = self.grid.move_robby_south()
            if success:
                return 0 #Reward: Successful Move
            else:
                return -5 #Reward: Crashed into wall
        #Move E
        elif action == 3:
            success = self.grid.move_robby_east()
            if success:
                return 0 #Reward: Successful Move
            else:
                return -5 #Reward: Crashed into wall
        #Move W
        elif action == 4:
            success = self.grid.move_robby_west()
            if success:
                return 0 #Reward: Successful Move
            else:
                return -5 #Reward: Crashed into wall

    def train(self, episodes = 5000, steps = 200, learning_rate = 0.2, discount = 0.9, epsilon = .1, graphics = False):
        episode_rewards = 0 
        episode_reward_list = []
        rewards_sum = 0

        #run each episode
        for episode in range(episodes):
            #create new environment
            self.grid = Grid()

            #Get first state
            self.state = self.sense_state()

            #Add to matrix if not there already
            self.add_state_to_q(self.state)

            #run each step
            for step in range(steps):
                #Choose Action
                action = self.decide(epsilon)
                #Perform Action, collect reward
                reward = self.act(action)
                #Observe the New State which now exists after our action
                next_state = self.sense_state()
                self.add_state_to_q(next_state)
                #Check if we have finished
                done = self.grid.check_done()
                #Update Q
                if not done:
                    self.q[self.state][action] = self.q[self.state][action] + learning_rate * (reward + discount* np.amax(self.q[next_state]) - self.q[self.state][action])
                else:
                    self.q[self.state][action] = self.q[self.state][action] + learning_rate * (reward - self.q[self.state][action])
                #Add to episode reward sum
                episode_rewards += reward
                #Set to next state
                self.set_state(*next_state)

                #Display if visibility is set
                if True:
                    if episode % 500 == 499 or episode == 0:
                        watchrobby.render(self.grid.grid, episode, step)
                    if done:
                        break
            #Print out numbers
            print("EP: {}    REWARD: {}    EPSILON: {}".format(episode, episode_rewards, epsilon))
            #add to plot list
            if episode % 100 == 0:
                episode_reward_list.append(episode_rewards)
            episode_rewards = 0
            #decay epsilon
            if episode % 50 == 0:
                epsilon -= .005

        return episode_reward_list

    def test(self, episodes = 5000, steps = 200):
        episode_rewards = 0
        reward_list = []
        for episode in range(episodes):
            #create new environment
            self.grid = Grid()
            #Get first state
            self.state = self.sense_state()
            self.add_state_to_q(self.state)
            for step in range(steps):
                #Choose Action
                action = self.decide()
                #Perform Action, collect reward
                reward = self.act(action)
                #Observe New State
                next_state = self.sense_state()
                self.add_state_to_q(next_state)
                #Check if we have finished
                done = self.grid.check_done()
                #Add to episode reward sum
                episode_rewards += reward
                #Set to next state
                self.set_state(*next_state)
                if done:
                    break
            if episode % 100 == 0:
                reward_list.append(episode_rewards)
            episode_rewards = 0
        plt.plot(reward_list)
        plt.figure()
        plt.show()


if __name__ == '__main__':
    robby = Robby()
    robby.train()
    robby.test()
    quit()

