"""Данный файл содержит в себе функции отрисовки элемента"""
import tkinter as tk


def calculating_intend_at_center(radius, x_center_start, y_center_start, x_center_end,
                                 y_center_end):
    """Подпрограмма высчитывает смещение начала и конца провода, чтобы он шел не из центра, а с края круга"""

    from math import sin, cos
    angle = definer_angle_inclination(x_center_start, y_center_start, x_center_end, y_center_end)
    dx = radius * cos(angle)
    dy = radius * sin(angle)

    x_s = x_center_start + dx
    x_e = x_center_end - dx
    y_s = y_center_start - dy
    y_e = y_center_end + dy

    return x_s, y_s, x_e, y_e


def definer_angle_inclination(x_start, y_start, x_end, y_end):
    """Подпрограмма определяет угол поворота относительно начальной тригонометрической точки 0 градусов, до прямой,
    соединяющей две точки на плоскости"""
    from math import atan, pi
    if x_end != x_start:
        fi = atan(abs((y_end - y_start) / (x_end - x_start)))
        if x_end > x_start and y_end <= y_start:
            gamma = fi
        elif x_end < x_start and y_end < y_start:
            gamma = pi - fi
        elif x_end < x_start and y_end >= y_start:
            gamma = pi + fi
        else:
            gamma = 2 * pi - fi
    else:
        if y_end < y_start:
            gamma = pi / 2
        else:
            gamma = 3 * pi / 2
    return gamma


def draw_node(canvas, coord, radius_clamp, width_line, col_lines, col_fill):
    x_main = coord[0]
    y_main = coord[1]

    elements = [canvas.create_oval((x_main - radius_clamp, y_main - radius_clamp),
                                   (x_main + radius_clamp, y_main + radius_clamp), width=width_line, outline=col_lines,
                                   fill=col_fill)]
    return elements


def draw_wire(canvas, coord_start, coord_end, width_line, col_lines):
    x_main_start = coord_start[0]
    y_main_start = coord_start[1]
    x_main_end = coord_end[0]
    y_main_end = coord_end[1]

    elements = [
        canvas.create_line(x_main_start, y_main_start, x_main_end, y_main_end, width=width_line, fill=col_lines)]
    return elements


def draw_resistor(canvas, coord_start, coord_end, normal_length, width_line, col_lines):
    from math import sqrt, cos, sin, pi
    x_main_start = coord_start[0]
    y_main_start = coord_start[1]
    x_main_end = coord_end[0]
    y_main_end = coord_end[1]
    additional_extension_contacts = sqrt(
        (x_main_start - x_main_end) ** 2 + (y_main_start - y_main_end) ** 2) - normal_length
    width = 0.16 * normal_length
    length_contact = 0.6 * normal_length / 2 + additional_extension_contacts / 2
    length_main_part = 0.4 * normal_length

    angle = definer_angle_inclination(x_main_start, y_main_start, x_main_end, y_main_end)
    elements = []

    # Первый контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_start = x_main_start
    y_start = y_main_start
    x_end = x_start + dx
    y_end = y_start - dy  # минус ставится из-за перевернутой системы координат

    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Верхняя половина первичной стенки резистора
    dx = width / 2 * cos(angle + pi / 2)
    dy = width / 2 * sin(angle + pi / 2)

    x_start = x_end
    y_start = y_end
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Верх основного тела
    dx = length_main_part * cos(angle)
    dy = length_main_part * sin(angle)

    x_start = x_end
    y_start = y_end
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Верхняя половину вторичной стенки резистора
    dx = width / 2 * cos(angle - pi / 2)
    dy = width / 2 * sin(angle - pi / 2)

    x_start = x_end
    y_start = y_end
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    buffer_x = x_end
    buffer_y = y_end

    # Второй контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_start = x_end
    y_start = y_end
    x_end = x_start + dx
    y_end = y_start - dy

    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Нижняя половина вторичной стенки резистора
    dx = width / 2 * cos(angle - pi / 2)
    dy = width / 2 * sin(angle - pi / 2)

    x_start = buffer_x
    y_start = buffer_y
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Нижняя часть основного тела резистора
    dx = length_main_part * cos(angle + pi)
    dy = length_main_part * sin(angle + pi)

    x_start = x_end
    y_start = y_end
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))
    # Нижняя половина первичной стенки резистора
    dx = width / 2 * cos(angle + pi / 2)
    dy = width / 2 * sin(angle + pi / 2)

    x_start = x_end
    y_start = y_end
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))
    return elements


