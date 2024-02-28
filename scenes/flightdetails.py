from utilities.animator import Animator
from setup import colours, fonts, screen

from rgbmatrix import graphics

# Setup
BAR_STARTING_POSITION = (0, 20)
BAR_PADDING = 2

FLIGHT_NO_POSITION = (1, 17)
FLIGHT_NO_TEXT_HEIGHT = 6  # based on font size
FLIGHT_NO_FONT = fonts.extrasmall

AIRLINE_FONT = fonts.extrasmall
AIRLINE_COLOR = colours.BLUE_LIGHT

DEST_AIRPORT_FONT = fonts.extrasmall
DEST_AIRPORT_COLOR = colours.YELLOW

FLIGHT_NUMBER_ALPHA_COLOUR = colours.BLUE
FLIGHT_NUMBER_NUMERIC_COLOUR = colours.BLUE_LIGHT

DATA_INDEX_POSITION = (52, 23)
DATA_INDEX_TEXT_HEIGHT = 6
DATA_INDEX_FONT = fonts.extrasmall

DIVIDING_BAR_COLOUR = colours.GREEN
DATA_INDEX_COLOUR = colours.GREY

def extract_words_until_length(string, length):
    """
    Extracts words from the input string until the total length reaches 12 characters.

    Args:
        string (str): The input string.

    Returns:
        str: A space-separated string containing the extracted words.
    """
    words = string.split()  # Split the string into words
    result = []
    total_length = 0

    for word in words:
        if total_length + len(word) <= length:
            result.append(word)
            total_length += len(word) + 1  # Add 1 for the space between words
        else:
            break  # Stop adding words once the total length exceeds length

    # add at least the first length letters, if the first word was to long right away
    if (len(result) == 0):
        result.append(string[:length])

    if (string.upper().startswith("SAN FRANCISCO")):
        return "San Fran"

    return ' '.join(result)

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
            BAR_STARTING_POSITION[1] - 7, # (FLIGHT_NO_TEXT_HEIGHT // 2),
            screen.WIDTH - 1,
            BAR_STARTING_POSITION[1] + 7, # (FLIGHT_NO_TEXT_HEIGHT // 2),
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
        airline_text_length = 0

        if (
            self._data[self._data_index]["airline"]
            and self._data[self._data_index]["airline"] != "N/A"
        ):
            airline_name = f'{self._data[self._data_index]["airline"]}'

            airline_name_max12 = extract_words_until_length(airline_name, 12)

            for ch in airline_name_max12:
                ch_length = graphics.DrawText(
                    self.canvas,
                    AIRLINE_FONT,
                    FLIGHT_NO_POSITION[0] + airline_text_length,
                    FLIGHT_NO_POSITION[1] + 6,
                    AIRLINE_COLOR,
                    ch,
                )
                airline_text_length += ch_length

        # Draw destination airport name if available
        if (
            self._data[self._data_index]["dest_airport_name"]
            and self._data[self._data_index]["dest_airport_name"] != "N/A"
        ):
            dest_airport = f'{self._data[self._data_index]["dest_airport_name"]}'

            dest_airport_max10 = extract_words_until_length(dest_airport, 15 - len(flight_no))

            # Draw text
            _ = graphics.DrawText(
                self.canvas,
                DEST_AIRPORT_FONT,
                flight_no_text_length + BAR_PADDING if flight_no_text_length else 0,
                BAR_STARTING_POSITION[1]  - 3,
                DEST_AIRPORT_COLOR,
                dest_airport_max10,
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
                airline_text_length + BAR_PADDING,
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
                airline_text_length + BAR_PADDING if airline_text_length else 0,
                BAR_STARTING_POSITION[1],
                screen.WIDTH,
                BAR_STARTING_POSITION[1],
                DIVIDING_BAR_COLOUR,
            )
