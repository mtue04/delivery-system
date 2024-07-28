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

    # Test
    game_parameter.level = 4

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
                    if game_parameter.level == 4:
                        path, goal = controller.plan_paths_multi()
                        if path:
                            render.set_path(game_parameter.main_agent.id, path)
                            for agent in game_parameter.agents:
                                if agent.id != game_parameter.main_agent.id:
                                    render.set_path(agent.id, agent.path)
                            path_found = True
                            path_exist = True
                            last_step_time = current_time
                        else:
                            print("No path found for main agent.")
                    else:
                        path, time_cost, fuel_left = controller.find_and_draw_path(
                            game_parameter.algorithm,
                            game_parameter.level,
                            game_parameter.time_limit,
                            game_parameter.fuel_limit,
                        )
                        if path:
                            print("Path:", path)
                            render.set_path("S", path)
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
            if game_parameter.level == 4:
                new_pos, completed = controller.move_multi_agents()

                # Update path progress for all agents
                render.update_path_progress()

                if render.draw_next_step_multi():
                    last_step_time = current_time
                if completed:
                    path_found = False
                    for agent in sorted(game_parameter.agents, key=lambda x: x.id):
                        print(agent.id)
                        print("Path: ", agent.path_all)
                    print("Main agent reached its goal!")
            else:
                if render.draw_next_step():
                    last_step_time = current_time
                    render.update_path_progress()
                else:
                    path_found = False
                    print("Main agent reached its goal!")

        render.draw()
        render.draw_grid()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
