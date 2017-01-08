import parser
import os

def length_tour(tour, dist_matrix):
    # Calculate the length of a tour
    length = 0
    for k in range(1, len(tour)):
        length = length + dist_matrix[tour[k-1]][tour[k]]
        print(length)
    length = length + dist_matrix[tour[-1]][tour[0]]
    return length  

if __name__ == '__main__':
    in_dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'input_test'))
    out_dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'output'))
    inputFiles = parser.get_input_files('input_test')
    for file in inputFiles:
        input_url = os.path.join(in_dir_path, file)
        output_url = os.path.join(out_dir_path, "file" + file)
        queue = parser.read_file(input_url)
        citiesNo = parser.next_number(queue)
        matrix = [[0 for x in range(citiesNo)] for y in range(citiesNo)]
        parser.populate_matrix(citiesNo, queue, matrix)
        tour = [2, 3, 7, 5, 4, 1, 8, 9, 11, 10, 6, 0]
        length = length_tour(tour, matrix)
        if sorted(tour) != list(range(len(tour))):
            print(sorted(tour))
            raise Exception("Misformed tour")
        print(input_url)
        print(tour)
        print(length)
        break
