from render import *
import heapq
from collections import deque, defaultdict
import math
import random


class Controller:
    def __init__(self, render):
        self.render = render
        self.rows = self.render.game_parameter.rows
        self.cols = self.render.game_parameter.cols
        self.map = self.render.game_parameter.map
        self.agents = self.render.game_parameter.agents
        self.main_agent = self.render.game_parameter.main_agent

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

    # For level 4 only
    def a_star_multi(self, agent, time_windows, time_step_start):
        start = agent.position
        goal = agent.goal
        initial_time = self.render.game_parameter.time_limit
        initial_fuel = self.render.game_parameter.fuel_limit

        pq = [
            (0, 0, start, initial_time, initial_fuel, time_step_start)
        ]  # Added time step
        visited = set()
        came_from = {}
        g_score = {(start, initial_time, initial_fuel, time_step_start): 0}
        f_score = {
            (start, initial_time, initial_fuel, time_step_start): self.heuristic(
                start, goal
            )
        }

        max_iterations = 1000  # Prevent infinite loops
        iterations = 0

        while pq and iterations < max_iterations:
            iterations += 1
            _, current_g, current, current_time, current_fuel, time_step = (
                heapq.heappop(pq)
            )

            if current == goal:
                path = self.reconstruct_path_multi(
                    came_from, (current, current_time, current_fuel, time_step)
                )
                return path, current_time, current_fuel

            state = (current, current_time, current_fuel, time_step)
            if state in visited:
                continue
            visited.add(state)

            for d in [
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
                (0, 0),
            ]:  # Include waiting as an option
                next_pos = (current[0] + d[0], current[1] + d[1])
                next_time_step = time_step + 1

                if self.is_valid_move(next_pos, time_windows, agent.id, next_time_step):
                    cell_value = self.map[next_pos[0]][next_pos[1]]
                    time_cost, fuel_cost = self.calculate_costs(cell_value)

                    new_time = current_time - time_cost
                    new_fuel = current_fuel - fuel_cost

                    if cell_value.startswith("F"):
                        new_fuel = self.render.game_parameter.fuel_limit

                    if new_fuel < 0 or new_time < 0:
                        continue

                    tentative_g_score = current_g + 1
                    new_state = (next_pos, new_time, new_fuel, next_time_step)

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
                                next_time_step,
                            ),
                        )

        return None  # No path found

    def find_alternative_path(
        self, agent, time_windows, conflicting_paths, main_agent_path, time_step_start
    ):
        start = agent.position
        goal = agent.goal
        initial_time = self.render.game_parameter.time_limit
        initial_fuel = self.render.game_parameter.fuel_limit

        pq = [(0, 0, start, initial_time, initial_fuel, time_step_start, [])]
        visited = set()
        came_from = {}
        g_score = {(start, initial_time, initial_fuel, time_step_start): 0}
        f_score = {
            (start, initial_time, initial_fuel, time_step_start): self.heuristic(
                start, goal
            )
        }

        max_iterations = 10000
        iterations = 0

        while pq and iterations < max_iterations:
            iterations += 1
            (
                _,
                current_g,
                current,
                current_time,
                current_fuel,
                time_step,
                current_path,
            ) = heapq.heappop(pq)

            if current == goal or time_step >= len(main_agent_path):
                return (
                    current_path + [current] * (len(main_agent_path) - time_step),
                    current_time,
                    current_fuel,
                )

            state = (current, current_time, current_fuel, time_step)
            if state in visited:
                continue
            visited.add(state)

            # Consider moving in all directions, including staying put and moving backwards
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]:
                next_pos = (current[0] + d[0], current[1] + d[1])
                next_time_step = time_step + 1

                # Check if the move conflicts with the main agent's path
                if (
                    next_time_step < len(main_agent_path)
                    and next_pos == main_agent_path[next_time_step]
                ):
                    continue

                # Check if the move conflicts with any other agent's path
                conflict = False
                for path in conflicting_paths:
                    if len(path) > next_time_step:
                        if next_pos == path[next_time_step] or (
                            current == path[next_time_step]
                            and next_pos == path[next_time_step - 1]
                        ):
                            conflict = True
                            break
                if conflict:
                    continue

                if self.is_valid_move(next_pos, time_windows, agent.id, next_time_step):
                    cell_value = self.map[next_pos[0]][next_pos[1]]
                    time_cost, fuel_cost = self.calculate_costs(cell_value)

                    new_time = current_time - time_cost
                    new_fuel = current_fuel - fuel_cost

                    if cell_value.startswith("F"):
                        new_fuel = self.render.game_parameter.fuel_limit

                    if new_fuel < 0 or new_time < 0:
                        continue

                    tentative_g_score = current_g + 1
                    new_state = (next_pos, new_time, new_fuel, next_time_step)

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
                        new_path = current_path + [current]
                        heapq.heappush(
                            pq,
                            (
                                f_score_value,
                                tentative_g_score,
                                next_pos,
                                new_time,
                                new_fuel,
                                next_time_step,
                                new_path,
                            ),
                        )

        # If no path is found, return a path that stays at the current position
        return [agent.position] * len(main_agent_path), initial_time, initial_fuel

    def is_valid_move(self, pos, time_windows, agent_id, time_step):
        if not (0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols):
            return False
        if self.map[pos[0]][pos[1]] == "-1":
            return False

        # Check if the position is occupied by another agent at the current time step
        if pos in time_windows and time_step in time_windows[pos]:
            if (
                time_windows[pos][time_step] is not None
                and time_windows[pos][time_step] != agent_id
            ):
                return False

        return True

    def calculate_costs(self, cell_value):
        time_cost = 1
        fuel_cost = 1
        if cell_value.isdigit():
            time_cost += int(cell_value)
        if cell_value.startswith("F"):
            time_cost += int(cell_value[1:])
        return time_cost, fuel_cost

    def plan_paths_multi(self):
        time_windows = self.get_current_time_windows()
        paths = {}
        max_path_length = 0

        # Update goals for all agents
        for agent in self.agents:
            self.update_agent_goal(agent)

        # First, find path for the main agent
        main_agent = next(agent for agent in self.agents if agent.id == "S")
        time_step_start = next(
            (
                t
                for t, pos in enumerate(self.main_agent.path)
                if pos == self.main_agent.position
            ),
            0,  # Default to 0 if position not found
        )
        result = self.a_star_multi(main_agent, time_windows, time_step_start)
        if result:
            path, time_left, fuel_left = result
            main_agent.path = path
            main_agent.time_left = time_left
            main_agent.fuel_left = fuel_left
            paths[main_agent.id] = path
            max_path_length = len(path)

            # Update time windows for the main agent
            for t, pos in enumerate(path):
                time_windows[pos][t] = main_agent.id
        else:
            print("No path found for main agent")
            return None, None

        # Then, find initial paths for other agents
        other_agents = [agent for agent in self.agents if agent.id != "S"]
        for agent in other_agents:
            result = self.a_star_multi(agent, time_windows, time_step_start)
            if result:
                path, time_left, fuel_left = result
                full_path = agent.path_all + path
                agent.path = path
                agent.time_left = time_left
                agent.fuel_left = fuel_left
                paths[agent.id] = path
                max_path_length = max(max_path_length, len(path))

                # Update time windows for this agent
                for t, pos in enumerate(full_path):
                    time_windows[pos][t] = agent.id
            else:
                print(f"No initial path found for agent {agent.id}")

        # Resolve conflicts
        self.resolve_conflicts(paths, time_windows, main_agent, other_agents)

        # Assign final paths to agents
        for agent in self.agents:
            if agent.id in paths:
                agent.path = paths[agent.id]
                agent.path_all += paths[agent.id]  # Store the full path
            else:
                print(f"No path found for agent {agent.id}")

        return main_agent.path, main_agent.goal

    def detect_conflicts(self, paths, max_length):
        conflicts = defaultdict(set)
        for t in range(max_length):
            positions = {}
            for agent_id, path in paths.items():
                if t < len(path):
                    pos = path[t]
                    if pos in positions:
                        conflicts[agent_id].add(positions[pos])
                        conflicts[positions[pos]].add(agent_id)
                    positions[pos] = agent_id

                    # Check for swap conflicts and agents passing through each other
                    if t > 0 and t < len(path):
                        prev_pos = path[t - 1]
                        for other_id, other_path in paths.items():
                            if other_id != agent_id and t < len(other_path):
                                # Check for swap conflicts
                                if (
                                    prev_pos == other_path[t]
                                    and pos == other_path[t - 1]
                                ):
                                    conflicts[agent_id].add(other_id)
                                    conflicts[other_id].add(agent_id)

                                # Check for agents passing through each other
                                if t + 1 < len(path) and t + 1 < len(other_path):
                                    if (
                                        pos == other_path[t + 1]
                                        and path[t + 1] == other_path[t]
                                    ):
                                        conflicts[agent_id].add(other_id)
                                        conflicts[other_id].add(agent_id)

        return conflicts

    def resolve_conflicts(self, paths, time_windows, main_agent, other_agents):
        conflict_resolution_attempts = 0
        max_resolution_attempts = 100
        agent_cannot_move = []

        while conflict_resolution_attempts < max_resolution_attempts:
            conflicts = self.detect_conflicts(
                paths, max(len(path) for path in paths.values())
            )
            if not conflicts:
                break

            conflict_resolution_attempts += 1

            for agent_id, conflicting_agents in conflicts.items():
                if agent_id == main_agent.id:
                    continue  # Skip resolving conflicts for the main agent

                agent = next(a for a in other_agents if a.id == agent_id)
                conflicting_paths = [
                    paths[conflicting_agent] for conflicting_agent in conflicting_agents
                ]

                time_step_start = next(
                    (
                        t
                        for t, pos in enumerate(paths[main_agent.id])
                        if pos == main_agent.position
                    ),
                    0,  # Default to 0 if position not found
                )
                result = self.find_alternative_path(
                    agent,
                    time_windows,
                    conflicting_paths,
                    paths[main_agent.id],
                    time_step_start,
                )
                if result:
                    new_path, new_time_left, new_fuel_left = result
                    full_path = agent.path_all + new_path
                    is_conflict, t = self.check_path_conflict(
                        full_path, paths[main_agent.id]
                    )
                if not is_conflict:
                    agent.path = new_path
                    paths[agent.id] = full_path

                    # Update time windows for this agent
                    for t, pos in enumerate(full_path):
                        time_windows[pos][t] = agent.id
                else:
                    agent_cannot_move.append(agent)

        if conflict_resolution_attempts == max_resolution_attempts:
            print(
                "Warning: Maximum conflict resolution attempts reached. Some conflicts may remain."
            )
            agent.path = [agent.position] * len(paths[main_agent.id])
            paths[agent.id] = agent.path

    def check_path_conflict(self, path1, path2):
        # Check if two paths have any conflicting positions at the same time step
        for t in range(min(len(path1), len(path2))):
            if path1[t] == path2[t]:
                return True, t
            elif path1[t] == path2[t - 1] and path1[t - 1] == path2[t]:
                return True, t
        return False, -1

    def generate_random_goal(self, agent, paths):
        occupied_positions = set((a.position for a in self.agents if a != agent))
        occupied_positions.update(a.goal for a in self.agents if a != agent and a.goal)
        while True:
            i, j = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (
                self.map[i][j] != "-1"
                and (i, j) not in occupied_positions
                and not self.map[i][j].startswith("S")
                and not self.map[i][j].startswith("G")
            ):
                for path in paths:
                    if (i, j) in path:
                        continue
                # return (i, j)
                if agent.id == "S1":
                    return (9, 0)
                elif agent.id == "S2":
                    return (5, 3)

    def update_agent_goal(self, agent):
        if agent.id == "S":
            return

        if not agent.goal:
            new_goal = self.generate_random_goal(agent, agent.path)
            agent.goal = new_goal
            new_goal_i, new_goal_j = new_goal
            self.map[new_goal_i][new_goal_j] = "G" + agent.id[1:]
            agent.completed = False

        if agent.position == agent.goal:
            # Remove old start and goal positions
            old_start_i, old_start_j = agent.start
            old_goal_i, old_goal_j = agent.goal
            self.map[old_start_i][old_start_j] = "0"
            self.map[old_goal_i][old_goal_j] = "0"

            # Assign new start and goal positions
            new_start = agent.position
            new_goal = self.generate_random_goal(agent, agent.path)
            agent.start = new_start
            agent.goal = new_goal
            new_start_i, new_start_j = new_start
            new_goal_i, new_goal_j = new_goal
            self.map[new_start_i][new_start_j] = "S" + agent.id[1:]
            self.map[new_goal_i][new_goal_j] = "G" + agent.id[1:]
            agent.completed = False

    def move_multi_agents(self):
        new_positions = {}
        waiting_agents = []
        main_agent = next(agent for agent in self.agents if agent.id == "S")
        time_step_start = next(
            (
                t
                for t, pos in enumerate(self.main_agent.path)
                if pos == self.main_agent.position
            ),
            0,  # Default to 0 if position not found
        )

        # First pass: attempt to move all agents
        for agent in self.agents:
            if agent.path:
                new_pos = (
                    agent.path[self.render.path_indices[agent.id] + 1]
                    if self.render.path_indices[agent.id] + 1 < len(agent.path)
                    else agent.path[-1]
                )
                if new_pos not in new_positions:
                    new_positions[new_pos] = agent
                else:
                    waiting_agents.append(agent)
            else:
                # If agent has no path, update its goal and recalculate path
                self.update_agent_goal(agent)
                result = self.a_star_multi(
                    agent, self.get_current_time_windows(), time_step_start
                )
                if result:
                    new_path, time_left, fuel_left = result
                    agent.path = new_path
                    agent.time_left = time_left
                    agent.fuel_left = fuel_left
                    if new_path:
                        new_pos = new_path[0]
                        if new_pos not in new_positions:
                            new_positions[new_pos] = agent
                        else:
                            waiting_agents.append(agent)
                else:
                    waiting_agents.append(agent)

        # Second pass: resolve collisions
        for agent in waiting_agents:
            current_pos = agent.position
            new_pos = (
                agent.path[self.render.path_indices[agent.id] + 1]
                if self.render.path_indices[agent.id] + 1 < len(agent.path)
                else agent.path[-1]
            )

            if new_pos in new_positions:
                if agent.id == "S" or (
                    agent.id != "S" and new_positions[new_pos].id != "S"
                ):
                    # Current agent has higher priority
                    displaced_agent = new_positions[new_pos]
                    displaced_agent.position = current_pos  # Move back
                    new_positions[new_pos] = agent
                    new_positions[current_pos] = displaced_agent
                else:
                    # Current agent waits
                    new_positions[current_pos] = agent
            else:
                new_positions[new_pos] = agent

        # Update agent positions and paths
        for pos, agent in new_positions.items():
            agent.position = pos
            self.render.update_agent_position(agent.id)
            agent.completed = True if agent.position == agent.goal else False
            if agent.position == agent.goal and agent.id != "S":
                self.update_agent_goal(agent)  # Generate new goal immediately
                new_result = self.a_star_multi(
                    agent, self.get_current_time_windows(), time_step_start
                )
                if new_result:
                    new_path, new_time_left, new_fuel_left = new_result
                    full_path = agent.path_all + new_path
                    is_conflict, t = self.check_path_conflict(
                        full_path, main_agent.path
                    )
                    if not is_conflict:
                        agent.path = (
                            agent.path[self.render.path_indices[agent.id] :] + new_path
                        )
                        agent.path_all += new_path
                        agent.time_left = new_time_left
                        agent.fuel_left = new_fuel_left
                        self.render.set_path(agent.id, agent.path)
                    else:
                        agent.path = [agent.position] * max(
                            self.render.game_parameter.time_limit - len(agent.path),
                            len(agent.path),
                        )
                        agent.path_all += agent.path
                        self.render.set_path(agent.id, agent.path)

        return self.main_agent.position, self.main_agent.completed

    def get_current_time_windows(self):
        time_windows = defaultdict(lambda: defaultdict(lambda: None))
        for agent in self.agents:
            full_path = agent.path_all

            for t, pos in enumerate(full_path):
                time_windows[pos][t] = agent.id

        return time_windows

    def reconstruct_path_multi(self, came_from, end_state):
        path = []
        current = end_state
        while current in came_from:
            path.append(current[0])
            current = came_from[current]
        path.append(current[0])
        return path[::-1]
