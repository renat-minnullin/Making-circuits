def bind_element_to_click(element_of_class, list_elements_of_class):
    """Подпрограмма отрабатывает нажатие по любой части элемента и биндит его удаление или переключение"""

    def click_left_btn_mouse_on_element(element, list_elements_class):
        """Подпрограмма отработки события нажатия на элемент"""

        def delete_highlighted_element(event_press_delete):
            """Подпрограмма удаляет выделенный элемент"""

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

            def delete_all_part_of_element(elems_ids):
                """Подпрограмма удаляет все части элемента"""
                for id_piece_elem in elems_ids:
                    canvas.delete(id_piece_elem)

            # ---Вход при нажатии клавиши DELETE при выделенном элементе---
            from make_circuit_by_user import element_highlighted, BRANCHES
            from reload_dates import reload_branches_when_deleting_wire

            if element_highlighted[0]:

                delete_all_part_of_element(element.elements_ids)
                canvas.delete(element.title_element_id)

                list_elements_class.remove(element)

                if element.__class__.__name__ == 'Wire':
                    reload_massive_clamped_clamps(element.clamp_start, element.clamp_end)
                    reload_branches_when_deleting_wire(BRANCHES, element)
                    delete_clamps_connections(element.clamp_start, element.clamp_end)
                else:
                    canvas.itemconfig(element.own_wire.elements_ids[0], state='normal')

                element.__del__()
                root.unbind('<Delete>')
                element_highlighted[0] = None

        from options_visualization import COLOR_BG_WORKSPACE
        from make_display import FRAME_INFO_ABOUT_ELEMENT
        from make_circuit_by_user import element_highlighted, area_quick_access_highlighted, moving_wire_line
        if moving_wire_line is None:
            if area_quick_access_highlighted[0]:
                area_quick_access_highlighted[0].config(area_quick_access_highlighted[0], bg=COLOR_BG_WORKSPACE)
                area_quick_access_highlighted[0] = None

            elif element_highlighted[0]:
                element_highlighted[0].exchange_color(element_highlighted[0].color_lines)

            frame_info = FRAME_INFO_ABOUT_ELEMENT
            frame_info.highlighted_element = element
            frame_info.exchange_name_element(element.name)
            frame_info.reload_state_entries(element.accesses_to_change)
            frame_info.btn_save_parameters.config(state='normal')
            frame_info.reload_values_of_parameters(element.parameters)

            element.exchange_color(element.color_highlight)
            element_highlighted[0] = element
            root.bind('<Delete>', delete_highlighted_element)

    def click_double_left_btn_mouse_on_element(element):
        """Подпрограмма отрабатывает двойное нажатие левой кнопкой мыши по элементу, благодаря которому на элементе либо
        появляется направление графа, в случае, если такого направления не было, либо меняется на противоположное, если
        такое направление было"""

        def set_the_direction(element_, wire_, branch_of_wire_):
            """Подпрограмма устанавливает направление провода и передает его на всю ветвь"""
            wire_.create_direction(element_.elements_ids)
            branch_of_wire_.arrow_direction = 'last'
            branch_of_wire_.main_wire = wire_

        def change_the_direction(element_, wire_, branch_of_wire_):
            """Подпрограмма изменяет уже установленное направление провода и ветви на противоположное"""
            branch_of_wire_.main_wire.delete_direction(element_.elements_ids)
            branch_of_wire_.main_wire = wire_
            branch_of_wire_.change_direction()
            wire_.change_direction(element_.elements_ids, branch_of_wire_.arrow_direction)

        from make_circuit_by_user import BRANCHES

        if element.__class__.__name__ == 'Wire':
            wire = element
        else:
            wire = element.own_wire

        branch_of_wire = wire.branch
        if branch_of_wire.arrow_direction == '':
            set_the_direction(element, wire, branch_of_wire)
        else:
            change_the_direction(element, wire, branch_of_wire)

    from make_display import root, WORKSPACE
    canvas = WORKSPACE

    for id_piece_element in element_of_class.elements_ids:
        canvas.tag_bind(id_piece_element, '<Button-1>',
                        lambda element: click_left_btn_mouse_on_element(element_of_class, list_elements_of_class))
        canvas.tag_bind(id_piece_element, '<Double-Button-1>',
                        lambda element: click_double_left_btn_mouse_on_element(element_of_class))
