from make_display import CLAMPS, WORKSPACE
from classes_elements import Wire, Resistor


def binding_btns_of_group(idx_group, idx_element_in_list):
    """Подпрограмма создает функции для кнопок группы, которые в данный момент открыты на экране"""

    def define_highlighted_wire():
        """Подпрограмма определяет экземпляр класса Wire, который в данный момент подсвечен"""
        from input_and_output_buffer import input_highlighted_wire
        global WIRES
        num_highlighted_wire = input_highlighted_wire()
        highlighted_wire_ = WIRES[num_highlighted_wire]
        return highlighted_wire_

    def hide_highlighted_wire(highlighted_wire_):
        """Подпрограмма скрывает провод, на который крепится элемент"""
        canvas = highlighted_wire_.canvas
        canvas.itemconfig(highlighted_wire_.elements_ids[0], state='hidden')

    def binding_btns_of_resistive_elements(idx_elem_in_list):
        """Подпрограмма создает функции для кнопок группы Резистивные элементы (индекс 0)"""
        highlighted_wire = define_highlighted_wire()

        if idx_elem_in_list == 0:
            global RESISTORS

            hide_highlighted_wire(highlighted_wire)
            resistor = Resistor(highlighted_wire.canvas, highlighted_wire.x_start, highlighted_wire.y_start,
                                highlighted_wire.x_end, highlighted_wire.y_end, highlighted_wire.normal_length,
                                highlighted_wire.clamp_start, highlighted_wire.clamp_end, highlighted_wire.width_lines,
                                highlighted_wire.color_highlight,
                                highlighted_wire.color_lines, highlighted_wire)
            resistor.draw()
            RESISTORS.append(resistor)

        elif idx_elem_in_list == 1:
            pass
        elif idx_elem_in_list == 2:
            pass

    def binding_btns_of_sources(idx_elem_in_list):
        highlighted_wire = define_highlighted_wire()

    def binding_btns_of_nonlinear_elements(idx_elem_in_list):
        highlighted_wire = define_highlighted_wire()

    def binding_btns_of_other(idx_elem_in_list):
        highlighted_wire = define_highlighted_wire()

    global flag_element_highlighted, flag_quick_frame_highlighted

    if flag_element_highlighted:

        if idx_group == 0:
            binding_btns_of_resistive_elements(idx_element_in_list)

        elif idx_group == 1:
            binding_btns_of_sources(idx_element_in_list)
        elif idx_group == 2:
            binding_btns_of_nonlinear_elements(idx_element_in_list)
        elif idx_group == 3:
            binding_btns_of_other(idx_element_in_list)
    elif flag_quick_frame_highlighted:
        pass


