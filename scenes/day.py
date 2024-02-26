from datetime import datetime

from utilities.animator import Animator
from setup import colours, fonts, frames

from rgbmatrix import graphics

# Setup
DAY_COLOUR = colours.PINK_DARK
DAY_FONT = fonts.small
DAY_POSITION = (2, 23)

def get_custom_day_string(day_of_week):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    custom_strings = [
        "Montag",
        "Dienstag",
        "Mittwoch",
        "Donnerstag",
        "Freitag",
        "Samstag",
        "Sunday"
    ]

    if 0 <= day_of_week < len(days):
        return custom_strings[day_of_week]
    else:
        return "Invalid day of the week"

class DayScene(object):
    def __init__(self):
        super().__init__()
        self._last_day = None

    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def day(self, count):
        if len(self._data):
            # Ensure redraw when there's new data
            self._last_day = None

        else:
            # If there's no data to display
            # then draw the day
            now = datetime.now().weekday()
            current_day = get_custom_day_string(now)

            # Only draw if time needs updated
            if self._last_day != current_day:
                # Undraw last day if different from current
                if not self._last_day is None:
                    _ = graphics.DrawText(
                        self.canvas,
                        DAY_FONT,
                        DAY_POSITION[0],
                        DAY_POSITION[1],
                        colours.BLACK,
                        self._last_day,
                    )
                self._last_day = current_day

                # Draw day
                _ = graphics.DrawText(
                    self.canvas,
                    DAY_FONT,
                    DAY_POSITION[0],
                    DAY_POSITION[1],
                    DAY_COLOUR,
                    current_day,
                )
