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

        # self.alpha_decay = 0.99

        self.q_table = np.zeros((n, n))  # Q[current, next]

    def select_action(self, state, unvisited, greedy=False):
        if not greedy and random.uniform(0, 1) < self.epsilon:
            return random.choice(list(unvisited))
        else:
            return max(unvisited,key = lambda x : self.q_table[state,x])

    def update_q_value(self, state, action, reward, next_state, unvisited):
        # compute max future Q (0 if terminal)
        if unvisited:
            max_future_q = max(self.q_table[next_state, a] for a in unvisited)
        else:
            max_future_q = 0
        # Q-learning formula
        self.q_table[state, action] += self.alpha*(reward + self.gamma*max_future_q - self.q_table[state, action])

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay)

    # def decay_alpha(self):
    #     self.alpha = max(0.01, self.alpha * self.alpha_decay)

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
        # agent.decay_alpha()
        # if epoch == 1500: 
        #     agent.gamma = 0.75
        #     agent.epsilon = 0.3

        if total_reward > -40000:
            break

        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Total Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.4f}, Alpha: {agent.alpha:.4f}")

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

# class QLAgent:
#     def __init__(self, n, alpha=0.1, gamma=0.9, epsilon=1.0, decay=0.995, min_epsilon=0.01, get_possible_actions=[]):
#         self.n = n
#         self.alpha = alpha
#         self.gamma = gamma
#         self.epsilon = epsilon
#         self.decay = decay
#         self.min_epsilon = min_epsilon
#         self.get_possible_actions = get_possible_actions

#         self.q_table = np.zeros((n, n)) 
    
#     def getQ(self, state, action):
#         return self.q_table[state, action]
    
#     def setQ(self, state, action, value):
#         self.q_table[state, action] = value

#     def update(self, state, action, reward, next_state, done):
#         if not done:
#             best_next_action = self.max_action(next_state)
#             td_target = reward + self.gamma * self.getQ(next_state, best_next_action) - self.getQ(state, action)
#         else:
#             td_target = reward - self.getQ(state, action)

#         new_value = self.getQ(state, action) + self.alpha * td_target
#         self.setQ(state, action, new_value)

#     def max_action(self, state):
#         actions = self.get_possible_actions(state)
#         best_action = []
#         max_q = float('-inf')
#         for action in actions:
#             q_s_a = self.getQ(state, action)
#             if q_s_a > max_q:
#                 max_q = q_s_a
#                 best_action = [action]
#             elif q_s_a == max_q:
#                 best_action.append(action)
        
#         return random.choice(best_action)
    
#     def get_action(self, state):
#         actions = self.get_possible_actions(state)

#         if len(actions) == 0:
#             return None
        
#         if np.random.rand() < self.epsilon:
#             return random.choice(actions)
#         else:
#             return self.max_action(state)
        
# def trainQL_agent(agent: QLAgent, distance_matrix, epoches=1000):
#     n = len(distance_matrix)
#     for epoch in range(epoches):
#         start = 0 # fixed start city (at 0)
#         state = start
#         # unvisited: all cities except start
#         unvisited = [i for i in range(1,n)]
#         path = [state]
#         total_reward = 0.0

#         while unvisited:
#             action = agent.get_action(state)
#             # reward: negative distance
#             reward = -distance_matrix[state][action]
#             next_state = action
#             # remove action from unvisited
#             unvisited.remove(action)

#             done = len(unvisited) == 0
#             agent.update(state, action, reward, next_state, done)
#             state = next_state
#             path.append(state)
#             total_reward += reward

#         # Return to the starting city (use stored start)
#         reward = -distance_matrix[state][start]
#         agent.update(state, start, reward, start, True)
#         total_reward += reward

#         agent.decay_epsilon()

#         if epoch % 10 == 0:
#             print(f"Epoch {epoch}, Total Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.4f}, Alpha: {agent.alpha:.4f}")

#     return agent