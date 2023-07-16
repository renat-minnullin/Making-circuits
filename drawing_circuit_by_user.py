from make_display import CLAMPS, WORKSPACE, NUMBER_CLAMP_ROWS, NUMBER_CLAMP_COLUMNS, root
from options_visualization import *
from paths_for_buffer_files import *


class Wire:

    def __init__(self, canvas, x_start, y_start, x_end, y_end, clamp_start, clamp_end, width, col_highlight,
                 col_lines):
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

    def make_wire(self):
        self.figure_id = self.canvas.create_line(self.x_start, self.y_start, self.x_end, self.y_end,
                                                 width=self.width,
                                                 fill=self.color_fill)

    def __del__(self):
        del self


def binding_clamps_for_making_wires(canvas, clamps__, rows, columns, wires_):
    """Подпрограмма запускает метод биндинга для рисования проводов"""

    def making_wires(canvas__, clamp, clamps___, wires__):
        """Подпрограмма поддерживает создание проводов между зажимами"""

        def press_left_btn_mouse_on_clamp(event):
            """Подпрограмма события нажатия на зажим"""

            from drawing_elements import calculating_intend_at_center

            def input_clamps_r_c_acceptable_highlighting():
                """Подпрограмма вводит из файла массив координат подсвеченных(доступных для нажатия) зажимов"""
                global path_buffer_row_col_acceptable_clamps
                fin = open(path_buffer_row_col_acceptable_clamps, 'r')
                clamps_r_c_acceptable_highlighting = []
                string = fin.readline().split()

                for i in range(len(string)):
                    coord = string[i].split('-')

                    clamps_r_c_acceptable_highlighting.append([])
                    clamps_r_c_acceptable_highlighting[i].append(int(coord[0]))
                    clamps_r_c_acceptable_highlighting[i].append(int(coord[1]))
                fin.close()

                return clamps_r_c_acceptable_highlighting

            def output_clamps_r_c_acceptable_highlighting(clamps_r_c_acceptable_highlighting):
                """Подпрограмма выводит в файл массив координат подсвеченных(доступных для нажатия) зажимов"""
                global path_buffer_row_col_acceptable_clamps
                fout = open(path_buffer_row_col_acceptable_clamps, 'w')
                for coord in clamps_r_c_acceptable_highlighting:
                    r_x = coord[0]
                    c_x = coord[1]
                    fout.write(str(r_x) + '-' + str(c_x) + ' ')
                fout.close()

            def make_acceptable_clamp_highlighting(clmp):
                """Подпрограмма создает подсвеченные круги зажимов, а также массив с их координатами"""
                global COLOR_HIGHLIGHT
                clamps_row_col_acceptable_highlighting = []

                for i in range(3):
                    for j in range(3):
                        r = clmp.row + i - 1
                        c = clmp.column + j - 1
                        if not (r == clmp.row and c == clmp.column) \
                                and 0 <= r < len(clamps___) \
                                and 0 <= c < len(clamps___[0]) \
                                and [clmp.row, clmp.column] not in clamps___[r][
                            c].list_row_col_connected_clamps:
                            canvas__.itemconfig(clamps___[r][c].figure_id, outline=COLOR_HIGHLIGHT)
                            clamps_row_col_acceptable_highlighting.append([r, c])

                output_clamps_r_c_acceptable_highlighting(clamps_row_col_acceptable_highlighting)

            def delete_acceptable_clamps():
                """Подпрограмма удаляет созданные подсвеченные круги зажимов"""
                clamps_row_col_acceptable_highlighting = input_clamps_r_c_acceptable_highlighting()
                for coord in clamps_row_col_acceptable_highlighting:
                    r = coord[0]
                    c = coord[1]
                    canvas__.itemconfig(clamps___[r][c].figure_id, outline=clamp.color_outline)

            def flag_acceptable_clamp(clmp, start_r, start_c):
                """Подпрограмма проверяет прожатый зажим на возможность нажатия"""
                clamps_row_col_acceptable_highlighting = input_clamps_r_c_acceptable_highlighting()
                fl_accept_clamp = [clmp.row, clmp.column] in clamps_row_col_acceptable_highlighting
                fl_not_repeat_wire = [clmp.row, clmp.column] not in clamps___[start_r][
                    start_c].list_row_col_connected_clamps

                if fl_accept_clamp and fl_not_repeat_wire:
                    return True
                else:
                    return False

            def input_id_moving_line():
                """Подпрограмма вводит из файла id движущейся линии"""
                global path_buffer_id_moving_line
                fin = open(path_buffer_id_moving_line, 'r')
                mov_w_line = int(fin.readline().split()[0])
                fin.close()
                return mov_w_line

            def output_id_moving_line(mov_w_line):
                """Подпрограмма выводит в файл id движущейся линии"""
                fout = open(path_buffer_id_moving_line, 'w')
                fout.write(str(mov_w_line))
                fout.close()

            def input_r_c_start_clamp():
                """Подпрограмма вводит из файла координаты начального зажима (row, col)"""
                global path_buffer_row_col_start_clamp
                fin = open(path_buffer_row_col_start_clamp, 'r')
                row_and_col = fin.readline().split()
                clamp_row, clamp_column = int(row_and_col[0]), int(row_and_col[1])
                fin.close()
                return clamp_row, clamp_column

            def output_r_c_start_clamp(cl):
                """Подпрограмма выводит в файл координаты начального зажима (row, col)"""
                fout = open(path_buffer_row_col_start_clamp, 'w')
                fout.write(str(cl.row) + ' ' + str(cl.column) + '\n')
                fout.close()

            def moving_mouse_with_line(ev):
                """Подпрограмма поддерживает движение линии за курсором мыши"""
                mov_wire_line = input_id_moving_line()
                canvas__.delete(mov_wire_line)

                if ev.x < clamp.x_center_circle and ev.y < clamp.y_center_circle:
                    mouse_indent_x = ev.x + 3
                    mouse_indent_y = ev.y + 3
                else:
                    mouse_indent_x = ev.x - 3
                    mouse_indent_y = ev.y - 3

                mov_wire_line = canvas__.create_line(clamp.x_center_circle, clamp.y_center_circle,
                                                     mouse_indent_x, mouse_indent_y, width=1)
                output_id_moving_line(mov_wire_line)
                output_r_c_start_clamp(clamp)

            def delete_moving_line(ev):
                """Подпрограмма останавливает рисование провода и удаляет линию"""

                global moving_wire_line, flag_moving_line_created
                moving_wire_line = input_id_moving_line()

                canvas__.delete(moving_wire_line)
                canvas__.unbind('<Motion>')
                root.unbind('<Escape>')
                moving_wire_line = None
                canvas__.itemconfig(clamp.figure_id, outline=clamp.color_outline)
                delete_acceptable_clamps()
                flag_moving_line_created = False

            def add_numbers_clamped_clamps(start_row, start_col, end_row, end_col):
                """Подпрограмма записывает данные зажатых зажимов"""

                def input_massive_clamped_clamps():
                    """Подпрограмма вводит из файла массив зажатых зажимов"""
                    global path_buffer_massive_clamped_clamps
                    fin = open(path_buffer_massive_clamped_clamps, 'r')
                    mas_clamped_cls = fin.readline().split()
                    fin.close()
                    return mas_clamped_cls

                def output_massive_clamped_clamps(sort_mas_clamped_cls):
                    """Подпрограмма выводит в файл массив зажатых зажимов"""
                    global path_buffer_massive_clamped_clamps
                    fout = open(path_buffer_massive_clamped_clamps, 'w')
                    for i in range(len(sort_mas_clamped_cls)):
                        fout.write(sort_mas_clamped_cls[i] + ' ')
                    fout.close()

                massive_clamped_clamps = input_massive_clamped_clamps()

                start_cords_str = str(start_row) + '-' + str(start_col)
                end_cords_str = str(end_row) + '-' + str(end_col)
                set_clamped_clamps = set(massive_clamped_clamps)

                if start_cords_str not in set_clamped_clamps:
                    set_clamped_clamps.add(start_cords_str)
                if end_cords_str not in set_clamped_clamps:
                    set_clamped_clamps.add(end_cords_str)
                sort_massive_clamped_clamps = sorted(set_clamped_clamps)

                output_massive_clamped_clamps(sort_massive_clamped_clamps)

            def press_left_btn_mouse_on_wire(ev):
                """Подпрограмма отработки события нажатия на провод"""

                def delete_highlighted_wire(e):
                    """Подпрограмма удаляет выделенный провод"""

                    def reload_massive_clamped_clamps(clmp_start, clmp_end):
                        """Подпрограмма перезаписывает данные зажатых зажимов"""
                        global path_buffer_massive_clamped_clamps

                        fin_clamped_clamps = open(path_buffer_massive_clamped_clamps, 'r')
                        massive_clamped_clamps = fin_clamped_clamps.readline().split()
                        fin_clamped_clamps.close()

                        fout_clamped_clamps = open(path_buffer_massive_clamped_clamps, 'w')
                        if clmp_start.number_connected_wires == 1:
                            massive_clamped_clamps.remove(
                                str(clmp_start.row) + '-' + str(clmp_start.column))
                        if clmp_end.number_connected_wires == 1:
                            massive_clamped_clamps.remove(str(clmp_end.row) + '-' + str(clmp_end.column))
                        set_massive_clamped_clamps = set(massive_clamped_clamps)
                        sort_set_massive_clamped_clamps = sorted(set_massive_clamped_clamps)
                        for i in range(len(sort_set_massive_clamped_clamps)):
                            fout_clamped_clamps.write(sort_set_massive_clamped_clamps[i] + ' ')
                        fout_clamped_clamps.close()

                    def delete_clamps_connections(clmp_start, clmp_end):
                        """Подпрограмма удаляет связь между двумя зажимами, составляющими удаленный провод"""

                        clmp_start.list_row_col_connected_clamps.remove([clmp_end.row, clmp_end.column])
                        clmp_start.number_connected_wires -= 1

                        clmp_end.list_row_col_connected_clamps.remove([clmp_start.row, clmp_start.column])
                        clmp_end.number_connected_wires -= 1

                    def reload_wire_numbers_in_list():
                        """Подпрограмма перезаписывания порядка нумерации проводов в списке (смещены из-за удаления
                        одного из проводов"""
                        for num in range(len(wires__)):
                            wires__[num].number_in_list = num

                    # ---Вход при нажатии клавиши DELETE при выделенном проводе---
                    global flag_element_highlighted, path_buffer_highlighted_wire
                    if flag_element_highlighted:
                        fin_highlighted_wire = open(path_buffer_highlighted_wire, 'r')
                        fin_highlighted_wire.readline()
                        num_highlight_wire = int(fin_highlighted_wire.readline().split()[0])
                        fin_highlighted_wire.close()

                        wire_x = wires__[num_highlight_wire]

                        fout_highlighted_wire = open(path_buffer_highlighted_wire, 'w')
                        fout_highlighted_wire.write('Номер провода в списке проводов:\n')
                        fout_highlighted_wire.close()

                        reload_massive_clamped_clamps(wire_x.clamp_start, wire_x.clamp_end)

                        delete_clamps_connections(wire_x.clamp_start, wire_x.clamp_end)

                        canvas__.delete(wire_x.figure_id)
                        wires__.remove(wire_x)

                        reload_wire_numbers_in_list()

                        wire_x.__del__()
                        root.unbind('<Delete>')
                        flag_element_highlighted = False

                # ---Вход смене выделенного провода---
                global flag_element_highlighted, path_buffer_highlighted_wire
                if flag_element_highlighted:
                    fin = open(path_buffer_highlighted_wire, 'r')
                    fin.readline()
                    num_highlighted_wire = int(fin.readline().split()[0])
                    fin.close()

                    canvas__.itemconfig(wires__[num_highlighted_wire].figure_id,
                                        fill=wires__[num_highlighted_wire].color_fill)
                    wires__[num_highlighted_wire].flag_highlighted_now = False

                    fout = open(path_buffer_highlighted_wire, 'w')
                    fout.write('Номер провода в списке проводов:\n')
                    fout.write(str(wires__[num_highlighted_wire].number_in_list))
                    fout.close()

                # ---Вход при первом выделении провода---
                fout = open(path_buffer_highlighted_wire, 'w')
                fout.write('Номер провода в списке проводов:\n')
                fout.write(str(wire.number_in_list))
                fout.close()

                canvas__.itemconfig(wire.figure_id, fill=wire.color_pressed)
                wire.flag_highlighted_now = True
                flag_element_highlighted = True

                root.bind('<Delete>', delete_highlighted_wire)

            def init_moving_line(canvas___, clmp_start, x_mouse, y_mouse):
                """Подпрограмма инициализирует движущую линию"""
                global moving_wire_line, root, flag_moving_line_created
                flag_moving_line_created = True
                make_acceptable_clamp_highlighting(clmp_start)
                moving_wire_line = canvas___.create_line(clmp_start.x_center_circle,
                                                         clmp_start.y_center_circle,
                                                         x_mouse, y_mouse, width=1)
                output_id_moving_line(moving_wire_line)
                output_r_c_start_clamp(clmp_start)

                canvas___.bind('<Motion>', moving_mouse_with_line)
                root.bind('<Escape>', delete_moving_line)

            global moving_wire_line, root, WIDTH_WIRES, COLOR_HIGHLIGHT, COLOR_LINES

            # ---Выполняется при первом нажатии на зажим---
            if moving_wire_line is None:
                init_moving_line(canvas__, clamp, event.x, event.y)
            else:
                # ---Выполняется при дальнейших нажатиях на зажим---
                moving_wire_line = input_id_moving_line()
                start_clamp_row, start_clamp_column = input_r_c_start_clamp()
                clamp_start = clamps___[start_clamp_row][start_clamp_column]
                clamp_end = clamp

                if flag_acceptable_clamp(clamp_end, start_clamp_row, start_clamp_column):
                    clamp_end.list_row_col_connected_clamps.append([clamp_start.row, clamp_start.column])
                    clamp_start.list_row_col_connected_clamps.append([clamp_end.row, clamp_end.column])
                    clamp_end.number_connected_wires += 1
                    clamp_start.number_connected_wires += 1

                    add_numbers_clamped_clamps(clamp_start.row, clamp_start.column, clamp_end.row,
                                               clamp_end.column)
                    delete_moving_line(0)  # ноль добавлен для аннулирования параметра event

                    x_start_wire, y_start_wire, x_end_wire, y_end_wire = calculating_intend_at_center(
                        clamp_start.radius_circle, clamp_start.x_center_circle, clamp_start.y_center_circle,
                        clamp_end.x_center_circle, clamp_end.y_center_circle)

                    wire = Wire(canvas__, x_start_wire, y_start_wire, x_end_wire, y_end_wire, clamp_start,
                                clamp_end, WIDTH_WIRES, COLOR_HIGHLIGHT, COLOR_LINES)
                    wire.make_wire()
                    wires__.append(wire)
                    wire.number_in_list = len(wires__) - 1
                    canvas__.tag_bind(wire.figure_id, '<Button-1>', press_left_btn_mouse_on_wire)

                    init_moving_line(canvas__, clamp_end, event.x, event.y)

        canvas__.tag_bind(clamp.figure_id, '<Button-1>', press_left_btn_mouse_on_clamp)

    for row in range(rows):
        for col in range(columns):
            making_wires(canvas, clamps__[row][col], clamps__, wires_)


moving_wire_line = None
flag_element_highlighted = False

wires = []
binding_clamps_for_making_wires(WORKSPACE, CLAMPS, NUMBER_CLAMP_ROWS, NUMBER_CLAMP_COLUMNS, wires)
