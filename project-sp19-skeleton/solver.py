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
    yes_reported_length = {}
    yes_reported_path = []

    #list of vertices that were not reported as having a guavabot
    no_reported = []
    no_reported_length = {}
    no_reported_path = []

    #student counter
    student_counter = 0

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
            student_counter += 1
        if student_counter > len(all_students) - 1:
            student_counter = 0

    #for each vertex in yes_reported find length of shortest path
    for yes_vertex in yes_reported:
        len_of_shortest_path = nx.dijkstra_path_length(client.G, client.home, yes_vertex)
        yes_reported_length[yes_vertex] = len_of_shortest_path
    #sort yes_reported_length by shortest path to longest path
    sorted_yes_reported = sorted(yes_reported_length.items(), key=lambda vertex: vertex[1])
    sorted_dict_paths_of_vertex = collections.OrderedDict(sorted_yes_reported)

    #find shortest path for each vertex in already sorted order
    for sorted_vertex in sorted_dict_paths_of_vertex:
        shortest_path_for_vertex = nx.dijkstra_path(client.G, client.home, sorted_vertex)
        yes_reported_path.append(shortest_path_for_vertex)

    #remotes all reported bots to home if there are bots
    for vertex_path in yes_reported_path:
        i = len(vertex_path) - 1 
        j = len(vertex_path) - 2
        while j >= 0:
            num_bots = client.remote(vertex_path[i], vertex_path[j])
            if num_bots == 0:
                break
            i -= 1
            j -= 1
    

    no_reported = [vertex for vertex in non_home if vertex not in yes_reported]

    #for each vertex in no_reported find length of shortest path
    for no_vertex in no_reported:
        len_of_shortest_path = nx.dijkstra_path_length(client.G, client.home, no_vertex)
        no_reported_length[no_vertex] = len_of_shortest_path
    #sort no_reported_length by shortest path to longest path
    sorted_no_reported = sorted(no_reported_length.items(), key=lambda vertex: vertex[1])
    sorted_dict_paths_of_vertex_no = collections.OrderedDict(sorted_no_reported)

    #find shortest path for each vertex in already sorted order
    for sorted_vertex in sorted_dict_paths_of_vertex_no:
        shortest_path_for_vertex = nx.dijkstra_path(client.G, client.home, sorted_vertex)
        no_reported_path.append(shortest_path_for_vertex)

    #remotes all reported bots to home if there are bots
    for vertex_path in no_reported_path:
        i = len(vertex_path) - 1 
        j = len(vertex_path) - 2
        while j > 0:
            num_bots = client.remote(vertex_path[i], vertex_path[j])
            i -= 1
            j -= 1
    client.end()
