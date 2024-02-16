"""Данная программа должна выполнять расчет цепей переменного/постоянного/несинусоидального тока"""
""" 
---Важно!
    1) Так как в Tkinter ширина измеряется в пикселях и нулях (10 кегль), то все переменные width_, height_ и т.д. должны
    быть в пикселях, и переходом //10 переводиться в ширину виджета
    2) Направление ветви должно быть только у провода, но не у прикрепленного к нему элемента
---CТОП-МЫСЛИ:
     - При создании на проводе с заданным направлением элемента, то направление неявно исчезает с экрана (по параметрам оно остается)
     - Заметить обычные tuple в FrameInfoElement и в классах элементов на namedtuple - кортежи, которые указывают,
     что именно лежит в каждом из их индексов
     - При создании элемента на проводе с выставленным током, ток исчезает
     - Убрать возможность менять направление провода при активированной moving_line
     
     - Разобраться с тестированием ветвей в start_circuit (до этого нужно подготовить создание базы данных)
     - Сделать множество тестов в reload_dates: на правильное создание ветвей, удаление проводов и изменение направлений:
---Необходимые довершения:
    - Изменить FrameInfoElement: в переменных self.frame_of_group_cur_vol и self.frame_of_group_res_con убери bg и увидишь проблему:
    из-за разности в размерах, строки едут
    
    - Сделать возможность менять один вид элемента на другой при нажатии на кнопку
    - Запретить выделение элемента, когда запущена moving_line, либо сделать так, что при его удалении (когда 
    выбранный зажим в близи с линией) была возможность ее снова достроить
    - Положение: цепь нарисована и запущена, ПУСК горит зеленым. После нажатия на какой-либо зажим ПУСК должен вновь
    становиться серым
    - Убрать разноименность в главном коде переменной WIDTH_INFO_FRAME. Сейчас эта переменная отвечает за количество символов
    в данной рамке и в расчете ширины рабочей области переводится коэффициентом 7,65
    - Избавиться от всех буфферных файлов
    - Избавиться от ненужных глобальных переменных на примере btns_elements_of_group: в избавлении от moving_wire_line может
    помочь система параметров tags от tkinter
    - Облегчить reload_dates. Добавь в метод провода synchronizing_wire_with_branch изменение массива координат в ветви, 
    благодаря этому облегчатся большинство подпрограмм и станут более явными. Теперь можно будет засовывать провод в ветвь
    любой стороной, зная, что он развернется нужным образом, будто он намагничен и выстраивается по магнитным линиям
    ветви.
---Features:
    - Добавить открытие настроек через основную программу и виджет TOPLEVEL
    - В FrameInfoElement сделать универсальный метод для любого вида расчета цепей( переходные, магнитные и тп.)
    - В options_window.py сделать сохранение выбранных параметров
    - Добавить возможность пользователю изменять full_id элемента
    - Добавить дружелюбную среду для программирования дополнительных элементов с тем, чтобы не залазить в код
"""

import sys
import os

sys.path.append(os.getcwd() + '\make_display')
sys.path.append(os.getcwd() + '\make_circuit')


import make_display

import make_circuit_by_user

import start_circuit
