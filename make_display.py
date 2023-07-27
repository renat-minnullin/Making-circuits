"""Данная подпрограмма создает окно приложения, в которое помещаются рамки информации и область построения цепи"""
import tkinter as tk
from tkinter import ttk


class Clamp:
    def __init__(self, canvas, x, y, radius, indent, color_fill, color_outline, color_outline_pushed, row, column):
        self.figure_id = -1
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

        self.elements_ids = []

    def draw(self):
        """Метод создает круг с отступами"""
        self.elements_ids = [self.canvas.create_oval((self.x_left_up_circle, self.y_left_up_circle),
                                                     (self.x_right_down_circle, self.y_right_down_circle),
                                                     fill=self.color_fill,
                                                     outline=self.color_outline,
                                                     width=self.width_outline)]


class FrameInfoElement(tk.LabelFrame):
    """Данный класс отвечает за все преобразования, происходящие с рамкой информации в ходе работы. Для упрощения кода, была
    принята система индексации параметров, входящих и выходящих в рамку:
    0 - сила тока
    1 - напряжение
    2 - сопротивление
    3 - проводимость"""

    def __init__(self, main_frame, col_bg_info_frame, col_text, width, height):
        super().__init__(main_frame, text='Параметры элемента', bg=col_bg_info_frame, fg=col_text)

        def make_widgets_of_one_parameter(frame_of_group, name_parameter, tuple_row_col, unit_of_measurement,
                                          state_ent):
            """Подпрограмма создает одну ячейку, включающую в себя:
            -Название параметра
            -Вводная ячейка для действующего значения
            -Знак угла
            -Вводная ячейка для угла
            -Знак градуса
            -Единица измерения"""
            row = tuple_row_col[0]
            col = tuple_row_col[1]
            frame_of_one_parameter = tk.Frame(frame_of_group)
            frame_of_one_parameter.grid(row=row, column=col, sticky='e')
            parameter_label = tk.Label(frame_of_one_parameter, text=name_parameter, bg=self.color_bg,
                                       fg=self.color_text)
            parameter_label.grid(row=0, column=0)

            module_str = tk.StringVar(self, value=0.0)
            entry_module = tk.Entry(frame_of_one_parameter, textvariable=module_str,
                                    state=state_ent, width=self.count_numbers_in_entry)
            entry_module.grid(row=0, column=1)
            tk.Label(frame_of_one_parameter, text='∠', bg=col_bg_info_frame, fg=col_text).grid(row=0, column=2)
            angle_str = tk.StringVar(self, value=0.0)
            entry_angle = tk.Entry(frame_of_one_parameter, textvariable=angle_str, state=state_ent,
                                   width=self.count_numbers_in_entry)
            entry_angle.grid(row=0, column=3)
            tk.Label(frame_of_one_parameter, text='°', bg=col_bg_info_frame, fg=col_text).grid(row=0, column=4)
            tk.Label(frame_of_one_parameter, text=unit_of_measurement, bg=col_bg_info_frame, fg=col_text).grid(row=0,
                                                                                                               column=5)
            return frame_of_one_parameter, parameter_label, module_str, entry_module, angle_str, entry_angle

        self.name_element = '----'
        self.color_bg = col_bg_info_frame
        self.color_text = col_text
        self.label_name_element = tk.Label(self, width=width, height=height,
                                           text=self.name_element,
                                           bg=col_bg_info_frame,
                                           fg=col_text)
        self.label_name_element.grid(row=0, column=0, columnspan=2)
        self.count_numbers_in_entry = 6
        self.frame_group_of_cur_vol = tk.Frame(self, bg=self.color_bg)
        self.frame_group_of_cur_vol.grid(row=1, column=0)

        self.frame_group_of_res_con = tk.Frame(self, bg=self.color_bg)
        self.frame_group_of_res_con.grid(row=1, column=1)

        self.count_parameters = 4
        self.names_parameters = ['I',
                                 'U',
                                 'Z',
                                 'Y']
        self.tuples_row_col_parameters = [(0, 0),
                                          (1, 0),
                                          (0, 1),
                                          (1, 1), ]

        self.units_measurement = ['А',
                                  'В',
                                  'Ом',
                                  'См']
        self.frames_parameters_in_group = [self.frame_group_of_cur_vol,
                                           self.frame_group_of_cur_vol,
                                           self.frame_group_of_res_con,
                                           self.frame_group_of_res_con]

        self.states_entries = ['disabled'] * self.count_parameters

        self.frames_parameters = [None] * self.count_parameters
        self.label_parameters = [None] * self.count_parameters
        self.modules_parameters = [0.0] * self.count_parameters
        self.entries_modules = [None] * self.count_parameters
        self.angles_parameters = [0.0] * self.count_parameters
        self.entry_angles = [None] * self.count_parameters

        for num_par in range(self.count_parameters):
            self.frames_parameters[num_par], \
                self.label_parameters[num_par], \
                self.modules_parameters[num_par], \
                self.entries_modules[num_par], \
                self.angles_parameters[num_par], \
                self.entry_angles[num_par] = make_widgets_of_one_parameter(self.frames_parameters_in_group[num_par],
                                                                           self.names_parameters[num_par],
                                                                           self.tuples_row_col_parameters[num_par],
                                                                           self.units_measurement[num_par],
                                                                           self.states_entries[num_par])

    def exchange_name_element(self, name_element):
        """Метод изменяет имя элемента на рамке"""
        self.name_element = name_element
        self.label_name_element.config(text=self.name_element)

    def reload_state_entries(self, accesses_parameters):
        """Метод обновляет состояния всех Entry"""

        def exchange_state(entry_module, entry_angle, state, access):
            if access:
                state = 'normal'

            else:
                state = 'disabled'
            entry_module.config(state=state)
            entry_angle.config(state=state)


        for num_par in range(self.count_parameters):
            exchange_state(self.entries_modules[num_par], self.entry_angles[num_par], self.states_entries[num_par],
                           accesses_parameters[num_par])

    def reload_values_of_parameters(self, parameters):
        """Метод обновляет значения всех параметров на информационной панели"""
        def set_conversion_to_exponential_form_with_phase(complex_arifm_value, module_var, angle_var):
            """Подпрограмма преобразует арифметическое представление в полярное"""
            from math import degrees
            from cmath import polar
            complex_polar_value = polar(complex_arifm_value)
            module_of_parameter = complex_polar_value[0]
            angle_of_parameter = degrees(complex_polar_value[1])
            module_var.set(module_of_parameter)
            angle_var.set(angle_of_parameter)

        for num_per in range(self.count_parameters):
            set_conversion_to_exponential_form_with_phase(parameters[num_per], self.modules_parameters[num_per],
                                                          self.angles_parameters[num_per])

    def transition_to_standard_state(self):
        self.exchange_name_element('----')
        self.reload_state_entries([False] * self.count_parameters)
        self.reload_values_of_parameters([0.0] * self.count_parameters)
