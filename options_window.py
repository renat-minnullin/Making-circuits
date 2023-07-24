"""Данный файл запускает окно, в котором пользователь может вписать характеристики запускаемой программы"""
import tkinter as tk
from tkinter import ttk


def save_options():
    global combo_size_work_window_height
    print(combo_size_work_window_height.get())


class Window(tk.Tk):
    def __init__(self, width: int, height: int, location: str, title: str, path_icon: str):
        super().__init__()
        self.title(title)
        self.geometry(str(width) + 'x' + str(height) + location)
        self.resizable(False, False)
        icon = tk.PhotoImage(file=path_icon)
        self.iconphoto(True, icon)
        self.run()

    def run(self):
        self.draw_widgets()

    def draw_widgets(self):

        def get_options_to_file():
            global NAME_FILE_OUTPUT
            main_window_width = combo_size_work_window_width.get()
            main_window_height = combo_size_work_window_height.get()

            fout = open(NAME_FILE_OUTPUT, 'w')
            fout.write('Размеры рабочей области:\n')
            fout.write('Ширина: \n{0:1d}\n'.format(int(main_window_width)))
            fout.write('Высота: \n{0:1d}\n'.format(int(main_window_height)))

            print('Options saved')
            fout.close()

        style_lables = ('Arial', 12)
        posible_sizes = tuple([_ for _ in range(500, 2100, 100)])

        lable_size_work_window = tk.Label(self, text='Размер рабочей области:', font=style_lables)
        lable_size_work_window.grid(row=0, column=0, columnspan=3)
        frame_sizes = tk.Frame(self)
        frame_sizes.grid(row=1, column=0, columnspan=3)
        combo_size_work_window_width = ttk.Combobox(frame_sizes, values=posible_sizes, width=5)
        combo_size_work_window_width.current(5)  # значение 1000 по умолчанию для ширины
        combo_size_work_window_width.grid(row=1, column=0, stick='w')

        lable_between_sizes = tk.Label(frame_sizes, text='X', font=style_lables)
        lable_between_sizes.grid(row=1, column=1, stick='w')

        combo_size_work_window_height = ttk.Combobox(frame_sizes, values=posible_sizes, width=5)
        combo_size_work_window_height.current(0)  # значение 500 по умолчанию для высоты
        combo_size_work_window_height.grid(row=1, column=2, stick='w')

        ttk.Button(self, text='Сохранить настройки', command=get_options_to_file).grid(row=2, column=0,
                                                                                       columnspan=3)


if __name__ == "__main__":
    WIDTH_WINDOW = 300
    HEIGHT_WINDOW = 500
    NAME_FILE_OUTPUT = 'date/options_window.txt'
    TITLE = 'Настройки'
    LOCATION = '+600+100'
    PATH_ICON = 'C:/Users/Ренат/Desktop/Программа для расчета цепей переменного тока/Icons/options.png'
    root = Window(WIDTH_WINDOW, HEIGHT_WINDOW, LOCATION, TITLE, PATH_ICON)
    root.mainloop()
