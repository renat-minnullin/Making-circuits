"""Данная программа должна выполнять расчет цепей переменного/постоянного/несинусоидального тока"""
""" 
---Важно!
    1) Так как в Tkinter ширина измеряется в пикселях и нулях (10 кегль), то все переменные width_, height_ и т.д. должны
    быть в пикселях, и переходом //10 переводиться в ширину виджета

---Cтоп-мысли: 
    - Оптимизировать систему добавления новой группы и нового элемента путем добавления всех параметров в массив (кортеж)
    - Продумать создание баз данных и сделать его
    
---Необходимые довершения:
    - Изменить FrameInfoElement, в переменных self.frame_of_group_cur_vol и self.frame_of_group_res_con убери bg и увидишь проблему:
    из-за разности в размерах, строки едут
    - Сделать возможность менять один вид элемента на другой при нажатии на кнопку
    -Запретить выделение элемента, когда запущена moving_line, либо сделать так, что при его удалении (когда 
    выбрнаыый зажим в близи с линией) была возможность ее снова достроить
    -Положение: цепь нарисована и запущена, ПУСК горит зеленым. После нажатия на какой-либо зажим ПУСК должен вновь
    становиться серым
    -Убрать разноименность в главном коде переменной WIDTH_INFO_FRAME. Сейчас эта переменная отвечает за количество символов
    в данной рамке и в расчете ширины рабочей области переводится коэффициентом 7,65
    -Избавиться от ненужных глобальных переменных на примере btns_elements_of_group: в избавлении от moving_wire_line может
    помочь система параметров tags от tkinter
---Features:
    -Добавить открытие настроек через основную программу и виджет TOPLEVEL
    - В FrameInfoElement сделать универсальный метод для любого вида расчета цепей( переходные, магнитные и тп.)
    -В options_window.py сделать сохранение выбранных параметров


---Исправление ошибок:
* Исправить ошибку, при которой пользователь мог бы создавать отдельные цепи, при этом количество узлов было бы равно нулю,
но количество ветвей нет (если создадим никак не связанные замкнутые цепи, то программа просмотрит лишь одну)


"""

import make_display

import make_circuit_by_user

import make_right_date_bases