class AreaQuickAccess(tk.Canvas):
    def __init__(self, frame, width, height, id_in_list, col_bg, col_highlight, col_text, col_outline):
        super().__init__(frame, bg=col_bg, height=height, width=width, highlightbackground=col_outline)
        self.width = width
        self.height = height
        self.id_in_list = id_in_list
        self.color_bg = col_bg
        self.color_highlight = col_highlight
        self.color_text = col_text
        self.color_outline = col_outline
        self.own_element = None
        self.own_list_elements_of_the_class = []
        self.own_elements_ids = []
        if self.id_in_list == 9:
            self.number_btn = 0
        else:
            self.number_btn = id_in_list + 1

        self.create_text(self.width, self.height, text=str(self.number_btn), anchor='se', fill=self.color_text)

    def delete_own_element(self):
        self.own_element = None
        self.own_list_elements_of_the_class = []
        for id_piece_of_element in self.own_elements_ids:
            self.delete(id_piece_of_element)


def input_options_window(path_fin):
    """Подпрограмма вводит размер окна и тип тока в цепи из файла с названием path_file_input"""
    fin = open(path_fin, 'r')
    fin.readline()
    fin.readline()
    width = int(fin.readline().split()[0])
    fin.readline()
    height = int(fin.readline().split()[0])

    fin.close()
    return width, height


def make_main_window(width, height, location, title, path_icon):
    window = tk.Tk()
    window.title(title)
    window.geometry(str(width) + 'x' + str(height) + location)
    icon = tk.PhotoImage(file=path_icon)
    window.iconphoto(False, icon)
    window.resizable(False, True)
    return window


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


