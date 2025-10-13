import QlearningAgent as ql
def calculateDistance(city1, city2):
    """
    Calculate the Pseudo-euclidean distance between two cities.

    Parameters:
    city1 (tuple): Coordinates of the first city (x1, y1).
    city2 (tuple): Coordinates of the second city (x2, y2).

    Returns:
    float: Pseudo-euclidean distance between the two cities.
    """
    return round((((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)/10.0)**0.5)
def readInputFile(filename:str)->dict[tuple[int,int]]:
    """
    Read city coordinates from a file.

    Parameters:
    filename (str): The name of the file containing city coordinates.

    Returns:
    list: A list of tuples representing city coordinates.
    """
    cities = {}
    start_reading = False
    with open(filename, 'r') as file:
        for line in file:
            if line == "NODE_COORD_SECTION\n":
                start_reading = True
                continue

            if line in ["EOF\n", "TOUR_SECTION\n"]:
                break

            if start_reading and line:
                i, x, y = map(int, line.strip().split())
                cities[i] = (x, y)
    return cities
def calculateDistanceMatrix(cities:dict[int,tuple[int,int]])->list[list[float]]:
    """
    Calculate the distance matrix for a list of cities.

    Parameters:
    cities (list): A list of tuples representing city coordinates.

    Returns:
    list: A 2D list representing the distance matrix.
    """
    num_cities = len(cities)
    distance_matrix = [[0.0] * num_cities for _ in range(num_cities)]

    for i in range(1, num_cities + 1):
        for j in range(1, num_cities + 1):
            if i != j:
                distance_matrix[i-1][j-1] = calculateDistance(cities[i], cities[j])
            else:
                distance_matrix[i-1][j-1] = 0.0

    return distance_matrix
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

def main():
    cities = readInputFile("input.txt")
    matrix = calculateDistanceMatrix(cities)
    
    # Get sample distance for verification
    city1 = cities[1]
    city2 = cities[2]
    print(f"Sample cities: {city1}, {city2}")
    distance = calculateDistance(city1, city2)
    print(f"Distance between city 1 and city 2: {distance}")
    
    agent = ql.QAgent(n=len(cities))
    trained_agent = ql.train_agent(agent, matrix, epoches=1000)
    solution_path = getSolution(trained_agent)
    print(f"Solution Path: {solution_path}")

if __name__ == "__main__":
    main()