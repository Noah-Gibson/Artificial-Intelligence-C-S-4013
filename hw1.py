# Problem: Implement the Breadth-First Search (BFS), Depth-First Search (DFS) 
# and Greedy Best-First Search (GBFS) algorithms on the graph from Figure 1 in hw1.pdf.


# Instructions:
# 1. Represent the graph from Figure 1 in any format (e.g. adjacency matrix, adjacency list).
# 2. Each function should take in the starting node as a string. Assume the search is being performed on
#    the graph from Figure 1.
#    It should return a list of all node labels (strings) that were expanded in the order they where expanded.
#    If there is a tie for which node is expanded next, expand the one that comes first in the alphabet.
# 3. You should only modify the graph representation and the function body below where indicated.
# 4. Do not modify the function signature or provided test cases. You may add helper functions. 
# 5. Upload the completed homework to Gradescope, it must be named 'hw1.py'.

# Examples:
#     The test cases below call each search function on node 'S' and node 'A'
# -----------------------------
import pandas as pd
import heapq

adjacency_matrix = {
    "A": [0, 4, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    "B": [4, 0, 2, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    "C": [-1, 2, 0, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, 3],
    "D": [-1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1, -1, -1, 2],
    "E": [1, -1, -1, -1, 0, 3, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1],
    "F": [-1, 2, -1, -1, 3, 0, -1, -1, -1, 6, 4, -1, -1, -1, -1, -1, -1],
    "G": [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, 4, 4, -1, 10, -1],
    "H": [-1, -1, 4, -1, -1, -1, -1, 0, -1, -1, 3, 7, -1, -1, -1, -1, -1],
    "I": [-1, -1, -1, -1, 6, -1, -1, -1, 0, 1, -1, -1, 5, -1, -1, -1, -1],
    "J": [-1, -1, -1, -1, -1, 6, -1, -1, 1, 0, 3, -1, -1, 3, -1, -1, -1],
    "K": [-1, -1, -1, -1, -1, 4, -1, 3, -1, 3, 0, 9, -1, -1, 3, -1, -1],
    "L": [-1, -1, -1, 8, -1, -1, -1, 7, -1, -1, 9, 0, -1, -1, -1, 10, -1],
    "M": [-1, -1, -1, -1, -1, -1, 4, -1, 5, -1, -1, -1, 0, -1, -1, -1, -1],
    "N": [-1, -1, -1, -1, -1, -1, 4, -1, -1, 3, -1, -1, -1, 0, 2, -1, -1],
    "P": [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, 2, 0, -1, -1],
    "Q": [-1, -1, -1, -1, -1, -1, 10, -1, -1, -1, -1, 10, -1, -1, -1, 0, -1],
    "S": [-1, -1, 3, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0]
}


df = pd.DataFrame(adjacency_matrix, index=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "P", "Q", "S"])

heuristics = {
    "A": 10,
    "B": 9,
    "C": 16,
    "D": 21,
    "E": 13,
    "F": 9,
    "G": 0,
    "H": 12,
    "I": 9,
    "J": 5,
    "K": 8,
    "L": 18,
    "M": 3,
    "N": 4,
    "P": 6,
    "Q": 9,
    "S": 17
}

#print(df.loc["I", "M"])
#print(df.iloc[5, 9])
visited = []

def BFS(start: str) -> list:
    # START: Your code here
    queue = [start]
    visited = [start]

    while len(queue) > 0:
        current = queue.pop(0)
        if current not in visited:
            visited.append(current)
    
        for column, i in df[current].items():
            if i > 0 and column not in visited:
                if column == "G":
                    visited.append(column)
                    return visited
                queue.append(column)
    return []
    # END: Your code here


def DFS(start: str) -> list:
    # START: Your code here
    if "G" in visited:
        visited.clear()

    if start not in visited:
        visited.append(start)

    for column, i in df[start].items():
        if i > 0 and column not in visited:
            if column == "G":
                visited.append(column)
                return visited
            result = DFS(column)
            if result:
                return result

    return []
    # END: Your code here

visited = []

def GBFS(start: str) -> list:
    global visited
    visited.clear()
    min_heap = []
    heapq.heappush(min_heap, (heuristics[start], start))

    while min_heap:
        _, current = heapq.heappop(min_heap)

        if current == "G":
            visited.append(current)
            return visited

        if current not in visited:
            visited.append(current)

            for column, i in df[current].items():
                if i > 0 and column not in visited:
                    heapq.heappush(min_heap, (heuristics[column], column))

    return visited
    # END: Your code here



# test cases - DO NOT MODIFY THESE
def run_tests():
    # Test case 1: BFS starting from node 'A'
    assert BFS('A') == ['A', 'B', 'E', 'C', 'F', 'I', 'H', 'S', 'J', 'K', 'M', 'G'], "Test case 1 failed"
    
    # Test case 2: BFS starting from node 'S'
    assert BFS('S') == ['S', 'C', 'D', 'B', 'H', 'L', 'A', 'F', 'K', 'Q', 'G'], "Test case 2 failed"

    # Test case 3: DFS starting from node 'A'
    assert DFS('A') == ['A', 'B', 'C', 'H', 'K', 'F', 'E', 'I', 'J', 'N', 'G'], "Test case 3 failed"
    
    # Test case 4: DFS starting from node 'S'
    assert DFS('S') == ['S', 'C', 'B', 'A', 'E', 'F', 'J', 'I', 'M', 'G'], "Test case 4 failed"

    # Test case 5: GBFS starting from node 'A'
    assert GBFS('A') == ['A', 'B', 'F', 'J', 'N', 'G'], "Test case 5 failed"
    
    # Test case 6: GBFS starting from node 'S'
    assert GBFS('S') == ['S', 'C', 'B', 'F', 'J', 'N', 'G'], "Test case 6 failed"

    
    
    print("All test cases passed!")

if __name__ == '__main__':
    run_tests()