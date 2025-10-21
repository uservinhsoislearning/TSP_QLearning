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
    # print(f"matrix = {matrix}")
    # distance_mat = pd.DataFrame(matrix)
    # distance_mat.to_csv("distance_sample.csv")
    
    # Initialize Q-learning agent
    agent = ql.QAgent(
        n=len(cities),
        alpha=0.08,
        gamma=0.9,
        epsilon=1.0, 
        decay=1,
        min_epsilon=0.005
    )

    # Train the agent
    num_epochs = 5000
    trained_agent = ql.train_agent(agent, matrix, epoches=num_epochs)
    solution_path = ql.getSolution(trained_agent)
    print(f"Solution Path: {solution_path}, Length: {s.calculateTourLength(solution_path, matrix)}")

if __name__ == "__main__":
    main()