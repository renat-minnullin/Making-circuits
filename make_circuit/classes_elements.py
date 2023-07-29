from drawing_elements import *
class Element:
    def __del__(self):
        del self


class Wire(Element):
    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines):
        super().__init__()
        self.name = 'Провод'
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

        self.parameters = [0,
                           0,
                           0,
                           float('inf')]

        self.accesses_to_change = [True,
                                   False,
                                   False,
                                   False]


    def draw(self):

        self.elements_ids = draw_wire(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                      self.width_lines,
                                      self.color_lines)
        self.canvas.itemconfig(self.elements_ids[0], state='normal')

    def exchange_color(self, color):
        """Подпрограмма заменяет цвет всех частей элемента"""
        for id_piece_of_element in self.elements_ids:
            tags = self.canvas.gettags(id_piece_of_element)

            if 'line' in tags:
                self.canvas.itemconfig(id_piece_of_element, fill=color)
            elif 'arc' or 'oval' in tags:
                self.canvas.itemconfig(id_piece_of_element, outline=color)


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

        self.elements_ids = draw_node(self.canvas, [self.x_center, self.y_center], self.radius_clamp, self.width_lines,
                                      self.color_lines, self.color_fill)


class ElementStandardCircuit(Wire):
    def __init__(self, canvas, x_start, y_start,
                 x_end, y_end, normal_length, clamp_start, clamp_end,
                 width_lines,
                 col_highlight,
                 col_lines, own_wire, id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines)
        self.own_wire = own_wire

        self.id = id



class Resistor(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id)
        self.name = 'Резистор'
        self.letter = 'R'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   True,
                                   True]

    def draw(self):
        self.elements_ids = draw_resistor(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                          self.normal_length,
                                          self.width_lines,
                                          self.color_lines)


class Capacitor(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id)
        self.name = 'Конденсатор'
        self.letter = 'C'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   True,
                                   True]

    def draw(self):
        self.elements_ids = draw_capacitor(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                           self.normal_length,
                                           self.width_lines,
                                           self.color_lines)


class InductorCoil(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id)
        self.name = 'Катушка индуктивности'
        self.letter = 'L'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   True,
                                   True]

    def draw(self):
        self.elements_ids = draw_inductor_coil(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                               self.normal_length,
                                               self.width_lines,
                                               self.color_lines)


class SourceEMF(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id)
        self.name = 'Источник ЭДС'
        self.letter = 'E'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   False,
                                   False]

    def draw(self):
        self.elements_ids = draw_source_of_emf(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                               self.normal_length,
                                               self.width_lines,
                                               self.color_lines)


class SourceCurrent(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id)
        self.name = 'Источник тока'
        self.letter = 'J'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   False,
                                   False]

    def draw(self):
        self.elements_ids = draw_current_source(self.canvas, [self.x_start, self.y_start], [self.x_end, self.y_end],
                                                self.normal_length,
                                                self.width_lines,
                                                self.color_lines)
