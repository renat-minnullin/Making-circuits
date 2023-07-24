def bind_element_to_click(element_of_class, list_elements_of_class):
    """Подпрограмма отрабатывает нажатие по любой части элемента и биндит его удаление или переключение"""
    from make_display import root, WORKSPACE
    canvas = WORKSPACE

    for id_piece_element in element_of_class.elements_ids:
        canvas.tag_bind(id_piece_element, '<Button-1>',
                        lambda element: click_left_btn_mouse_on_element(element_of_class, list_elements_of_class))

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
            from make_circuit_by_user import element_highlighted

            if element_highlighted[0]:

                delete_all_part_of_element(element.elements_ids)

                list_elements_class.remove(element)

                if element.__class__.__name__ == 'Wire':
                    reload_massive_clamped_clamps(element.clamp_start, element.clamp_end)
                    delete_clamps_connections(element.clamp_start, element.clamp_end)
                else:
                    canvas.itemconfig(element.own_wire.elements_ids[0], state='normal')

                element.__del__()
                root.unbind('<Delete>')
                element_highlighted[0] = None

        def exchange_all_part_of_element_color(elems_ids, color):
            """Подпрограмма заменяет цвет всех частей элемента"""
            for id_piece_elem in elems_ids:
                tags = canvas.gettags(id_piece_elem)

                if 'line' in tags:
                    canvas.itemconfig(id_piece_elem, fill=color)
                elif 'arc' or 'oval' in tags:
                    canvas.itemconfig(id_piece_elem, outline=color)

        from options_visualization import COLOR_BG_WORKSPACE
        from make_circuit_by_user import element_highlighted, area_quick_access_highlighted

        if area_quick_access_highlighted[0]:
            area_quick_access_highlighted[0].config(area_quick_access_highlighted[0], bg=COLOR_BG_WORKSPACE)
            area_quick_access_highlighted[0] = None

        elif element_highlighted[0]:
            element_highlighted[0].exchange_color(element_highlighted[0].color_lines)

        element.exchange_color(element.color_highlight)
        element_highlighted[0] = element
        root.bind('<Delete>', delete_highlighted_element)
