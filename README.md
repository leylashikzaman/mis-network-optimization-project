# Cybersecurity Attack-Path Analysis

## 1. Real-World Problem Context
Modern organizations face constant threats from malicious actors attempting
to breach internal networks. This project models how an attacker might
navigate a corporate IT network — moving from a public-facing entry point
through a series of vulnerable connections — in order to reach the company's
main database. Identifying this path allows security teams to prioritize
which vulnerabilities to patch first.

## 2. Problem Definition
Given a directed network graph representing a corporate IT infrastructure,
where each connection between devices carries a vulnerability score (lower
= easier to exploit), find the optimal attack path from the Public Web
Server to the Main Database using the minimum total vulnerability score.

## 3. Network Model
A directed weighted graph (DiGraph) was constructed using NetworkX.
Nodes represent network devices and security boundaries. Edges represent
logical connections between devices. Edge weights represent vulnerability
scores — a measure of how easy each connection is to compromise.

## 4. Nodes and Edges

**Nodes (6):**
- Public Web Server — internet-facing entry point
- Phishing Email Gateway — mail server vulnerable to phishing attacks
- Employee Laptop — end-user device, susceptible to social engineering
- Internal Firewall — network boundary, partially misconfigured
- Admin Terminal — privileged access device
- Main Database — the attacker's final target

**Edges (9):** See `data/network_data.csv` for the full list.
Each edge includes source, target, and vulnerability_score.

## 5. Selected Algorithm
**Dijkstra's Shortest Path Algorithm**

Dijkstra's algorithm was selected because it efficiently finds the path
with the minimum cumulative weight in a directed weighted graph. In this
context, minimizing total vulnerability score is equivalent to finding
the path of least resistance — the route a rational attacker would take.

## 6. Python Implementation
See `src/solution.py` for the full implementation.
Built using NetworkX for graph modeling and Dijkstra's algorithm.
Matplotlib is used for visualization. Pandas is used to load edge data
from CSV. All code sections are commented to explain the real-world
meaning of each modeling decision.

## 7. Results
- **Optimal Attack Path:** Public Web Server → Phishing Email Gateway → Employee Laptop → Admin Terminal → Main Database
- **Total Vulnerability Score:** 8
- **Visualization:** See `results/network_visualization.png`
- **Full Output:** See `results/solution_output.txt`

## 8. Managerial Interpretation
The analysis reveals that the path of least resistance runs through the
Phishing Email Gateway and Employee Laptop — not through the firewall.
This means the company's biggest security risk is not a technical one
but a human one: employees being tricked via phishing emails. Management
should immediately prioritize cybersecurity awareness training, implement
multi-factor authentication on all employee devices, and increase
monitoring on the Admin Terminal, which sits one step away from the
main database.

## 9. How to Run the Code
```bash
pip install -r requirements.txt
python src/solution.py
```

## 10. References
See `references/references.md`