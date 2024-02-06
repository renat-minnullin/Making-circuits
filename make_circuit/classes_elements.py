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

        self.coord_start = [x_start, y_start]
        self.coord_end = [x_end, y_end]
        self.normal_length = normal_length
        self.width_lines = width_lines
        self.color_lines = col_lines
        self.color_highlight = col_highlight

        self.clamp_start = clamp_start
        self.clamp_end = clamp_end

        self.arrow_direction = ''  # 'last', 'first'

        self.arrow_parameters = str(self.normal_length / 8) + ' ' + str(self.normal_length / 6) + ' ' + str(
            self.normal_length / 15)

        self.elements_ids = []

        self.parameters = ['-',
                           0,
                           0,
                           float('inf')]

        self.accesses_to_change = [True,
                                   False,
                                   False,
                                   False]
        self.title_element_id = None
        self.branch = None
        self.element = None

    def draw(self):

        self.elements_ids = draw_wire(self.canvas, self.coord_start, self.coord_end,
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
            if self.title_element_id is not None:
                self.canvas.itemconfigure(self.title_element_id, fill=color)

    def create_direction(self, out_elements_ids):
        """Метод задает направление тока от начального зажима к конечному, при этом на входе
        поступает список индексов линий прикрепленного элемента (либо самого провода, если такого элемента нет)"""
        self.arrow_direction = draw_arrow(self.canvas, out_elements_ids, self.arrow_parameters)

    def change_direction(self, out_elements_ids, brch_of_wire_arrow_direction):
        """Метод меняет направление тока в элементе на противоположное, при этом на входе
        поступает список индексов линий прикрепленного элемента (либо самого провода, если такого элемента нет)"""
        self.arrow_direction = brch_of_wire_arrow_direction
        change_direction_arrow(self.canvas, out_elements_ids, self.arrow_direction, self.arrow_parameters)

    def delete_direction(self, out_elements_ids):
        """Подпрограмма удаляет направление элемента, при этом на входе
        поступает список индексов линий прикрепленного элемента (либо самого провода, если такого элемента нет)"""
        self.arrow_direction = delete_direction_arrow(self.canvas, out_elements_ids)

    def synchronizing_wire_with_branch(self, brch):
        """Метод меняет местами начальную и конечную координату зажимов провода так, чтобы они были в списке зажимов ветви
        в установленном в ней порядке - от начала ветви к концу ветви."""
        if brch.own_coords.index(self.clamp_start.coord) > brch.own_coords.index(self.clamp_end.coord):
            self.clamp_start, self.clamp_end = self.clamp_end, self.clamp_start
            self.coord_start, self.coord_end = self.coord_end, self.coord_start
            self.x_start, self.x_end = self.x_end, self.x_start
            self.y_start, self.y_end = self.y_end, self.y_start
            self.canvas.coords(self.elements_ids[0], self.x_start, self.y_start, self.x_end, self.y_end)


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
                 col_lines, own_wire, id, color_full_id, font_full_id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines)
        self.own_wire = own_wire

        self.id = id
        self.color_full_id = color_full_id

        self.font_full_id = font_full_id
        self.parameters = ['-',
                           '-',
                           0,
                           float('inf')]

        self.arrow_direction = 'No direction in parameter of element. Check direction of own_wire'


class Resistor(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id, color_full_id, font_full_id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id, color_full_id, font_full_id)
        self.name = 'Резистор'
        self.letter = 'R'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   True,
                                   True]

    def draw(self):
        self.elements_ids, self.title_element_id = total_draw_element(self.canvas, draw_resistor,
                                                                      self.coord_start, self.coord_end,
                                                                      self.normal_length,
                                                                      self.width_lines, self.full_id,
                                                                      self.color_lines,
                                                                      self.color_full_id, self.font_full_id)


class Capacitor(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id, color_full_id, font_full_id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id, color_full_id, font_full_id)
        self.name = 'Конденсатор'
        self.letter = 'C'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   True,
                                   True]

    def draw(self):
        self.elements_ids, self.title_element_id = total_draw_element(self.canvas, draw_capacitor,
                                                                      self.coord_start, self.coord_end,
                                                                      self.normal_length,
                                                                      self.width_lines, self.full_id,
                                                                      self.color_lines,
                                                                      self.color_full_id, self.font_full_id)


class InductorCoil(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id, color_full_id, font_full_id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id, color_full_id, font_full_id)
        self.name = 'Катушка индуктивности'
        self.letter = 'L'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   True,
                                   True]

    def draw(self):
        self.elements_ids, self.title_element_id = total_draw_element(self.canvas, draw_inductor_coil,
                                                                      self.coord_start, self.coord_end,
                                                                      self.normal_length,
                                                                      self.width_lines, self.full_id,
                                                                      self.color_lines,
                                                                      self.color_full_id, self.font_full_id)


class SourceEMF(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id, color_full_id, font_full_id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id, color_full_id, font_full_id)
        self.name = 'Источник ЭДС'
        self.letter = 'E'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   False,
                                   False]

    def draw(self):
        self.elements_ids, self.title_element_id = total_draw_element(self.canvas, draw_source_of_emf,
                                                                      self.coord_start, self.coord_end,
                                                                      self.normal_length,
                                                                      self.width_lines, self.full_id,
                                                                      self.color_lines,
                                                                      self.color_full_id, self.font_full_id)


class SourceCurrent(ElementStandardCircuit):

    def __init__(self, canvas, x_start, y_start, x_end, y_end, normal_length, clamp_start, clamp_end, width_lines,
                 col_highlight,
                 col_lines, own_wire, id, color_full_id, font_full_id):
        super().__init__(canvas, x_start, y_start,
                         x_end, y_end, normal_length, clamp_start, clamp_end,
                         width_lines,
                         col_highlight,
                         col_lines, own_wire, id, color_full_id, font_full_id)
        self.name = 'Источник тока'
        self.letter = 'J'
        self.full_id = self.letter + self.id
        self.accesses_to_change = [True,
                                   True,
                                   False,
                                   False]
        self.parameters = ['-',
                           '-',
                           float('inf'),
                           0]

    def draw(self):
        self.elements_ids, self.title_element_id = total_draw_element(self.canvas, draw_current_source,
                                                                      self.coord_start, self.coord_end,
                                                                      self.normal_length,
                                                                      self.width_lines, self.full_id,
                                                                      self.color_lines,
                                                                      self.color_full_id, self.font_full_id)
