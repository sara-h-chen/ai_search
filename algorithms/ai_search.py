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


######################################################################
#                         MAIN METHOD                                #
######################################################################

if __name__ == '__main__':
    fileName = sys.argv[1:]
    dir_path = os.path.dirname(os.path.dirname(__file__))
    dir = os.path.join(dir_path + 'input/' + str(fileName[0]))
    queue = read_file(dir)
    citiesNo = next_number(queue)
    matrix = [[0 for x in range(citiesNo)] for y in range(citiesNo)]
    populate_matrix(citiesNo, queue, matrix)
    for i in range(0, len(matrix[0])):
        print(matrix[i])