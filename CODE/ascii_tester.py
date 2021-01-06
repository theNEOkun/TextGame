from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.widgets import Widget, Frame, Layout


def main_screen(screen):
    frame = Frame(screen, 80, 20)
    layout1 = Layout([100])
    frame.add_layout(layout1)
    layout1.add_widget(Widget.Text(label="Search:", name="search_string"))

    layout2 = Layout([100])
    frame.add_layout(layout2)
    layout1.add_widget(Widget.TextBox(Widget.FILL_FRAME, name="results"))

    screen.play([Scene(frame, 500)])


def demo(screen):
    effects = [
        Cycle(
            screen,
            FigletText("ASCIIMATICS", font='big'),
            screen.height // 2 - 8),
        Cycle(
            screen,
            FigletText("ROCKS!", font='big'),
            screen.height // 2 + 3),
        Stars(screen, (screen.width + screen.height) // 2)
    ]
    screen.play([Scene(effects, 500)])


def main_part():
    Screen.wrapper(main_screen)
