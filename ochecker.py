from collections import defaultdict

class _Graph:

    def __init__(self, debug = False):
        self._debug= debug

        # default dictionary to store graph
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        """Adds an edge to graph"""
        self.graph[u].append(v)

    def _dfs(self, v):
        """recursive function used by DFS"""

        # Mark the current node as visited
        # and print it
        self.visited.add(v)
        if self._debug:
            print(v, end=' ')

        # Recur for all the vertices
        # adjacent to this vertex
        for neighbour in self.graph[v]:
            if neighbour not in self.visited:
                self._dfs(neighbour)

    def traverse(self, v):
        """Does DFS traversal"""

        # Create a set to store visited vertices
        self.visited = set()

        # Call the recursive helper function
        # to print DFS traversal
        self._dfs(v)


class OrphanedChecker(object):

    def __init__(self, graph, translation, head_sha):
        """"""
        self._g = graph
        self._tr = translation
        self._g.traverse(self._tr[head_sha])

    def __call__(self, ocandidate_sha):
        return (self._tr[ocandidate_sha] in self._g.visited)

    @classmethod
    def originate_checker(cls, commits_supplier):
        """"""
        g = _Graph()
        tr = dict([])

        commits, head = commits_supplier()

        for idx, i in enumerate(reversed(commits)):
            tr[i['sha']] = idx
            if idx == 0:
                continue
            for p in i['parents']:
                g.addEdge(idx, tr[p['sha']])

        return cls(g, tr, head)
