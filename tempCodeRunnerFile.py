    def find_and_draw_path(self, algorithm, level, time_limit, fuel_limit):
        path = []
        time_limit = time_limit if (level > 1) else math.inf
        fuel_limit = fuel_limit if (level > 2) else math.inf

        if algorithm == "BFS":
            result = self.BFS(time_limit, fuel_limit)
        elif algorithm == "DFS":
            result = self.DFS(time_limit, fuel_limit)
        elif algorithm == "UCS":
            result = self.UCS(time_limit, fuel_limit)
        elif algorithm == "GBFS":
            result = self.GBFS(time_limit, fuel_limit)
        elif algorithm == "A*":
            result = self.a_star(time_limit, fuel_limit)

        if result:
            path, time_left, fuel_left = result
            return path, time_left, fuel_left
        else:
            return [], time_limit, fuel_limit