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


'''
#Вывод массива для проверки
for i in range(len(names_of_groups)):
    for j in range(len(names_elements_of_groups[i])):
        print(names_elements_of_groups[i][j], end='   ')
    print()
'''
