import QlearningAgent as ql
import IOReader as io
def main():
    cities = io.readInputFile("input.txt")
    matrix = io.calculateDistanceMatrix(cities)
    # Get sample distance for verification
    city1 = cities[1]
    city2 = cities[2]
    print(f"Sample cities: {city1}, {city2}")
    distance = io.calculateDistance(city1, city2)
    print(f"Distance between city 1 and city 2: {distance}")
    # Initialize Q-learning agent
    agent = ql.QAgent(
        n=len(cities),
        alpha=0.1,
        gamma=0.99,
        epsilon=1.0, # fixed parameter
        decay=0.995,
        min_epsilon=0.005
    )
    print(f"Initial Q-table:\n{agent.q_table}")
    # Train the agent
    num_epochs = 2000
    trained_agent = ql.train_agent(agent, matrix, epoches=num_epochs)
    print(f"FInal Q-table:\n{agent.q_table}")
    solution_path = ql.getSolution(trained_agent)
    print(f"Solution Path: {solution_path}")

if __name__ == "__main__":
    main()