def draw_capacitor(canvas, coord_start, coord_end, normal_length, width_line, col_lines):
    from math import sqrt, cos, sin, pi
    x_main_start = coord_start[0]
    y_main_start = coord_start[1]
    x_main_end = coord_end[0]
    y_main_end = coord_end[1]
    additional_extension_contacts = sqrt(
        (x_main_start - x_main_end) ** 2 + (y_main_start - y_main_end) ** 2) - normal_length
    width = 0.32 * normal_length
    length_contact = 0.94 * normal_length / 2 + additional_extension_contacts / 2
    length_between_plates = 0.06 * normal_length

    angle = definer_angle_inclination(x_main_start, y_main_start, x_main_end, y_main_end)
    elements = []

    # Первый контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_start = x_main_start
    y_start = y_main_start
    x_end = x_start + dx
    y_end = y_start - dy  # минус ставится из-за перевернутой системы координат

    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    buffer_x = x_end
    buffer_y = y_end

    # Первая пластина первая половина
    dx = width / 2 * cos(angle + pi / 2)
    dy = width / 2 * sin(angle + pi / 2)

    x_start = x_end
    y_start = y_end
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Первая пластина вторая половина
    dx = width / 2 * cos(angle - pi / 2)
    dy = width / 2 * sin(angle - pi / 2)

    x_start = buffer_x
    y_start = buffer_y
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    transfer_x = length_between_plates * cos(angle)
    transfer_y = length_between_plates * sin(angle)

    # Вторая пластина первая половина
    buffer_x = x_start + transfer_x
    buffer_y = y_start - transfer_y

    dx = width / 2 * cos(angle + pi / 2)
    dy = width / 2 * sin(angle + pi / 2)

    x_start = buffer_x
    y_start = buffer_y
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Вторая пластина вторая половина
    dx = width / 2 * cos(angle - pi / 2)
    dy = width / 2 * sin(angle - pi / 2)

    x_start = buffer_x
    y_start = buffer_y
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Второй контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_start = buffer_x
    y_start = buffer_y
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))
    return elements


def draw_inductor_coil(canvas, coord_start, coord_end, normal_length, width_line, col_lines):
    from math import sqrt, cos, sin, degrees

    x_main_start = coord_start[0]
    y_main_start = coord_start[1]
    x_main_end = coord_end[0]
    y_main_end = coord_end[1]

    if x_main_end < x_main_start:  # Замена координат необходима для разворота катушки, чтобы она не была в верх тормашками
        x_main_start, x_main_end = x_main_end, x_main_start
        y_main_start, y_main_end = y_main_end, y_main_start

    additional_extension_contacts = sqrt(
        (x_main_start - x_main_end) ** 2 + (y_main_start - y_main_end) ** 2) - normal_length
    radius = 0.1 * normal_length
    length_contact = 0.2 * normal_length / 2 + additional_extension_contacts / 2

    angle = definer_angle_inclination(x_main_start, y_main_start, x_main_end, y_main_end)
    elements = []

    # Первый контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_start = x_main_start
    y_start = y_main_start
    x_end = x_start + dx
    y_end = y_start - dy

    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))
    # Повторяющиеся витки
    dx = radius * cos(angle)
    dy = radius * sin(angle)
    x_start = x_end
    y_start = y_end
    x_end += 2 * dx
    y_end -= 2 * dy

    for coil in range(4):
        x_left_up = x_start - radius * (1 - cos(angle))
        y_left_up = y_start - radius * (1 + sin(angle))
        x_right_down = x_end + radius * (1 - cos(angle))
        y_right_down = y_end + radius * (1 + sin(angle))
        elements.append(canvas.create_arc((x_left_up, y_left_up), (x_right_down, y_right_down), width=width_line,
                                          start=0 + degrees(angle), extent=180,
                                          style='arc', fill=col_lines))
        x_start = x_end
        y_start = y_end
        if coil != 3:
            x_end += 2 * dx
            y_end -= 2 * dy
    # Второй контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))
    return elements


