# import os

# def main(v: str) -> list[list[int]]:
#     lines = v.strip().split('\n')
#     edges = []
#     verts = set()

#     for line in lines:
#         v1, v2 = line.split(',')
#         verts.add(v1)
#         verts.add(v2)
#         edges.append((v1,v2))

#     verts = sorted(list(verts))

#     n = len(verts)
#     matrix = [[0] * n for _ in range(n)]

#     for v1, v2 in edges:
#         i = verts.index(v1)
#         j = verts.index(v2)
#         matrix[i][j] = 1
#         matrix[j][i] = 1

#     return matrix

# if __name__ == "__main__":

#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     csv_path = os.path.join(current_dir, "task0.csv")

#     with open(csv_path,"r") as file:
#         input_data = file.read()

#     result = main(input_data)

#     for row in result:
#         print(row)
# [0, 1, 1, 0, 0]
# [1, 0, 0, 0, 0]
# [1, 0, 0, 1, 1]
# [0, 0, 1, 0, 0]
# [0, 0, 1, 0, 0]
import os

def main(csv_content: str) -> list[list[int]]:
    # Разбиваем строки и создаем множество вершин
    raw_lines = csv_content.strip().splitlines()
    edges_list = []
    vertices_set = set()

    for line in raw_lines:
        start, end = line.split(',')
        vertices_set.update([start, end])
        edges_list.append((start, end))

    vertices = sorted(vertices_set)
    size = len(vertices)
    
    # Инициализация матрицы смежности нулями
    adjacency = [[0 for _ in range(size)] for _ in range(size)]
    
    # Заполняем единицы по ребрам
    for start, end in edges_list:
        i = vertices.index(start)
        j = vertices.index(end)
        adjacency[i][j] = 1
        adjacency[j][i] = 1

    return adjacency


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "task0.csv")

    with open(file_path, "r") as f:
        data = f.read()

    adj_matrix = main(data)

    for line in adj_matrix:
        print(line)

