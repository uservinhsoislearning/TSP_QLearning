import IOReader as io
def readTour(filename):
    cities = []
    start_reading = False
    with open(filename, 'r') as file:
        for line in file:
            if line == "TOUR_SECTION\n":
                start_reading = True
                continue

            if line == "EOF":
                break

            if start_reading and line:
                cities.append(int(line.strip()))
    return cities
def calculateTourLength(tour, distance_matrix):
    total_length = 0
    for i in range(len(tour) - 1):
        total_length += distance_matrix[tour[i] - 1][tour[i + 1] - 1]
    # Add distance to return to the starting city
    total_length += distance_matrix[tour[-2] - 1][0]
    return total_length
def main():
    cities = io.readInputFile("input.txt")
    distance_matrix = io.calculateDistanceMatrix(cities)
    tour = readTour("input.txt")
    tour_length = calculateTourLength(tour, distance_matrix)
    print(f"Tour: {tour}")
    print(f"Tour Length: {tour_length}")
    # This is just for verification purpose (min tour length should be 11292)
if __name__ == "__main__":
    main()