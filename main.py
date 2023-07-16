"""Данная программа должна выполнять расчет цепей переменного/постоянного/несинусоидального тока"""

""" 
---Важно!
    1) Так как в Tkinter ширина измеряется в пикселях и нулях (10 кегль), то все переменные width_, height_ и т.д. должны
    быть в пикселях, и переходом //10 переводиться в ширину виджета

---Cтоп-мысли: 
    1) доделать подпрограмму bind_area для области быстрого доступа
    2) Продумать подключение bind к кнопкам, сделать какой-то универсальный вариант, который подойдет для всех кнопок:
    bind включает в себя создание элемента по заданной подпрограмме по двум точкам и определенному canvas (универсальный вариант
    для любого угла между точками)
    3) Продумать, как быть с несколькими элементами рисования элемента. Либо работать с массивом элементов, либо работать
    с тегами "Название элемента" + "id"
---Необходимые довершения:
    -Положение: цепь нарисована и запущена, ПУСК горит зеленым. После нажатия на какой-либо зажим ПУСК должен вновь
    становиться серым
    -Сделать качественное выравнивание областей в рамке быстрого выбора: отступ от крайнего слева адекватный, а правый неверный,
    нужно сделать так, чтобы они все были по центру
    -Запретить выделение элемента, когда включена moving_line
    -Убрать разноименность в главном коде переменной WIDTH_INFO_FRAME. Сейчас эта переменная отвечает за количество символов
    в данной рамке и в расчете ширины рабочей области переводится коэффициентом 7,65
    -ПОЛНОСТЬЮ ПЕРЕДЕЛАТЬ ДИЗАЙН И РАЗМЕРЫ ПРОГРАММЫ
    -Избавиться от ненужных глобальных переменных на примере btns_elements_of_group
    -Переделать код под tags tkinter
---Features:
    -Добавить открытие настроек через основную программу и виджет TOPLEVEL
    -В options.py сделать сохранение выбранных параметров


---Исправление ошибок:
* Исправить ошибку, при которой пользователь мог бы создавать отдельные цепи, при этом количество узлов было бы равно нулю,
но количество ветвей нет (если создадим никак не связанные замкнутые цепи, то программа просмотрит лишь одну)

* Избавиться от name______ по типу canvas. Добавить их в глобальные




"""
import tkinter as tk
from tkinter import ttk

'''
from classes_elements import Wire
'''
from create_list_library_elements import create_list_library_elements


class Window(tk.Tk):
    def __init__(self, width: int, height: int, location: str, title: str, path_icon: str):
        super().__init__()
        self.title(title)
        self.geometry(str(width) + 'x' + str(height) + location)
        icon = tk.PhotoImage(file=path_icon)
        self.iconphoto(False, icon)
        self.resizable(False, True)


class Clamp:
    def __init__(self, canvas, x, y, radius, indent, color_fill, color_outline, color_outline_pushed, row, column):
        self.figure_id = None
        self.canvas = canvas
        self.x_left_up_shell = x
        self.y_left_up_shell = y
        self.radius_circle = radius
        self.width_outline = 1
        self.indent = indent  # отступ от краев, для создания расстояния между крепежами

        self.row = row
        self.column = column

        self.x_left_up_circle = self.x_left_up_shell + self.indent
        self.y_left_up_circle = self.y_left_up_shell + self.indent
        self.x_right_down_circle = self.x_left_up_circle + self.radius_circle * 2
        self.y_right_down_circle = self.y_left_up_circle + self.radius_circle * 2

        self.x_center_circle = self.x_left_up_circle + self.radius_circle
        self.y_center_circle = self.y_left_up_circle + self.radius_circle
        self.color_fill = color_fill
        self.color_outline = color_outline
        self.color_outline_pushed = color_outline_pushed
        self.number_connected_wires = 0
        self.list_row_col_connected_clamps = []

    def make_circle(self):
        """Метод создает круг с отступами"""
        self.figure_id = self.canvas.create_oval((self.x_left_up_circle, self.y_left_up_circle),
                                                 (self.x_right_down_circle, self.y_right_down_circle),
                                                 fill=self.color_fill,
                                                 outline=self.color_outline,
                                                 width=self.width_outline)


