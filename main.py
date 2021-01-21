from pulp import LpProblem, LpStatus, lpSum, LpVariable, GLPK, LpMinimize, json
import pandas as pd


def main():
    """
    load the file resulted from the naive algorithm. The file loaded contains 3 fields in each line
    The first field is the adjacency matrix of 15 nodes graph in a format of 1 array of 225 cells of zeros and ones.
    The second field contains 1 array of the optimal solution. This array consists of 15 cells of zeros and ones where
     a one at a place i means that node i is in the vertex cover. The third field is an integer indicating the size of
     the optimal vertex cover.
    :return: nothing
    """
    df = pd.read_csv('linkedGraphsWithSolutions2.csv', engine='python')
    # n_nodes is the size of the graph, it can be change to any size
    n_nodes = 15
    model = LpProblem(name="find-minimum-vertex-cover", sense=LpMinimize)
    x = {i: LpVariable(name=f"x{i}", lowBound=0, cat="Binary") for i in range(0, n_nodes)}
    model += lpSum([x.values()])
    file = open("size_of_minimum_vertex_cover_from_linear_programing_algorithm_y", "w")
    count_diffs = 0
    # since df.size includes 3 fields for each line, the number of lines is df.size/3
    num_of_graphs = int(df.size / 3)
    for k in range(num_of_graphs):
        # clear all constraints before adding the constraints for a new graph
        model.constraints.clear()
        # use jason loads to convert the string format of the adjacency matrix to an array
        e = json.loads(df.iloc[k][0])
        #  res contains the size of the minimum vertex cover of the graph which given by the naive algorithm
        res = df.iloc[k][2]
        # for every edge between xi to xj, add a constraint - xi+xj>=1 to the model
        for i in range(0, n_nodes):
            for j in range(0, n_nodes):
                if i < j and e[i * n_nodes + j] == 1:
                    model += (x[i] + x[j] >= 1, "edge " + str(i) + "--" + str(j))
                    print("b", str(i) + str(j))
        #  run the GLPK algorithm
        model.solve(solver=GLPK(msg=True))
        # print the results the GLPK algorithm
        print(f"status: {model.status}, {LpStatus[model.status]}")
        print(f"objective: {model.objective.value()}")
        for var in model.variables():
            print(f"{var.name}: {var.value()}")
        for name, constraint in model.constraints.items():
            print(f"{name}: {constraint.value()}")
        if model.objective.value() != res:
            print("difference at line ", k)
            count_diffs += 1
        file.write(str(model.objective.value()) + "\n")
    print("the total number of differences is: ", count_diffs)
    return 0


if __name__ == '__main__':
    main()
