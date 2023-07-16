"""Данная подпрограмма создает окно приложения, в которое помещаются рамки информации и область построения цепи"""
import tkinter as tk
from tkinter import ttk

from options_visualization import *


class Clamp:
    def __init__(self, canvas, x, y, radius, indent, color_fill, color_outline, color_outline_pushed, row, column):
        self.figure_id = None
        self.canvas = canvas
        self.x_left_up_shell = x
        self.y_left_up_shell = y
        self.radius_circle = radius
        self.width_outline = 1
        self.indent = indent

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


def make_main_window(width, height, location, title, path_icon):
    window = tk.Tk()
    window.title(title)
    window.geometry(str(width) + 'x' + str(height) + location)
    icon = tk.PhotoImage(file=path_icon)
    window.iconphoto(False, icon)
    window.resizable(False, True)
    return window


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


def create_list_library_elements():
    """Подпрограмма создает лист имен групп элементов и лист самих элементов"""
    names_of_groups = ['Резистивные элементы',
                       'Источники',
                       'Нелинейные элементы',
                       'Другое']
    names_elements_of_groups = [''] * len(names_of_groups)

    names_elements_of_groups[0] = ['Резистор', 'Катушка индуктивности', 'Конденсатор']
    names_elements_of_groups[1] = ['Источник ЭДС', 'Источник тока']
    names_elements_of_groups[2] = ['Диод', 'Варистор', 'Стабилитрон']
    names_elements_of_groups[3] = ['Обрыв']
    return names_of_groups, names_elements_of_groups


def frame_info_making(type_current, width_frame, height_string, color_bg_frame, color_text):
    def frame_info_circuit_making(main_frame, type_cur, width, height, col_bg_frame, col_text):
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

        frame_info_circuit = tk.LabelFrame(main_frame, text='Параметры цепи', bg=col_bg_frame, fg=col_text)
        frame_info_circuit.grid(column=0, row=0, stick='w', padx=5)

        lbl_name_file = tk.Label(frame_info_circuit, width=round(width / 3), height=height,  # подгонка
                                 text='Название файла:',
                                 bg=col_bg_frame, fg=col_text)

        lbl_name_file.grid(row=0, column=0, stick='w')

        entry_name_file = tk.Entry(frame_info_circuit, width=round(width * 0.77))  # подгонка
        entry_name_file.grid(row=0, column=1, stick='w')

        btn_save_name = tk.Button(frame_info_circuit, text='Сохранить', command=get_save_name_file, fg=col_text)
        btn_save_name.grid(row=1, column=1, sticky='e')

        lbl_type_current = tk.Label(frame_info_circuit, height=height,
                                    text='Ток: ' + translater_type_current(type_cur),
                                    bg=col_bg_frame, fg=col_text)
        lbl_type_current.grid(row=2, column=0, sticky='w', columnspan=2)

        lbl_counter_nodes = tk.Label(frame_info_circuit, height=height,
                                     text='Количество узлов: ',
                                     bg=col_bg_frame, fg=col_text)
        lbl_counter_nodes.grid(row=3, column=0, sticky='w', columnspan=2)
        lbl_counter_branches = tk.Label(frame_info_circuit, height=height,
                                        text='Количество ветвей: ',
                                        bg=col_bg_frame, fg=col_text)
        lbl_counter_branches.grid(row=4, column=0, sticky='w', columnspan=2)

        btn_run = tk.Button(frame_info_circuit, text='ПУСК', font='bold', fg=col_text,
                            bg='grey')
        btn_run.grid(row=5, column=0, columnspan=2)
        return btn_run

    def frame_info_element_making(main_frame, width, height, col_bg_frame, col_text):
        """Подпрограмма создает рамку под рамкой информации о цепи (СТОЛБЕЦ 0, РЯД 1), в которой будет появляться
        информация об элементе, на который в данный момент направлен курсор"""

        frame_info_element = tk.LabelFrame(main_frame, text='Параметры элемента', bg=col_bg_frame, fg=col_text)
        frame_info_element.grid(column=0, row=1, stick='w', padx=5)
        label_name_element = tk.Label(frame_info_element, width=width, height=height,
                                      text='Элемент: Resistor',
                                      bg=col_bg_frame,
                                      fg=col_text)
        label_name_element.grid(row=0, column=0, stick='w', columnspan=2)

    frame_info = tk.Frame(bg=color_bg_frame, width=width_frame)
    frame_info.grid(row=0, column=0, sticky='ns')
    btn_run_circuit = frame_info_circuit_making(frame_info, type_current, width_frame, height_string,
                                                color_bg_frame, color_text)
    frame_info_element_making(frame_info, width_frame, height_string, color_bg_frame, color_text)

    return btn_run_circuit


