from render import *
import heapq
from collections import deque
import math


class Controller:
    def __init__(self, render):
        self.render = render
        self.rows = self.render.game_parameter.rows
        self.cols = self.render.game_parameter.cols
        self.map = self.render.game_parameter.map

    def find_positions(self):
        start, goal = None, None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j] == "S":
                    start = (i, j)
                elif self.map[i][j] == "G":
                    goal = (i, j)
        return start, goal

    def heuristic(self, current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        return path[::-1]

    def BFS(self):
        start, goal = self.find_positions()
        if not start or not goal:
            return None

        queue = deque([(start)])
        visited = set([start])
        came_from = {}

        while queue:
            current = queue.popleft()
            if current == goal:
                return self.reconstruct_path(came_from, current)

            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + d[0], current[1] + d[1])
                if (
                    0 <= next_pos[0] < self.rows
                    and 0 <= next_pos[1] < self.cols
                    and next_pos not in visited
                    and self.map[next_pos[0]][next_pos[1]] != "-1"
                ):
                    queue.append(next_pos)
                    visited.add(next_pos)
                    came_from[next_pos] = current

        return None  # No path found

    def DFS(self):
        start, goal = self.find_positions()
        if not start or not goal:
            return None

        stack = [(start)]
        visited = set([start])
        came_from = {}

        while stack:
            current = stack.pop()
            if current == goal:
                return self.reconstruct_path(came_from, current)

            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + d[0], current[1] + d[1])
                if (
                    0 <= next_pos[0] < self.rows
                    and 0 <= next_pos[1] < self.cols
                    and next_pos not in visited
                    and self.map[next_pos[0]][next_pos[1]] != "-1"
                ):
                    stack.append(next_pos)
                    visited.add(next_pos)
                    came_from[next_pos] = current

        return None  # No path found

    def UCS(self, time_limit):
        start, goal = self.find_positions()
        if not start or not goal:
            return None

        pq = [(0, start, time_limit)]  # (cost, position, time_left)
        came_from = {}
        cost_so_far = {(start, time_limit): 0}

        while pq:
            current_cost, current, current_time = heapq.heappop(pq)

            if current == goal and current_time >= 0:
                path = self.reconstruct_path(came_from, (current, current_time))
                return path, current_time

            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + d[0], current[1] + d[1])
                if (
                    0 <= next_pos[0] < self.rows
                    and 0 <= next_pos[1] < self.cols
                    and self.map[next_pos[0]][next_pos[1]] != "-1"
                ):
                    cell_value = self.map[next_pos[0]][next_pos[1]]
                    time_cost = 1  # Default time cost for normal cells

                    if cell_value.isdigit():
                        time_cost += int(cell_value)
                    elif cell_value.startswith("F"):
                        time_cost += int(cell_value[1:])

                    new_time = current_time - time_cost
                    new_cost = current_cost + 1

                    if (
                        next_pos,
                        new_time,
                    ) not in cost_so_far or new_cost < cost_so_far[
                        (next_pos, new_time)
                    ]:
                        cost_so_far[(next_pos, new_time)] = new_cost
                        priority = new_cost
                        heapq.heappush(pq, (priority, next_pos, new_time))
                        came_from[(next_pos, new_time)] = (current, current_time)

        return None  # No path found that meets the constraints

    def GBFS(self):
        start, goal = self.find_positions()
        if not start or not goal:
            return None

        pq = [(self.heuristic(start, goal), start)]
        visited = set()
        came_from = {}

        while pq:
            _, current = heapq.heappop(pq)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            if current in visited:
                continue
            visited.add(current)

            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + d[0], current[1] + d[1])
                if (
                    0 <= next_pos[0] < self.rows
                    and 0 <= next_pos[1] < self.cols
                    and next_pos not in visited
                    and self.map[next_pos[0]][next_pos[1]] != "-1"
                ):
                    heapq.heappush(pq, (self.heuristic(next_pos, goal), next_pos))
                    came_from[next_pos] = current

        return None  # No path found.

    def a_star(self, time_limit, fuel_limit):
        start, goal = self.find_positions()
        if not start or not goal:
            return None

        pq = [
            (0, 0, start, time_limit, fuel_limit)
        ]  # (f_score, g_score, position, time_left, fuel_left)
        visited = set()
        came_from = {}
        g_score = {(start, time_limit, fuel_limit): 0}
        f_score = {(start, time_limit, fuel_limit): self.heuristic(start, goal)}

        while pq:
            _, current_g, current, current_time, current_fuel = heapq.heappop(pq)

            if current == goal:
                path = self.reconstruct_path(
                    came_from, (current, current_time, current_fuel)
                )
                return path, current_time, current_fuel

            state = (current, current_time, current_fuel)
            if state in visited:
                continue
            visited.add(state)

            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_pos = (current[0] + d[0], current[1] + d[1])
                if (
                    0 <= next_pos[0] < self.rows
                    and 0 <= next_pos[1] < self.cols
                    and self.map[next_pos[0]][next_pos[1]] != "-1"
                ):

                    cell_value = self.map[next_pos[0]][next_pos[1]]
                    time_cost = 1  # Default time cost for normal cells
                    fuel_cost = 1  # Default fuel cost for movement

                    if cell_value.isdigit():
                        time_cost += int(
                            cell_value
                        )  # Add additional time cost for numbered cells

                    new_time = current_time - time_cost
                    new_fuel = current_fuel - fuel_cost

                    if cell_value.startswith("F"):
                        new_fuel = fuel_limit  # Refill fuel tank
                        time_cost += int(cell_value[1:])  # Add refuel time

                    if new_fuel < 0 or new_time < 0:
                        continue

                    tentative_g_score = current_g + 1
                    new_state = (next_pos, new_time, new_fuel)

                    if (
                        new_state not in g_score
                        or tentative_g_score < g_score[new_state]
                    ):
                        came_from[new_state] = state
                        g_score[new_state] = tentative_g_score
                        f_score_value = tentative_g_score + self.heuristic(
                            next_pos, goal
                        )
                        f_score[new_state] = f_score_value
                        heapq.heappush(
                            pq,
                            (
                                f_score_value,
                                tentative_g_score,
                                next_pos,
                                new_time,
                                new_fuel,
                            ),
                        )

        return None  # No path found that meets the constraints

    def find_and_draw_path(self, algorithm, level, time_limit, fuel_limit):
        path = []
        time_limit = time_limit if (level > 1) else math.inf
        fuel_limit = fuel_limit if (level > 2) else math.inf

        if algorithm == "BFS":
            result = self.BFS()
        elif algorithm == "DFS":
            result = self.DFS()
        elif algorithm == "UCS":
            result = self.UCS(time_limit)
        elif algorithm == "GBFS":
            result = self.GBFS()
        elif algorithm == "A*":
            result = self.a_star(time_limit, fuel_limit)

        if result:
            if algorithm != "A*":
                if algorithm != "UCS":
                    path = result
                    time_left = time_limit
                    fuel_left = fuel_limit
                else:
                    full_path, time_left = result

                    path = [coord for coord, _ in full_path]
                    time_left = time_left if not math.isnan(time_left) else time_limit
                    fuel_left = fuel_limit
            else:
                full_path, time_left, fuel_left = result

                path = [coord for coord, _, _ in full_path]
                time_left = time_left if not math.isnan(time_left) else time_limit
                fuel_left = fuel_left if not math.isnan(fuel_left) else fuel_limit
            return path, time_left, fuel_left
        else:
            return [], time_limit, fuel_limit
