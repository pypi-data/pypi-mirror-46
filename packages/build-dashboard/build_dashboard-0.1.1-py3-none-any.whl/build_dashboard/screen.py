from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
from build_dashboard.views import BuildbotView
from time import sleep

def draw_screen(model, loop, update_secs=5):
    screen = Screen.open()
    scenes = [Scene([BuildbotView(screen, model)], -1, name="BuildbotView")]
    screen.set_scenes(scenes)

    while True:
        try:
            loop.run_until_complete(model.update())
            screen.force_update()
            screen.draw_next_frame(repeat=True)
            sleep(update_secs)
        except ResizeScreenError as e:
            pass
        except KeyboardInterrupt as e:
            break
    screen.close()