def workspace_making_and_building(window, list_names_of_groups_elements, list_elements_by_groups, width_library,
                                  width_workspace, height_workspace, width_quick_access, height_quick_access,
                                  radius_clamp, indent, color_text,
                                  color_bg_info_frame, color_bg_workspace, color_clamps_fill,
                                  color_clamps_outline, color_clamps_outline_pushed, color_frame_outline,
                                  color_highlight,
                                  color_lines):
    """Подпрограмма для создания рамок: рабочей области зажимов, области быстрого доступа, области библиотеки элементов и запуска их"""

    def make_frame_quick_access(frame_wrksp, width_quick_access_, height_quick_access_, radius_clamp_, indent_,
                                col_bg_info_frame, col_frame_outline, col_clamps_outline,
                                col_bg_workspace):
        """Подпрограмма создает область сверху области зажимов, на которой изображены элементы быстрого доступа; настраивает контакт с ними"""

        def calculating_sizes_and_count_areas(width_quick_access_x, height_quick_access_x, radius_clamp_x,
                                              indent_x):
            """Вычисление количества и размеров областей, в которых будут отображаться элементы быстрого доступа"""
            from math import floor

            width_ar = 2 * (indent_x + radius_clamp_x)
            height_ar = height_quick_access_x
            indent_between_ars = 2 * (indent_x + radius_clamp_x)
            count_ars = floor((width_quick_access_x - indent_between_ars) / (width_ar + indent_between_ars))
            return count_ars, width_ar, height_ar, indent_between_ars

        def make_areas(frame_qck_acs, count_ars, width_ar, height_ar, intend_between_ars, col_clamps_outline_x,
                       col_bg_workspace_x):
            """Подпрограмма создает максимально возможное количество областей"""

            def make_one_area(frame_q_a, width, height, intend_between, areas_q_a, idx, col_clamps_outline_xx,
                              col_bg_workspace_xx):
                """Подпрограмма создает одну область быстрого нажатия"""
                areas_q_a[idx] = tk.Canvas(frame_q_a, bg=col_bg_workspace_xx, width=width, height=height,
                                           highlightbackground=col_clamps_outline_xx)
                areas_q_a[idx].grid(row=0, column=idx, padx=intend_between / 2)

            areas_quick_access = [''] * count_ars

            for idx_area in range(count_ars):
                make_one_area(frame_qck_acs, width_ar, height_ar, intend_between_ars, areas_quick_access, idx_area,
                              col_clamps_outline_x, col_bg_workspace_x)

        def binding_areas():
            pass

        frame_quick_access = tk.Frame(frame_wrksp, bg=col_bg_info_frame, highlightthickness=1,
                                      highlightbackground=col_frame_outline)
        frame_quick_access.grid(row=0, column=0, sticky='we')

        count_areas, width_area, height_area, intend_between_areas = calculating_sizes_and_count_areas(
            width_quick_access_, height_quick_access_, radius_clamp_, indent_)
        if count_areas == 0:
            print(
                'Фатальная ошибка построения архитектуры! Количество областей в рамке быстрого доступа равно нулю!')
        else:
            make_areas(frame_quick_access, count_areas, width_area, height_area, intend_between_areas,
                       col_clamps_outline, col_bg_workspace)
            binding_areas()

    def make_workspace_for_clamping(frame_wrksp, width_workspace_, height_workspace_, radius_clamp_, indent_,
                                    col_bg_workspace,
                                    col_clamps_fill,
                                    col_clamps_outline, col_clamps_outline_pushed, col_frame_outline):
        """Подпрограмма создает рабочее пространство с набором зажимов, на котором будет возможно рисовать провода и элементы"""

        def making_clamps(canvas, rows, columns, size_area, rad_clamp, ind, col_fill, col_outline,
                          col_outline_pushed):
            """Подпрограмма создает зажимное поле, на котором будут располагаться провода и элементы"""
            clamps_ = [[0] * columns for _ in range(rows)]
            for row in range(rows):
                for col in range(columns):
                    clamps_[row][col] = Clamp(canvas, col * size_area, row * size_area, rad_clamp, ind,
                                              col_fill, col_outline, col_outline_pushed, row, col)
                    clamps_[row][col].make_circle()
            return clamps_

        workspace_ = tk.Canvas(frame_wrksp, bg=col_bg_workspace, width=width_workspace_, height=height_workspace_,
                               highlightthickness=1, highlightbackground=col_frame_outline)
        workspace_.grid(row=1, column=0, sticky='ns')

        size_clamp_area = indent_ * 2 + radius_clamp_ * 2
        number_clamp_rows_ = floor(height_workspace_ / size_clamp_area)
        number_clamp_columns_ = floor(width_workspace_ / size_clamp_area)

        clamps_ = making_clamps(workspace_, number_clamp_rows_, number_clamp_columns_, size_clamp_area, radius_clamp_,
                                indent_, col_clamps_fill, col_clamps_outline, col_clamps_outline_pushed)

        return clamps_, workspace_, number_clamp_rows_, number_clamp_columns_

    def make_frame_elements_library(frame_wrksp, list_names_of_groups, list_elements_groups, width_library_,
                                    col_bg_info_frame):
        """Подпрограмма создает рамку для библиотеки элементов"""

        def selected_group(btns_elems_group, list_names_of_groups_x, list_elements_groups_x, width_libr_x):
            """Подпрограмма отзывается на выбор группы из списка комбобокса"""

            def making_buttons_element_of_selected_group(index_group, btns, list_elements_groups_xx, width_libr_xx):
                """Подпрограмма создает кнопки с привязкой к элементам определенной группы"""

                count_element_in_group = len(list_elements_groups_xx[index_group])
                for i in range(count_element_in_group):
                    btns.append([''])

                for i in range(count_element_in_group):
                    btns[i] = tk.Button(frame_library_elements,
                                        text=list_elements_groups_xx[index_group][i],
                                        width=width_libr_xx // 10)
                    btns[i].grid(row=i + 1, column=0)  # +1 необходим, чтобы пропустить combobox

            def delete_old_btns(btns):
                """Подпрограмма удаляет прошлые кнопки и обнуляет массив"""
                for btn in btns:
                    btn.destroy()
                btns.clear()

            delete_old_btns(btns_elems_group)
            selection = cmbbx_list_headings_groups.get()
            index_selected_group = list_names_of_groups_x.index(selection)
            making_buttons_element_of_selected_group(index_selected_group, btns_elems_group, list_elements_groups_x,
                                                     width_libr_x)

        frame_library_elements = tk.Frame(frame_wrksp, bg=col_bg_info_frame)
        frame_library_elements.grid(row=0, column=1, rowspan=2, sticky='news')

        cmbbx_list_headings_groups = ttk.Combobox(frame_library_elements, values=list_names_of_groups,
                                                  state='readonly')

        btns_elements_of_group = []
        cmbbx_list_headings_groups.grid(row=0, column=0, sticky='ew')
        cmbbx_list_headings_groups.bind('<<ComboboxSelected>>',
                                        lambda event: selected_group(btns_elements_of_group, list_names_of_groups,
                                                                     list_elements_groups, width_library_))

        default_index = 0  # индекс группы элементов, которая выбирается при включении программы
        cmbbx_list_headings_groups.current(default_index)
        selected_group(btns_elements_of_group, list_names_of_groups, list_elements_groups, width_library_)

    from math import floor

    frame_workspace = tk.Frame(window)
    frame_workspace.grid(row=0, column=1, sticky='ns')

    make_frame_quick_access(frame_workspace, width_quick_access, height_quick_access, radius_clamp, indent,
                            color_bg_info_frame, color_frame_outline, color_clamps_outline,
                            color_bg_workspace)

    clamps, workspace, number_clamp_rows, number_clamp_columns = make_workspace_for_clamping(frame_workspace,
                                                                                             width_workspace,
                                                                                             height_workspace,
                                                                                             radius_clamp, indent,
                                                                                             color_bg_workspace,
                                                                                             color_clamps_fill,
                                                                                             color_clamps_outline,
                                                                                             color_clamps_outline_pushed,
                                                                                             color_frame_outline)

    make_frame_elements_library(frame_workspace, list_names_of_groups_elements, list_elements_by_groups,
                                width_library, color_bg_info_frame)

    return clamps, workspace, number_clamp_rows, number_clamp_columns


moving_wire_line = None
flag_element_highlighted = False
flag_moving_line_created = False
flag_running = False

path_file_input = 'date/options_date.txt'

WIDTH_WINDOW, HEIGHT_WINDOW, TYPE_CURRENT = input_date(path_file_input)

TITLE = 'Расчет цепей'
LOCATION = '+10+150'
path_main_icon = 'Icons/left_angle_main_icon.png'

root = make_main_window(WIDTH_WINDOW, HEIGHT_WINDOW, LOCATION, TITLE, path_main_icon)

LIST_NAMES_OF_GROUPS_ELEMENTS, LIST_ELEMENTS_BY_GROUPS = create_list_library_elements()

MAX_COUNT_SIMBOLS_LIST_NGE = ''

WIDTH_INFO_FRAME = 40  # Количество символов в строке рамки информации
HEIGHT_STRING_INFO_FRAME = 1
BUTTON_RUN = frame_info_making(TYPE_CURRENT, WIDTH_INFO_FRAME, HEIGHT_STRING_INFO_FRAME, COLOR_BG_INFO_FRAME,
                               COLOR_TEXT)

WIDTH_LIBRARY = 200  # ПОКА ЧТО ВЫБРАНА НАУГАД
HEIGHT_LIBRARY = HEIGHT_WINDOW
WIDTH_WORKSPACE = WIDTH_WINDOW - WIDTH_LIBRARY - WIDTH_INFO_FRAME * 7.65  # подгонка для левого края и перевод с символов в длину

WIDTH_QUICK_ACCESS = WIDTH_WORKSPACE
HEIGHT_QUICK_ACCESS = 2 * (INDENT + RADIUS_CLAMP)

HEIGHT_WORKSPACE = HEIGHT_WINDOW - HEIGHT_QUICK_ACCESS - 3  # небольшой отступ от нижней стороны

CLAMPS, WORKSPACE, NUMBER_CLAMP_ROWS, NUMBER_CLAMP_COLUMNS = workspace_making_and_building(root,
                                                                                           LIST_NAMES_OF_GROUPS_ELEMENTS,
                                                                                           LIST_ELEMENTS_BY_GROUPS,
                                                                                           WIDTH_LIBRARY,
                                                                                           WIDTH_WORKSPACE,
                                                                                           HEIGHT_WORKSPACE,
                                                                                           WIDTH_QUICK_ACCESS,
                                                                                           HEIGHT_QUICK_ACCESS,
                                                                                           RADIUS_CLAMP, INDENT,
                                                                                           COLOR_TEXT,
                                                                                           COLOR_BG_INFO_FRAME,
                                                                                           COLOR_BG_WORKSPACE,
                                                                                           COLOR_CLAMPS_FILL,
                                                                                           COLOR_CLAMPS_OUTLINE,
                                                                                           COLOR_CLAMPS_OUTLINE_PUSHED,
                                                                                           COLOR_FRAME_OUTLINE,
                                                                                           COLOR_HIGHLIGHT,
                                                                                           COLOR_LINES)
