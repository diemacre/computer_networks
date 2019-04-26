# coding: utf-8

'''
@title: CS542 Link State Routing Simulator
@author: Diego Martin Crespo
@id: A20432558
@section: 02
@seat: 36
@date: Spring 2019

To run the program simply 'python project.py' in the terminal

Then commands from 1 to 6 are available:
  (1) Input a Network Topology
  (2) Create a Forward Table
  (3) Paths from Source to Destination (4) Update Network Topology
  (5) Best Router for Broadcast
  (6) Exit
  
A command is refered to: type the number in the terminal and press enter key from the keyboard
'''

'''
Import the necesary libraries
'''

from collections import defaultdict
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def makeGraph(matrix):
    '''
    This method converts the panda datagrame matrix into a graph of networkx

    Params:
      matrix.......pandas dataframe

    Returns:
      G.......graph from networkx
    '''
    G = nx.Graph()
    n = matrix.shape[0]
    names = []
    for i in range(1, n+1):
        names.append(i)

    for i, row in matrix.iterrows():
        for j in range(len(row)):
            if row[j] > 0:
                G.add_edge(names[i], names[j], weight=row[j])
    pos = nx.spring_layout(G)
    nx.draw(G, pos)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    plt.axis('off')
    plt.show()

    return G


def makeMatrix(G):
    '''
    This method converts a networkx graph into a pandas dataframe

    Params:
      G.......graph from networkx

    Returns:
      matrixd.......panda dataframe

    '''
    nodes = list(G.nodes)
    edges = G.edges()
    matrix = []
    for i in nodes:
        row = []
        for j in nodes:
            if i == j:
                row.append(0)
            elif [i, j] not in edges and [j, i] not in edges:
                row.append(-1)
            else:
                row.append(edges[i, j]['weight'])
        matrix.append(row)
    names = []
    for i in nodes:
        names.append('R'+str(i))
    matrixd = pd.DataFrame(matrix, columns=names, index=names)
    return matrixd


def makeFordwardTable(G, source):
    '''
    This method makes the forward table for a given source and graph. It uses the djkstra algorithm
    to assign the interfaces to each destination from the source router.

    Params:
      G.......graph from networkx
      source.......node from graph

    Returns:
      table.......arraylist

    '''
    table = []
    nodes = list(G.nodes)

    for node in nodes:
        if source == node:
            table.append([node, '-'])
        else:
            hop = dijkstra(G, source, node)[0]
            table.append([node, hop[1]])

    table.sort(key=lambda x: x[0])
    return table


def dijkstra(graph, start, goal):
    '''
    This method implements the dijkstra algorithm for a given graph from the start node to
    the goal node

    Params:
      graph.......graph from networkx
      start.......node from graph
      goal.......node from graph

    Returns:
      path.......arraylist containing the nodes of the shortest path
      shortest_distance.......acumulative cost of the weights from the shortest path  
    '''
    nodes = set(graph.nodes)
    unseenNodes = defaultdict(dict)
    edges = graph.edges()

    # we change the format of the network graph to a dictionary of dictionaries for better handling
    for node in nodes:
        for neigh in graph.neighbors(node):
            if node < neigh and [node, neigh] in edges:
                unseenNodes[node][neigh] = edges[node, neigh]['weight']
                unseenNodes[neigh][node] = edges[node, neigh]['weight']
            if node > neigh and [neigh, node] in edges:
                unseenNodes[node][neigh] = edges[neigh, node]['weight']
                unseenNodes[neigh][node] = edges[neigh, node]['weight']
    # iticiaze the variables
    infinity = 1000*max(nx.get_edge_attributes(graph, 'weight').values())
    graph = unseenNodes
    shortest_distance = {}
    predecessor = {}
    path = []
    # set al node to infinity value
    for node in unseenNodes:
        shortest_distance[node] = infinity
    # initialize start node distance
    shortest_distance[start] = 0
    # begin the loop for searching the shortest path and its cost
    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node

        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + \
                    shortest_distance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)

    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
        except:
            print('Path not reachable')
            break
    path.insert(0, start)
    if shortest_distance[goal] != infinity:
        return(path, shortest_distance[goal])


def find_all_paths(graph, start, end, path=[]):
    '''
    This method finds all paths from an start node to an end from a graph. It is a recursive method

    Params:
      graph.......graph from networkx
      start.......node from graph
      end.......node from graph
      path.......actual path arraylist

    Returns:
      paths......arraylist shorted by their costcontaining the list of possible paths 
      along with their respective cost
    '''

    edges = graph.edges()
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                cost = 0
                if node == end:
                    for i in range(len(newpath)-1):
                        if [newpath[i], newpath[i+1]] in edges:
                            cost += edges[newpath[i], newpath[i+1]]['weight']
                        elif [newpath[i+1], newpath[i]] in edges:
                            cost += edges[newpath[i+1], newpath[i]]['weight']

                    paths.append([newpath, cost])
                else:
                    paths.append(newpath)

    return sorted(paths, key=lambda x: x[1])


