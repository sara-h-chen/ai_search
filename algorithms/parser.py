import re, queue
import sys, os

######################################################################
#                 PRE-PROCESS DATA GIVEN IN TOUR                     #
######################################################################


def read_file(filename):
    file = open(filename)

    # takes name from the file
    firstline = file.readline()
    NAME = firstline[7:-2]

    # strips non-numerical characters
    info = file.read()
    parsedfile = re.sub(r'[^\d,]', '', info)
    q = queue.Queue()
    # removes empty strings
    [q.put(v) for v in list(filter(None, parsedfile.split(",")))]

    # check contents of queue
    # for elem in list(q.queue):
    #     print(elem)

    return q


def next_number(queue):
    return int(queue.get())


def populate_matrix(citiesNo, queue, matrix):
    for i in range(0, citiesNo - 1):
        for j in range(1, citiesNo - i):
            next = next_number(queue)
            matrix[i][j + i] = next
            matrix[j + i][i] = next


def get_current_node(row, col, matx):
    return matx[row][col]


def get_input_files():
    # GETS THE FOLDER WITH ALL INPUT FILES
    dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'input'))

    # LISTS ALL THE FILES IN THE FOLDER
    allFiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    return allFiles


######################################################################
#                         MAIN METHOD                                #
######################################################################

# UNCOMMENT ONLY WHEN TESTING
# if __name__ == '__main__':
#     dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'input'))
#     inputFiles = get_input_files()
#
#     for file in inputFiles:
#         dir = os.path.join(dir_path, file)
#         queue = read_file(dir)
#         citiesNo = next_number(queue)
#         matrix = [[0 for x in range(citiesNo)] for y in range(citiesNo)]
#         populate_matrix(citiesNo, queue, matrix)
#         for i in range(0, len(matrix[0])):
#             print(matrix[i])