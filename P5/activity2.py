from dsa_graph import DSAGraph


def read_adjacency(file_path: str) -> DSAGraph:
    graph = DSAGraph()
    with open(file_path) as file:
        for line_num, line in enumerate(file, 1):
            line = line.rstrip('\n')
            cols = line.split()
            if not 2 <= len(cols) <= 3:
                raise ValueError(
                    f"Invalid syntax on line {line_num}: expected 2 or 3 columns but got {len(cols)}.")
            label1 = cols[0]
            label2 = cols[1]

            # Add vertices, ignore if they already exist.
            try:
                graph.add_vertex(label1)
            except ValueError:
                pass
            try:
                graph.add_vertex(label2)
            except ValueError:
                pass

            graph.add_edge(label1, label2)
    return graph


if __name__ == "__main__":
    graph = read_adjacency("prac6_1.al")
    graph.display_as_list()