def addRouter(G, connections, weights):
    '''
    This method adds a new node to the actual graph

    Params:
      G.......graph from networkx
      connections.......string with the nodes to connect the new node
      weigths.......string with the weights of the connections

    Returns:
      G......graph with the new connections
    '''
    nodes = list(G.nodes)
    newnode = nodes[-1] + 1
    cn = connections.split(',')  # c1,c2,c3...cn
    cn = [int(i) for i in cn]
    ws = weights.split(',')  # w1,w2,w3...wn
    ws = [int(i) for i in ws]

    if len(cn) == len(ws):
        for i in range(len(cn)):
            if cn[i] in G.nodes:
                G.add_edge(cn[i], newnode, weight=ws[i])
            else:
                print('connection not in Graph nodes')
                return  # causes an error to input again
    else:
        print('number of connections not equal to the number of weights')
        return  # causes an error to input again
    return G


def delRouter(G, node):
    '''
    This method deletes a node from the graph

    Params:
      G......graph from networkx
      node.......node from graph to be deleted

    Returns:
      G......graph with the updated connections
    '''
    if node in G.nodes:
        G.remove_node(node)
    return G


def find_all_shortest(graph):
    '''
    This method dfinds the best router for broadcasting. It computes dijsktra algorthims for each
    node to the others and calculates the total cost for those paths

    Params:
      graph......graph from networkx

    Returns:
      cost......dictionary ordered by cost containing the total cost (sum of all cost of paths) for
      each node to the others.
    '''
    nodes = list(graph.nodes)
    cost = {}
    for node1 in nodes:
        cost[node1] = 0
        for node2 in nodes:
            cost[node1] += dijkstra(graph, node1, node2)[1]
    return sorted(cost.items(), key=lambda x: x[1])


def menu():
    '''
    This is the menu funtion. It is called every time a command is done to rememer 
    the user the possible options

    Params:
      None

    Returns:
      print the possible commands of the program 

    '''
    print("\nCS542 Link State Routing Simulator\n")
    print("(1) Input a Network Topology")
    print("(2) Create a Forward Table")
    print("(3) Paths from Source to Destination")
    print("(4) Update Network Topology")
    print("(5) Best Router for Broadcast")
    print("(6) Exit")


