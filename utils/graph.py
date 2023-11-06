class Edge():
    """The Edge class, simply composed of two vertices and a weight to go from one to the other.
    """
    def __init__(self, vertex_1: str, vertex_2: str, weight: int):
        self.weight = weight
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2


class Graph():
    """The Graph class, composed of edges, helps to deal with graph operations.
    """
    def __init__(self):
        self._edges = []
        self._vertices = set()

    def _add_undirected_edge(self, vertex_1: str, vertex_2: str, weight: int) -> None:
        """Function that adds an undirected edge to the graph, also adds new vertices.

        Args:
            vertex_1 (str): The name of the first vertex.
            vertex_2 (str): The name of the second vertex.
            weight (int): The cost of going from one to the other.
        """
        already_existing = False
        for edge in self._edges:
            if (vertex_1, vertex_2) == (edge.vertex_1, edge.vertex_2):
                already_existing = True
        if not already_existing:
            # Add new vertices
            self._vertices.add(vertex_1)
            self._vertices.add(vertex_2)
            # Add edge in both directions
            self._edges.append(Edge(vertex_1, vertex_2, weight))
            self._edges.append(Edge(vertex_2, vertex_1, weight))
        else:
            print(f'Undirected edge {vertex_1}<->{vertex_2}={weight} already exists')


    def process_routes_dict(self, routes_dict: dict[tuple[str, str], int]) -> None:
        """This function takes a dictionnary of the routes extracted from the universe.db
        and creates the complete universe graph from it.
        Args:
            routes_dict (dict[tuple[str, str], int]): The dictionnary of the routes extracted from
            the universe.db using the load_db_data utils function.
        """
        for route, cost in routes_dict.items():
            self._add_undirected_edge(*route, cost)


    @property
    def vertices(self) -> set[str]:
        """Getter for the vertices of the graph, decorated as a property for easy access.
        Returns:
            set[str]: A set of the names of all verices in the graph.
        """
        return self._vertices
    

    def get_neighbors(self, vertex: str) -> list[tuple[str, int]]:
        """Returns all the neigbors of the given vertex.

        Args:
            vertex (str): The name of the vertex for which we want the neighbors.

        Returns:
            list[tuple[str, int]]: A list of tuples composed of the name of the neighboring vertex and the weight that links them
        """
        neighbors = []
        for edge in self._edges:
            if edge.vertex_1 == vertex:
                neighbors.append((edge.vertex_2, edge.weight))
        return neighbors


    def __str__(self) -> str:
        """Override of the print function.

        Returns:
            str: A formatted string to display the graph.
        """
        edges = ''
        for edge in self._edges:
            edges += f'        {edge.vertex_1}->{edge.vertex_2}={edge.weight}\n'

        return f'    Vertices: {self._vertices}\n    Edges:\n{edges}'