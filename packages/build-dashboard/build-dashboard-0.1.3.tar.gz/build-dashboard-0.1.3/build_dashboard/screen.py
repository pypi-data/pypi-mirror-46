from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
from build_dashboard.views import BuildersView, BuildsView, StepsView, LogView
from build_dashboard import logger

def draw_screen(model, loop, update_secs=5):
    screen = Screen.open()
    scenes = []
    scenes.append(Scene([BuildersView(screen, model)], -1, name="BuildersView"))
    scenes.append(Scene([BuildsView(screen, model)], -1, name="BuildsView"))
    scenes.append(Scene([StepsView(screen, model)], -1, name="StepsView"))
    scenes.append(Scene([LogView(screen, model)], -1, name="LogView"))
    screen.set_scenes(scenes)

    while True:
        try:
            loop.run_until_complete(model.update())
            screen.force_update()
            screen.draw_next_frame(repeat=True)
            screen.wait_for_input(0.05)
        except RuntimeError as e:
            logger.debug(e)
            break
        except ResizeScreenError as e:
            logger.debug(e)
            break
        except KeyboardInterrupt as e:
            logger.debug(e)
            break
    screen.close()
