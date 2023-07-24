"""Данный файл включает в себя все функции по вводу/выводу буферных файлов"""


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


def input_id_moving_line():
    """Подпрограмма вводит из файла id движущейся линии"""
    from paths_for_buffer_files import path_buffer_id_moving_line

    fin = open(path_buffer_id_moving_line, 'r')
    mov_w_line = int(fin.readline().split()[0])
    fin.close()
    return mov_w_line


def output_id_moving_line(moving_line):
    """Подпрограмма выводит в файл id движущейся линии"""
    from paths_for_buffer_files import path_buffer_id_moving_line
    fout = open(path_buffer_id_moving_line, 'w')
    fout.write(str(moving_line))
    fout.close()


def input_r_c_start_clamp():
    """Подпрограмма вводит из файла координаты начального зажима (row, col)"""
    from paths_for_buffer_files import path_buffer_row_col_start_clamp
    fin = open(path_buffer_row_col_start_clamp, 'r')
    row_and_col = fin.readline().split()
    clamp_row, clamp_column = int(row_and_col[0]), int(row_and_col[1])
    fin.close()
    return clamp_row, clamp_column


def output_r_c_start_clamp(clicked_clamp_):
    """Подпрограмма выводит в файл координаты начального зажима (row, col)"""
    from paths_for_buffer_files import path_buffer_row_col_start_clamp
    fout = open(path_buffer_row_col_start_clamp, 'w')
    fout.write(str(clicked_clamp_.row) + ' ' + str(clicked_clamp_.column) + '\n')
    fout.close()


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
