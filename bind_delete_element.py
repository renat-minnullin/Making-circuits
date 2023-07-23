def bind_element_to_click(element_of_class):
    from make_display import root, WORKSPACE
    canvas = WORKSPACE
    for id_piece_element in element_of_class.elements_ids:
        canvas.tag_bind(id_piece_element, '<Button-1>',
                        lambda element: click_left_btn_mouse_on_element(element_of_class))

    def click_left_btn_mouse_on_element(element):
        """Подпрограмма отработки события нажатия на провод"""

        def delete_highlighted_element(event_press_delete):
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
                """Подпрограмма перезаписывания порядка нумерации элементов в списке (смещены из-за удаления
                одного из экземпляров"""
                for num in range(len(list_elements)):
                    list_elements[num].number_in_list = num

            def delete_lines(elems_ids):
                for id_piece_elem in elems_ids:
                    canvas.delete(id_piece_elem)

            def define_list_objects_like_element(elem):
                name_class_element = elem.__class__.__name__

                if name_class_element == 'Wire':
                    from make_circuit_by_user import WIRES
                    list_elems = WIRES
                elif name_class_element == 'Resistor':
                    from make_circuit_by_user import RESISTORS
                    list_elems = RESISTORS
                else:
                    list_elems = ['MISTAKE']
                return list_elems

            # ---Вход при нажатии клавиши DELETE при выделенном проводе---
            from make_circuit_by_user import element_highlighted

            if element_highlighted[0]:
                reload_massive_clamped_clamps(element.clamp_start, element.clamp_end)

                delete_clamps_connections(element.clamp_start, element.clamp_end)

                delete_lines(element.elements_ids)

                list_elements = define_list_objects_like_element(element)

                list_elements.remove(element)

                reload_wire_numbers_in_list()

                element.__del__()
                root.unbind('<Delete>')
                element_highlighted[0] = None

        def exchange_color_element_lines(elems_ids, color):
            for id_piece_elem in elems_ids:
                canvas.itemconfig(id_piece_elem, fill=color)

        from make_circuit_by_user import element_highlighted

        if element_highlighted[0]:
            # ---Вход смене выделенного элемента---

            canvas.itemconfig(element_highlighted[0].elements_ids[0],
                              fill=element.color_lines)
            element_highlighted[0].flag_highlighted_now = False
            element_highlighted[0] = element

        # ---Вход при первом выделении элемента---

        element.flag_highlighted_now = True
        element_highlighted[0] = element
        exchange_color_element_lines(element_highlighted[0].elements_ids, element_highlighted[0].color_highlight)

        root.bind('<Delete>', delete_highlighted_element)