def make_frames_info(width_frame, height_string):
    def make_frame_info_circuit(main_frame, width, height, col_bg_info_frame, col_text):
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

        frame_info_circuit = tk.LabelFrame(main_frame, text='Параметры цепи', bg=col_bg_info_frame, fg=col_text)
        frame_info_circuit.grid(column=0, row=0, stick='w', padx=5)

        lbl_name_file = tk.Label(frame_info_circuit, width=round(width / 3), height=height,  # подгонка
                                 text='Название файла:',
                                 bg=col_bg_info_frame, fg=col_text)

        lbl_name_file.grid(row=0, column=0, stick='w')

        entry_name_file = tk.Entry(frame_info_circuit, width=round(width * 0.77))  # подгонка
        entry_name_file.grid(row=0, column=1, stick='w')

        btn_save_name = tk.Button(frame_info_circuit, text='Сохранить', command=get_save_name_file, fg=col_text)
        btn_save_name.grid(row=1, column=1, sticky='e')

        lbl_counter_nodes = tk.Label(frame_info_circuit, height=height,
                                     text='Количество узлов: ',
                                     bg=col_bg_info_frame, fg=col_text)
        lbl_counter_nodes.grid(row=2, column=0, sticky='w', columnspan=2)
        lbl_counter_branches = tk.Label(frame_info_circuit, height=height,
                                        text='Количество ветвей: ',
                                        bg=col_bg_info_frame, fg=col_text)
        lbl_counter_branches.grid(row=3, column=0, sticky='w', columnspan=2)

        btn_run = tk.Button(frame_info_circuit, text='ПУСК', font='bold', fg=col_text,
                            bg='grey')
        btn_run.grid(row=4, column=0, columnspan=2)
        return btn_run

    def make_frame_info_element(main_frame, width, height, col_bg_info_frame, col_text):
        """Подпрограмма создает рамку под рамкой информации о цепи (СТОЛБЕЦ 0, РЯД 1), в которой будет появляться
        информация об элементе, на который в данный момент направлен курсор"""
        frame_info_element = FrameInfoElement(main_frame, col_bg_info_frame, col_text, width, height)
        frame_info_element.grid(column=0, row=1, stick='w', padx=5)

        return frame_info_element

    from options_visualization import COLOR_BG_INFO_FRAME, COLOR_TEXT
    frame_info = tk.Frame(bg=COLOR_BG_INFO_FRAME, width=width_frame)
    frame_info.grid(row=0, column=0, sticky='ns')
    btn_run_circuit = make_frame_info_circuit(frame_info, width_frame, height_string,
                                              COLOR_BG_INFO_FRAME, COLOR_TEXT)
    frame_info_about_element = make_frame_info_element(frame_info, width_frame, height_string, COLOR_BG_INFO_FRAME,
                                                       COLOR_TEXT)

    return btn_run_circuit, frame_info_about_element


