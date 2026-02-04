import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.artists = []
        self.dict_artists = {}
        self.path = []
        self.path_edges = []
        self.sol_best = 0

    def build_graph(self, role: str):
        self.G.clear()
        self.artists = DAO.read_artisti(role)
        for artist in self.artists:
            self.dict_artists[artist.artist_id] = artist
        for artist in self.artists:
            self.G.add_node(artist)
        for artist1 in self.artists:
            for artist2 in self.artists:
                if artist1 != artist2:
                    if artist1.num_objects > artist2.num_objects:
                        u = artist2
                        v = artist1
                    else:
                        u = artist1
                        v = artist2
                    peso = abs(u.num_objects - v.num_objects)
                    if peso != 0:
                        self.G.add_edge(u, v, weight=peso)



    def classifica(self):
        result = []
        for n in self.G.nodes():
            delta = self.G.out_degree(n) - self.G.in_degree(n)
            result.append((n.name, delta))
        final = sorted(result, key=lambda x: x[1])
        return final

    def get_role(self):
        return DAO.get_authorship()

    def compute_path(self, valore, artista):
        self.path = []
        self.path_edges = []
        self.sol_best = 0

        partial = [artista]

        self._ricorsione(partial, [], valore)

    def _ricorsione(self, partial, partial_edges, valore):
        n_last = partial[-1]

        neigh = self.get_admissible_neigh(n_last,partial_edges, partial)
        if len(partial) == valore:
            weigh_path = self.compute_weight_path(partial_edges)
            if weigh_path > self.sol_best:
                self.sol_best = weigh_path
                self.path_edges = partial_edges[:]
                self.path = partial[:]
        for n in neigh:
            if len(partial) > 1:
                partial.append(n)
                partial_edges.append((n_last, n, self.G.get_edge_data(n_last, n)['weight']))
                self._ricorsione(partial, partial_edges, valore)
                partial.pop()
                partial_edges.pop()

    def compute_weight_path(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]
        return weight



    def get_admissible_neigh(self, n_last, partial_edges, partial):
        all_neigh = self.G.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if e[2]['weight'] > partial_edges[-1][2]:
                if e[1] not in partial:
                    result.append(e[1])
        return result
