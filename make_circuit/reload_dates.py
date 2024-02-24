class Branch:
    def __init__(self, start_coord, end_coord):

        self.start_coord = start_coord  # Всегда расположены в положении arrow_direction = 'last'
        self.end_coord = end_coord  # Всегда расположены в положении arrow_direction = 'last'
        self.own_coords = []  # Всегда расположены в положении arrow_direction = 'last'
        self.own_wires = []  # Всегда расположены в положении arrow_direction = 'last'
        self.main_wire = None
        self.current = '-'
        self.arrow_direction = ''  # 'last', 'first'

    def change_direction(self):
        """Метод меняет направление ветви на противоположное. Важно: используется только тогда, когда направление уже
        было задано"""
        if self.arrow_direction == 'last':
            self.arrow_direction = 'first'
        elif self.arrow_direction == 'first':
            self.arrow_direction = 'last'
        else:
            print(
                'Непредвиденная ошибка! Попытка изменить направление ветви, когда это направление не было задано изначально')

    def reload_parameter_of_branch_for_own_wires(self):
        """Метод меняет параметр branch для каждого провода, входящего в own_wires на данную ветвь, а также для каждого прикрепленного к проводам элемента"""
        for wire in self.own_wires:
            wire.branch = self
            if wire.element is not None:
                wire.branch = self

    def universal_changes_current(self, current):
        """Метод активируется при изменении тока на любой составляющей ветви, включая все провода и подключенные к ним элементы"""
        self.current = current
        for wire in self.own_wires:
            wire.parameters[0] = current
            if wire.element is not None:
                wire.element.parameters[0] = current

    def __del__(self):
        del self


def define_type_clamp(clamp):
    """Подпрограмма определяет тип зажима: пустой, неподключенный конец, соединение или узел. +1 добавлен из-за того,
        что перезагрузка ветвей происходит ПОСЛЕ прикрепления провода к зажимам"""
    if clamp.number_connected_wires == 0 + 1:
        type_clamp = 'empty'
    elif clamp.number_connected_wires == 1 + 1:
        type_clamp = 'unconnected_end'
    elif clamp.number_connected_wires == 2 + 1:
        type_clamp = 'connection'
    else:
        type_clamp = 'node'

    return type_clamp


def reload_start_and_end_coord_of_all_branches(branches_):
    """Подпрограмма обновляет все начальные и конечные координаты зажимов для всех ветвей"""
    for brch in branches_:
        brch.start_coord = brch.own_coords[0]
        brch.end_coord = brch.own_coords[-1]


