from utilities.animator import Animator
from setup import colours, fonts, screen

from rgbmatrix import graphics

# Setup
BAR_STARTING_POSITION = (0, 18)
BAR_PADDING = 2

FLIGHT_NO_POSITION = (1, 21)
FLIGHT_NO_TEXT_HEIGHT = 8  # based on font size
FLIGHT_NO_FONT = fonts.small

AIRLINE_FONT = fonts.extrasmall


FLIGHT_NUMBER_ALPHA_COLOUR = colours.BLUE
FLIGHT_NUMBER_NUMERIC_COLOUR = colours.BLUE_LIGHT

DATA_INDEX_POSITION = (52, 21)
DATA_INDEX_TEXT_HEIGHT = 6
DATA_INDEX_FONT = fonts.extrasmall

DIVIDING_BAR_COLOUR = colours.GREEN
DATA_INDEX_COLOUR = colours.GREY


class FlightDetailsScene(object):
    def __init__(self):
        super().__init__()

    @Animator.KeyFrame.add(0)
    def flight_details(self):

        # Guard against no data
        if len(self._data) == 0:
            return

        # Clear the whole area
        self.draw_square(
            0,
            BAR_STARTING_POSITION[1] - (FLIGHT_NO_TEXT_HEIGHT // 2),
            screen.WIDTH - 1,
            BAR_STARTING_POSITION[1] + (FLIGHT_NO_TEXT_HEIGHT // 2),
            colours.BLACK,
        )

        # Draw flight number if available
        flight_no_text_length = 0
        if (
            self._data[self._data_index]["callsign"]
            and self._data[self._data_index]["callsign"] != "N/A"
        ):
            flight_no = f'{self._data[self._data_index]["callsign"]}'

            for ch in flight_no:
                ch_length = graphics.DrawText(
                    self.canvas,
                    FLIGHT_NO_FONT,
                    FLIGHT_NO_POSITION[0] + flight_no_text_length,
                    FLIGHT_NO_POSITION[1],
                    FLIGHT_NUMBER_NUMERIC_COLOUR
                    if ch.isnumeric()
                    else FLIGHT_NUMBER_ALPHA_COLOUR,
                    ch,
                )
                flight_no_text_length += ch_length

        # Draw airline name if available
        if (
            self._data[self._data_index]["airline"]
            and self._data[self._data_index]["airline"] != "N/A"
        ):
            flight_no = f'{self._data[self._data_index]["airline"]}'

            # Draw text
            _ = graphics.DrawText(
                self.canvas,
                AIRLINE_FONT,
                flight_no_text_length + BAR_PADDING if flight_no_text_length else 0,
                BAR_STARTING_POSITION[1] + 2,
                FLIGHT_NUMBER_NUMERIC_COLOUR,
                flight_no,
            )

        # Draw destination airport name if available
        if (
            self._data[self._data_index]["dest_airport_name"]
            and self._data[self._data_index]["dest_airport_name"] != "N/A"
        ):
            dest_airport = f'{self._data[self._data_index]["dest_airport_name"]}'

            # Draw text
            _ = graphics.DrawText(
                self.canvas,
                AIRLINE_FONT,
                flight_no_text_length + BAR_PADDING if flight_no_text_length else 0,
                BAR_STARTING_POSITION[1]  - 6,
                FLIGHT_NUMBER_ALPHA_COLOUR,
                dest_airport,
            )

        # Draw bar
        if len(self._data) > 1:
            # Clear are where N of M might have been
            self.draw_square(
                DATA_INDEX_POSITION[0] - BAR_PADDING,
                BAR_STARTING_POSITION[1] - (FLIGHT_NO_TEXT_HEIGHT // 2),
                screen.WIDTH,
                BAR_STARTING_POSITION[1] + (FLIGHT_NO_TEXT_HEIGHT // 2),
                colours.BLACK,
            )

            # Dividing bar
            graphics.DrawLine(
                self.canvas,
                flight_no_text_length + BAR_PADDING,
                BAR_STARTING_POSITION[1],
                DATA_INDEX_POSITION[0] - BAR_PADDING - 1,
                BAR_STARTING_POSITION[1],
                DIVIDING_BAR_COLOUR,
            )

            # Draw text
            text_length = graphics.DrawText(
                self.canvas,
                fonts.extrasmall,
                DATA_INDEX_POSITION[0],
                DATA_INDEX_POSITION[1],
                DATA_INDEX_COLOUR,
                f"{self._data_index + 1}/{len(self._data)}",
            )
        else:
            # Dividing bar
            graphics.DrawLine(
                self.canvas,
                flight_no_text_length + BAR_PADDING if flight_no_text_length else 0,
                BAR_STARTING_POSITION[1],
                screen.WIDTH,
                BAR_STARTING_POSITION[1],
                DIVIDING_BAR_COLOUR,
            )
