import QlearningAgent as ql
import IOReader as io
import sumOfTour as s
import pandas as pd 
def main():
    cities = io.readInputFile("input.txt")
    matrix = io.calculateDistanceMatrix(cities)
    # Get sample distance for verification
    city1 = cities[1]
    city2 = cities[2]
    print(f"Sample cities: {city1}, {city2}")
    print(f"matrix = {matrix}")
    distance = io.calculateDistance(city1, city2)
    # distance_mat = pd.DataFrame(matrix)
    # distance_mat.to_csv("distance_sample.csv", index=False)
    # Initialize Q-learning agent
    agent = ql.QAgent(
        n=len(cities),
        alpha=0.1,
        gamma=0.99,
        epsilon=1.0, # fixed parameter
        decay=0.997,
        min_epsilon=0.005
    )
    print(f"Initial Q-table:\n{agent.q_table}")
    # Train the agent
    num_epochs = 1000
    trained_agent = ql.train_agent(agent, matrix, epoches=num_epochs)
    solution_path = ql.getSolution(trained_agent)
    print(f"Solution Path: {solution_path}, Length: {s.calculateTourLength(solution_path, matrix)}")

if __name__ == "__main__":
    main()