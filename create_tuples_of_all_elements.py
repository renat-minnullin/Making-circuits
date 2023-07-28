"""Данный файл содержит кортеж, заполненный согласно группе и элементу необходимыми для его создания данными
"""
from classes_elements import Resistor, InductorCoil, Capacitor, SourceEMF, SourceCurrent
from drawing_elements import *

RESISTORS = []
CAPACITORS = []
INDUCTOR_COILS = []
SOURCES_EMF = []
SOURCES_CURRENT = []
TUPLE_NAMES_GROUPS = ('Резистивные элементы',
                      'Источники',
                      'Нелинейные элементы',
                      'Другое')
TUPLE_NAMES_ELEMENTS = (
    ('Резистор', 'Катушка индуктивности', 'Конденсатор'),
    ('Источник ЭДС', 'Источник тока'),
    ('Диод', 'Варистор', 'Стабилитрон'),
    ('Обрыв')
)

TUPLE_CHARACTERISTIC_ELEMENTS = (
    (
        (Resistor, RESISTORS, draw_resistor),
        (InductorCoil, INDUCTOR_COILS, draw_inductor_coil),
        (Capacitor, CAPACITORS, draw_capacitor)
    ),
    (
        (SourceEMF, SOURCES_EMF, draw_source_of_emf),
        (SourceCurrent, SOURCES_CURRENT, draw_current_source)
    )

)
