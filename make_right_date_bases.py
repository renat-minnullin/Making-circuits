from make_display import BUTTON_RUN, CLAMPS, root
from paths_for_buffer_files import *


class Node:
    def __init__(self, clamp):
        self.clamp = clamp
        self.row = clamp.row
        self.column = clamp.column

    def __del__(self):
        del self


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

        def recognition_circuit():
            """Подпрограмма пробегает по всей цепи, выделяет и нумерует: узлы, ветви, элементы. В случае ошибки досрочно
            завершает подпрограмму и возвращает текст ошибки"""

            def create_massive_clamped_clamps():
                """Подпрограмма создает массив, содержащий двухячейные массивы с номером строки и столбца
                зажатого зажима """

                def decoding_row_col(massive_row_col):
                    """Подпрограмма переводит формат записи координат с ['столбец-строка'] в [[столбец, строка]]"""
                    for i in range(len(massive_row_col)):
                        coord = massive_row_col[i].split('-')
                        row = int(coord[0])
                        column = int(coord[1])
                        massive_row_col[i] = [row, column]

                global path_buffer_massive_clamped_clamps

                fin = open(path_buffer_massive_clamped_clamps, 'r')
                massive_row_col_clamped_clamps = fin.readline().split()
                decoding_row_col(massive_row_col_clamped_clamps)

                return massive_row_col_clamped_clamps

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

            def create_massive_nodes(massive_row_col_clamped_clamps):
                """Подпрограмма создает массив, содержащий двухячейные массивы с номером строки и столбца
                зажима, являющегося узлом, причем в массиве все элементы будут упорядочены по возрастанию.
                Также подпрограмма создает экземпляры класса Node"""
                massive_row_col_nodes = []
                nodes_x = []
                for coord in massive_row_col_clamped_clamps:
                    row = coord[0]
                    col = coord[1]
                    if clamps[row][col].number_connected_wires >= 3:
                        massive_row_col_nodes.append([row, col])
                        node = Node(clamps[row][col])
                        nodes_x.append(node)
                return massive_row_col_nodes, nodes_x

            def create_massive_no_nodes(massive_row_col_clamped_clamps, massive_row_col_nodes):
                """Подпрограмма создает массив, содержащий двухячейные массивы с номером строки и столбца
                               зажима, являющегося соединителем для проводов, но не узлом"""
                massive_row_col_no_nodes = [coord for coord in massive_row_col_clamped_clamps if
                                            coord not in massive_row_col_nodes]
                return massive_row_col_no_nodes

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

            def create_massive_branches(massive_row_col_nodes, massive_row_col_no_nodes):
                """Подпрограмма создает ветвь. Обрати внимание, что для случая с несколькими ветвями первый и последний элемент
                 в массиве list_massive_row_column_branch_clamps[i] для каждого провода является узлом, а все между -
                 зажимами с одиночной связью"""

                def create_buffer_massive_all_list_row_col_connected_clamps():
                    """Подпрограмма создает массив, в котором хранятся все массивы по каждому зажиму в соответствующем индексе
                    для того, чтобы не удалять параметры зажимов"""
                    buffer_massive_all_list_r_c_connected_clamps = []
                    for row in range(len(clamps)):
                        buffer_massive_all_list_r_c_connected_clamps.append([])
                        for col in range(len(clamps[0])):
                            buffer_massive_all_list_r_c_connected_clamps[row].append([])
                            for connected_clamps in clamps[row][col].list_row_col_connected_clamps:
                                buffer_massive_all_list_r_c_connected_clamps[row][col].append(connected_clamps)
                    return buffer_massive_all_list_r_c_connected_clamps

                def bypassing_single_branch(coord, list_massive_row_col_branch_clamps):
                    """Подпрограмма запускает рекурсивный алгоритм для обхода ветви.
                    Отрабатывается только для случая с одной ветвью и без узлов"""
                    if coord not in list_massive_row_col_branch_clamps[0]:
                        list_massive_row_col_branch_clamps[0].append(coord)
                        list_r_c_connected_clamps = buffer_massive_all_list_row_col_connected_clamps[coord[0]][coord[1]]

                        if list_r_c_connected_clamps[0] in list_massive_row_col_branch_clamps[0]:
                            new_coord = list_r_c_connected_clamps[1]
                        else:
                            new_coord = list_r_c_connected_clamps[0]
                        bypassing_single_branch(new_coord, list_massive_row_col_branch_clamps)

                def bypassing_branch(coord, list_massive_row_col_branch_clamps, massive_r_c_nodes, idx_brch):
                    """Подпрограмма запускает рекурсивный алгоритм для обхода ветви"""

                    def fl_coord_need_check(crd, list_r_c_brch_cl):
                        """Подпрограмма проверки введенной координаты на отношение ее к данному проводу, и необходимости
                        ее прокрутки в подпрограмме bypassing_branch"""
                        fl_not_coord_in_list_branch = crd not in list_r_c_brch_cl
                        fl_it_start_node = len(list_r_c_brch_cl) > 1 and crd == list_r_c_brch_cl[0]
                        return fl_not_coord_in_list_branch or fl_it_start_node

                    def fl_branch_end(crd, mas_r_c_nodes, list_r_c_brch_cl):
                        """Подпрограмма проверяет, является ли введенный зажим узлом, который завершает провод"""
                        fl_it_node = crd in mas_r_c_nodes
                        fl_it_not_start_node = len(list_r_c_brch_cl) != 0 and list_r_c_brch_cl[0] != coord
                        fl_it_end_node = list_r_c_brch_cl[-1] == crd and len(list_r_c_brch_cl) > 1
                        return fl_it_node and (fl_it_not_start_node or fl_it_end_node)

                    def fl_selecting_the_next_clamp(list_r_c_con_cl, list_r_c_brch_cl):
                        """Подпрограмма обработки выбора следующего зажима в цепи"""
                        fl_not_clamp_at_list_branch = list_r_c_con_cl[0] not in list_r_c_brch_cl
                        fl_ending_at_start_node = len(list_r_c_brch_cl) > 2 and list_r_c_con_cl[0] == \
                                                  list_r_c_brch_cl[0]
                        return fl_not_clamp_at_list_branch or fl_ending_at_start_node

                    if fl_coord_need_check(coord, list_massive_row_col_branch_clamps[idx_brch]):
                        list_massive_row_col_branch_clamps[idx_brch].append(coord)
                        list_r_c_connected_clamps = buffer_massive_all_list_row_col_connected_clamps[coord[0]][coord[1]]

                        if fl_branch_end(coord, massive_r_c_nodes, list_massive_row_col_branch_clamps[idx_brch]):
                            print('Ветвь №{0:2d} определена'.format(idx_brch))
                        else:
                            '''Этот путь используется, если рассматриваемый зажим не узел, то есть у него только два
                            связанных с ним зажима'''
                            if fl_selecting_the_next_clamp(list_r_c_connected_clamps,
                                                           list_massive_row_col_branch_clamps[idx_brch]):
                                new_coord = list_r_c_connected_clamps[0]
                            else:
                                new_coord = list_r_c_connected_clamps[1]

                            bypassing_branch(new_coord, list_massive_row_col_branch_clamps, massive_r_c_nodes,
                                             idx_brch)

                buffer_massive_all_list_row_col_connected_clamps = create_buffer_massive_all_list_row_col_connected_clamps()
                list_massive_row_column_branch_clamps = []

                if len(massive_row_col_nodes) == 0:
                    list_massive_row_column_branch_clamps.append([])
                    start_coord = massive_row_col_no_nodes[0]  # [row, col]
                    bypassing_single_branch(start_coord, list_massive_row_column_branch_clamps)
                else:
                    buffer_massive_row_col_nodes = massive_row_col_nodes.copy()

                    index_branch = 0
                    while len(buffer_massive_row_col_nodes) != 0:
                        list_massive_row_column_branch_clamps.append([])

                        start_coord_node = buffer_massive_row_col_nodes[0]
                        bypassing_branch(start_coord_node, list_massive_row_column_branch_clamps,
                                         massive_row_col_nodes,
                                         index_branch)
                        end_coord_node = list_massive_row_column_branch_clamps[index_branch][-1]

                        coord_first_clamp_after_start_node = list_massive_row_column_branch_clamps[index_branch][1]
                        buffer_massive_all_list_row_col_connected_clamps[start_coord_node[0]][
                            start_coord_node[1]].remove(
                            coord_first_clamp_after_start_node)

                        if len(buffer_massive_all_list_row_col_connected_clamps[start_coord_node[0]][
                                   start_coord_node[1]]) == 0:
                            buffer_massive_row_col_nodes.remove(start_coord_node)

                        coord_last_clamp_before_end_node = list_massive_row_column_branch_clamps[index_branch][-2]
                        buffer_massive_all_list_row_col_connected_clamps[end_coord_node[0]][
                            end_coord_node[1]].remove(coord_last_clamp_before_end_node)

                        if len(buffer_massive_all_list_row_col_connected_clamps[end_coord_node[0]][
                                   end_coord_node[1]]) == 0:
                            buffer_massive_row_col_nodes.remove(end_coord_node)

                        index_branch += 1

                return list_massive_row_column_branch_clamps

            def analise_branches(massive_row_col_in_branches, massive_row_col_nodes, massive_row_col_no_nodes):
                """Подпрограмма анализирует массив веток на возможные ошибки"""
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

            # --------------RUN------------------
            massive_row_column_clamped_clamps = create_massive_clamped_clamps()
            fl_error, txt_error = analise_clamped_clamps(massive_row_column_clamped_clamps)
            if not fl_error:
                print('Зажимы определены')
                massive_row_column_nodes, nodes = create_massive_nodes(massive_row_column_clamped_clamps)
                massive_row_column_no_nodes = create_massive_no_nodes(massive_row_column_clamped_clamps,
                                                                      massive_row_column_nodes)
                fl_error, txt_error = analise_nodes(massive_row_column_nodes)
                if not fl_error:
                    print('Узлы определены')
                    massive_row_column_in_branches = create_massive_branches(massive_row_column_nodes,
                                                                             massive_row_column_no_nodes)
                    fl_error, txt_error = analise_branches(massive_row_column_in_branches, massive_row_column_nodes,
                                                           massive_row_column_no_nodes)
                    if not fl_error:
                        print('Ветви определены')
            return fl_error, txt_error

        global flag_running, flag_moving_line_created
        flag_error = False
        text_error = 'Not error'

        if not flag_moving_line_created:
            flag_running = exchange_state_running(flag_running)
            if flag_running:
                flag_error, text_error = recognition_circuit()
        else:
            flag_error = True
            text_error = 'Ошибка! Уберите руки от провода перед нажатием!'

        if flag_error:
            print(text_error)
            flag_running = exchange_state_running(flag_running)
        else:
            pass

    btn_run_circuit.configure(command=click_run_btn)


flag_moving_line_created = False
flag_running = False
working_circuit(BUTTON_RUN, CLAMPS)

root.mainloop()  # Должен находится в самом конце последнего исполняемого файла
