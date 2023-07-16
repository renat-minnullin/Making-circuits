class Element:
    def __init__(self):
        pass

    def __del__(self):
        del self


class Wire(Element):
    def __init__(self, canvas, x_start, y_start, x_end, y_end, clamp_start, clamp_end, width, col_highlight, col_lines):
        super().__init__()
        self.canvas = canvas
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end

        self.width = width
        self.color_fill = col_lines
        self.color_pressed = col_highlight

        self.clamp_start = clamp_start
        self.clamp_end = clamp_end

        self.number_in_list = None
        self.figure_id = None

        self.flag_highlighted_now = False

        self.elements = []

        self.current_strength = 0

    def make_wire(self):
        from drawing_elements import draw_wire
        self.elements = draw_wire(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end], self.width, self.color_fill)


class Connection(Element):
    """Данный класс отвечает за объект соединения исключительно двух проводов на одном clamp"""

    def __init__(self, clamp, col_lines):
        super().__init__()
        self.clamp = clamp
        self.row = clamp.row
        self.column = clamp.column

        self.color_fill = col_lines

        self.potential = 0


class Node(Element):

    def __init__(self, clamp, col_lines):
        super().__init__()
        self.clamp = clamp
        self.row = clamp.row
        self.column = clamp.column

        self.color_fill = col_lines

        self.potential = 0


class Resistor(Element):

    def __init__(self, clamp_start, clamp_end, width_line, col_lines):
        super().__init__()
        self.clamp_start = clamp_start
        self._clamp_end = clamp_end
        self.width_line = width_line

        self.color_fill = col_lines

        self.resistance = 0
        self.conductivity = 0
        self.current_strength = 0
        self.voltage = 0


class Capacitor(Element):

    def __init__(self, clamp_start, clamp_end, width_line, col_lines):
        super().__init__()
        self.clamp_start = clamp_start
        self._clamp_end = clamp_end
        self.width_line = width_line

        self.color_fill = col_lines

        self.resistance = 0
        self.conductivity = 0
        self.current_strength = 0
        self.voltage = 0


class Inductor_Coil(Element):

    def __init__(self, clamp_start, clamp_end, width_line, col_lines):
        super().__init__()
        self.clamp_start = clamp_start
        self._clamp_end = clamp_end
        self.width_line = width_line

        self.color_fill = col_lines

        self.resistance = 0
        self.conductivity = 0
        self.current_strength = 0
        self.voltage = 0


class Source_of_EMF(Element):

    def __init__(self, clamp_start, clamp_end, width_line, col_lines):
        super().__init__()
        self.clamp_start = clamp_start
        self._clamp_end = clamp_end
        self.width_line = width_line

        self.color_fill = col_lines

        self.current_strength = 0
        self.voltage = 0


class Current_Source(Element):

    def __init__(self, clamp_start, clamp_end, width_line, col_lines):
        super().__init__()
        self.clamp_start = clamp_start
        self._clamp_end = clamp_end
        self.width_line = width_line

        self.color_fill = col_lines

        self.current_strength = 0
        self.voltage = 0
