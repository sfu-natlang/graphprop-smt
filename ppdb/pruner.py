

class Pruner:

    #def __init__(self, oovs_file, graph_type):
    #    global graph
    #    with open(graph_file) as inp:
    #        for line in inp:
    #            parts = line.strip().split()
    #            node1= parts[0]
    #            node2= parts[1]
    #            weight= parts[2]
    #            if node1 in graph:
    #                graph[node1].append((node2,weight))  
    #            else:
    #                graph[node1] = [(node2,weight)]           

    #def sort_by_weight(self):

    def prune(self, graph, labeled_node_list, oov_list, output_graph_type, neighbour_prunning_method, neighbour_prunning_input):
        oovs=oov_list
        new_graph={}
#        with open(oovs_file) as inp:
#            for oov in inp:
#                oovs.append(oov.strip())
#                # TODO change to code
        if output_graph_type == "bipartite":
            for node1 in graph.keys():
                print node1
                if node1 in oovs:
                    #print node1
                    list= graph[node1]
                    if neighbour_prunning_method == "knn":
                        list.sort(key=lambda x: x[1],reverse=True)
                        list = list[:neighbour_prunning_input]

                    for (node2,w) in list:
                        if neighbour_prunning_method == "radius":
                            if w <= neighbour_prunning_input:
                                continue
                        new_graph[node1] = []
                        if node2 in labeled_node_list and node2 not in oovs:
                            new_graph[node1].append((node2,w))
                            if node2 in new_graph:
                                new_graph[node2].append((node1,w))
                            else:
                                new_graph[node2]=[(node1,w)]

        elif output_graph_type == "tripartite":
            for node1 in graph.keys():
                if node1 in oovs:
                    list= graph[node1]
                    if neighbour_prunning_method == "knn":
                        list.sort(key=lambda x: x[1],reverse=True)
                        list = list[:neighbour_prunning_input]

                    for (node2,w) in list:
                        if neighbour_prunning_method == "radius":
                            if w <= neighbour_prunning_input:
                                continue
                        new_graph[node1] = []
                        if node2 in labeled_node_list:
                            new_graph[node1].append((node2,w))
                            if node2 in new_graph:
                                new_graph[node2].append((node1,w))
                            else:
                                new_graph[node2]=[(node1,w)]
                        else:
                            not_connected = True
                            for (node,w2) in graph[node2]:
                                if node in labeled_node_list:
                                    not_connected = False
                                    if node2 in new_graph:
                                        new_graph[node2].append((node,w2))
                                    else:
                                        new_graph[node2]=[(node,w2)]

                                    if node in new_graph:
                                        new_graph[node].append((node2,w2))
                                    else:
                                        new_graph[node]=[(node2,w2)]
                            if not_connected == False:
                                new_graph[node1].append((node2,w))
                                if node2 in newgraph:
                                    new_graph[node2].append((node1,w))
                                else:
                                    new_graph[node2]=[(node1,w)]
        #TODO remove connections between labeled nodes
        #TODO other types
        return new_graph
