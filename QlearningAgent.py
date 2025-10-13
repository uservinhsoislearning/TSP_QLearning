import numpy as np
import random
class QAgent:
    def __init__ ( self , n , alpha =0.1 , gamma =0.9 , epsilon =1.0 , decay =0.995,
min_epsilon =0.01):
        self.n = n # Number of cities
        self.alpha = alpha # Learning rate
        self.gamma = gamma # Discount factor
        self.epsilon = epsilon # Initial exploration rate
        self.decay = decay # Decay factor for epsilon
        self.min_epsilon = min_epsilon # Minimum allowed epsilon
        self.q_table = np.zeros(( n , n )) # Q- table : each entry Q(i,j)

    def select_action(self, state, unvisited):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(unvisited) # Explore: random action
        else:
            q_values = [self.q_table[state][a] for a in unvisited]
            max_q = max(q_values)

            max_actions = [a for a in unvisited if self.q_table[state][a] == max_q]
            return random.choice(max_actions) # Exploit: best action based on Q- values, randomize if there are ties
    
    def update_q_value(self, state, action, reward, next_state, unvisited):
        if unvisited:
            max_future_q = max([self.q_table[next_state][a] for a in unvisited])
        else :
            max_future_q = 0 # Terminal state : no future actions

            self.q_table[state,action] += self.alpha*(reward + self.gamma*max_future_q - self.q_table[state ,
            action]) # UPdate Q-value using Bellman equation

    def decay_epsilon(self) :
        self.epsilon = max(self.min_epsilon , self.epsilon * self.decay)

def train_agent(agent:QAgent, distance_matrix:list[list[float]], epoches=1000):
    for epoch in range(epoches):
        state = random.randint(0, len(distance_matrix) - 1) # Start from a random city
        unvisited = list(range(1, len(distance_matrix))) # All cities except the starting city
        path = [state] # Start path with the first city
        total_reward = 0

        while unvisited:
            action = agent.select_action(state, unvisited)
            reward = -distance_matrix[state][action] # Negative distance as reward
            next_state = action
            unvisited.remove(action)

            agent.update_q_value(state, action, reward, next_state, unvisited)
            state = next_state
            path.append(state)
            total_reward += reward

        # Return to the starting city
        reward = -distance_matrix[state][0]
        agent.update_q_value(state, 0, reward, 0, [])
        total_reward += reward

        agent.decay_epsilon()
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Total Reward: {total_reward}, Epsilon: {agent.epsilon}")
        
    return agent

def getSolution(agent, start_city=0):
    state = start_city
    unvisited = list(range(len(agent.q_table)))
    unvisited.remove(start_city)
    path = [start_city+1]  # Store cities in 1-based indexing   
    
    while unvisited:
        action = agent.select_action(state, unvisited)
        path.append(action+1)
        unvisited.remove(action)
        state = action
    
    path.append(-1)  # Return to starting city
    return path