def main():
    '''
    This is the main function that contains the logic for the diferent commands. It starts by calling the menu 
    function
    '''
    menu()
    global matrix
    global G
    global source
    global destination

    '''
  Runtime loop of the program
  '''

    while (True):
        '''
        It ask for the input command every time in the while loop
        '''
        command = input("\nCommand: ")

        if command == '1':
            '''
            If command == 1 the terminal ask the user to enter the file path with the matrix. This file should
            be in the folder ./data/.
            It sets the source node to 1 by default and the destination node to '' for next commands an runtime
            of the program. If the path is correct a graph and a matrix are created calling their respective methods.
            Then the matrix is printed. And the menu appears again
            If a wrong file is entered an exception occurs and it ask again for the file path.
            '''
            try:
                source = 1
                destination = ''
                fil = input('\nEnter the name of file in folder ./data: ')
                filename = './data/' + fil
                print(filename)
                matrix = pd.read_csv(filename, header=None, sep=r'\s+')
                print(matrix)
                G = makeGraph(matrix)
                print('\nReview Topology Matrix\n',)
                matrix = makeMatrix(G)
                print(matrix)
                menu()
            except:
                print('\nWrong file path entered!\n')

        elif command == '2':
            '''
            If command == 2 ask to enter the source node. It checks if the graph has less than two nodes and if that
            source is in the graph. If it is correct it creates the fordward table for that source node calling the
            method makeForwartable and it is printed.

            If the node is not in the graph os a wrong input is entered an exception occurs and the menu appears again.
            '''
            try:
                source = int(input('\nInput the source route number: '))
                if len(list(G.nodes)) < 2:
                    print(
                        '\n Add nodes to topology with command: 4, number of nodes equal to 1 or less!')
                elif source in list(G.nodes):
                    table = makeFordwardTable(G, source)
                    print('\nRouter', source, 'Connection Table')
                    print('\nDestination     Interface\n')
                    print('===========================')
                    for [u, v] in table:
                        print('   ', u, '            ', v)
                else:
                    print('\nSource node not in Graph!')
                menu()
            except:
                print('\nWrong format router entered!\n')
                menu()
        elif command == '3':
            '''
            if command == 3 it ask for the input of the destination node/router. 

            If the destination is the same as the source. It is printed with cost=0 and telling 
            the destination == source.
            If the destination and source are in graph nodes it finds allpaths and also it calculates the djistra
            algorithm from source to destination to get the shortest path and its cost. Then the menu is shown again.

            If there is a wrong input an exception occurs and the menu is shown again.
            '''
            try:
                destination = int(
                    input('\nInput de destination router number: '))
                if destination == source:
                    print('\nSource = Destination=', destination)
                    print('Cost= 0')
                elif source not in list(G.nodes):
                    print('\nSource removed, please add a new source with command: 2')
                elif destination in list(G.nodes):
                    allpaths = find_all_paths(G, source, destination, path=[])
                    m = pd.DataFrame(allpaths, columns=['Path', 'Cost'])
                    print(m)
                    shortestpath, cost = dijkstra(G, source, destination)
                    print('\nShortest distance is ' + str(cost))
                    print('And the path is ' + str(shortestpath))
                else:
                    print('\nDestination node not in Graph!')
                menu()
            except:
                print('\nWrong input!')
                menu()
        elif command == '4':
            '''
            If command == 4 it ask for a new input. If the input== 1 goes to option 1 and if it is 2 it goes
            to option 2.
            '''
            try:
                option = input('\nEnter: 1 to add || 2 to delete: ')
                if option == '1':
                    '''
                    Option 1 is choosed to add a new router to the network. It asks first for the nodes to connect the new
                    node in the form "Connection of new router to routers 1 and 2. Format of input: 1,2". Then it ask for
                    enter the input of the corresponding weight to the connections in the form : "Weights from new router
                    to routers 1 and 2 are 5 and 6. Format of input: 5,6"

                    It is called the funtion addrouter. If the parameters do not have the correct form an exception occurs.
                    If it is correct the graph is updated and the new matrix is printed.

                    If the destination has been previously set. the updated forward tabkle is shoewn along with the possible
                    new shortest path with its cost.

                    Finally the menu is shown again

                    If there is a wrong input an exception occurs and the menu is shown again.
                    '''
                    try:
                        print(
                            '\nConnection of new router to routers 1 and 2. Format of input: 1,2')
                        contoothers = input('\nEnter the connections: ')
                        print(
                            '\nWeights from new router to routers 1 and 2 are 5 and 6. Format of input: 5,6')
                        weights = input('\nEnter Weights: ')
                        G = addRouter(G, contoothers, weights)
                        matrix = makeMatrix(G)
                        print(matrix)
                        if destination != '':
                            table = makeFordwardTable(G, source)
                            print('\nRouter', source, 'Connection Table')
                            print('\nDestination     Interface\n')
                            print('===========================')
                            for [u, v] in table:
                                print('   ', u, '            ', v)
                            shortestpath, cost = dijkstra(
                                G, source, destination)
                            print('\nShortest distance is ' + str(cost))
                            print('And the path is ' + str(shortestpath))
                        menu()
                    except:
                        print('\nWrong input format entered!')

                elif option == '2':
                    '''
                    Option 2 is choosed to delete a router from the network. The input ask for the number of node to delete.
                    The delRouter funtion is called and if the node is in the graph it is deleted. Then the matrix is printed.

                    If the source or destination are deleted it is printed the warning. And if the destination exist the shortest
                    path and cost it is printed

                    It is called the funtion addrouter. If the parameters do not have the correct form an exception occurs.
                    If it is correct the graph is updated and the new matrix is printed.

                    If there is a wrong input an exception occurs and the menu is shown again. 
                    '''
                    try:
                        dele = int(
                            input('\nEnter the number of the router to delete: '))
                        G = delRouter(G, dele)
                        matrix = makeMatrix(G)
                        print(matrix)
                        if dele == destination:
                            print('\nDestination deleted')
                        elif dele == source:
                            print('\nSource deleted!')
                        elif destination != '':
                            shortestpath, cost = dijkstra(
                                G, source, destination)
                            print('\nShortest distance is ' + str(cost))
                            print('And the path is ' + str(shortestpath))
                        menu()
                    except:
                        print('\nWrong input!')

            except:
                print('\nWrong option entered!')
        elif command == '5':
            '''
            If command == 5 the funtion find_all_shortest is called to get the best router for broadcasting.
            Which will be the first element of the returned dictionary as it is returned in order by cost.

            If there is an error an exception occurs.
            '''
            try:
                router, cost = find_all_shortest(G)[0]
                print('\nThe router with shortest path to other routers is: ', router)
                print('The sum of cost to other routers of router',
                      router, 'is:', cost)
                menu()
            except:
                print('\n Something when wrong')
        elif command == "6":
            '''
            If command==6 the program ends.
            '''
            print("\nExit CS542 2019 Spring project. GoodBye!\n")
            break
        else:
            print("\nWrong command!")
            menu()


if __name__ == '__main__':
    main()
