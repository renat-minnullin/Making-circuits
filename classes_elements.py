class Element:
    def __del__(self):
        del self


class Wire(Element):
    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines):
        super().__init__()
        self.canvas = canvas
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end

        self.normal_length = normal_length
        self.width_lines = width_lines
        self.color_lines = col_lines
        self.color_highlight = col_highlight

        self.clamp_start = clamp_start
        self.clamp_end = clamp_end






        self.elements_ids = []

        self.current_strength = 0

    def draw(self):
        from drawing_elements import draw_wire
        self.elements_ids = draw_wire(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                      self.width_lines,
                                      self.color_lines)


class Connection(Element):
    """Данный класс отвечает за объект соединения исключительно двух проводов на одном clamp"""

    def __init__(self, clamp, col_lines):
        super().__init__()
        self.clamp = clamp
        self.row = clamp.row
        self.column = clamp.column

        self.color_lines = col_lines

        self.potential = 0


class Node(Element):

    def __init__(self, canvas, clamp, width_lines, col_lines, col_fill):
        super().__init__()
        self.canvas = canvas
        self.clamp = clamp
        self.row = clamp.row
        self.column = clamp.column
        self.radius_clamp = clamp.radius_circle
        self.x_center = clamp.x_center_circle
        self.y_center = clamp.y_center_circle

        self.width_lines = width_lines

        self.color_lines = col_lines
        self.color_fill = col_fill

        self.potential = 0

        self.elements_ids = []

    def draw(self):
        from drawing_elements import draw_node
        self.elements_ids = draw_node(self.canvas, [self.x_center, self.y_center], self.radius_clamp, self.width_lines,
                                      self.color_lines, self.color_fill)


class Resistor(Wire):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire):
        super().__init__(canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                         col_highlight,
                         col_lines)
        self.name = 'Резистор'
        self.own_wire = own_wire

        self.resistance = 0
        self.conductivity = 0
        self.current_strength = 0
        self.voltage = 0

        self.elements_ids = []

    def draw(self):
        from drawing_elements import draw_resistor
        self.elements_ids = draw_resistor(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                          self.normal_length,
                                          self.width_lines,
                                          self.color_lines)


class Capacitor(Wire):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire):
        super().__init__(canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                         col_highlight,
                         col_lines)
        self.name = 'Конденсатор'
        self.own_wire = own_wire

        self.resistance = 0
        self.conductivity = 0
        self.current_strength = 0
        self.voltage = 0

        self.elements_ids = []

    def draw(self):
        from drawing_elements import draw_capacitor
        self.elements_ids = draw_capacitor(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                           self.normal_length,
                                           self.width_lines,
                                           self.color_lines)


class Inductor_Coil(Wire):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire):
        super().__init__(canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                         col_highlight,
                         col_lines)
        self.name = 'Катушка индуктивности'
        self.own_wire = own_wire

        self.resistance = 0
        self.conductivity = 0
        self.current_strength = 0
        self.voltage = 0

        self.elements_ids = []

    def draw(self):
        from drawing_elements import draw_inductor_coil
        self.elements_ids = draw_inductor_coil(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                               self.normal_length,
                                               self.width_lines,
                                               self.color_lines)


class Source_of_EMF(Wire):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire):
        super().__init__(canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                         col_highlight,
                         col_lines)
        self.name = 'Источник ЭДС'
        self.own_wire = own_wire
        self.current_strength = 0
        self.voltage = 0

        self.elements_ids = []

    def draw(self):
        from drawing_elements import draw_source_of_emf
        self.elements_ids = draw_source_of_emf(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                               self.normal_length,
                                               self.width_lines,
                                               self.color_lines)


class Current_Source(Wire):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire):
        super().__init__(canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                         col_highlight,
                         col_lines)
        self.name = 'Источник тока'
        self.own_wire = own_wire
        self.current_strength = 0
        self.voltage = 0

        self.elements_ids = []

    def draw(self):
        from drawing_elements import draw_current_source
        self.elements_ids = draw_current_source(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                                self.normal_length,
                                                self.width_lines,
                                                self.color_lines)
