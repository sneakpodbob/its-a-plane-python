from datetime import datetime

from animator import Animator
from constants import framerate, colours, fonts

from rgbmatrix import graphics

DATE_COLOUR = colours.COLOUR_PINK_DARKER
DATE_FONT = fonts.fonts_small
DATE_POSITION = (1, 31)

class DateScene:

    @Animator.KeyFrame.add(framerate.FRAMES_PER_SECOND * 1)
    def date(self, count):
        if len(self._data):
            # Ensure redraw when there's new data
            self._last_date = None

        else:
            # If there's no data to display
            # then draw the date
            now = datetime.now()
            current_date = now.strftime("%-d-%-m-%Y")

            # Only draw if date needs updated
            if self._last_date != current_date:
                # Undraw last date if different from current
                if not self._last_date is None:
                    _ = graphics.DrawText(
                        self.canvas,
                        DATE_FONT,
                        DATE_POSITION[0],
                        DATE_POSITION[1],
                        colours.COLOUR_BLACK,
                        self._last_date,
                    )
                self._last_date = current_date

                # Draw date
                _ = graphics.DrawText(
                    self.canvas,
                    DATE_FONT,
                    DATE_POSITION[0],
                    DATE_POSITION[1],
                    DATE_COLOUR,
                    current_date,
                )