def make_frames_workspace(window, list_names_of_groups_elements, list_elements_by_groups, width_library,
                          width_workspace, height_workspace, width_quick_access, height_quick_access,
                          min_width_one_area_quick_access, ):
    """Подпрограмма для создания рамок: рабочей области зажимов, области быстрого доступа, области библиотеки элементов и запуска их"""

    def make_frame_quick_access(frame_wrksp, width_quick_access_, height_quick_access_,
                                min_width_one_area_quick_access_,
                                col_bg_info_frame, col_frame_outline, col_clamps_outline,
                                col_bg_workspace):
        """Подпрограмма создает область сверху области зажимов, на которой изображены элементы быстрого доступа; настраивает контакт с ними"""

        def calculating_sizes_and_count_areas(width_quick_access_x, height_quick_access_x,
                                              min_width_one_area_quick_access_x):
            """Вычисление количества и размеров областей, в которых будут отображаться элементы быстрого доступа"""
            from math import floor

            width_ar = width_quick_access_x
            height_ar = height_quick_access_x
            count_ars = 0
            while count_ars < 10 and width_ar > min_width_one_area_quick_access_x:
                count_ars += 1
                width_ar = width_quick_access_x / count_ars - 4  # 4 - это попытка уменьшить разрыв между крайним правым и библиотекой элементов

            return count_ars, width_ar, height_ar

        def make_areas(frame_qck_acs, count_ars, width_ar, height_ar, col_clamps_outline_x,
                       col_bg_workspace_x):
            """Подпрограмма создает максимально возможное количество областей"""

            def make_one_area(frame_q_a, width, height, areas_q_a, id_area, col_clamps_outline_xx,
                              col_bg_workspace_xx):
                """Подпрограмма создает одну область быстрого нажатия"""
                from options_visualization import COLOR_TEXT, COLOR_HIGHLIGHT
                areas_q_a[id_area] = AreaQuickAccess(frame_q_a, width, height, id_area, col_bg_workspace_xx,
                                                     COLOR_HIGHLIGHT, COLOR_TEXT, col_clamps_outline_xx)

                areas_q_a[id_area].grid(row=0, column=id_area)

            areas_quick_access = [''] * count_ars

            for index_area in range(count_ars):
                make_one_area(frame_qck_acs, width_ar, height_ar, areas_quick_access, index_area,
                              col_clamps_outline_x, col_bg_workspace_x)
            return areas_quick_access

        def binding_areas_to_exchange_color_for_click(count_ars, areas_quick_access):
            """Подпрограмма запускает забиндивание для каждой области быстрого доступа"""

            def bind_one_area(id_area, areas_q_a):
                def click_on_area(clicked_area_):
                    from make_circuit_by_user import bind_areas_of_quick_access_to_click
                    bind_areas_of_quick_access_to_click(clicked_area_)

                clicked_area = areas_q_a[id_area]
                clicked_area.bind('<Button-1>',
                                  lambda clicked_area_: click_on_area(clicked_area))

            for index_area in range(count_ars):
                bind_one_area(index_area, areas_quick_access)

        frame_quick_access = tk.Frame(frame_wrksp, bg=col_bg_info_frame, highlightthickness=1,
                                      highlightbackground=col_frame_outline)
        frame_quick_access.grid(row=0, column=0, sticky='we')

        count_areas, width_area, height_area = calculating_sizes_and_count_areas(
            width_quick_access_, height_quick_access_, min_width_one_area_quick_access_)
        if count_areas == 0:
            exit(
                'Фатальная ошибка построения архитектуры! Количество областей в рамке быстрого доступа равно нулю!')
        else:
            areas_canvas_quick_access = make_areas(frame_quick_access, count_areas, width_area, height_area,

                                                   col_clamps_outline, col_bg_workspace)
            binding_areas_to_exchange_color_for_click(count_areas, areas_canvas_quick_access)

    def make_workspace_for_clamping(frame_wrksp, width_workspace_, height_workspace_, radius_clamp_, indent_,
                                    col_bg_workspace,
                                    col_clamps_fill,
                                    col_clamps_outline, col_clamps_outline_pushed, col_frame_outline):
        """Подпрограмма создает рабочее пространство с набором зажимов, на котором будет возможно рисовать провода и элементы"""

        def making_clamps(canvas, rows, columns, size_area, rad_clamp, ind, col_fill, col_outline,
                          col_outline_pushed):
            """Подпрограмма создает зажимное поле, на котором будут располагаться провода и элементы"""
            clamps_x = [[0] * columns for _ in range(rows)]
            for row in range(rows):
                for col in range(columns):
                    clamps_x[row][col] = Clamp(canvas, col * size_area, row * size_area, rad_clamp, ind,
                                               col_fill, col_outline, col_outline_pushed, row, col)
                    clamps_x[row][col].draw()
            return clamps_x

        from options_visualization import NORMAL_LENGTH

        workspace_ = tk.Canvas(frame_wrksp, bg=col_bg_workspace, width=width_workspace_, height=height_workspace_,
                               highlightthickness=1, highlightbackground=col_frame_outline)
        workspace_.grid(row=1, column=0, sticky='ns')

        size_clamp_area = NORMAL_LENGTH
        number_clamp_rows_ = floor(height_workspace_ / size_clamp_area)
        number_clamp_columns_ = floor(width_workspace_ / size_clamp_area)

        clamps_ = making_clamps(workspace_, number_clamp_rows_, number_clamp_columns_, size_clamp_area, radius_clamp_,
                                indent_, col_clamps_fill, col_clamps_outline, col_clamps_outline_pushed)

        return clamps_, workspace_

    def make_frame_elements_library(frame_wrksp, list_names_of_groups, list_elements_groups,
                                    width_library_,
                                    col_bg_info_frame):
        """Подпрограмма создает рамку для библиотеки элементов"""

        def selected_group(btns_elems_group, list_names_of_groups_x, list_elements_groups_x,
                           width_libr_x):
            """Подпрограмма отзывается на выбор группы из списка комбобокса"""

            def making_buttons_element_of_selected_group(index_group, btns, list_elements_groups_xx,
                                                         width_libr_xx):
                """Подпрограмма создает кнопки с привязкой к элементам определенной группы"""

                def bind_one_btn(index_group_, index_element_in_list_):
                    """Подпрограмма не несет явного смысла, однако она позволяет переводить index_element_in_list в
                    область локальную, из-за чего в файл make_circuit_by_user переносится реальный индекс, а не последний"""

                    def click_on_button_element(idx_group, idx_element):
                        from make_circuit_by_user import binding_btns_of_group
                        binding_btns_of_group(idx_group, idx_element)

                    btns[index_element_in_list_] = tk.Button(frame_library_elements,
                                                             text=list_elements_groups_xx[index_group_][
                                                                 index_element_in_list_],
                                                             width=width_libr_xx // 10,
                                                             command=lambda: click_on_button_element(index_group_,
                                                                                                     index_element_in_list_))

                count_element_in_group = len(list_elements_groups_xx[index_group])
                for index_element_in_list in range(count_element_in_group):
                    btns.append([''])
                for index_element_in_list in range(count_element_in_group):
                    bind_one_btn(index_group, index_element_in_list)

                    btns[index_element_in_list].grid(row=index_element_in_list + 1,
                                                     column=0)  # +1 необходим, чтобы пропустить combobox

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
                                                                     list_elements_groups,
                                                                     width_library_))

        default_index = 0  # индекс группы элементов, которая выбирается при включении программы
        cmbbx_list_headings_groups.current(default_index)
        selected_group(btns_elements_of_group, list_names_of_groups, list_elements_groups,
                       width_library_)

    from math import floor
    from options_visualization import RADIUS_CLAMP, INDENT
    from options_visualization import COLOR_BG_INFO_FRAME, COLOR_BG_WORKSPACE, COLOR_CLAMPS_FILL, COLOR_CLAMPS_OUTLINE, \
        COLOR_CLAMPS_OUTLINE_PUSHED, COLOR_FRAME_OUTLINE
    frame_workspace = tk.Frame(window)
    frame_workspace.grid(row=0, column=1, sticky='ns')

    make_frame_quick_access(frame_workspace, width_quick_access, height_quick_access,
                            min_width_one_area_quick_access,
                            COLOR_BG_INFO_FRAME, COLOR_FRAME_OUTLINE,
                            COLOR_CLAMPS_OUTLINE,
                            COLOR_BG_WORKSPACE)

    clamps, workspace = make_workspace_for_clamping(frame_workspace,
                                                    width_workspace,
                                                    height_workspace,
                                                    RADIUS_CLAMP,
                                                    INDENT,
                                                    COLOR_BG_WORKSPACE,
                                                    COLOR_CLAMPS_FILL,
                                                    COLOR_CLAMPS_OUTLINE,
                                                    COLOR_CLAMPS_OUTLINE_PUSHED,
                                                    COLOR_FRAME_OUTLINE)

    make_frame_elements_library(frame_workspace, list_names_of_groups_elements, list_elements_by_groups,
                                width_library, COLOR_BG_INFO_FRAME)

    return clamps, workspace