class Node:
    def __init__(self, clamp):
        self.clamp = clamp
        self.row = clamp.row
        self.column = clamp.column

    def __del__(self):
        del self


class Wire:

    def __init__(self, canvas, x_start, y_start, x_end, y_end, clamp_start, clamp_end, width, col_highlight, col_lines):
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
        self.figure_id = self.canvas.create_line(self.x_start, self.y_start, self.x_end, self.y_end, width=self.width,
                                                 fill=self.color_fill)

    def __del__(self):
        del self


def cleaning_contents_buffer_txt_files():
    """Подпрограмма очищает все текстовые файлы от содержимого прошлого запуска при запуске"""

    open(path_buffer_massive_clamped_clamps, 'w').close()
    open(path_buffer_row_col_acceptable_clamps, 'w').close()
    open(path_buffer_highlighted_wire, 'w').close()
    open(path_buffer_id_moving_line, 'w').close()
    open(path_buffer_row_col_start_clamp, 'w').close()


def input_date(path_fin):
    """Подпрограмма вводит размер окна и тип тока в цепи из файла с названием path_file_input"""
    fin = open(path_fin, 'r')
    fin.readline()
    fin.readline()
    width = int(fin.readline().split()[0])
    fin.readline()
    height = int(fin.readline().split()[0])
    fin.readline()
    type_current = int(fin.readline().split()[0])
    fin.close()
    return width, height, type_current


def frame_info_making(type_current, width_frame, height_string, color_bg_frame):
    def frame_info_circuit_making(main_frame, type_cur, width, height, color_bg):
        """Подпрограмма создает рамку слева в главном окне (СТОЛБЕЦ 0, РЯД 0). В ней будет записана информация о цепи:
        тип тока, количество узлов, количество ветвей и тд."""

        def get_save_name_file():
            """Подпрограмма сохраняй имя файла, после нажатие на кнопку в рамке информации о цепи и создает файл с
            данными для повторной загрузки той же самой схемы"""
            name_file = entry_name_file.get()
            if name_file:
                print(name_file)
            else:
                print('Имя пустое')

        def translater_type_current(type_c: int):
            """Переводит тип тока из 0, 1, 2 в название"""
            if type_c == 0:
                str_type_current = 'постоянный'
            elif type_c == 1:
                str_type_current = 'синусоидальный'
            else:
                str_type_current = 'несинусоидальный'
            return str_type_current

        global COL_TEXT
        frame_info_circuit = tk.LabelFrame(main_frame, text='Параметры цепи', bg=color_bg, fg=COL_TEXT)
        frame_info_circuit.grid(column=0, row=0, stick='w', padx=5)

        lbl_name_file = tk.Label(frame_info_circuit, width=round(width / 3), height=height,  # подгонка
                                 text='Название файла:',
                                 bg=color_bg, fg=COL_TEXT)
        lbl_name_file.grid(row=0, column=0, stick='w')

        entry_name_file = tk.Entry(frame_info_circuit, width=round(width * 0.77))  # подгонка
        entry_name_file.grid(row=0, column=1, stick='w')

        btn_save_name = tk.Button(frame_info_circuit, text='Сохранить', command=get_save_name_file, fg=COL_TEXT)
        btn_save_name.grid(row=1, column=1, sticky='e')

        lbl_type_current = tk.Label(frame_info_circuit, height=height,
                                    text='Ток: ' + translater_type_current(type_cur),
                                    bg=color_bg, fg=COL_TEXT)
        lbl_type_current.grid(row=2, column=0, sticky='w', columnspan=2)

        lbl_counter_nodes = tk.Label(frame_info_circuit, height=height,
                                     text='Количество узлов: ',
                                     bg=color_bg, fg=COL_TEXT)
        lbl_counter_nodes.grid(row=3, column=0, sticky='w', columnspan=2)
        lbl_counter_branches = tk.Label(frame_info_circuit, height=height,
                                        text='Количество ветвей: ',
                                        bg=color_bg, fg=COL_TEXT)
        lbl_counter_branches.grid(row=4, column=0, sticky='w', columnspan=2)

        btn_run = tk.Button(frame_info_circuit, text='ПУСК', font='bold', fg=COL_TEXT,
                            bg='grey')
        btn_run.grid(row=5, column=0, columnspan=2)
        return btn_run

    def frame_info_element_making(main_frame, width, height, color_bg):
        """Подпрограмма создает рамку под рамкой информации о цепи (СТОЛБЕЦ 0, РЯД 1), в которой будет появляться
        информация об элементе, на который в данный момент направлен курсор"""

        frame_info_element = tk.LabelFrame(main_frame, text='Параметры элемента', bg=color_bg, fg=COL_TEXT)
        frame_info_element.grid(column=0, row=1, stick='w', padx=5)
        label_name_element = tk.Label(frame_info_element, width=width, height=height,
                                      text='Элемент: Resistor',
                                      bg=color_bg,
                                      fg=COL_TEXT)
        label_name_element.grid(row=0, column=0, stick='w', columnspan=2)

    frame_info = tk.Frame(bg=color_bg_frame, width=width_frame)
    frame_info.grid(row=0, column=0, sticky='ns')
    btn_run_circuit = frame_info_circuit_making(frame_info, type_current, width_frame, height_string, color_bg_frame)
    frame_info_element_making(frame_info, width_frame, height_string, color_bg_frame)

    return btn_run_circuit


