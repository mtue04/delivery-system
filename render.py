from config import *
import pygame


class GameParameter:
    def __init__(self):
        self.level = 1
        self.map_type = 1

        self.map = []
        self.rows = 0
        self.cols = 0
        self.time_limit = 0
        self.fuel_limit = 0

        # Define levels with their respective configurations
        self.levels = {
            1: (False, False, False),  # No time limit, no fuel limit, single agent
            2: (True, False, False),  # Time limit, no fuel limit, single agent
            3: (True, True, False),  # Time limit, fuel limit, single agent
            4: (True, True, True),  # Time limit, fuel limit, multiple agents
        }

        # Define maps with their file paths
        self.maps = {
            1: "assets/maps/map1.txt",
            2: "assets/maps/map2.txt",
            3: "assets/maps/map3.txt",
            4: "assets/maps/map4.txt",
            5: "assets/maps/map5.txt",
        }

        # Initialize fonts
        self.small_font = pygame.font.SysFont(FONT_SMALL, FONT_SIZE_SMALL)
        self.medium_font = pygame.font.Font(FONT_MEDIUM, FONT_SIZE_MEDIUM)
        self.big_font = pygame.font.Font(FONT_BIG, FONT_SIZE_BIG)

    def set_level(self, level):
        """
        Set the game level.
        """
        self.level = level

    def set_map_type(self, map_type):
        """
        Set the map type.
        """
        self.map_type = map_type

    def set_map(self):
        """
        Set the game map based on the current level and map type.
        """
        map_path = f"assets/maps/map{self.map_type}.txt"

        with open(map_path, "r") as file:
            lines = file.readlines()

            # First line contains rows, columns, time limit, and fuel limit
            first_line = lines[0].strip().split()
            self.rows = int(first_line[0])
            self.cols = int(first_line[1])
            self.time_limit = int(first_line[2])
            self.fuel_limit = int(first_line[3])

            # Initialize the map
            self.map = []

            # Read the map
            for line in lines[1:]:
                row = line.strip().split()

                if self.level == 1:
                    row = [
                        "0" if cell not in ["0", "-1", "S", "G"] else cell
                        for cell in row
                    ]
                elif self.level == 2:
                    row = [
                        (
                            "0"
                            if not (cell.isdigit() or cell in ["0", "-1", "S", "G"])
                            else cell
                        )
                        for cell in row
                    ]
                elif self.level == 3:
                    row = [
                        (
                            "0"
                            if (cell.startswith("S") and cell[1:].isdigit())
                            or (cell.startswith("G") and cell[1:].isdigit())
                            else cell
                        )
                        for cell in row
                    ]

                self.map.append(row)


