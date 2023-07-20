from make_display import CLAMPS, WORKSPACE
from classes_elements import Wire


def binding_btns_of_group(idx_group, idx_element):
    """Подпрограмма создает функции для кнопок группы, которые в данный момент открыты на экране"""
    idx_class = str(idx_group) + '_' + str(idx_element)

def binding_clamps_for_making_wires(canvas, wires, clamps):
    """Подпрограмма запускает метод биндинга для рисования проводов"""

    def bind_one_clamp_for_making_wires(clicked_clamp):
        def click_left_btn_mouse_on_clamp(event_press_clamp):
            """Подпрограмма события нажатия на зажим"""

            def input_clamps_r_c_acceptable_highlighting():
                """Подпрограмма вводит из файла массив координат подсвеченных(доступных для нажатия) зажимов"""
                from paths_for_buffer_files import path_buffer_row_col_acceptable_clamps

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

            def delete_acceptable_clamps():
                """Подпрограмма удаляет созданные подсвеченные круги зажимов"""
                clamps_row_col_acceptable_highlighting = input_clamps_r_c_acceptable_highlighting()
                for coord in clamps_row_col_acceptable_highlighting:
                    r = coord[0]
                    c = coord[1]
                    canvas.itemconfig(clamps[r][c].elements_ids[0], outline=clicked_clamp.color_outline)

            def flag_acceptable_clamp(clicked_clamp_, start_r, start_c):
                """Подпрограмма проверяет прожатый зажим на возможность нажатия"""
                clamps_row_col_acceptable_highlighting = input_clamps_r_c_acceptable_highlighting()
                fl_accept_clamp = [clicked_clamp_.row, clicked_clamp_.column] in clamps_row_col_acceptable_highlighting
                fl_not_repeat_wire = [clicked_clamp_.row, clicked_clamp_.column] not in clamps[start_r][
                    start_c].list_row_col_connected_clamps

                if fl_accept_clamp and fl_not_repeat_wire:
                    return True
                else:
                    return False

            def input_id_moving_line():
                """Подпрограмма вводит из файла id движущейся линии"""
                from paths_for_buffer_files import path_buffer_id_moving_line

                fin = open(path_buffer_id_moving_line, 'r')
                mov_w_line = int(fin.readline().split()[0])
                fin.close()
                return mov_w_line

            def input_r_c_start_clamp():
                """Подпрограмма вводит из файла координаты начального зажима (row, col)"""
                from paths_for_buffer_files import path_buffer_row_col_start_clamp
                fin = open(path_buffer_row_col_start_clamp, 'r')
                row_and_col = fin.readline().split()
                clamp_row, clamp_column = int(row_and_col[0]), int(row_and_col[1])
                fin.close()
                return clamp_row, clamp_column

            def output_id_moving_line(moving_line):
                """Подпрограмма выводит в файл id движущейся линии"""
                from paths_for_buffer_files import path_buffer_id_moving_line
                fout = open(path_buffer_id_moving_line, 'w')
                fout.write(str(moving_line))
                fout.close()

            def output_r_c_start_clamp(clicked_clamp_):
                """Подпрограмма выводит в файл координаты начального зажима (row, col)"""
                from paths_for_buffer_files import path_buffer_row_col_start_clamp
                fout = open(path_buffer_row_col_start_clamp, 'w')
                fout.write(str(clicked_clamp_.row) + ' ' + str(clicked_clamp_.column) + '\n')
                fout.close()

            def delete_moving_line(event):
                """Подпрограмма останавливает рисование провода и удаляет линию"""

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

                def input_massive_clamped_clamps():
                    """Подпрограмма вводит из файла массив зажатых зажимов"""
                    from paths_for_buffer_files import path_buffer_massive_clamped_clamps
                    fin = open(path_buffer_massive_clamped_clamps, 'r')
                    mas_clamped_cls = fin.readline().split()
                    fin.close()
                    return mas_clamped_cls

                def output_massive_clamped_clamps(sort_mas_clamped_cls):
                    """Подпрограмма выводит в файл массив зажатых зажимов"""
                    from paths_for_buffer_files import path_buffer_massive_clamped_clamps
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

                def press_left_btn_mouse_on_wire(event_press_wire):
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
                        from paths_for_buffer_files import path_buffer_highlighted_wire
                        global flag_element_highlighted
                        if flag_element_highlighted:
                            fin_highlighted_wire = open(path_buffer_highlighted_wire, 'r')
                            fin_highlighted_wire.readline()
                            num_highlight_wire = int(fin_highlighted_wire.readline().split()[0])
                            fin_highlighted_wire.close()

                            wire_x = wires[num_highlight_wire]

                            fout_highlighted_wire = open(path_buffer_highlighted_wire, 'w')
                            fout_highlighted_wire.write('Номер провода в списке проводов:\n')
                            fout_highlighted_wire.close()

                            reload_massive_clamped_clamps(wire_x.clamp_start, wire_x.clamp_end)

                            delete_clamps_connections(wire_x.clamp_start, wire_x.clamp_end)

                            canvas.delete(wire_x.elements_ids[0])
                            wires.remove(wire_x)

                            reload_wire_numbers_in_list()

                            wire_x.__del__()
                            root.unbind('<Delete>')
                            flag_element_highlighted = False

                    from paths_for_buffer_files import path_buffer_highlighted_wire
                    global flag_element_highlighted
                    if flag_element_highlighted:
                        # ---Вход смене выделенного провода---
                        fin = open(path_buffer_highlighted_wire, 'r')
                        fin.readline()
                        num_highlighted_wire = int(fin.readline().split()[0])
                        fin.close()

                        canvas.itemconfig(wires[num_highlighted_wire].elements_ids[0],
                                          fill=wires[num_highlighted_wire].color_fill)
                        wires[num_highlighted_wire].flag_highlighted_now = False

                        fout = open(path_buffer_highlighted_wire, 'w')
                        fout.write('Номер провода в списке проводов:\n')
                        fout.write(str(wires[num_highlighted_wire].number_in_list))
                        fout.close()

                    # ---Вход при первом выделении провода---
                    fout = open(path_buffer_highlighted_wire, 'w')
                    fout.write('Номер провода в списке проводов:\n')
                    fout.write(str(wire.number_in_list))
                    fout.close()

                    canvas.itemconfig(wire.elements_ids[0], fill=wire.color_pressed)
                    wire.flag_highlighted_now = True
                    flag_element_highlighted = True

                    root.bind('<Delete>', delete_highlighted_wire)

                x_start_wire, y_start_wire, x_end_wire, y_end_wire = calculating_intend_at_center(
                    clamp_start_.radius_circle, clamp_start_.x_center_circle, clamp_start_.y_center_circle,
                    clamp_end_.x_center_circle, clamp_end_.y_center_circle)

                wire = Wire(canvas, x_start_wire, y_start_wire, x_end_wire, y_end_wire, clamp_start_,
                            clamp_end_, WIDTH_WIRES, COLOR_HIGHLIGHT, COLOR_LINES)
                wire.draw()
                wires.append(wire)
                wire.number_in_list = len(wires) - 1
                canvas.tag_bind(wire.elements_ids[0], '<Button-1>', press_left_btn_mouse_on_wire)

            from make_display import root
            from options_visualization import WIDTH_WIRES, COLOR_HIGHLIGHT, COLOR_LINES
            global moving_wire_line

            if moving_wire_line is None:
                init_moving_line(clicked_clamp, event_press_clamp.x, event_press_clamp.y)
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
                    delete_moving_line(0)  # ноль добавлен для аннулирования параметра event_press_clamp

                    init_wire(clamp_start, clamp_end)

                    init_moving_line(clamp_end, event_press_clamp.x, event_press_clamp.y)

        canvas.tag_bind(clicked_clamp.elements_ids[0], '<Button-1>', click_left_btn_mouse_on_clamp)

    for row in range(len(clamps)):
        for col in range(len(clamps[0])):
            bind_one_clamp_for_making_wires(clamps[row][col])


moving_wire_line = None
flag_element_highlighted = False
flag_moving_line_created = False

WIRES = []
binding_clamps_for_making_wires(WORKSPACE, WIRES, CLAMPS)
