from controller import *
from menu import *


def main():
    # Check and install required packages
    # check_and_install_packages()

    # Initialize program
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + 300, SCREEN_SIZE))
    pygame.display.set_caption("HCMUS Logistic Co. LTD")
    clock = pygame.time.Clock()

    game_parameter = GameParameter()
    game_parameter.algorithm = "A*"

    while True:
        action = main_menu(
            screen, clock, game_parameter.big_font, game_parameter.medium_font
        )

        if action == "QUIT":
            break
        elif action == "SETTINGS":
            settings_action = settings_menu(
                screen, clock, game_parameter.medium_font, game_parameter
            )
            pygame.display.set_caption("HCMUS Logistic Co. LTD")
            if settings_action == "QUIT":
                break
        elif action == "SHOW":
            game_parameter.set_map()
            render = Render(game_parameter)
            render.initialize()
            controller = Controller(render)

            # Main program
            run_game(screen, clock, controller, render, game_parameter)

    pygame.quit()


def run_game(screen, clock, controller, render, game_parameter):
    running = True
    step_delay = 500
    last_step_time = 0
    path_found = False
    path_exist = False

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    path, time_cost, fuel_left = controller.find_and_draw_path(
                        game_parameter.algorithm,
                        game_parameter.level,
                        game_parameter.time_limit,
                        game_parameter.fuel_limit,
                    )
                    if path:
                        print("Path:", path)
                        render.set_path(path)
                        print("Time left:", time_cost)
                        print("Fuel left:", fuel_left)
                        path_found = True
                        path_exist = True
                        last_step_time = current_time
                    else:
                        if not path_exist:
                            print("No path found.")
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if path_found and current_time - last_step_time > step_delay:
            if render.draw_next_step():
                last_step_time = current_time
            else:
                path_found = False

        render.draw()
        render.draw_grid()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