def draw_source_of_emf(canvas, coord_start, coord_end, normal_length, width_line, col_lines):
    from math import sqrt, cos, sin
    x_main_start = coord_start[0]
    y_main_start = coord_start[1]
    x_main_end = coord_end[0]
    y_main_end = coord_end[1]
    additional_extension_contacts = sqrt(
        (x_main_start - x_main_end) ** 2 + (y_main_start - y_main_end) ** 2) - normal_length
    radius = 0.4 / 2 * normal_length
    length_contact = 0.6 * normal_length / 2 + additional_extension_contacts / 2

    angle = definer_angle_inclination(x_main_start, y_main_start, x_main_end, y_main_end)
    elements = []

    # Первый контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_start = x_main_start
    y_start = y_main_start
    x_end = x_start + dx
    y_end = y_start - dy

    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Окружность
    dx = radius * cos(angle)
    dy = radius * sin(angle)
    x_start = x_end
    y_start = y_end
    x_end += 2 * dx
    y_end -= 2 * dy

    x_left_up = x_start - radius * (1 - cos(angle))
    y_left_up = y_start - radius * (1 + sin(angle))
    x_right_down = x_end + radius * (1 - cos(angle))
    y_right_down = y_end + radius * (1 + sin(angle))
    elements.append(
        canvas.create_oval((x_left_up, y_left_up), (x_right_down, y_right_down), width=width_line, fill=col_lines))

    # Стрелка
    arrow_normal_length = radius / 2
    arrow_tangen_length = radius / 2
    arrow_width = radius / 5
    arrow_parameters = str(arrow_normal_length) + ' ' + str(arrow_tangen_length) + ' ' + str(arrow_width)
    elements.append(
        canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, arrow='last', arrowshape=arrow_parameters,
                           fill=col_lines))

    # Второй контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_start = x_end
    y_start = y_end
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))
    return elements


def draw_current_source(canvas, coord_start, coord_end, normal_length, width_line, col_lines):
    from math import sqrt, cos, sin
    x_main_start = coord_start[0]
    y_main_start = coord_start[1]
    x_main_end = coord_end[0]
    y_main_end = coord_end[1]
    additional_extension_contacts = sqrt(
        (x_main_start - x_main_end) ** 2 + (y_main_start - y_main_end) ** 2) - normal_length
    radius = 0.4 / 2 * normal_length
    length_contact = 0.6 * normal_length / 2 + additional_extension_contacts / 2

    angle = definer_angle_inclination(x_main_start, y_main_start, x_main_end, y_main_end)
    elements = []

    # Первый контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_start = x_main_start
    y_start = y_main_start
    x_end = x_start + dx
    y_end = y_start - dy

    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    # Окружность
    dx = radius * cos(angle)
    dy = radius * sin(angle)
    x_start = x_end
    y_start = y_end
    x_end += 2 * dx
    y_end -= 2 * dy

    x_left_up = x_start - radius * (1 - cos(angle))
    y_left_up = y_start - radius * (1 + sin(angle))
    x_right_down = x_end + radius * (1 - cos(angle))
    y_right_down = y_end + radius * (1 + sin(angle))
    elements.append(
        canvas.create_oval((x_left_up, y_left_up), (x_right_down, y_right_down), width=width_line, fill=col_lines))

    # Линия внутри круга
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))

    buffer_x = x_end
    buffer_y = y_end

    arrow_normal_length = radius / 4
    arrow_tangen_length = radius / 2
    arrow_width = radius / 2
    arrow_parameters = str(arrow_normal_length) + ' ' + str(arrow_tangen_length) + ' ' + str(arrow_width)

    # Первая стрелка
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(
        canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, arrow='last', arrowshape=arrow_parameters,
                           fill=col_lines))
    # Вторая стрелка
    x_end += dx / 2
    y_end -= dy / 2
    elements.append(
        canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, arrow='last', arrowshape=arrow_parameters,
                           fill=col_lines))

    # Второй контакт
    dx = length_contact * cos(angle)
    dy = length_contact * sin(angle)
    x_start = buffer_x
    y_start = buffer_y
    x_end = x_start + dx
    y_end = y_start - dy
    elements.append(canvas.create_line(x_start, y_start, x_end, y_end, width=width_line, fill=col_lines))
    return elements


def draw_break(canvas, coord_start, coord_end, normal_length, width_line):
    pass


def draw_diode(canvas, coord_start, coord_end, normal_length, width_line):
    pass


def draw_varistor(canvas, coord_start, coord_end, normal_length, width_line):
    pass


def draw_zener_diode(canvas, coord_start, coord_end, normal_length, width_line):
    pass


if __name__ == "__main__":
    root = tk.Tk()
    CANVAS = tk.Canvas(root, width=400, height=400)
    CANVAS.pack()
    c_start = [200, 200]
    c_end = [400, 200]
    N_Length = 200

    draw_current_source(CANVAS, c_start, c_end, N_Length, 2, 'black')

    root.mainloop()
