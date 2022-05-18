import sys

"MAGIC_VARIABLES:"
ERROR_MSG = "something has gone wrong! please check the input of your files :)"
DIRECTIONS = {"u", "d", "r", "l", "w", "x", "y", "z"}


def read_wordlist(filename):
    """
    This func is capable to extract the data from a file.
    :param filename: a file that holds data canonising the program
    :return: list of the data from the file.
    """
    word_list = []
    with open(filename, "r") as x:
        for line in x.readlines():
            temp_line = line.replace("\n", "")
            word_list.append(temp_line)
    return word_list


def read_matrix(filename):
    """
    This function is capable to extract the data from a file.
    :param filename: a file that holds data canonising the program
    :return: 2D list of the data from the file.
        """
    Two_d_list = []
    with open(filename, "r") as file:
        for line in file.readlines():
            clean_line = line.replace("\n", "")
            temp_line = clean_line.split(",")
            Two_d_list.append(temp_line)
    return Two_d_list


def find_words(word_list, matrix, directions):
    """
    This function contains the actual structure for the game.
    :param word_list: list of word to look for.
    :param matrix: a 2D list of the matrix (board) of the game.
    :param directions: a string of directions regarding where we are supposed
    to look at the metrix.
    :return: a list of tuples that contains all the results.
    """
    words_in_matrix_dict = dict()
    word_set = set(word_list)
    for dir in directions:
        current_list_of_words = indicator(dir, matrix)
        for word in current_list_of_words:
            if word in word_set:
                if word in words_in_matrix_dict:
                    words_in_matrix_dict[word] += 1
                else:
                    words_in_matrix_dict[word] = 1

    list_of_results = [(key, words_in_matrix_dict[key]) for key in
                       words_in_matrix_dict.keys()]
    return list_of_results


def valid_input(directions):
    """
    This function is checking if the input from the directions file is
    valid for the program.
    :param directions: a string from the directions file.
    :return: False if the input isn't valid else a list of the
    directions without repetition.
    """
    complete_list_of_directions = set()
    for dir in directions:
        if dir not in DIRECTIONS:
            return False
        else:
            if dir not in complete_list_of_directions:
                complete_list_of_directions.add(dir)
    return list(complete_list_of_directions)


def add_one_in_dir(last, dir):
    """
    This func is aid function that helps the recursive to work and get
    all the values.
    :param last: the point which we have lest been.
    :param dir: the current directions.
    :return: coordinates of the next position.
    """
    if dir == "u":
        return last[0] - 1, last[1]
    elif dir == "d":
        return last[0] + 1, last[1]
    elif dir == "l":
        return last[0], last[1] - 1
    elif dir == "r":
        return last[0], last[1] + 1
    elif dir == "w":
        return last[0] - 1, last[1] + 1
    elif dir == "x":
        return last[0] - 1, last[1] - 1
    elif dir == "y":
        return last[0] + 1, last[1] + 1
    else:
        return last[0] + 1, last[1] - 1


def recursion_in_matrix(path, matrix, dir):
    """
    This func is the recursive engine that is going over the matrix
    in all the combinations in the desired direction.
    :param path: the current directions.
    :param matrix: a 2D list of the matrix (board) of the game.
    :param dir: the direction of the path.
    :return: a list of all the combinations in the desired direction.
    """
    row_length = len(matrix)
    col_length = len(matrix[0])

    last = path[-1]
    new_coord = add_one_in_dir(last, dir)

    if (new_coord[0] >= row_length or new_coord[0] < 0 or new_coord[
        1] >= col_length
            or new_coord[1] < 0):
        return []

    new_path = path + [new_coord]
    word = ""
    for coord in new_path:
        word += matrix[coord[0]][coord[1]]

    return [word] + recursion_in_matrix(new_path, matrix, dir)


def indicator(directions, matrix):
    """
    this function in assembling the full list of all the combinations
    in a direction.
    :param directions: the direction in which we are looking at.
    :param matrix:  a 2D list of the matrix (board) of the game.
    :return: returns the final list of all the combinations.
    """
    row_length = len(matrix)
    col_length = len(matrix[0])
    list_of_words = []
    for dir in directions:
        for i in range(row_length):
            for j in range(col_length):
                list_of_words.append(matrix[i][j])
                list_of_words += recursion_in_matrix([(i, j)], matrix, dir)

    return list_of_words


def write_output(results, filename):
    """
    This function is writing in to a file all the results that was founded
    in the matrix.
    :param results: a list of tuples in which the first value is the name and
    the letter are the amount of times it was funded.
    :param filename: the name of the file in which we are writing to.
    :return: None
    """
    with open(filename, "w") as result_file:
        for result in results:
            result_file.write(f"{result[0]},{result[1]}\n")
    return


def main(word_file_path, matrix_file_path, put_file_path, directions):
    """
    this function is the "MAIN" function that combines all the functions
    in the program to work together for the game.
    :param word_file_path: the file that contains the words.
    :param matrix_file_path: the file that contains the matrix.
    :param put_file_path: the file the name of the file we are going to give
    back the results to.
    :param directions: a string that contains the directions of the checking.
    :return: a reattended file of the results in the required way.
    """
    word_file = read_wordlist(word_file_path)
    matrix_file = read_matrix(matrix_file_path)
    good_directions = valid_input(directions)
    if not good_directions:
        print(ERROR_MSG)
        return

    if not word_file or not matrix_file or not good_directions:
        return write_output([], put_file_path)

    res_list = find_words(word_file, matrix_file, good_directions)
    return write_output(res_list, put_file_path)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print(ERROR_MSG)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# python3 wordsearch.py word_list.txt mat.txt output_file_test.txt directions
