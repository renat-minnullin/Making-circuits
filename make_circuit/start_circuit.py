from make_display import BUTTON_RUN, CLAMPS, root


def working_circuit(btn_run_circuit, clamps):
    """Подпрограмма, отвечающая за работу с распознаванием цепи и созданием соответствующих таблиц"""

    def click_run_btn():
        """Подпрограмма отвечает за отклик на кнопку запуска цепи и анализ созданной цепи"""

        def exchange_state_running(fl_running):
            """Подпрограмма отвечает за изменение цвета кнопки ПУСК и флага состояния"""
            if fl_running is False:
                fl_running = True
                btn_run_circuit.configure(bg='green')
            else:
                fl_running = False
                btn_run_circuit.configure(bg='grey')
            return fl_running

        def testing_circuit():
            """Подпрограмма необходима, для анализа созданной цепи: проверяются элементы на разных уровнях от зажатого зажима
            до ветви и выдается ошибка в случае несоответствия"""

            def analise_clamped_clamps(massive_row_col_clamped_clamps):
                """Подпрограмма анализирует созданный в ходе рисования массив зажатых зажимов на возможные ошибки"""
                fl_err = False
                txt_err = 'Not error'

                if len(massive_row_col_clamped_clamps) == 0:
                    fl_err = True
                    txt_err = 'Ошибка! Не зажато ни одного зажима'
                elif len(massive_row_col_clamped_clamps) == 1:
                    fl_err = True
                    txt_err = 'Ошибка! Зажат только один зажим'
                else:
                    i = 0
                    while fl_err is False and i < len(massive_row_col_clamped_clamps):
                        row = massive_row_col_clamped_clamps[i][0]
                        col = massive_row_col_clamped_clamps[i][1]
                        if clamps[row][col].number_connected_wires == 0:
                            fl_err = True
                            txt_err = 'Непредвиденная ошибка! Число присоединенных проводов к одному из зажимов равно нулю'

                        elif clamps[row][col].number_connected_wires == 1:
                            fl_err = True
                            txt_err = 'Ошибка! Цепь не замкнута. Число присоединенных проводов к одному из зажимов равно единице'
                        elif clamps[row][col].number_connected_wires >= 9:
                            fl_err = True
                            txt_err = 'Непредвиденная ошибка! Число присоединенных проводов к одному из зажимов больше либо ' \
                                      'равно девяти (максимальное возможное число - восемь)'
                        else:
                            i += 1

                return fl_err, txt_err

            def analise_nodes(massive_row_col_nodes):
                """Подпрограмма анализирует массив узлов на возможные ошибки"""
                fl_err = False
                txt_err = 'Not error'
                i = 0
                while fl_err is False and i < len(massive_row_col_nodes):
                    row = massive_row_col_nodes[i][0]
                    col = massive_row_col_nodes[i][1]
                    if clamps[row][col].number_connected_wires <= 2:
                        fl_err = True
                        txt_err = 'Непредвиденная ошибка! Один из узлов не является узлом. Число присоединенных проводов ' \
                                  'меньше или равно двум'
                    else:
                        i += 1

                return fl_err, txt_err

            def analise_massive_row_col_branches(massive_row_col_in_branches, massive_row_col_nodes,
                                                 massive_row_col_no_nodes):
                """Подпрограмма анализирует массив веток row and col на возможные ошибки"""
                fl_err = False
                txt_err = 'Not error'

                if len(massive_row_col_nodes) == 0:
                    index_clamp = 0
                    while fl_err is False and index_clamp < len(massive_row_col_in_branches[0][0]):
                        if massive_row_col_in_branches[0][index_clamp] not in massive_row_col_no_nodes:
                            fl_err = True
                            txt_err = 'Ошибка! В однопроводной цепи зажима номер {0:2d} нет в списке промежуточных точек massive_row_column_no_nodes'.format(
                                index_clamp)
                        else:
                            index_clamp += 1
                else:
                    index_branch = 0
                    while fl_err is False and index_branch < len(massive_row_col_in_branches):
                        index_clamp = 0
                        while fl_err is False and index_clamp < len(massive_row_col_in_branches[index_branch]):
                            if index_clamp == 0:
                                if massive_row_col_in_branches[index_branch][
                                    index_clamp] not in massive_row_col_nodes:
                                    fl_err = True
                                    txt_err = 'Ошибка! Первого зажима в ветви {0:2d} нет в списке узлов massive_row_column_nodes'.format(
                                        index_branch)
                            elif index_clamp != len(massive_row_col_in_branches[index_branch]) - 1:
                                if massive_row_col_in_branches[index_branch][
                                    index_clamp] not in massive_row_col_no_nodes:
                                    fl_err = True
                                    txt_err = 'Ошибка! Зажима номер {0:2d} в ветви {1:2d} нет в списке промежуточных точек massive_row_column_no_nodes'.format(
                                        index_clamp, index_branch)
                            else:
                                if massive_row_col_in_branches[index_branch][index_clamp] not in massive_row_col_nodes:
                                    fl_err = True
                                    txt_err = 'Ошибка! Последнего зажима в ветви {0:2d} нет в списке узлов massive_row_column_nodes'.format(
                                        index_branch)

                            index_clamp += 1
                        index_branch += 1

                return fl_err, txt_err

            def analise_branches(branches_):
                """Подпрограмма анализирует ветви на возможные ошибки"""
                fl_err = False
                txt_err = 'Not error'
                if not fl_err:
                    if len(branches_) == 0:
                        fl_err = True
                        txt_err = 'Непредвиденная ошибка! В массиве ветвей нет элементов'

                if not fl_err:
                    for brch in branches_:
                        if len(brch) == 0:
                            fl_err = True
                            txt_err = 'Непредвиденная ошибка! В массиве ветвей в одной из ветвей нет элементов'

                if not fl_err:
                    for brch in branches_:
                        for wire in brch:
                            if wire.__class__.__name__ != 'Wire':
                                fl_err = True
                                txt_err = 'Непредвиденная ошибка! В массиве ветвей один из элементов не является экземпляром' \
                                          'класса Wire'

                return fl_err, txt_err

            # --------------RUN------------------

            fl_error, txt_error = analise_clamped_clamps(massive_row_column_clamped_clamps)
            if not fl_error:
                print('Зажимы определены')
                fl_error, txt_error = analise_nodes(massive_row_column_nodes)
                if not fl_error:
                    print('Узлы определены')
                    fl_error, txt_error = analise_massive_row_col_branches(massive_row_column_in_branches,
                                                                           massive_row_column_nodes,
                                                                           massive_row_column_no_nodes)

                    if not fl_error:
                        print('Массив ветвей по координатам зажимов определен')
                        fl_error, txt_error = analise_branches(branches)
                        if not fl_error:
                            print('Ветви полностью определены')

            return fl_error, txt_error

        from make_circuit_by_user import moving_wire_line
        global flag_running
        flag_error = False
        text_error = 'Not error'

        if moving_wire_line is None:
            flag_running = exchange_state_running(flag_running)
            if flag_running:
                flag_error, text_error = testing_circuit()
        else:
            flag_error = True
            text_error = 'Ошибка! Уберите руки от провода перед нажатием!'

        if flag_error:
            print(text_error)
        else:
            print('Цепь успешно запущена!')

    btn_run_circuit.configure(command=click_run_btn)


flag_running = False
working_circuit(BUTTON_RUN, CLAMPS)
root.mainloop()  # Должен находится в самом конце последнего исполняемого файла