def binding_clamps_for_making_wires(canvas, wires, clamps):
    """Подпрограмма запускает метод биндинга для рисования проводов"""

    def bind_one_clamp_for_making_wires(clicked_clamp):
        def click_left_btn_mouse_on_clamp(event_click_clamp):
            """Подпрограмма события нажатия на зажим"""

            def delete_acceptable_clamps():
                """Подпрограмма удаляет созданные подсвеченные круги зажимов"""
                from input_and_output_buffer import input_clamps_r_c_acceptable_highlighting
                clamps_row_col_acceptable_highlighting = input_clamps_r_c_acceptable_highlighting()
                for coord in clamps_row_col_acceptable_highlighting:
                    r = coord[0]
                    c = coord[1]
                    canvas.itemconfig(clamps[r][c].elements_ids[0], outline=clicked_clamp.color_outline)

            def flag_acceptable_clamp(clicked_clamp_, start_r, start_c):
                """Подпрограмма проверяет прожатый зажим на возможность нажатия"""
                from input_and_output_buffer import input_clamps_r_c_acceptable_highlighting
                clamps_row_col_acceptable_highlighting = input_clamps_r_c_acceptable_highlighting()
                fl_accept_clamp = [clicked_clamp_.row, clicked_clamp_.column] in clamps_row_col_acceptable_highlighting
                fl_not_repeat_wire = [clicked_clamp_.row, clicked_clamp_.column] not in clamps[start_r][
                    start_c].list_row_col_connected_clamps

                if fl_accept_clamp and fl_not_repeat_wire:
                    return True
                else:
                    return False

            def delete_moving_line(event):
                """Подпрограмма останавливает рисование провода и удаляет линию"""
                from input_and_output_buffer import input_id_moving_line
                global moving_wire_line, flag_moving_line_created
                moving_wire_line = input_id_moving_line()

                canvas.delete(moving_wire_line)
                canvas.unbind('<Motion>')
                root.unbind('<Escape>')
                moving_wire_line = None
                canvas.itemconfig(clicked_clamp.elements_ids[0], outline=clicked_clamp.color_outline)
                delete_acceptable_clamps()
                flag_moving_line_created = False

            def add_numbers_clamped_clamps(start_row, start_col, end_row, end_col):
                """Подпрограмма записывает данные зажатых зажимов"""

                from input_and_output_buffer import input_massive_clamped_clamps, output_massive_clamped_clamps
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

            def init_moving_line(clamp_start_, x_mouse, y_mouse):
                """Подпрограмма инициализирует движущую линию"""

                def make_acceptable_clamp_highlighting(clamp_):
                    """Подпрограмма создает подсвеченные круги зажимов, а также массив с их координатами"""

                    def output_clamps_r_c_acceptable_highlighting(clamps_r_c_acceptable_highlighting):
                        """Подпрограмма выводит в файл массив координат подсвеченных(доступных для нажатия) зажимов"""
                        from paths_for_buffer_files import path_buffer_row_col_acceptable_clamps
                        fout = open(path_buffer_row_col_acceptable_clamps, 'w')
                        for coord in clamps_r_c_acceptable_highlighting:
                            r_x = coord[0]
                            c_x = coord[1]
                            fout.write(str(r_x) + '-' + str(c_x) + ' ')
                        fout.close()

                    from options_visualization import COLOR_HIGHLIGHT

                    clamps_row_col_acceptable_highlighting = []

                    for i in range(3):
                        for j in range(3):
                            r = clamp_.row + i - 1
                            c = clamp_.column + j - 1
                            if not (r == clamp_.row and c == clamp_.column) \
                                    and 0 <= r < len(clamps) \
                                    and 0 <= c < len(clamps[0]) \
                                    and [clamp_.row, clamp_.column] not in clamps[r][
                                c].list_row_col_connected_clamps:
                                canvas.itemconfig(clamps[r][c].elements_ids[0], outline=COLOR_HIGHLIGHT)
                                clamps_row_col_acceptable_highlighting.append([r, c])

                    output_clamps_r_c_acceptable_highlighting(clamps_row_col_acceptable_highlighting)

                def moving_line_with_mouse(event_moving_mouse):
                    """Подпрограмма поддерживает движение линии за курсором мыши"""
                    from input_and_output_buffer import input_id_moving_line, output_id_moving_line, \
                        output_r_c_start_clamp
                    mov_wire_line = input_id_moving_line()
                    canvas.delete(mov_wire_line)

                    if event_moving_mouse.x < clicked_clamp.x_center_circle and event_moving_mouse.y < clicked_clamp.y_center_circle:
                        mouse_indent_x = event_moving_mouse.x + 3
                        mouse_indent_y = event_moving_mouse.y + 3
                    else:
                        mouse_indent_x = event_moving_mouse.x - 3
                        mouse_indent_y = event_moving_mouse.y - 3

                    mov_wire_line = canvas.create_line(clicked_clamp.x_center_circle, clicked_clamp.y_center_circle,
                                                       mouse_indent_x, mouse_indent_y, width=1)
                    output_id_moving_line(mov_wire_line)
                    output_r_c_start_clamp(clicked_clamp)

                from make_display import root
                from input_and_output_buffer import output_id_moving_line, output_r_c_start_clamp
                global moving_wire_line, flag_moving_line_created
                flag_moving_line_created = True
                make_acceptable_clamp_highlighting(clamp_start_)
                moving_wire_line = canvas.create_line(clamp_start_.x_center_circle,
                                                      clamp_start_.y_center_circle,
                                                      x_mouse, y_mouse, width=1)
                output_id_moving_line(moving_wire_line)
                output_r_c_start_clamp(clamp_start_)

                canvas.bind('<Motion>', moving_line_with_mouse)
                root.bind('<Escape>', delete_moving_line)

            def init_wire(clamp_start_, clamp_end_):
                """Подпрограмма создает провод на представленных зажимах"""

                def click_left_btn_mouse_on_wire(event_click_wire):
                    """Подпрограмма отработки события нажатия на провод"""

                    def delete_highlighted_wire(event):
                        """Подпрограмма удаляет выделенный провод"""

                        def reload_massive_clamped_clamps(clamp_start_x, clamp_end_x):
                            """Подпрограмма перезаписывает данные зажатых зажимов"""
                            from paths_for_buffer_files import path_buffer_massive_clamped_clamps

                            fin_clamped_clamps = open(path_buffer_massive_clamped_clamps, 'r')
                            massive_clamped_clamps = fin_clamped_clamps.readline().split()
                            fin_clamped_clamps.close()

                            fout_clamped_clamps = open(path_buffer_massive_clamped_clamps, 'w')
                            if clamp_start_x.number_connected_wires == 1:
                                massive_clamped_clamps.remove(
                                    str(clamp_start_x.row) + '-' + str(clamp_start_x.column))
                            if clamp_end_x.number_connected_wires == 1:
                                massive_clamped_clamps.remove(str(clamp_end_x.row) + '-' + str(clamp_end_x.column))
                            set_massive_clamped_clamps = set(massive_clamped_clamps)
                            sort_set_massive_clamped_clamps = sorted(set_massive_clamped_clamps)
                            for i in range(len(sort_set_massive_clamped_clamps)):
                                fout_clamped_clamps.write(sort_set_massive_clamped_clamps[i] + ' ')
                            fout_clamped_clamps.close()

                        def delete_clamps_connections(clamp_start_x, clamp_end_x):
                            """Подпрограмма удаляет связь между двумя зажимами, составляющими удаленный провод"""

                            clamp_start_x.list_row_col_connected_clamps.remove([clamp_end_x.row, clamp_end_x.column])
                            clamp_start_x.number_connected_wires -= 1

                            clamp_end_x.list_row_col_connected_clamps.remove([clamp_start_x.row, clamp_start_x.column])
                            clamp_end_x.number_connected_wires -= 1

                        def reload_wire_numbers_in_list():
                            """Подпрограмма перезаписывания порядка нумерации проводов в списке (смещены из-за удаления
                            одного из проводов"""
                            for num in range(len(wires)):
                                wires[num].number_in_list = num

                        # ---Вход при нажатии клавиши DELETE при выделенном проводе---
                        from input_and_output_buffer import input_highlighted_wire, output_highlighted_wire
                        from paths_for_buffer_files import path_buffer_highlighted_wire
                        global flag_element_highlighted
                        if flag_element_highlighted:
                            num_highlight_wire = input_highlighted_wire()

                            wire_x = wires[num_highlight_wire]

                            output_highlighted_wire('')

                            reload_massive_clamped_clamps(wire_x.clamp_start, wire_x.clamp_end)

                            delete_clamps_connections(wire_x.clamp_start, wire_x.clamp_end)

                            canvas.delete(wire_x.elements_ids[0])
                            wires.remove(wire_x)

                            reload_wire_numbers_in_list()

                            wire_x.__del__()
                            root.unbind('<Delete>')
                            flag_element_highlighted = False

                    from input_and_output_buffer import input_highlighted_wire, output_highlighted_wire
                    global flag_element_highlighted
                    if flag_element_highlighted:
                        # ---Вход смене выделенного провода---
                        num_highlighted_wire = input_highlighted_wire()

                        canvas.itemconfig(wires[num_highlighted_wire].elements_ids[0],
                                          fill=wires[num_highlighted_wire].color_lines)
                        wires[num_highlighted_wire].flag_highlighted_now = False
                        output_highlighted_wire(wires[num_highlighted_wire].number_in_list)

                    # ---Вход при первом выделении провода---
                    output_highlighted_wire(wire.number_in_list)

                    canvas.itemconfig(wire.elements_ids[0], fill=wire.color_highlight)
                    wire.flag_highlighted_now = True
                    flag_element_highlighted = True

                    root.bind('<Delete>', delete_highlighted_wire)

                from drawing_elements import calculating_intend_at_center
                from options_visualization import NORMAL_LENGTH
                x_start_wire, y_start_wire, x_end_wire, y_end_wire = calculating_intend_at_center(
                    clamp_start_.radius_circle, clamp_start_.x_center_circle, clamp_start_.y_center_circle,
                    clamp_end_.x_center_circle, clamp_end_.y_center_circle)

                wire = Wire(canvas, x_start_wire, y_start_wire, x_end_wire, y_end_wire, NORMAL_LENGTH, clamp_start_,
                            clamp_end_, WIDTH_WIRES, COLOR_HIGHLIGHT, COLOR_LINES)
                wire.draw()
                wires.append(wire)
                wire.number_in_list = len(wires) - 1
                canvas.tag_bind(wire.elements_ids[0], '<Button-1>', click_left_btn_mouse_on_wire)

            from make_display import root
            from options_visualization import WIDTH_WIRES, COLOR_HIGHLIGHT, COLOR_LINES
            from input_and_output_buffer import input_id_moving_line, input_r_c_start_clamp
            global moving_wire_line

            if moving_wire_line is None:
                init_moving_line(clicked_clamp, event_click_clamp.x, event_click_clamp.y)
            else:
                moving_wire_line = input_id_moving_line()
                start_clamp_row, start_clamp_column = input_r_c_start_clamp()
                clamp_start = clamps[start_clamp_row][start_clamp_column]
                clamp_end = clicked_clamp

                if flag_acceptable_clamp(clamp_end, start_clamp_row, start_clamp_column):
                    clamp_end.list_row_col_connected_clamps.append([clamp_start.row, clamp_start.column])
                    clamp_start.list_row_col_connected_clamps.append([clamp_end.row, clamp_end.column])
                    clamp_end.number_connected_wires += 1
                    clamp_start.number_connected_wires += 1

                    add_numbers_clamped_clamps(clamp_start.row, clamp_start.column, clamp_end.row,
                                               clamp_end.column)
                    delete_moving_line(0)  # ноль добавлен для аннулирования параметра event_click_clamp

                    init_wire(clamp_start, clamp_end)

                    init_moving_line(clamp_end, event_click_clamp.x, event_click_clamp.y)

        canvas.tag_bind(clicked_clamp.elements_ids[0], '<Button-1>', click_left_btn_mouse_on_clamp)

    for row in range(len(clamps)):
        for col in range(len(clamps[0])):
            bind_one_clamp_for_making_wires(clamps[row][col])


moving_wire_line = None
flag_element_highlighted = False
flag_quick_frame_highlighted = False
flag_moving_line_created = False

WIRES = []
RESISTORS = []
binding_clamps_for_making_wires(WORKSPACE, WIRES, CLAMPS)
