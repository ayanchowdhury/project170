# Put your solution here.
import networkx as nx
import random
import collections
from collections import Counter

def solve(client):
    client.end()
    client.start()

    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    num_students= len(all_students)
    #list of vertices that were reported as having a guavabot
    yes_reported =[]
    test_dict = {}

    #list of vertices that were not reported as having a guavabot
    no_reported = []
    test_dict_no = {}

    #Send one student to each vertex and add vertex to yes_reported for each vertex with positive report
    for nonhome_vertex in non_home:
        truth_counter = 0
        false_counter = 0
        gbot_boolean_dict = client.scout(nonhome_vertex, all_students)
        #get num reported true and num reported false
        for student_report in gbot_boolean_dict.values():
            if student_report == True:
                truth_counter += 1
            else:
                false_counter += 1
        if truth_counter > (num_students / 3):
            yes_reported.append(nonhome_vertex)

    #for each vertex in yes_reported find length of shortest path
    for yes_vertex in yes_reported:
        short_path, path_length = nx.single_source_dijkstra(client.G, client.home, yes_vertex)
        test_dict[yes_vertex] = [short_path, path_length]

    #test_dict
    sorted_test = sorted(test_dict.items(), key=lambda vertex: vertex[1][0])
    sorted_test_dict = collections.OrderedDict(sorted_test)

    #remotes all reported bots to home if there are bots
    for vertex_path in sorted_test_dict.values():
        i = len(vertex_path[1]) - 1 
        j = len(vertex_path[1]) - 2
        while j >= 0:
            num_bots = client.remote(vertex_path[1][i], vertex_path[1][j])
            if num_bots == 0:
                break
            i -= 1
            j -= 1
    

    no_reported = [vertex for vertex in non_home if vertex not in yes_reported]

    #for each vertex in no_reported find length of shortest path
    for no_vertex in no_reported:
        short_path, path_length = nx.single_source_dijkstra(client.G, client.home, yes_vertex)
        test_dict_no[yes_vertex] = [short_path, path_length]
    sorted_test_no = sorted(test_dict_no.items(), key=lambda vertex: vertex[1][0])
    sorted_test_dict_no = collections.OrderedDict(sorted_test)

    #remotes all reported bots to home if there are bots
    for vertex_path in sorted_test_dict_no.values():
        i = len(vertex_path[1]) - 1 
        j = len(vertex_path[1]) - 2
        while j > 0:
            num_bots = client.remote(vertex_path[1][i], vertex_path[1][j])
            if num_bots == 0:
                break
            i -= 1
            j -= 1
    client.end()