def reload_branches_when_creating_wire(branches, wire):
    """Подпрограмма перезагружает массив ветвей, добавляя новые, удаляю исчезнувшие и обновляя необходимые при создании нового провода"""

    def create_branch(wire_):
        """Подпрограмма создает новую ветвь, состоящую из одного провода"""

        branch_ = Branch(wire_.clamp_start.coord, wire_.clamp_end.coord)
        branches.append(branch_)
        branch_.own_wires.append(wire_)
        branch_.own_coords.append(wire_.clamp_start.coord)
        branch_.own_coords.append(wire_.clamp_end.coord)
        wire_.branch = branch_

    def lengthening_branch(wire_):
        """Подпрограмма расширяет уже существующую ветвь нарисованным проводом
        * В Теоретических материалах есть данные по этой подпрограмме"""

        def define_branch_of_wire(wire_x):
            """Подпрограмма определяет ветвь, в которой должен содержаться данный провод"""

            def flag_one_of_wire_clamp_is_start_or_end_clamp_of_branch(wire_xx, brch_):
                """Подпрограмма отрабатывает флаг, показывающий, что один из концов провода является началом/концом ветви"""
                return (
                        wire_xx.clamp_start.coord == brch_.start_coord and wire_xx.clamp_start.number_connected_wires == 2) or (
                        wire_xx.clamp_start.coord == brch_.end_coord and wire_xx.clamp_start.number_connected_wires == 2) or (
                        wire_xx.clamp_end.coord == brch_.start_coord and wire_xx.clamp_end.number_connected_wires == 2) or (
                        wire_xx.clamp_end.coord == brch_.end_coord and wire_xx.clamp_end.number_connected_wires == 2)

            branch_of_wire_ = None

            idx_brch = 0
            while branch_of_wire_ is None and idx_brch < len(branches):
                if flag_one_of_wire_clamp_is_start_or_end_clamp_of_branch(wire_x, branches[idx_brch]):
                    branch_of_wire_ = branches[idx_brch]
                else:
                    idx_brch += 1

            if idx_brch >= len(branches):
                print('Непредвиденная ошибка! Удлиняемая ветвь не была найдена!')

            return branch_of_wire_

        def add_wire_in_branch(branch_x, wire_x):
            """Подпрограмма добавляет провод, который только что был нарисован в массив own_wires с учетом направления ветви"""
            if branch_x.start_coord == wire_x.clamp_start.coord or branch_x.start_coord == wire_x.clamp_end.coord:
                branch_x.own_wires.insert(0, wire)
            else:
                branch_x.own_wires.append(wire)

        def add_coords_of_wire_in_branch(wire_start_coord, wire_end_coord, branch_x):
            """Подпрограмма отвечает за добавление координаты, которой нет в массиве ветви в own_coords"""
            if wire_start_coord in [branch_x.start_coord, branch_x.end_coord] and wire_end_coord not in [
                branch_x.start_coord, branch_x.end_coord]:
                new_coord = wire_end_coord
                common_clamp = wire_start_coord
            else:
                new_coord = wire_start_coord
                common_clamp = wire_end_coord

            if common_clamp == branch_x.start_coord:
                branch_x.own_coords.insert(0, new_coord)
            else:
                branch_x.own_coords.append(new_coord)

        def synchronizing_wire_with_branch(branch_x, wire_x):
            """Подпрограмма меняет местами начальную и конечную координату зажимов провода так, чтобы они были в списке зажимов ветви
            в установленном в ней порядке - от начала ветви к концу ветви"""

            def find_idx_start_and_end_coord(branch_xx, wire_start_coord, wire_end_coord):
                """Подпрограмма находит реальные индексы начальной и конечной координаты провода в массиве координат их ветви с
                учетом самоподключения"""
                id_start_coord = -1
                id_end_coord = -1
                counter_start_coord = 0
                counter_end_coord = 0
                for coord in branch_xx.own_coords:
                    if wire_start_coord == coord:
                        counter_start_coord += 1
                    if wire_end_coord == coord:
                        counter_end_coord += 1
                probable_idx_start_coord = branch_x.own_coords.index(wire_start_coord)
                probable_idx_end_coord = branch_x.own_coords.index(wire_end_coord)
                if counter_start_coord == 0 or counter_end_coord == 0:
                    print('Непредвиденная ошибка! При счете координат недосчитались одной из них!')
                elif counter_start_coord > 1 and counter_end_coord > 1:
                    print('Непредвиденная ошибка! При счете координат обе координаты провода встретились по два раза!')
                elif (counter_start_coord == 1 and counter_end_coord == 1) or (
                        abs(probable_idx_start_coord - probable_idx_end_coord) == 1):
                    id_start_coord = probable_idx_start_coord
                    id_end_coord = probable_idx_end_coord
                elif counter_start_coord > 1:
                    id_start_coord = branch_x.own_coords[probable_idx_start_coord + 1:].index(
                        wire_start_coord) + probable_idx_start_coord + 1
                    id_end_coord = probable_idx_end_coord
                elif counter_end_coord > 1:
                    id_start_coord = probable_idx_start_coord
                    id_end_coord = branch_x.own_coords[probable_idx_end_coord + 1:].index(
                        wire_end_coord) + probable_idx_end_coord + 1
                else:
                    print('Непредвиденная ошибка!')
                return id_start_coord, id_end_coord

            idx_start_coord, idx_end_coord = find_idx_start_and_end_coord(branch_x, wire.clamp_start.coord,
                                                                          wire.clamp_end.coord)
            if idx_start_coord > idx_end_coord:
                wire_x.clamp_start, wire_x.clamp_end = wire_x.clamp_end, wire_x.clamp_start
                wire_x.coord_start, wire_x.coord_end = wire_x.coord_end, wire_x.coord_start
                wire_x.x_start, wire_x.x_end = wire_x.x_end, wire_x.x_start
                wire_x.y_start, wire_x.y_end = wire_x.y_end, wire_x.y_start
                wire_x.canvas.coords(wire_x.elements_ids[0], wire_x.x_start, wire_x.y_start, wire_x.x_end, wire_x.y_end)

        branch_ = define_branch_of_wire(wire_)
        add_wire_in_branch(branch_, wire_)
        add_coords_of_wire_in_branch(wire_.clamp_start.coord, wire_.clamp_end.coord, branch_)
        wire_.branch = branch_
        wire_.current = branch_.current
        synchronizing_wire_with_branch(branch_, wire_)

    def divide_branch_with_clamp(wire_, division_coord):
        """Подпрограмма отрабатывает деление ветви на дочерние, принимая во внимание возможность, что изначальная ветвь
        может быть круговой, то есть не делится при присоединении.
        * В Теоретических материалах есть данные по этой подпрограмме"""

        def search_for_old_branch(wire_x, coord):
            """Подпрограмма ищет ветвь, которая будет разделяться на дочерние ветви по данному зажиму"""

            def flag_define_old_branch(brch, wire_xx, coord_):
                """Подпрограмма отвечает за определение, является ли данная ветвь искомой для разделения"""

                flag_main = coord_ in brch.own_coords
                flag_for_standard_situation = wire_xx not in brch.own_wires
                flag_self_connection = wire_xx in brch.own_wires and brch.own_coords.count(coord_) > 1
                return flag_main and (flag_for_standard_situation or flag_self_connection)

            idx_brch = 0
            old_branch_ = None
            flag_branch_found = False
            while not flag_branch_found and idx_brch < len(branches):
                if flag_define_old_branch(branches[idx_brch], wire_x, coord):
                    flag_branch_found = True
                    old_branch_ = branches[idx_brch]
                else:
                    idx_brch += 1

            if idx_brch >= len(branches):
                print('Непредвиденная ошибка! Разделяемая ветвь не была найдена!')
            return old_branch_

        def find_second_common_coord(attached_branch_, div_coord):
            if div_coord == attached_branch_.start_coord:
                return attached_branch_.end_coord
            else:
                return attached_branch_.start_coord

        def define_priority_child_branch(old_brch, own_wires, own_coords):
            """Подпрограмма определяет приоритет дочерней ветви"""
            if old_brch.start_coord in own_coords:
                priority = 1
            else:
                priority = 0

            if old_brch.main_wire in own_wires:
                priority += 2
            return priority

        def define_main_and_additional_coord(old_brch, div_coord, sec_common_coord):
            """Подпрограмма определяет, какой из концов ветви, делящей кольцевую, находится в списке own_coords кольцевой ветви
            old_branch первее"""
            index_division_coord = old_brch.own_coords.index(div_coord)
            index_second_common_coord = old_brch.own_coords.index(sec_common_coord)
            if index_division_coord < index_second_common_coord:
                return index_division_coord, index_second_common_coord
            else:
                return index_second_common_coord, index_division_coord

        old_branch = search_for_old_branch(wire_, division_coord)
        attached_branch = wire_.branch
        flag_there_is_second_connection = old_branch.own_coords.count(attached_branch.own_coords[0]) == 1 and old_branch.own_coords.count(attached_branch.own_coords[-1]) == 1
        flag_connection_to_circle_circuit = old_branch.start_coord == old_branch.end_coord and not flag_there_is_second_connection
        flag_self_connection = wire_ in old_branch.own_wires and old_branch.own_coords.count(division_coord) > 1
        if flag_connection_to_circle_circuit and not flag_self_connection:
            pass
        else:
            own_wires_first_branch = []
            own_coords_first_branch = []
            own_wires_second_branch = []
            own_coords_second_branch = []
            if flag_self_connection:
                attached_branch = None
                index_division_coord = old_branch.own_coords.index(division_coord)
                second_index_division_coord = old_branch.own_coords.index(division_coord, index_division_coord + 1)
                if index_division_coord == 0:
                    own_wires_first_branch = old_branch.own_wires[:second_index_division_coord]
                    own_coords_first_branch = old_branch.own_coords[:second_index_division_coord + 1]
                    own_wires_second_branch = old_branch.own_wires[second_index_division_coord:]
                    own_coords_second_branch = old_branch.own_coords[second_index_division_coord:]
                else:
                    own_wires_first_branch = old_branch.own_wires[:index_division_coord]
                    own_coords_first_branch = old_branch.own_coords[:index_division_coord + 1]
                    own_wires_second_branch = old_branch.own_wires[index_division_coord:]
                    own_coords_second_branch = old_branch.own_coords[index_division_coord:]

            elif old_branch.start_coord != old_branch.end_coord:
                index_division_coord = old_branch.own_coords.index(division_coord)

                own_wires_first_branch = old_branch.own_wires[:index_division_coord]
                own_coords_first_branch = old_branch.own_coords[:index_division_coord + 1]
                own_wires_second_branch = old_branch.own_wires[index_division_coord:]
                own_coords_second_branch = old_branch.own_coords[index_division_coord:]

            elif flag_there_is_second_connection:
                second_common_coord = find_second_common_coord(attached_branch, division_coord)
                index_main_coord, index_additional_coord = define_main_and_additional_coord(old_branch, division_coord,
                                                                                            second_common_coord)
                if index_main_coord == 0:
                    own_wires_first_branch = old_branch.own_wires[:index_additional_coord]
                    own_coords_first_branch = old_branch.own_coords[:index_additional_coord + 1]
                    own_wires_second_branch = old_branch.own_wires[index_additional_coord:]
                    own_coords_second_branch = old_branch.own_coords[index_additional_coord:]
                else:
                    own_wires_first_branch = old_branch.own_wires[index_main_coord:index_additional_coord]
                    own_coords_first_branch = old_branch.own_coords[index_main_coord:index_additional_coord + 1]
                    own_wires_second_branch = old_branch.own_wires[index_additional_coord:] + old_branch.own_wires[
                                                                                              :index_main_coord]
                    own_coords_second_branch = old_branch.own_coords[index_additional_coord:] + old_branch.own_coords[
                                                                                                1:index_main_coord + 1]
            else:
                print("Непредвиденная ошибка! Не прошли условия отсейки в divide_branch_with_clamp")

            priority_first_branch = define_priority_child_branch(old_branch, own_wires_first_branch,
                                                                 own_coords_first_branch)

            priority_second_branch = define_priority_child_branch(old_branch, own_wires_second_branch,
                                                                  own_coords_second_branch)

            if priority_first_branch > priority_second_branch:
                first_branch = old_branch
                first_branch.own_wires = own_wires_first_branch
                first_branch.own_coords = own_coords_first_branch

                second_branch = Branch(own_coords_second_branch[0], own_coords_second_branch[-1])
                branches.append(second_branch)
                second_branch.own_wires = own_wires_second_branch
                second_branch.own_coords = own_coords_second_branch

            else:
                first_branch = Branch(own_coords_first_branch[0], own_coords_first_branch[-1])
                branches.append(first_branch)
                first_branch.own_wires = own_wires_first_branch
                first_branch.own_coords = own_coords_first_branch

                second_branch = old_branch
                second_branch.own_wires = own_wires_second_branch
                second_branch.own_coords = own_coords_second_branch

            first_branch.reload_parameter_of_branch_for_own_wires()
            second_branch.reload_parameter_of_branch_for_own_wires()

    def merging_branches(wire_):
        """Подпрограмма объединяет две отдельные ветви, которые соединяются новым проводом в одну ветвь"""

        def search_for_connected_branches(wire_x):
            """Подпрограмма ищет ветви, которые соединятся в одну новым проводом"""
            start_coord_of_wire = wire_x.clamp_start.coord
            end_coord_of_wire = wire_x.clamp_end.coord
            num_brch = 0
            first_branch_ = None
            flag_branch_found = False
            while not flag_branch_found:
                first_branch_ = branches[num_brch]
                if start_coord_of_wire in first_branch_.own_coords:
                    flag_branch_found = True
                else:
                    num_brch += 1

            num_brch = 0
            second_branch_ = None
            flag_branch_found = False
            while not flag_branch_found:
                second_branch_ = branches[num_brch]
                if end_coord_of_wire in second_branch_.own_coords:
                    flag_branch_found = True
                else:
                    num_brch += 1
            return first_branch_, second_branch_

        def define_priority_merged_branch(wire_x, branch_x):
            """Подпрограмма определяет приоритет объединяемой ветви"""
            if wire_x.clamp_start.coord in branch_x.own_coords:
                priority = 1
            else:
                priority = 0

            if branch_x.main_wire is not None:
                priority += 2
            return priority

        def connect_branches(main_branch, attached_branch, wire_x):  # В Теоретических материалах есть пояснение
            """Подпрограмма отвечает за процесс слияния двух ветвей, где первая ветвь - та, которая останется, а вторая -
             исчезнет"""
            if main_branch != attached_branch:
                if main_branch.end_coord == wire_x.clamp_start.coord:
                    main_branch.own_wires.append(wire_x)
                    main_branch.own_coords.append(wire_x.clamp_end.coord)
                    if wire_x.clamp_end.coord == attached_branch.start_coord:
                        main_branch.own_wires += attached_branch.own_wires
                        main_branch.own_coords += attached_branch.own_coords[1:]
                    else:
                        main_branch.own_wires += attached_branch.own_wires[::-1]
                        main_branch.own_coords += attached_branch.own_coords[::-1][1:]

                elif main_branch.end_coord == wire_x.clamp_end.coord:
                    main_branch.own_wires.append(wire_x)
                    main_branch.own_coords.append(wire_x.clamp_start.coord)

                    if wire_x.clamp_start.coord == attached_branch.start_coord:
                        main_branch.own_wires += attached_branch.own_wires
                        main_branch.own_coords += attached_branch.own_coords[1:]
                    else:
                        main_branch.own_wires += attached_branch.own_wires[::-1]
                        main_branch.own_coords += attached_branch.own_coords[::-1][1:]

                elif main_branch.start_coord == wire_x.clamp_start.coord:
                    main_branch.own_wires.insert(0, wire_x)
                    main_branch.own_coords.insert(0, wire_x.clamp_end.coord)
                    if wire_x.clamp_end.coord == attached_branch.start_coord:
                        main_branch.own_wires = attached_branch.own_wires[::-1] + main_branch.own_wires
                        main_branch.own_coords = attached_branch.own_coords[1:][::-1] + main_branch.own_coords
                    else:
                        main_branch.own_wires = attached_branch.own_wires + main_branch.own_wires
                        main_branch.own_coords = attached_branch.own_coords[
                                                 :len(attached_branch.own_coords) - 1] + main_branch.own_coords

                elif main_branch.start_coord == wire_x.clamp_end.coord:
                    main_branch.own_wires.insert(0, wire_x)
                    main_branch.own_coords.insert(0, wire_x.clamp_start.coord)
                    if wire_x.clamp_start.coord == attached_branch.start_coord:
                        main_branch.own_wires = attached_branch.own_wires + main_branch.own_wires
                        main_branch.own_coords = attached_branch.own_coords[
                                                 :len(attached_branch.own_coords) - 1] + main_branch.own_coords
                    else:
                        main_branch.own_wires = attached_branch.own_wires[::-1] + main_branch.own_wires
                        main_branch.own_coords = attached_branch.own_coords[:-1] + main_branch.own_coords

                if attached_branch.main_wire is not None:
                    if attached_branch.main_wire.element is None:
                        attached_branch.main_wire.delete_direction(attached_branch.main_wire.elements_ids)
                    else:
                        attached_branch.main_wire.delete_direction(attached_branch.main_wire.element.elements_ids)
                branches.remove(attached_branch)
                attached_branch.__del__()

                main_branch.reload_parameter_of_branch_for_own_wires()
            else:
                branch_ = main_branch
                branch_.own_wires.append(wire_x)
                if wire_x.clamp_end.coord == branch_.end_coord:
                    branch_.own_coords.append(wire_x.clamp_start.coord)
                else:
                    branch_.own_coords.append(wire_x.clamp_end.coord)
                branch_.reload_parameter_of_branch_for_own_wires()

        first_branch, second_branch = search_for_connected_branches(wire_)
        priority_first_branch = define_priority_merged_branch(wire_, first_branch)
        priority_second_branch = define_priority_merged_branch(wire_, second_branch)
        if priority_first_branch > priority_second_branch:
            connect_branches(first_branch, second_branch, wire_)
        else:
            connect_branches(second_branch, first_branch, wire_)

    type_clamp_start = define_type_clamp(wire.clamp_start)
    type_clamp_end = define_type_clamp(wire.clamp_end)
    wire_temporary_start_coord = wire.clamp_start.coord
    wire_temporary_end_coord = wire.clamp_end.coord
    if type_clamp_start == 'empty':
        if type_clamp_end == 'empty':
            create_branch(wire)
        elif type_clamp_end == 'unconnected_end':
            lengthening_branch(wire)
        elif type_clamp_end == 'connection':
            create_branch(wire)
            divide_branch_with_clamp(wire, wire_temporary_end_coord)
        elif type_clamp_end == 'node':
            create_branch(wire)
        else:
            print('Непредвиденная ошибка! Неопределенный зажим')

    elif type_clamp_start == 'unconnected_end':
        if type_clamp_end == 'empty':
            lengthening_branch(wire)
        elif type_clamp_end == 'unconnected_end':
            merging_branches(wire)
        elif type_clamp_end == 'connection':
            lengthening_branch(wire)
            divide_branch_with_clamp(wire, wire_temporary_end_coord)
        elif type_clamp_end == 'node':
            lengthening_branch(wire)
        else:
            print('Непредвиденная ошибка! Неопределенный зажим')

    elif type_clamp_start == 'connection':
        if type_clamp_end == 'empty':
            create_branch(wire)
            divide_branch_with_clamp(wire, wire_temporary_start_coord)
        elif type_clamp_end == 'unconnected_end':
            lengthening_branch(wire)
            divide_branch_with_clamp(wire, wire_temporary_start_coord)
        elif type_clamp_end == 'connection':
            create_branch(wire)
            divide_branch_with_clamp(wire, wire_temporary_start_coord)
            divide_branch_with_clamp(wire, wire_temporary_end_coord)
        elif type_clamp_end == 'node':
            create_branch(wire)
            divide_branch_with_clamp(wire, wire_temporary_start_coord)
        else:
            print('Непредвиденная ошибка! Неопределенный зажим')

    elif type_clamp_start == 'node':
        if type_clamp_end == 'empty':
            create_branch(wire)
        elif type_clamp_end == 'unconnected_end':
            lengthening_branch(wire)
        elif type_clamp_end == 'connection':
            create_branch(wire)
            divide_branch_with_clamp(wire, wire_temporary_end_coord)
        elif type_clamp_end == 'node':
            create_branch(wire)
        else:
            print('Непредвиденная ошибка! Неопределенный зажим')
    reload_start_and_end_coord_of_all_branches(branches)

    TEST = True  # Флаг, отвечающий за включение и отключение выдачи полной информации о ветвях
    if TEST:
        i = 0
        for branch in branches:
            print('_________Ветвь номер {0:2d}_________'.format(i))
            print(branch)
            for attr in ['start_coord', 'end_coord', 'own_coords', 'own_wires', 'main_wire', 'current',
                         'arrow_direction']:
                print(attr, getattr(branch, attr))
            print('____________________________________')
            i += 1
        print('\n\n')


