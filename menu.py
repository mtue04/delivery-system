from config import *
import pygame


class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def main_menu(screen, clock, big_font, medium_font):
    title = big_font.render("HCMUS Logistic Co. LTD", True, "#273D73")
    title_rect = title.get_rect(center=((SCREEN_SIZE + 300) // 2, 100))

    show_button = Button(
        (SCREEN_SIZE + 300) // 2 - 150,
        200,
        300,
        150,
        "SHOW",
        "#273D73",
        "#FFFFFF",
        medium_font,
    )
    settings_button = Button(
        (SCREEN_SIZE + 300) // 2 - 150,
        400,
        300,
        150,
        "SETTINGS",
        "#273D73",
        "#FFFFFF",
        medium_font,
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_button.is_clicked(event.pos):
                    return "SHOW"
                if settings_button.is_clicked(event.pos):
                    return "SETTINGS"

        screen.fill("#FFFFFF")
        screen.blit(title, title_rect)
        show_button.draw(screen)
        settings_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def settings_menu(screen, clock, medium_font, game_parameter):
    title = medium_font.render("- SETTINGS -", True, "#273D73")
    title_rect = title.get_rect(center=((SCREEN_SIZE + 300) // 2, 50))

    level_button = Button(
        (SCREEN_SIZE + 300) // 2 - 250,
        150,
        500,
        75,
        f"Level: {game_parameter.level}",
        "#273D73",
        "#FFFFFF",
        medium_font,
    )
    map_button = Button(
        (SCREEN_SIZE + 300) // 2 - 250,
        250,
        500,
        75,
        f"Map: {game_parameter.map_type}",
        "#273D73",
        "#FFFFFF",
        medium_font,
    )
    algo_button = Button(
        (SCREEN_SIZE + 300) // 2 - 250,
        350,
        500,
        75,
        f"Algorithm: {game_parameter.algorithm}",
        "#273D73",
        "#FFFFFF",
        medium_font,
    )
    back_button = Button(
        (SCREEN_SIZE + 300) // 2 - 250,
        450,
        500,
        75,
        "Back",
        "#732727",
        "#FFFFFF",
        medium_font,
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level_button.is_clicked(event.pos):
                    game_parameter.level = (game_parameter.level % 4) + 1
                if map_button.is_clicked(event.pos):
                    game_parameter.map_type = (game_parameter.map_type % 5) + 1
                if algo_button.is_clicked(event.pos):
                    algorithms = (
                        ["BFS", "DFS", "UCS", "GBFS", "A*"]
                        if game_parameter.level == 1
                        else (["UCS", "A*"] if game_parameter.level == 2 else ["A*"])
                    )
                    current_index = algorithms.index(game_parameter.algorithm)
                    game_parameter.algorithm = algorithms[
                        (current_index + 1) % len(algorithms)
                    ]
                if back_button.is_clicked(event.pos):
                    return "BACK"

        # Handle cases lead to misundertanding
        if game_parameter.level == 2 and (
            game_parameter.algorithm == "BFS"
            or game_parameter.algorithm == "DFS"
            or game_parameter.algorithm == "GBFS"
        ):
            game_parameter.algorithm = "UCS"
            pygame.display.set_caption(
                "Warning: Level 2 cannot handle by BFS, DFS, UCS or GBFS algorithm. Auto changing to the suitable algorithm."
            )
        elif game_parameter.level == 3 and (
            game_parameter.algorithm == "BFS"
            or game_parameter.algorithm == "DFS"
            or game_parameter.algorithm == "UCS"
            or game_parameter.algorithm == "GBFS"
        ):
            game_parameter.algorithm = "A*"
            pygame.display.set_caption(
                "Warning: Level 3 cannot handle by BFS, DFS, UCS or GBFS algorithm. Auto changing to the suitable algorithm."
            )

        level_button.text = f"Level: {game_parameter.level}"
        map_button.text = f"Map: {game_parameter.map_type}"
        algo_button.text = f"Algorithm: {game_parameter.algorithm}"

        screen.fill("#FFFFFF")
        screen.blit(title, title_rect)
        level_button.draw(screen)
        map_button.draw(screen)
        algo_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