class Render:
    def __init__(self, game_parameter):
        self.game_parameter = game_parameter
        self.backup_map = [row[:] for row in game_parameter.map]
        self.screen = None
        self.clock = None
        self.grid = None
        self.cell_size = 0
        self.running = True
        self.current_path = []
        self.path_index = 0

    def initialize(self):
        """
        Initialize the game window.
        """
        pygame.display.set_caption("HCMUS Logistic Co. LTD")
        self.screen = pygame.display.set_mode((SCREEN_SIZE + 300, SCREEN_SIZE))
        self.clock = pygame.time.Clock()
        self.grid = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
        self.cell_size = SCREEN_SIZE // self.game_parameter.cols

    def draw_grid(self):
        """
        Draw the grid lines on the game window.
        """
        self.grid.fill(BACKGROUND_COLOR)
        for i in range(self.game_parameter.rows):
            for j in range(self.game_parameter.cols):
                cell = self.game_parameter.map[i][j]
                color = BACKGROUND_COLOR
                if cell.startswith("S"):
                    color = START_COLOR
                elif cell.startswith("G"):
                    color = GOAL_COLOR
                elif cell.startswith("F"):
                    color = FUEL_COLOR
                elif cell.isdigit() and cell != "-1" and cell != "0":
                    color = TIME_COLOR
                elif cell == "-1":
                    color = OBSTACLE_COLOR
                elif cell == "P":
                    color = PATH_COLOR

                # Draw the cell background
                pygame.draw.rect(
                    self.grid,
                    color,
                    (
                        j * self.cell_size,
                        i * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

                # Draw the cell content
                cell_font = pygame.font.Font(None, int(self.cell_size * 0.5))
                text_surface = cell_font.render(cell, True, GRID_LINE_COLOR)
                if cell != "0" and cell != "-1" and cell != "P":
                    text_rect = text_surface.get_rect(
                        center=(
                            j * self.cell_size + self.cell_size // 2,
                            i * self.cell_size + self.cell_size // 2,
                        )
                    )
                    self.grid.blit(text_surface, text_rect)

        for i in range(self.game_parameter.rows + 1):
            pygame.draw.line(
                self.grid,
                GRID_LINE_COLOR,
                (0, i * self.cell_size),
                (SCREEN_SIZE, i * self.cell_size),
            )
        for j in range(self.game_parameter.cols + 1):
            pygame.draw.line(
                self.grid,
                GRID_LINE_COLOR,
                (j * self.cell_size, 0),
                (j * self.cell_size, SCREEN_SIZE),
            )

    def draw_text(self, text, font, color, x, y):
        """
        Draw text on the game window.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_info_board(self):
        """
        Draw the information board on the game window.
        """
        # Fill the information board with black color
        pygame.draw.rect(
            self.screen,
            GRID_LINE_COLOR,
            (SCREEN_SIZE, 0, 300, SCREEN_SIZE),
        )

        # Draw the level
        self.draw_text(
            f"Level {self.game_parameter.level}",
            self.game_parameter.medium_font,
            BACKGROUND_COLOR,
            SCREEN_SIZE + 150,
            50,
        )

        # Draw algorithm information
        self.draw_text(
            f"Algo: {self.game_parameter.algorithm}",
            self.game_parameter.medium_font,
            BACKGROUND_COLOR,
            SCREEN_SIZE + 150,
            200,
        )
        # Draw the time limit
        if self.game_parameter.levels[self.game_parameter.level][0]:
            self.draw_text(
                f"Time: {self.game_parameter.time_limit}",
                self.game_parameter.medium_font,
                BACKGROUND_COLOR,
                SCREEN_SIZE + 150,
                300,
            )
        else:
            self.draw_text(
                "Time: ∞",
                self.game_parameter.medium_font,
                BACKGROUND_COLOR,
                SCREEN_SIZE + 150,
                300,
            )

        # Draw the fuel limit
        if self.game_parameter.levels[self.game_parameter.level][1]:
            self.draw_text(
                f"Fuel: {self.game_parameter.fuel_limit}",
                self.game_parameter.medium_font,
                BACKGROUND_COLOR,
                SCREEN_SIZE + 150,
                400,
            )
        else:
            self.draw_text(
                "Fuel: ∞",
                self.game_parameter.medium_font,
                BACKGROUND_COLOR,
                SCREEN_SIZE + 150,
                400,
            )

    def set_path(self, path):
        self.current_path = path
        self.path_index = 0

    def draw_next_step(self):
        if self.path_index < len(self.current_path):
            step = self.current_path[self.path_index]
            row, col = step
            if self.game_parameter.map[row][col] not in ["S", "G"]:
                self.game_parameter.map[row][col] = "P"
                pygame.draw.rect(
                    self.grid,
                    PATH_COLOR,
                    (
                        col * self.cell_size,
                        row * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )
            self.path_index += 1
            return True
        return False

    def clear_path(self):
        """
        Clear the drawn path from the game window.
        """
        self.game_parameter.map = [row[:] for row in self.backup_map]

        # Redraw the grid to clear the path
        self.draw_grid()

    def draw(self):
        """
        Draw the game window.
        """
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid()
        self.screen.blit(self.grid, (0, 0))
        self.draw_info_board()
        pygame.display.flip()