path_file_input = 'date/options_window.txt'
WIDTH_WINDOW, HEIGHT_WINDOW = input_options_window(path_file_input)

TITLE = 'Расчет цепей'
LOCATION = '+10+150'
path_main_icon = 'Icons/left_angle_main_icon.png'

root = make_main_window(WIDTH_WINDOW, HEIGHT_WINDOW, LOCATION, TITLE, path_main_icon)

LIST_NAMES_OF_GROUPS_ELEMENTS, LIST_ELEMENTS_BY_GROUPS = create_list_library_elements()

MAX_COUNT_SIMBOLS_LIST_NGE = ''

WIDTH_INFO_FRAME = 40  # Количество символов в строке рамки информации
HEIGHT_STRING_INFO_FRAME = 1
BUTTON_RUN, FRAME_INFO_ABOUT_ELEMENT = make_frames_info(WIDTH_INFO_FRAME, HEIGHT_STRING_INFO_FRAME)

WIDTH_LIBRARY = 200  # ПОКА ЧТО ВЫБРАНА НАУГАД
HEIGHT_LIBRARY = HEIGHT_WINDOW
WIDTH_WORKSPACE = WIDTH_WINDOW - WIDTH_LIBRARY - WIDTH_INFO_FRAME * 7.65  # подгонка для левого края и перевод с символов в длину

WIDTH_QUICK_ACCESS = WIDTH_WORKSPACE
HEIGHT_QUICK_ACCESS = 50
MIN_WIDTH_ONE_AREA_QUICK_ACCESS = 80

HEIGHT_WORKSPACE = HEIGHT_WINDOW - HEIGHT_QUICK_ACCESS - 3  # небольшой отступ от нижней стороны

CLAMPS, WORKSPACE = make_frames_workspace(root,
                                          LIST_NAMES_OF_GROUPS_ELEMENTS,
                                          LIST_ELEMENTS_BY_GROUPS,
                                          WIDTH_LIBRARY,
                                          WIDTH_WORKSPACE,
                                          HEIGHT_WORKSPACE,
                                          WIDTH_QUICK_ACCESS,
                                          HEIGHT_QUICK_ACCESS,
                                          MIN_WIDTH_ONE_AREA_QUICK_ACCESS)