def reload_branches_when_deleting_wire(branches, wire):
    """Подпрограмма перезагружает массив ветвей, добавляя новые, удаляя исчезнувшие и обновляя необходимые при создании нового провода
    Важно: для симметрии, тип зажима рассматривается в момент, когда провод уже удален"""

    def delete_branch(wire_):
        """Подпрограмма удаляет, состоящую из одного провода"""
        branch_ = wire_.branch
        branches.remove(branch_)
        wire_.branch = None
        branch_.__del__()

    def shortening_branch(wire_):
        """Подпрограмма укорачивает уже существующую ветвь на нарисованный провод"""

        branch_ = wire_.branch
        branch_.own_wires.remove(wire_)
        if wire_.clamp_start.coord == branch_.start_coord or wire_.clamp_start.coord == branch_.end_coord:
            branch_.own_coords.remove(wire_.clamp_start.coord)
        else:
            branch_.own_coords.remove(wire_.clamp_end.coord)

        if branch_.main_wire == wire_:
            branch_.arrow_direction = ''

    def recovery_branch(division_coord):
        """Подпрограмма объединяет две дочерние ветви в одну основную"""

        def search_for_daughter_branches_with_coord(coord):
            """Подпрограмма ищет дочерние ветви, подключенные к данному зажиму"""

            index_brch = 0
            first_branch_, second_branch_ = None, None
            flag_branch_found = False
            while not flag_branch_found:
                if coord == branches[index_brch].start_coord or coord == branches[index_brch].end_coord:
                    flag_branch_found = True
                    first_branch_ = branches[index_brch]
                else:
                    index_brch += 1

            index_brch += 1
            flag_branch_found = False
            while not flag_branch_found:
                if coord == branches[index_brch].start_coord or coord == branches[index_brch].end_coord:
                    flag_branch_found = True
                    second_branch_ = branches[index_brch]
                else:
                    index_brch += 1

            return first_branch_, second_branch_

        def define_priority_daughter_branches(first_branch_, second_branch_):
            """Подпрограмма определяет приоритет дочерних ветвей"""
            if len(first_branch_.own_wires) >= len(second_branch_.own_wires):
                priority_first_branch_ = 1
                priority_second_branch_ = 0
            else:
                priority_first_branch_ = 0
                priority_second_branch_ = 1

            if first_branch_.current != '-':
                priority_first_branch_ += 2

            if second_branch_.current != '-':
                priority_second_branch_ += 2

            return priority_first_branch_, priority_second_branch_

        first_branch, second_branch = search_for_daughter_branches_with_coord(division_coord)
        priority_first_branch, priority_second_branch = define_priority_daughter_branches(first_branch, second_branch)

        if priority_first_branch > priority_second_branch:
            main_branch = first_branch
            doomed_branch = second_branch
        else:
            main_branch = second_branch
            doomed_branch = first_branch

        if main_branch.end_coord == doomed_branch.start_coord:
            main_branch.own_wires += doomed_branch.own_wires
            main_branch.own_coords += doomed_branch.own_coords[1:]

        elif main_branch.start_coord == doomed_branch.start_coord:
            main_branch.own_wires = doomed_branch.own_wires[::-1] + main_branch.own_wires
            main_branch.own_coords = doomed_branch.own_coords[:0:-1] + main_branch.own_coords

        elif main_branch.end_coord == doomed_branch.end_coord:
            main_branch.own_wires += doomed_branch.own_wires[::-1]
            main_branch.own_coords += doomed_branch.own_coords[::-1][1:]

        elif main_branch.start_coord == doomed_branch.end_coord:
            main_branch.own_wires = doomed_branch.own_wires + main_branch.own_wires
            main_branch.own_coords = doomed_branch.own_coords + main_branch.own_coords[1:]

        else:
            print('Ошибка в параметрах отсейки направления подпрограммы recovery_branch: Проверь условия отсейки')

        if doomed_branch.main_wire is not None:
            doomed_branch.main_wire.delete_direction(doomed_branch.main_wire.elements_ids)

        branches.remove(doomed_branch)
        doomed_branch.__del__()
        first_branch.reload_parameter_of_branch_for_own_wires()
        second_branch.reload_parameter_of_branch_for_own_wires()

    def divide_branch_with_wire(wire_):
        """Подпрограмма разделяет ветвь на две дочерние ветви, образующиеся при удалении провода внутри общей (основной) ветви"""

        def divide_main_branch_in_daughters_branches(main_branch_, wire_x):
            """Подпрограмма разделяет ветвь на две дочерние для случая с незамкнутой ветвью"""
            index_wire_x = main_branch_.own_wires.index(wire_x)
            first_branch = Branch(main_branch_.start_coord, main_branch_.own_coords[index_wire_x])
            first_branch.own_wires = main_branch_.own_wires[:index_wire_x]
            first_branch.own_coords = main_branch_.own_coords[:index_wire_x + 1]

            second_branch = Branch(main_branch_.own_coords[index_wire_x + 1], main_branch_.end_coord)
            second_branch.own_wires = main_branch_.own_wires[index_wire_x + 1:]
            second_branch.own_coords = main_branch_.own_coords[index_wire_x + 1:]

            if main_branch_.main_wire is not None:
                if main_branch_.main_wire in first_branch.own_wires:
                    first_branch.main_wire = main_branch_.main_wire
                    first_branch.arrow_direction = first_branch.main_wire.arrow_direction
                    first_branch.current = main_branch_.current
                elif main_branch_.main_wire in second_branch.own_wires:
                    second_branch.main_wire = main_branch_.main_wire
                    second_branch.arrow_direction = second_branch.main_wire.arrow_direction
                    second_branch.current = main_branch_.current
                else:
                    print(
                        'Непредвиденная ошибка! В подпрограмме divide_branch_with_wire направляющий провод не найден в дочерних ветвях')
            first_branch.reload_parameter_of_branch_for_own_wires()
            second_branch.reload_parameter_of_branch_for_own_wires()
            branches.remove(main_branch_)
            main_branch_.__del__()
            branches.append(first_branch)
            branches.append(second_branch)

        def breaking_closed_branch(main_branch_, wire_x):
            """Подпрограмма разрывает замкнутую ветвь"""

            def define_index_start_and_end_coord_of_branch(branch_coords, wire_xx):
                """Подпрограмма определяет начальную и конечную координату зажима"""
                start_coord_ = []
                end_coord_ = []
                index_crd = 0
                while index_crd < len(branch_coords) and start_coord_ == []:
                    if branch_coords[index_crd] == wire_xx.clamp_start.coord:
                        start_coord_ = wire_xx.clamp_end.coord
                        end_coord_ = wire_xx.clamp_start.coord
                    elif branch_coords[index_crd] == wire_xx.clamp_end.coord:
                        start_coord_ = wire_xx.clamp_end.coord
                        end_coord_ = wire_xx.clamp_start.coord
                    else:
                        index_crd += 1

                index_start_coord_ = branch_coords.index(start_coord_)
                index_end_coord_ = branch_coords.index(end_coord_)

                return index_start_coord_, index_end_coord_

            index_wire_x = main_branch_.own_wires.index(wire_x)

            main_branch_.own_wires = main_branch_.own_wires[index_wire_x + 1:] + main_branch.own_wires[:index_wire_x]
            # Рассматривается случай, когда удаляется провод с концом на начале(конце) витка
            if main_branch_.start_coord in [wire_x.clamp_start.coord, wire_x.clamp_end.coord]:
                main_branch_.own_coords = main_branch_.own_coords[:-1]
            else:
                index_start_coord, index_end_coord = define_index_start_and_end_coord_of_branch(main_branch_.own_coords,
                                                                                                wire_x)

                main_branch_.own_coords = main_branch_.own_coords[index_start_coord:] + main_branch_.own_coords[
                                                                                        :index_end_coord + 1]
            if main_branch_.main_wire == wire_x:
                main_branch_.arrow_direction = ''

        main_branch = wire_.branch
        if main_branch.start_coord != main_branch.end_coord:
            divide_main_branch_in_daughters_branches(main_branch, wire_)
        else:
            breaking_closed_branch(main_branch, wire_)

    type_clamp_start = define_type_clamp(wire.clamp_start)
    type_clamp_end = define_type_clamp(wire.clamp_end)

    if type_clamp_start == 'empty':
        if type_clamp_end == 'empty':
            delete_branch(wire)
        elif type_clamp_end == 'unconnected_end':
            shortening_branch(wire)
        elif type_clamp_end == 'connection':
            delete_branch(wire)
            recovery_branch(wire.clamp_end.coord)
        elif type_clamp_end == 'node':
            delete_branch(wire)
        else:
            print('Непредвиденная ошибка! Неопределенный зажим')

    elif type_clamp_start == 'unconnected_end':
        if type_clamp_end == 'empty':
            shortening_branch(wire)
        elif type_clamp_end == 'unconnected_end':
            divide_branch_with_wire(wire)
        elif type_clamp_end == 'connection':
            shortening_branch(wire)
            recovery_branch(wire.clamp_end.coord)
        elif type_clamp_end == 'node':
            shortening_branch(wire)
        else:
            print('Непредвиденная ошибка! Неопределенный зажим')

    elif type_clamp_start == 'connection':
        if type_clamp_end == 'empty':
            delete_branch(wire)
            recovery_branch(wire.clamp_start.coord)
        elif type_clamp_end == 'unconnected_end':
            shortening_branch(wire)
            recovery_branch(wire.clamp_start.coord)

        elif type_clamp_end == 'connection':
            delete_branch(wire)
            recovery_branch(wire.clamp_start.coord)
            recovery_branch(wire.clamp_end.coord)
        elif type_clamp_end == 'node':
            delete_branch(wire)
            recovery_branch(wire.clamp_start.coord)
        else:
            print('Непредвиденная ошибка! Неопределенный зажим')

    elif type_clamp_start == 'node':
        if type_clamp_end == 'empty':
            delete_branch(wire)
        elif type_clamp_end == 'unconnected_end':
            shortening_branch(wire)
        elif type_clamp_end == 'connection':
            delete_branch(wire)
            recovery_branch(wire.clamp_end.coord)
        elif type_clamp_end == 'node':
            delete_branch(wire)
        else:
            print('Непредвиденная ошибка! Неопределенный зажим')
    reload_start_and_end_coord_of_all_branches(branches)

    TEST = False
    if TEST:
        i = 0
        for branch in branches:
            print('_________Ветвь номер {0:2d}_________'.format(i))
            print(branch)
            for attr in ['start_coord', 'end_coord', 'own_coords', 'own_wires', 'main_wire', 'current',
                         'arrow_direction']:
                print(attr, getattr(branch, attr))
            print('____________________________________')
            i += 1
        print('\n\n')
