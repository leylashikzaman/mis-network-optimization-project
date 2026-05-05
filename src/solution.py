import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os

# ── Load Data ──────────────────────────────────────────────────────────────────
# We load the network data from a CSV file. Each row represents a directional
# connection (edge) between two network devices, along with a vulnerability score.
df = pd.read_csv("data/network_data.csv")

# ── Build the Graph ────────────────────────────────────────────────────────────
# The graph was created using NetworkX. Nodes represent network devices and
# security boundaries in a corporate IT environment (e.g. firewalls, servers,
# laptops). Edges represent logical connections between these devices.
# The vulnerability_score on each edge represents how easy that specific
# connection is to exploit — a lower score means the link is easier to compromise.
# The shortest path algorithm will calculate the path of least resistance
# from the attacker's entry point to the main database.
G = nx.DiGraph()

for _, row in df.iterrows():
    G.add_edge(row["source"], row["target"], weight=row["vulnerability_score"])

# ── Define Source and Target ───────────────────────────────────────────────────
source_node = "Public Web Server"
target_node = "Main Database"

# ── Solve Using Dijkstra's Shortest Path Algorithm ─────────────────────────────
# Dijkstra's algorithm finds the path with the minimum cumulative vulnerability
# score. This simulates how a rational attacker would move through the network,
# always choosing the easiest connection to exploit next.
path = nx.dijkstra_path(G, source_node, target_node, weight="weight")
path_length = nx.dijkstra_path_length(G, source_node, target_node, weight="weight")

# ── Print Results ──────────────────────────────────────────────────────────────
print("=" * 55)
print("     CYBERSECURITY ATTACK-PATH ANALYSIS")
print("=" * 55)
print(f"\n  Entry Point : {source_node}")
print(f"  Target      : {target_node}")
print(f"\n  Optimal Attack Path:")
for i, node in enumerate(path):
    print(f"    {'→ ' if i > 0 else '  '}{node}")
print(f"\n  Total Vulnerability Score : {path_length}")
print("  (Lower score = path of least resistance)")
print("=" * 55)

# ── Save Results to File ───────────────────────────────────────────────────────
os.makedirs("results", exist_ok=True)
with open("results/solution_output.txt", "w", encoding="utf-8") as f:
    f.write("CYBERSECURITY ATTACK-PATH ANALYSIS\n")
    f.write("=" * 55 + "\n")
    f.write(f"Entry Point : {source_node}\n")
    f.write(f"Target      : {target_node}\n")
    f.write(f"Attack Path : {' → '.join(path)}\n")
    f.write(f"Total Vulnerability Score : {path_length}\n")

# ── Visualize the Network ──────────────────────────────────────────────────────
# Nodes are color coded:
#   Red    = attacker entry point (Public Web Server)
#   Dark   = target (Main Database)
#   Orange = nodes along the optimal attack path
#   Grey   = nodes not involved in the attack path
# Red edges highlight the optimal attack route.
pos = nx.spring_layout(G, seed=42)
path_edges = list(zip(path, path[1:]))

node_colors = []
for node in G.nodes():
    if node == source_node:
        node_colors.append("#e74c3c")
    elif node == target_node:
        node_colors.append("#2c3e50")
    elif node in path:
        node_colors.append("#e67e22")
    else:
        node_colors.append("#95a5a6")

plt.figure(figsize=(16, 10))
plt.title(
    "Cybersecurity Attack-Path Analysis\n"
    "Shortest Path = Path of Least Resistance (Lowest Vulnerability Score)",
    fontsize=13, fontweight="bold"
)

nx.draw_networkx_edges(G, pos, edge_color="lightgrey", arrows=True,
                       arrowsize=20, width=2)
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red",
                       arrows=True, arrowsize=25, width=3)
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=4500)

# Wrap long node labels
import textwrap
wrapped_labels = {node: '\n'.join(textwrap.wrap(node, width=12)) for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=wrapped_labels, font_size=8,
                        font_color="white", font_weight="bold")

edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color="red", linewidth=2, label="Optimal Attack Path"),
    Line2D([0], [0], color="lightgrey", linewidth=2, label="Other Connections"),
    plt.scatter([], [], color="#e74c3c", label="Entry Point", s=100),
    plt.scatter([], [], color="#e67e22", label="Compromised Node", s=100),
    plt.scatter([], [], color="#2c3e50", label="Target (Main Database)", s=100),
    plt.scatter([], [], color="#95a5a6", label="Safe Node", s=100),
]
plt.legend(handles=legend_elements, loc="lower left", fontsize=9)

plt.axis("off")
plt.tight_layout()
plt.savefig("results/network_visualization.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nVisualization saved → results/network_visualization.png")
print("\nVisualization saved → results/network_visualization.png")