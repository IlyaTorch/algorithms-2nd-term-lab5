import random
import numpy as np

from typing import List, Tuple

MATRIX_SIZE: int = 10
MAX_VALUE: int = 10


def generate_matrix_of_weights(matrix_size: int) -> List[List[int]]:
    matrix: List[List[int]] = np.array([
        np.array([
            0 for __ in range(matrix_size)
        ])
        for _ in range(matrix_size)
    ])
    for i in range(matrix_size):
        for j in range(matrix_size):
            if i == j:
                continue
            if i > j:
                matrix[i][j] = matrix[j][i]
            else:
                matrix[i][j] = random.randint(1, MAX_VALUE)

    return matrix


def generate_transposition(vertices: List[int]) -> List[int]:
    transposion: List[int] = random.sample(vertices, len(vertices))
    return transposion


def calculate_transposition_weight(transposition: List[int], weights: List[List[int]]) -> int:
    weight: int = 0

    for index in range(len(transposition) - 1):
        current_vertex_index: int = transposition[index]
        next_vertex_index: int = transposition[index + 1]
        weight += weights[current_vertex_index][next_vertex_index]
    weight += weights[transposition[-1]][transposition[0]]

    return weight


def _swap_positions_in_list(elements: List[int], position_1: int, position_2: int):
    elements_copy = elements.copy()
    elements_copy[position_1], elements_copy[position_2] = elements_copy[position_2], elements_copy[position_1]
    return elements_copy


def find_transposition_neighborhood(transposion: List[int]) -> List[List[int]]:
    neighborhood: List[List[int]] = []
    for i in range(len(transposion) - 2):
        for j in range(i + 2, len(transposion)):
            new_transposition = _swap_positions_in_list(transposion, i, j)
            neighborhood.append(new_transposition)
    return neighborhood


def find_cheapest_way(weights_matrix: List[List[int]]) -> Tuple[int, List[int]]:
    print("weights:")
    print(weights_matrix)

    vertices = [_ for _ in range(MATRIX_SIZE)]
    cheapest_transposition: List[int] = generate_transposition(vertices)
    min_weight: int = calculate_transposition_weight(cheapest_transposition, weights_matrix)
    cheapest_transposition_found: bool

    print("initial transposition: ", cheapest_transposition)
    print("weight of initial transposition: ", min_weight)

    while True:
        print("===========================")
        print("transition:", cheapest_transposition)
        print("weight:", min_weight)
        cheapest_transposition_found = True
        neighborhood: List[List[int]] = find_transposition_neighborhood(cheapest_transposition)

        print("neighborhood:")

        for neighborhood_transposition in neighborhood:
            neighborhood_transposition_weight = calculate_transposition_weight(
                neighborhood_transposition, weights_matrix
            )

            print("transposition: ", neighborhood_transposition)
            print("weight: ", neighborhood_transposition_weight)

            if neighborhood_transposition_weight < min_weight:
                min_weight = neighborhood_transposition_weight
                cheapest_transposition = neighborhood_transposition
                cheapest_transposition_found = False
        if cheapest_transposition_found:
            break

    return min_weight, cheapest_transposition


if __name__ == '__main__':
    input_matrix = generate_matrix_of_weights(MATRIX_SIZE)
    min_transposition_weight, min_transposition = find_cheapest_way(input_matrix)
    print("==================")
    print("min weight: ", min_transposition_weight)
    print("transposition with min weight: ", min_transposition)