def workspace_making_and_building(window):
    """Подпрограмма для создания рамок: рабочей области зажимов, области быстрого доступа, области библиотеки элементов и запуска их"""

    def make_frame_quick_access(frame_wrksp):
        """Подпрограмма создает область сверху области зажимов, на которой изображены элементы быстрого доступа; настраивает контакт с ними"""

        def calculating_sizes_and_count_areas():
            """Вычисление количества и размеров областей, в которых будут отображаться элементы быстрого доступа"""
            from math import floor
            global WIDTH_QUICK_ACCESS, HEIGHT_QUICK_ACCESS, INDENT, RADIUS_CLAMP
            width_ar = 2 * (INDENT + RADIUS_CLAMP)
            height_ar = HEIGHT_QUICK_ACCESS
            indent_between_ars = 2 * (INDENT + RADIUS_CLAMP)
            count_ars = floor((WIDTH_QUICK_ACCESS - indent_between_ars) / (width_ar + indent_between_ars))
            return count_ars, width_ar, height_ar, indent_between_ars

        def make_areas(frame_qck_acs, count_ars, width_ar, height_ar, intend_between_ars):
            """Подпрограмма создает максимально возможное количество областей"""

            def make_one_area(frame_q_a, width, height, intend_between, areas_q_a, idx):
                """Подпрограмма создает одну область быстрого нажатия"""
                global COL_CLAMPS_OUTLINE, COL_BG_WORKSPACE
                areas_q_a[idx] = tk.Canvas(frame_q_a, bg=COL_BG_WORKSPACE, width=width, height=height,
                                           highlightbackground=COL_CLAMPS_OUTLINE)
                areas_q_a[idx].grid(row=0, column=idx, padx=intend_between / 2)

            areas_quick_access = [''] * count_ars

            for idx_area in range(count_ars):
                make_one_area(frame_qck_acs, width_ar, height_ar, intend_between_ars, areas_quick_access, idx_area)

        def binding_areas():
            pass

        global COL_BG_INFO_FRAME, COL_FRAME_OUTLINE
        frame_quick_access = tk.Frame(frame_wrksp, bg=COL_BG_INFO_FRAME, highlightthickness=1,
                                      highlightbackground=COL_FRAME_OUTLINE)
        frame_quick_access.grid(row=0, column=0, sticky='we')

        count_areas, width_area, height_area, intend_between_areas = calculating_sizes_and_count_areas()
        if count_areas == 0:
            print('Фатальная ошибка построения архитектуры! Количество областей в рамке быстрого доступа равно нулю!')
        else:
            make_areas(frame_quick_access, count_areas, width_area, height_area, intend_between_areas)
            binding_areas()

    def make_workspace_for_clamping(frame_wrksp):
        """Подпрограмма создает рабочее пространство с набором зажимов, на котором будет возможно рисовать провода и элементы"""

        def making_clamps(canvas, rows, columns, size_area, rad_clamp, ind, col_fill, col_outline, col_outline_pushed):
            """Подпрограмма создает шахматное зажимное поле, на котором будут располагаться провода и элементы"""
            clamps_ = [[0] * columns for _ in range(rows)]
            for row in range(rows):
                for col in range(columns):
                    clamps_[row][col] = Clamp(canvas, col * size_area, row * size_area, rad_clamp, ind,
                                              col_fill, col_outline, col_outline_pushed, row, col)
                    clamps_[row][col].make_circle()
            return clamps_

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
                        global COL_HIGHLIGHT
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
                                    canvas__.itemconfig(clamps___[r][c].figure_id, outline=COL_HIGHLIGHT)
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
                                    massive_clamped_clamps.remove(str(clmp_start.row) + '-' + str(clmp_start.column))
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

                    global moving_wire_line, root, WIDTH_WIRES, COL_HIGHLIGHT, COL_LINES

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
                                        clamp_end, WIDTH_WIRES, COL_HIGHLIGHT, COL_LINES)
                            wire.make_wire()
                            wires__.append(wire)
                            wire.number_in_list = len(wires__) - 1
                            canvas__.tag_bind(wire.figure_id, '<Button-1>', press_left_btn_mouse_on_wire)

                            init_moving_line(canvas__, clamp_end, event.x, event.y)

                canvas__.tag_bind(clamp.figure_id, '<Button-1>', press_left_btn_mouse_on_clamp)

            for row in range(rows):
                for col in range(columns):
                    making_wires(canvas, clamps__[row][col], clamps__, wires_)

        global COL_BG_WORKSPACE, COL_CLAMPS_FILL, COL_CLAMPS_OUTLINE, COL_CLAMPS_OUTLINE_PUSHED, COL_FRAME_OUTLINE, WIDTH_WORKSPACE, HEIGHT_WORKSPACE, RADIUS_CLAMP, INDENT

        workspace = tk.Canvas(frame_wrksp, bg=COL_BG_WORKSPACE, width=WIDTH_WORKSPACE, height=HEIGHT_WORKSPACE,
                              highlightthickness=1, highlightbackground=COL_FRAME_OUTLINE)
        workspace.grid(row=1, column=0, sticky='ns')

        size_clamp_area = INDENT * 2 + RADIUS_CLAMP * 2
        number_clamp_rows = floor(HEIGHT_WORKSPACE / size_clamp_area)
        number_clamp_columns = floor(WIDTH_WORKSPACE / size_clamp_area)

        clamps_ = making_clamps(workspace, number_clamp_rows, number_clamp_columns, size_clamp_area, RADIUS_CLAMP,
                                INDENT, COL_CLAMPS_FILL, COL_CLAMPS_OUTLINE, COL_CLAMPS_OUTLINE_PUSHED)

        wires = []
        binding_clamps_for_making_wires(workspace, clamps_, number_clamp_rows, number_clamp_columns, wires)
        return clamps_

    def make_frame_elements_library(frame_wrksp):
        """Подпрограмма создает рамку для библиотеки элементов"""

        def selected_group(btns_elems_group):
            """Подпрограмма отзывается на выбор группы из списка комбобокса"""

            def making_buttons_element_of_selected_group(index_group, btns):
                """Подпрограмма создает кнопки с привязкой к элементам определенной группы"""
                global WIDTH_LIBRARY, LIST_ELEMENTS_BY_GROUPS
                count_element_in_group = len(LIST_ELEMENTS_BY_GROUPS[index_group])
                for i in range(count_element_in_group):
                    btns.append([''])

                for i in range(count_element_in_group):
                    btns[i] = tk.Button(frame_library_elements,
                                        text=LIST_ELEMENTS_BY_GROUPS[index_group][i],
                                        width=WIDTH_LIBRARY // 10)
                    btns[i].grid(row=i + 1, column=0)  # +1 необходим, чтобы пропустить combobox

            def delete_old_btns(btns):
                """Подпрограмма удаляет прошлые кнопки и обнуляет массив"""
                for btn in btns:
                    btn.destroy()
                btns.clear()

            delete_old_btns(btns_elems_group)
            selection = cmbbx_list_headings_groups.get()
            index_selected_group = LIST_NAMES_OF_GROUPS_ELEMENTS.index(selection)
            making_buttons_element_of_selected_group(index_selected_group, btns_elems_group)

        global HEIGHT_QUICK_ACCESS, COL_FRAME_OUTLINE, COL_BG_INFO_FRAME, LIST_NAMES_OF_GROUPS_ELEMENTS
        frame_library_elements = tk.Frame(frame_wrksp, bg=COL_BG_INFO_FRAME)
        frame_library_elements.grid(row=0, column=1, rowspan=2, sticky='news')

        cmbbx_list_headings_groups = ttk.Combobox(frame_library_elements, values=LIST_NAMES_OF_GROUPS_ELEMENTS,
                                                  state='readonly')

        btns_elements_of_group = []
        cmbbx_list_headings_groups.grid(row=0, column=0, sticky='ew')
        cmbbx_list_headings_groups.bind('<<ComboboxSelected>>', lambda event: selected_group(btns_elements_of_group))

        default_index = 0  # индекс группы элементов, которая выбирается при включении программы
        cmbbx_list_headings_groups.current(default_index)
        selected_group(btns_elements_of_group)

    from math import floor

    frame_workspace = tk.Frame(window)
    frame_workspace.grid(row=0, column=1, sticky='ns')

    make_frame_quick_access(frame_workspace)
    clamps = make_workspace_for_clamping(frame_workspace)
    make_frame_elements_library(frame_workspace)

    return clamps


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

                def bypassing_single_branch(coord, list_massive_row_col_branch_clamps):
                    """Подпрограмма запускает рекурсивный алгоритм для обхода ветви.
                    Отрабатывается только для случая с одной ветвью и без узлов"""
                    if coord not in list_massive_row_col_branch_clamps[0]:
                        list_massive_row_col_branch_clamps[0].append(coord)
                        list_r_c_connected_clamps = clamps[coord[0]][coord[1]].list_row_col_connected_clamps
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
                        fl_ending_at_start_node = len(list_r_c_brch_cl) > 2 and list_r_c_con_cl[0] == list_r_c_brch_cl[
                            0]
                        return fl_not_clamp_at_list_branch or fl_ending_at_start_node

                    if fl_coord_need_check(coord, list_massive_row_col_branch_clamps[idx_brch]):
                        list_massive_row_col_branch_clamps[idx_brch].append(coord)
                        list_r_c_connected_clamps = clamps[coord[0]][coord[1]].list_row_col_connected_clamps
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

                            bypassing_branch(new_coord, list_massive_row_col_branch_clamps, massive_r_c_nodes, idx_brch)

                list_massive_row_column_branch_clamps = []

                if len(massive_row_col_nodes) == 0:
                    list_massive_row_column_branch_clamps.append([])
                    start_coord = massive_row_col_no_nodes[0]  # [row, col]
                    bypassing_single_branch(start_coord, list_massive_row_column_branch_clamps)
                else:
                    buffer_massive_row_col_nodes = massive_row_col_nodes.copy()

                    index_branch = 0
                    while buffer_massive_row_col_nodes:
                        list_massive_row_column_branch_clamps.append([])

                        start_coord_node = buffer_massive_row_col_nodes[0]
                        bypassing_branch(start_coord_node, list_massive_row_column_branch_clamps, massive_row_col_nodes,
                                         index_branch)
                        end_coord_node = list_massive_row_column_branch_clamps[index_branch][-1]

                        coord_first_clamp_after_start_node = list_massive_row_column_branch_clamps[index_branch][1]
                        clamps[start_coord_node[0]][start_coord_node[1]].list_row_col_connected_clamps.remove(
                            coord_first_clamp_after_start_node)

                        if not clamps[start_coord_node[0]][start_coord_node[1]].list_row_col_connected_clamps:
                            buffer_massive_row_col_nodes.remove(start_coord_node)

                        coord_last_clamp_before_end_node = list_massive_row_column_branch_clamps[index_branch][-2]
                        clamps[end_coord_node[0]][end_coord_node[1]].list_row_col_connected_clamps.remove(
                            coord_last_clamp_before_end_node)

                        if not clamps[end_coord_node[0]][end_coord_node[1]].list_row_col_connected_clamps:
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
                                if massive_row_col_in_branches[index_branch][index_clamp] not in massive_row_col_nodes:
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


if __name__ == "__main__":
    moving_wire_line = None
    flag_element_highlighted = False
    flag_moving_line_created = False
    flag_running = False

    path_buffer_massive_clamped_clamps = 'cache/massive_clamped_clamps.txt'
    path_buffer_row_col_acceptable_clamps = 'cache/buffer_row_col_acceptable_clamps.txt'
    path_buffer_highlighted_wire = 'cache/buffer_highlighted_wire.txt'
    path_buffer_id_moving_line = 'cache/buffer_id_moving_line.txt'
    path_buffer_row_col_start_clamp = 'cache/buffer_row_col_start_clamp.txt'
    cleaning_contents_buffer_txt_files()
    path_file_input = 'date/options_date.txt'

    WIDTH_WINDOW, HEIGHT_WINDOW, TYPE_CURRENT = input_date(path_file_input)

    TITLE = 'Расчет цепей'
    LOCATION = '+10+150'
    path_main_icon = 'Icons/left_angle_main_icon.png'

    root = Window(WIDTH_WINDOW, HEIGHT_WINDOW, LOCATION, TITLE, path_main_icon)

    COL_TEXT = '#121717'
    COL_BG_INFO_FRAME = '#789897'
    COL_BG_WORKSPACE = '#dcddd8'
    COL_CLAMPS_FILL = '#afc6c0'
    COL_CLAMPS_OUTLINE = '#516a64'
    COL_CLAMPS_OUTLINE_PUSHED = 'black'
    COL_FRAME_OUTLINE = '#303A25'
    COL_HIGHLIGHT = 'yellow'
    COL_LINES = 'black'

    LIST_NAMES_OF_GROUPS_ELEMENTS, LIST_ELEMENTS_BY_GROUPS = create_list_library_elements()

    MAX_COUNT_SIMBOLS_LIST_NGE = ''
    RADIUS_CLAMP = 8
    INDENT = 15
    WIDTH_WIRES = 2

    WIDTH_INFO_FRAME = 40  # Количество символов в строке рамки информации
    HEIGHT_STRING_INFO_FRAME = 1
    BUTTON_RUN = frame_info_making(TYPE_CURRENT, WIDTH_INFO_FRAME, HEIGHT_STRING_INFO_FRAME, COL_BG_INFO_FRAME)

    WIDTH_LIBRARY = 200  # ПОКА ЧТО ВЫБРАНА НАУГАД
    HEIGHT_LIBRARY = HEIGHT_WINDOW
    WIDTH_WORKSPACE = WIDTH_WINDOW - WIDTH_LIBRARY - WIDTH_INFO_FRAME * 7.65  # подгонка для левого края и перевод с символов в длину

    WIDTH_QUICK_ACCESS = WIDTH_WORKSPACE
    HEIGHT_QUICK_ACCESS = 2 * (INDENT + RADIUS_CLAMP)

    HEIGHT_WORKSPACE = HEIGHT_WINDOW - HEIGHT_QUICK_ACCESS - 3  # небольшой отступ от нижней стороны

    CLAMPS = workspace_making_and_building(root)

    working_circuit(BUTTON_RUN, CLAMPS)
    root.mainloop()
