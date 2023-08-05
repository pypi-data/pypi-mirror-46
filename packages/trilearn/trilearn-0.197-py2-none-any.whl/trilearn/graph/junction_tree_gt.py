import graph_tool.all as gt
import trilearn.graph.junction_tree as jtlib


class JunctionTreeGT(gt.Graph):

    def __init__(self, graph=None, **attr):
        if graph is not None:
            gt.Graph.__init__(self, graph, prune=True)
        else:
            gt.Graph.__init__(self, directed=False)
            # This gives the internal vertex representation for the node.
            self.graph_properties["vert_dict"] = self.new_graph_property("object")
            self.graph_properties["vert_dict"] = {}
            # This gives the node for a given internal vertex representation
            self.vertex_properties["nodes"] = self.new_vertex_property("object")
            #self.edge_properties["separators"] = self.new_edge_property("object")
            #self.edge_properties["log_nus"] = self.new_edge_property("float")
            self.graph_properties["log_nus"] = self.new_graph_property("object")
            self.graph_properties["log_nus"] = {}
            self.graph_properties["separators"] = self.new_graph_property("object")
            self.graph_properties["separators"] = None

    def log_nu(self, sep):
        if sep not in self.gp.log_nus:
            self.gp.log_nus[sep] = jtlib.log_nu(self, sep)
        return self.gp.log_nus[sep]

    def log_n_junction_trees(self, seps):
        lm = 0.0
        for sep in seps:
            lm += self.log_nu(sep)
        return lm

    def order(self):
        return self.num_vertices()

    def size(self):
        return self.num_edges()

    def get_separators(self):
        if self.gp.separators is None:
            self.gp.separators = jtlib.separators(self)
        return self.gp.separators

    def update_node(self, n, new_n):
        vert = self.gp.vert_dict[n]
        self.gp.vert_dict[new_n] = vert
        del self.gp.vert_dict[n]
        self.vp.nodes[vert] = new_n

    def add_node(self, n, **attr):
        v = self.add_vertex()
        self.vp.nodes[v] = n
        self.gp.vert_dict[n] = int(v)

    def add_nodes_from(self, nodes):
        for n in nodes:
            self.add_node(n)

    def remove_node(self, n, **attr):
        """
        Relabel the nodes.
        :param n: the node (typically a frozenset, not the internal integer representation.)
        :param attr:
        :return:
        """
        # Problem that when a graph is copied, the vertices
        # gets invalid.
        self.gp.separators = None
        self.gp.log_nus = {}

        super(JunctionTreeGT, self).remove_vertex(self.gp.vert_dict[n])
        # Re-calculate the vertex dict
        self.gp.vert_dict = {self.vp.nodes[v]: int(v) for v in self.vertices()}

    def remove_nodes_from(self, nodes):
        for node in nodes:
            self.remove_node(node)

    def remove_edge(self, e):
        self.gp.separators = None
        self.gp.log_nus = {}
        # print(self.gp.vert_dict)
        if e[0] in self.gp.vert_dict and e[1] in self.gp.vert_dict:
            edge = self.edge(self.gp.vert_dict[e[0]], self.gp.vert_dict[e[1]])
            super(JunctionTreeGT, self).remove_edge(edge)

    def remove_edges_from(self, ebunch):
        self.gp.separators = None
        self.gp.log_nus = {}

        for e in ebunch:
            self.remove_edge(e)

    def nodes(self):
        for v in super(JunctionTreeGT, self).vertices():
            yield self.vp.nodes[v]

    def add_edge(self, u_of_edge, v_of_edge, label=None, **attr):
        self.gp.separators = None
        self.gp.log_nus = {}

        u = None
        v = None

        assert u_of_edge in self.nodes()
        assert v_of_edge in self.nodes()

        for ver in self.vertices():
            if self.vp.nodes[ver] == u_of_edge:
                u = ver
            elif self.vp.nodes[ver] == v_of_edge:
                v = ver
            if u is not None and v is not None:
                break

        edge = super(JunctionTreeGT, self).add_edge(u, v, **attr)
        #self.ep.separators[edge] = u_of_edge & v_of_edge

    def add_edges_from(self, edge_list, label=None):
        """
        Assume that all the nodes are in the graph.
        """
        self.gp.separators = None
        self.gp.log_nus = {}
        edge_list2 = [(self.gp.vert_dict[e[0]], self.gp.vert_dict[e[1]]) for e in edge_list]
        #super(JunctionTreeGT, self).add_edge_list(edge_list2)
        self.add_edge_list(edge_list2)

    # def add_edge_list(self, edge_list):
    #     self.gp.separators = None
    #     self.gp.log_nus = {}
    #
    #     edge_list2 = [(self.gp.vert_dict[e.source()], self.gp.vert_dict[e.target()]) for e in edge_list]
    #     #for e in edge_list:
    #     #    self.ep.separators[e] = e[0] & e[1]
    #     super(JunctionTreeGT, self).add_edge_list(edge_list2)

    def edges(self):
        for e in super(JunctionTreeGT, self).edges():
            yield (self.vp.nodes[e.source()],
                   self.vp.nodes[e.target()])

    def neighbors(self, n):
        #print(list(self.vertices()))
        #print("negs of " +str(n) + " ("+ str(self.gp.vert_dict[n])+ ")")
        #print(self.gp.vert_dict[n])
        #print(list(self.vertices()))
        for vertex in self.vertex(self.gp.vert_dict[n]).all_neighbors():
            #print(vertex)
            #print(self.vp.nodes[vertex])
            yield self.vp.nodes[vertex]

    def subgraph(self, nodes, prune=True):
        vfilt = self.new_vertex_property('bool')
        for node in nodes:
            vfilt[self.gp.vert_dict[node]] = True
        sub = gt.GraphView(self, vfilt)
        jt = JunctionTreeGT(sub, prune=prune)

        jt.gp.vert_dict = {jt.vp.nodes[v]: int(v) for v in jt.vertices()}
        # TODO: fix the
        # print(jt.gp.vert_dict)

#        if prune:
#            jt.gp. = None
#            jt.gp.log_nus = {}
        return jt

    def connected_components(self, prune=True):
        c = gt.label_components(self)[0]
        for i in range(max(c.a)+1):
            yield JunctionTreeGT(gt.GraphView(self, vfilt=c.a == i), prune=prune)

    def connected_component_vertices(self):
        return [list(t.nodes()) for t in self.connected_components(prune=False)]

    def has_node(self, n):
        pass

    def has_edge(self, n):
        pass

    def copy(self):
        c = JunctionTreeGT(self)
        return c


