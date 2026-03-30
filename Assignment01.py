import tkinter as tk
import time
import random
from queue import Queue
from heapq import heappush, heappop

GRID_SIZE = 12
CELL_SIZE = 40
DELAY = 0.05

class AIPathfinder:
    def __init__(self, root, algo_choice):
        self.root = root
        self.algo_choice = algo_choice
        
        self.canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
        self.canvas.pack()
        self.snode = (1, 1)
        self.tnode = (GRID_SIZE-2, GRID_SIZE-2)
        
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.dMaze()
        
        self.dGrid()
        self.root.after(1000, self.runAlgo)

    def dMaze(self):
        for i in range(3, 9):
            self.grid[i][5] = 1

    def dGrid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                color = "black" if self.grid[r][c] == 1 else "white"
                self.dCell(r, c, color)
        self.dCell(self.snode[0], self.snode[1], "green", "S")
        self.dCell(self.tnode[0], self.tnode[1], "blue", "T")

    def dCell(self, r, c, color, label=""):
        x1, y1 = c * CELL_SIZE, r * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        if label:
            self.canvas.create_text(x1+20, y1+20, text=label, fill="white")

    def get_neighbors(self, r, c):
        order = [
            (-1, 0),  # Up
            (0, 1),   # Right
            (1, 0),   # Bottom
            (1, 1),   # Bottom-Right
            (0, -1),  # Left
            (-1, -1)  # Top-Left
        ]
        valid = []
        for dr, dc in order:
            nr, nc = r + dr, c + dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                if self.grid[nr][nc] == 0:
                    valid.append((nr, nc))
        return valid

    def markVisited(self, node, color="lightgray"):
        if node != self.snode and node != self.tnode:
            self.dCell(node[0], node[1], color)
            self.root.update()
            time.sleep(DELAY)

    def finalPath(self, parents, end):
        curr = end
        while curr in parents and parents[curr] is not None:
            curr = parents[curr]
            if curr != self.snode:
                self.dCell(curr[0], curr[1], "red")
                self.root.update()
                time.sleep(DELAY)

    def runAlgo(self):
        if self.algo_choice == "1": self.bfs()
        elif self.algo_choice == "2": self.dfs()
        elif self.algo_choice == "3": self.ucs()
        elif self.algo_choice == "4": self.dls(10)
        elif self.algo_choice == "5": self.iddfs()
        elif self.algo_choice == "6": self.bidirectional()

    def bfs(self):
        visited = {self.snode: None}
        q = Queue()
        q.put(self.snode)
        
        while not q.empty():
            current = q.get()
            if current == self.tnode:
                return self.finalPath(visited, current)
            
            self.markVisited(current, "yellow")
            
            for neighbor in self.get_neighbors(*current):
                if neighbor not in visited:
                    visited[neighbor] = current
                    q.put(neighbor)
                    self.markVisited(neighbor, "cyan")

    def dfs(self):
        stack = [self.snode]
        visited = {self.snode: None}
        
        while stack:
            current = stack.pop()
            if current == self.tnode:
                return self.finalPath(visited, current)
            
            self.markVisited(current, "yellow")
            
            for neighbor in reversed(self.get_neighbors(*current)):
                if neighbor not in visited:
                    visited[neighbor] = current
                    stack.append(neighbor)
                    self.markVisited(neighbor, "cyan")

    def ucs(self):
        pq = [(0, self.snode)]
        visited = {self.snode: None}
        costs = {self.snode: 0}
        
        while pq:
            cost, current = heappop(pq)
            if current == self.tnode:
                return self.finalPath(visited, current)
            
            self.markVisited(current, "yellow")
            
            for neighbor in self.get_neighbors(*current):
                new_cost = cost + 1
                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    visited[neighbor] = current
                    heappush(pq, (new_cost, neighbor))
                    self.markVisited(neighbor, "cyan")

    def dls(self, limit):
        stack = [(self.snode, 0)]
        visited = {self.snode: None}
        
        while stack:
            current, depth = stack.pop()
            if current == self.tnode:
                self.finalPath(visited, current)
                return True
            
            if depth < limit:
                self.markVisited(current, "yellow")
                for neighbor in reversed(self.get_neighbors(*current)):
                    if neighbor not in visited:
                        visited[neighbor] = current
                        stack.append((neighbor, depth + 1))
                        self.markVisited(neighbor, "cyan")
        return False

    def iddfs(self):
        for depth_limit in range(GRID_SIZE * GRID_SIZE):
            self.dGrid() 
            if self.dls(depth_limit):
                break

    def bidirectional(self):
        f_q, b_q = [self.snode], [self.tnode]
        f_visited, b_visited = {self.snode: None}, {self.tnode: None}
        
        while f_q and b_q:
            # Forward
            curr_f = f_q.pop(0)
            self.markVisited(curr_f, "yellow")
            for n in self.get_neighbors(*curr_f):
                if n in b_visited:
                    f_visited[n] = curr_f
                    self.finalPath(f_visited, n)
                    self.finalPath(b_visited, n)
                    return
                if n not in f_visited:
                    f_visited[n] = curr_f
                    f_q.append(n)
            
            # Backward
            curr_b = b_q.pop(0)
            self.markVisited(curr_b, "orange")
            for n in self.get_neighbors(*curr_b):
                if n in f_visited:
                    b_visited[n] = curr_b
                    self.finalPath(f_visited, n)
                    self.finalPath(b_visited, n)
                    return
                if n not in b_visited:
                    b_visited[n] = curr_b
                    b_q.append(n)

if __name__ == "__main__":
    print("AI Search Algorithms:")
    print("1: BFS, 2: DFS, 3: UCS, 4: DLS, 5: IDDFS, 6: Bidirectional")
    choice = input("Select (1-6): ")
    
    app_root = tk.Tk()
    app = AIPathfinder(app_root, choice)
    app_root.mainloop()