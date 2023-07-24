from make_display import CLAMPS, WORKSPACE
from classes_elements import Wire, Resistor, Capacitor, Inductor_Coil


def bind_areas_of_quick_access_exchange_color(clicked_area_q_a, areas_q_a):
    """Подпрограмма биндит область быстрого доступа на нажатие"""
    from options_visualization import COLOR_HIGHLIGHT, COLOR_BG_WORKSPACE
    global area_quick_access_highlighted, element_highlighted, moving_wire_line
    if moving_wire_line is None:
        if element_highlighted[0]:
            element_highlighted[0].exchange_color(element_highlighted[0].color_lines)
            element_highlighted[0] = None

        if area_quick_access_highlighted[0]:
            area_quick_access_highlighted[0].config(area_quick_access_highlighted[0], bg=COLOR_BG_WORKSPACE)
            area_quick_access_highlighted[0] = clicked_area_q_a
            clicked_area_q_a.config(clicked_area_q_a, bg=COLOR_HIGHLIGHT)
        else:
            area_quick_access_highlighted[0] = clicked_area_q_a
            clicked_area_q_a.config(bg=COLOR_HIGHLIGHT)


def binding_btns_of_group(idx_group, idx_element_in_list, areas_q_a):
    """Подпрограмма создает функции для кнопок группы, которые в данный момент открыты на экране"""

    def hide_highlighted_wire(hl_wire_):
        """Подпрограмма скрывает провод, на который крепится элемент"""
        canvas = hl_wire_.canvas
        canvas.itemconfig(hl_wire_.elements_ids[0], state='hidden')

    def bind_one_btn(hl_wire, Class_element, list_elements_of_the_class):
        from bind_the_element_to_click import bind_element_to_click
        element_of_the_class = Class_element(hl_wire.canvas, hl_wire.x_start, hl_wire.y_start,
                                             hl_wire.x_end, hl_wire.y_end, hl_wire.normal_length,
                                             hl_wire.clamp_start, hl_wire.clamp_end, hl_wire.width_lines,
                                             hl_wire.color_highlight,
                                             hl_wire.color_lines, hl_wire)
        element_of_the_class.draw()
        list_elements_of_the_class.append(element_of_the_class)
        bind_element_to_click(element_of_the_class, list_elements_of_the_class)

    def binding_btns_of_resistive_elements(idx_elem_in_list, highlight_wire):
        """Подпрограмма создает функции для кнопок группы Резистивные элементы (индекс 0)"""

        hide_highlighted_wire(highlight_wire)
        if idx_elem_in_list == 0:
            global RESISTORS
            bind_one_btn(highlight_wire, Resistor, RESISTORS)
        elif idx_elem_in_list == 1:
            global INDUCTOR_COILS
            bind_one_btn(highlight_wire, Inductor_Coil, INDUCTOR_COILS)
        elif idx_elem_in_list == 2:
            global CAPACITORS
            bind_one_btn(highlight_wire, Capacitor, CAPACITORS)

    def binding_btns_of_sources(idx_elem_in_list, hl_wire):
        pass

    def binding_btns_of_nonlinear_elements(idx_elem_in_list, hl_wire):
        pass

    def binding_btns_of_other(idx_elem_in_list, hl_wire):
        pass

    global element_highlighted, area_quick_access_highlighted

    if element_highlighted[0].__class__.__name__ == 'Wire':
        highlighted_wire = element_highlighted[0]
        if idx_group == 0:
            binding_btns_of_resistive_elements(idx_element_in_list, highlighted_wire)
        elif idx_group == 1:
            binding_btns_of_sources(idx_element_in_list, highlighted_wire)
        elif idx_group == 2:
            binding_btns_of_nonlinear_elements(idx_element_in_list, highlighted_wire)
        elif idx_group == 3:
            binding_btns_of_other(idx_element_in_list, highlighted_wire)
    elif area_quick_access_highlighted[0]:
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

                from drawing_elements import calculating_intend_at_center
                from options_visualization import NORMAL_LENGTH
                from bind_the_element_to_click import bind_element_to_click

                x_start_wire, y_start_wire, x_end_wire, y_end_wire = calculating_intend_at_center(
                    clamp_start_.radius_circle, clamp_start_.x_center_circle, clamp_start_.y_center_circle,
                    clamp_end_.x_center_circle, clamp_end_.y_center_circle)

                wire = Wire(canvas, x_start_wire, y_start_wire, x_end_wire, y_end_wire, NORMAL_LENGTH, clamp_start_,
                            clamp_end_, WIDTH_WIRES, COLOR_HIGHLIGHT, COLOR_LINES)
                wire.draw()
                wires.append(wire)

                bind_element_to_click(wire, wires)

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
element_highlighted = [None]
area_quick_access_highlighted = [None]
flag_moving_line_created = False

WIRES = []
RESISTORS = []
CAPACITORS = []
INDUCTOR_COILS = []
binding_clamps_for_making_wires(WORKSPACE, WIRES, CLAMPS)
