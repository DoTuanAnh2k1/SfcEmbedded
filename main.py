from pulp import *

prob = LpProblem(name="The mapping Problem",sense=LpMinimize)

#rrns = Request Resource Node Sfc
rrns = 2

#arnp = Available Resource Node Phy
arnp = 10

#rrcs =  Request Resource Connect Sfc
rrcs = 2

#arcp = Available Resource Connect Phy 
arcp = 10

#cost
c = 2

Ns, Nv, Es, Ev = 3, 2, 6, 1
Es_id = [12, 13, 21, 23, 31, 32]
Ev_id = [12]

ids = {
  "x": [[1,1], [1,2], [1,3],
        [2,1], [2,2], [2,3]],
  "y": [[1,2,1,2],[1,2,1,3],
        [1,2,2,1],[1,2,2,3],
        [1,2,3,1],[1,2,3,2]]
}

# Initialize the decision variables: x and y are binaries
x = LpVariable.dicts(name="x", indices=[(v+1, i+1) 
                    for v in range(Nv) for i in range(Ns)], cat='Binary')
y = LpVariable.dicts(name="y", indices=[(Ev_id[ev], Es_id[es]) 
                    for ev in range(Ev) for es in range(Es)], cat='Binary')

#Problem
prob += (x[1, 1] + x[1, 2] + x[1, 3] + x[2, 1] + x[2, 2] + x[2, 3]) * c, "Total cost:"

#Constain
#Constain C1
'''
prob += (x[1, 1] + x[2, 1]) * rrns <= arnp, "C1_1"
prob += (x[1, 2] + x[2, 2]) * rrns <= arnp, "C1_2"
prob += (x[1, 3] + x[2, 3]) * rrns <= arnp, "C1_3"
'''

for i in range(1, Ns+1):
    prob += (lpSum(x[v, i] for v in range(1, Nv+1)) * rrns <= arnp, f"C1_{i}")


#Constain C2
'''
prob += y[12,12] * rrcs <= arcp, "C2_1"
prob += y[12,23] * rrcs <= arcp, "C2_2"
prob += y[12,13] * rrcs <= arcp, "C2_3"
'''

for es in [12, 23, 13]:
    prob += y[12, es] * rrcs <= arcp, f"C2_{es}"

#Constain C3
'''
prob += x[1, 1] + x[2, 1] <= 1, "C3_1"
prob += x[1, 2] + x[2, 2] <= 1, "C3_2"
prob += x[1, 3] + x[2, 3] <= 1, "C3_3"
'''

for i in range(1, 4):
    prob += (x[1, i] + x[2, i]) <= 1, f"C3_{i}"


#Constain C4
'''
prob += x[1, 1] + x[1, 2] + x[1, 3] == 1, "C4_1"
prob += x[2, 1] + x[2, 2] + x[2, 3] == 1, "C4_2"
'''

for i in range(Ns):
    prob += lpSum([x[v + 1, i + 1] for v in range(Nv)]) == 1, f"C4_{i + 1}"

#Constain C5
'''
prob += y[12,12] + y[12,13] - y[12,21] - y[12,31] - x[1,1] + x[2,1] == 0, "C5_1"
prob += y[12,21] + y[12,23] - y[12,12] - y[12,32] - x[1,2] + x[2,2] == 0, "C5_2"
prob += y[12,31] + y[12,32] - y[12,13] - y[12,23] - x[1,3] + x[2,3] == 0, "C5_3"
'''
c5_vars = [(12, 12, 13, 21, 31, 1), (12, 21, 23, 12, 32, 2), (12, 31, 32, 13, 23, 3)]
for var in c5_vars:
    prob += y[var[0], var[1]] + y[var[0], var[2]] - y[var[0], var[3]] - y[var[0], var[4]] - x[1,var[5]] + x[2,var[5]] == 0, f"C5_{var[5]}"

prob.solve()

prob.writeLP("TheProblem.lp")