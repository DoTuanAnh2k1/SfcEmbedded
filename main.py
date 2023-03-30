import networkx as nx
import matplotlib.pyplot as plt
from pulp import *

#rrns = Request Resource Node Sfc
rrns = 2

#arnp = Available Resource Node Phy
arnp = 10

#rrcs =  Request Resource Connect Sfc
rrcs = 2

#arcp = Available Resource Connect Phy 
arcp = 10

#Cost of node
c = 2

# Define The Problem
prob = LpProblem(name="The mapping Problem", sense=LpMinimize)

# Create Phy Graph
Gp = nx.Graph()

# Number Node of Gp
nGp = 3

# Add Node in Gp
for i in range (1, nGp + 1):
    Gp.add_node(i, weight=arnp, number=i)

# Add edge in Gp
Gp.add_edge(1, 2, weight=arcp)
Gp.add_edge(2, 3, weight=arcp)
Gp.add_edge(3, 1, weight=arcp)

# Number Edge in Gp
nEp = 6

# Posible edge in Gp
Ep_id = [12, 13, 
         21, 23, 
         31, 32]

# Creat Sfc Graph Gs
Gs = nx.DiGraph()

# Number Node of Gs
nGs = 2

# Add Node in Gs
for i in range (1, nGs + 1):
    Gs.add_node(i, weight=rrns, number=i)

# Add Edge in Gs
Gs.add_edge(1, 2, weight=rrcs)

# Posible edge in Gs
Es_id = [12]

# Number Edge in Gp
nEs = 1

# Define phi v in i
x = [[i, j] 
     for i in range(1, nGs + 1) 
     for j in range(1, nGp + 1)]

# Define phi vw in ij
y = [[i, j, k, l] 
     for i in range(1, nGs) 
     for j in range(1, nGs + 1) 
     for k in range(1, nGp + 1) 
     for l in range(1, nGp + 1) if (i,j) != (k,l)]

# Initialize the decision variables: x and y are binaries
x = LpVariable.dicts(name="x", 
                     indices=[(v+1, i+1) 
                    for v in range(nGs) 
                    for i in range(nGp)], 
                     cat='Binary')

y = LpVariable.dicts(name="y", 
                     indices=[(Es_id[es], Ep_id[ep]) 
                    for es in range(nEs) 
                    for ep in range(nEp)], 
                     cat='Binary')

# Problem: Min Cost
prob += lpSum([x[i, j] for i in range(1, nGs + 1) for j in range(1, nGp + 1)]) * c, "Total cost:"

#CONSTAINS
#Constain C1
for i in range(1, nGp + 1):
    prob += (lpSum(x[v, i] for v in range(1, nGs + 1)) * rrns <= arnp, f"C1_{i}")

#Constain C2
for es in [12, 23, 13]:
    prob += y[12, es] * rrcs <= arcp, f"C2_{es}"

#Constain C3
for i in range(1, 4):
    prob += (x[1, i] + x[2, i]) <= 1, f"C3_{i}"

#Constain C4
for i in range(nGp):
    prob += lpSum([x[v + 1, i + 1] for v in range(nGs)]) == 1, f"C4_{i + 1}"

#Constain C5
c5_vars = [(12, 12, 13, 21, 31, 1), (12, 21, 23, 12, 32, 2), (12, 31, 32, 13, 23, 3)]
for var in c5_vars:
    prob += y[var[0], var[1]] + y[var[0], var[2]] - y[var[0], var[3]] - y[var[0], var[4]] - x[1,var[5]] + x[2,var[5]] == 0, f"C5_{var[5]}"

prob.solve()

prob.writeLP("TheProblem.lp")

# Plot 2 Graph
plt.figure(figsize=(10, 5))

plt.subplot(121)
nx.draw(Gp, with_labels=True)

plt.subplot(122)
nx.draw(Gs, with_labels=True)

plt.show()

