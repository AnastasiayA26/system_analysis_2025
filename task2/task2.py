import os
import math
from typing import List, Tuple

def entropy_from_mats(rel_mats: List[List[List[int]]]) -> Tuple[float, float]:
    size = len(rel_mats[0])
    layers = len(rel_mats)
    acc = 0.0

    for mat in rel_mats:
        for r in range(size):
            for c in range(size):
                if r != c:
                    p = mat[r][c] / (size - 1)
                    if p > 0:
                        acc += p * math.log2(p)

    H = -acc
    Hmax = (1 / math.e) * size * layers
    hnorm = H / Hmax if Hmax > 0 else 0.0
    return H, hnorm


def edge_replacements(edge_list: List[Tuple[str, str]], nodes: List[str]) -> List[List[Tuple[str, str]]]:
    all_pairs = [(a, b) for a in nodes for b in nodes if a != b]
    current = set(edge_list)
    candidates = [e for e in all_pairs if e not in current]

    out = []
    for pos in range(len(edge_list)):
        for cand in candidates:
            tmp = edge_list.copy()
            tmp[pos] = cand
            out.append(tmp)
    return out


def relations_from_edges(edges: List[Tuple[str, str]], nodes: List[str]) -> List[List[List[int]]]:
    L = len(nodes)
    idx = {n: i for i, n in enumerate(nodes)}

    R1 = [[0] * L for _ in range(L)]
    for a, b in edges:
        R1[idx[a]][idx[b]] = 1

    R2 = [[R1[j][i] for j in range(L)] for i in range(L)]

    closure = [row[:] for row in R1]
    for _ in range(L - 1):
        tmp = [[0] * L for _ in range(L)]
        for i in range(L):
            for j in range(L):
                if closure[i][j]:
                    tmp[i][j] = 1
                else:
                    for k in range(L):
                        if closure[i][k] and R1[k][j]:
                            tmp[i][j] = 1
                            break
        closure = tmp

    R3 = [[int(closure[i][j] and not R1[i][j]) for j in range(L)] for i in range(L)]
    R4 = [[R3[j][i] for j in range(L)] for i in range(L)]

    R2_bool = [[bool(R2[i][j]) for j in range(L)] for i in range(L)]
    R5 = [[0] * L for _ in range(L)]
    for i in range(L):
        for j in range(i + 1, L):
            if any(R2_bool[i][k] and R2_bool[j][k] for k in range(L)):
                R5[i][j] = R5[j][i] = 1

    return [R1, R2, R3, R4, R5]


def solve_block(text: str, anchor: str) -> Tuple[float, float]:
    rows = text.strip().split("\n")
    arcs = []
    nodes = set()

    for row in rows:
        if row.strip():
            a, b = row.split(",")
            a, b = a.strip(), b.strip()
            arcs.append((a, b))
            nodes.add(a)
            nodes.add(b)

    nodes = sorted(v for v in nodes if v != anchor)
    nodes = [anchor] + nodes

    best_H, best_h = -float('inf'), 0.0

    for variant in edge_replacements(arcs, nodes):
        mats = relations_from_edges(variant, nodes)
        H, h = entropy_from_mats(mats)
        if H > best_H:
            best_H, best_h = H, h

    return best_H, best_h


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    fpath = os.path.join(here, "task2.csv")

    with open(fpath, "r") as fh:
        data = fh.read()

    base = input("Введите значение корневой вершины: ").strip()
    H, h = solve_block(data, base)

    print(f"\nРезультат:")
    print(f"H(M,R) = {H:.4f}")
    print(f"h(M,R) = {h:.4f}")
