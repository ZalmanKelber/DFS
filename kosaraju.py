#input_data = [[1, 10],[1, 1],[2, 11],[2, 13],[3, 5],[5, 9],[5, 2],[6, 1],[6, 12],[7, 1],[8, 11],[8, 2],[9, 3],[9, 2],[9, 4],[10, 6],[10, 3],[10, 5],[11, 13],[12, 1],[13, 8]]

f = open("EdgesInput.txt", "r")
input_data = []
for line in f:
    string_entries = line.split()
    row = [int(n) for n in string_entries]
    input_data.append(row)


#find number of nodes
num_nodes = input_data[-1][0]

print("found num_nodes")

#create table (index 0 unused so that index corresponds to node, first column is a boolean that turns to true once it's been found by DFS, 
#second column is found order, third column is list of outnodes)
nodes = []
for i in range(num_nodes + 1):
    nodes.append([False, 0, []])
for i in range(len(input_data)):
    index = input_data[i][0]
    nodes[index][2].append(input_data[i][1])

print("created first table")

#create reverse table
reverse_nodes = []
for i in range(num_nodes + 1):
    reverse_nodes.append([False, 0, []])
for i in range(len(input_data)):
    index = input_data[i][1]
    reverse_nodes[index][2].append(input_data[i][0])

print("created second table")

#delete earlier items to save memory
del input_data

#recursive operation for DFS
def search_node (graph, num, counter):
    for i in range(len(graph[num][2])):
        next_node = graph[num][2][i]
        if not graph[next_node][0]:
            graph[next_node][0] = True
            counter = search_node(graph, next_node, counter)
    graph[num][1] = counter
    return counter + 1

#use DFS to find the found-numbers of the nodes in the reverse graph
found_counter = 1
for i in range(1, num_nodes + 1):
    if not reverse_nodes[i][0]:
        reverse_nodes[i][0] = True
        found_counter = search_node(reverse_nodes, i, found_counter)

print("executed first DFS")

#use found orders to create key list
found_values = [0]
for i in range(1, num_nodes + 1):
    found_values.append(reverse_nodes[i][1])
key_list = [None] * (num_nodes + 1)
for i in range(1, num_nodes + 1):
    order = num_nodes + 1 - found_values[i]
    key_list[order] = i

del reverse_nodes

#use key and DFS to search nodes in the original graph and record the leaders in a list
#leaders will be formatted so that each entry is a sublist of length two, containing the number of the 
#leading node and its size
leaders = []
found_counter = 1
for i in range(1, num_nodes + 1):
    k = key_list[i]
    #searches node graph for SCC
    if not nodes[k][0]:
        nodes[k][0] = True
        found_counter = search_node(nodes, k, found_counter)

        #adds leading node and SCC size to leaders
        leaders.append([k, found_counter - 1])

print("executed second DFS")

#adjust leaders so that second entries are the right size
for i in range(1, len(leaders)):
    leaders[len(leaders) - i][1] -= leaders[len(leaders) - i - 1][1]

print(leaders)
