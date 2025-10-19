# qlearning.py — corrected minimal version

import numpy as np
import random

class QAgent:
    def __init__(self, n, alpha=0.1, gamma=0.9, epsilon=1.0, decay=0.995, min_epsilon=0.01):
        self.n = n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.decay = decay
        self.min_epsilon = min_epsilon
        self.q_table = np.zeros((n, n))  # Q[current, next]

    def select_action(self, state, unvisited, greedy=False):
        if not greedy and random.uniform(0, 1) < self.epsilon:
            return random.choice(list(unvisited))
        else :
            return max(unvisited,key = lambda x : self.q_table[state,x])

    def update_q_value(self, state, action, reward, next_state, unvisited):
        # compute max future Q (0 if terminal)
        if unvisited:
            max_future_q = max(self.q_table[next_state, a] for a in unvisited)
        else:
            max_future_q = 0
        # Q-learning formula
        self.q_table[state, action] += self.alpha*(reward + self.gamma * max_future_q - self.q_table[state, action])

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay)


def train_agent(agent: QAgent, distance_matrix, epoches=1000):
    n = len(distance_matrix)
    for epoch in range(epoches):
        start = 0 # fixed start city (at 0)
        state = start
        # unvisited: all cities except start
        unvisited = [i for i in range(1,n)]
        path = [state]
        total_reward = 0.0

        while unvisited:
            action = agent.select_action(state, unvisited)
            # reward: negative distance
            reward = -distance_matrix[state][action]
            next_state = action
            # remove action from unvisited
            unvisited.remove(action)

            agent.update_q_value(state, action, reward, next_state, unvisited)
            state = next_state
            path.append(state)
            total_reward += reward

        # Return to the starting city (use stored start)
        reward = -distance_matrix[state][start]
        agent.update_q_value(state, start, reward, start, [])
        total_reward += reward

        agent.decay_epsilon()

        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Total Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.4f}")

    return agent


def getSolution(agent, start_city=0):
    """Extract a greedy route from the learned Q-table (no exploration)."""
    state = start_city
    n = agent.q_table.shape[0]
    unvisited = [i for i in range(n) if i != start_city]
    path = [start_city + 1]  # 1-based for printing

    while unvisited:
        action = agent.select_action(state, unvisited, greedy=True)  # greedy extraction
        path.append(action + 1)
        unvisited.remove(action)
        state = action

    path.append(start_city + 1)  # return to start (1-based)
    return path
