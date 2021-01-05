from asciimatics.screen import ManagedScreen
from time import sleep
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText

@ManagedScreen
def demo(screen=None):
    screen.print_at('Hello world!', 0, 0)
    screen.refresh()
    sleep(10)

demo()