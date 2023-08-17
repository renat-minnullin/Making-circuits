class Branch:
    def __init__(self, start_coord, end_coord):

        self.start_coord = start_coord  # Всегда расположены в положении arrow_direction = 'last'
        self.end_coord = end_coord  # Всегда расположены в положении arrow_direction = 'last'
        self.own_coords = []  # Всегда расположены в положении arrow_direction = 'last'
        self.own_wires = []  # Всегда расположены в положении arrow_direction = 'last'
        self.main_wire = None
        self.current = 0
        self.arrow_direction = ''  # 'last', 'first'

    def define_direction(self, wire):
        """Метод определяет направление ветви по уже выбранному направлению провода, включенного в данную ветвь"""

        def flag_direction_wire_and_branch_coincide(wire_):
            """Подпрограмма отрабатывает функцию флага совпадения направления провода и ветви"""
            coord_start = wire_.clamp_start.coord
            coord_end = wire_.clamp_end.coord
            index_coord_start = self.own_coords.index(coord_start)
            index_coord_end = self.own_coords.index(coord_end)

            return (wire_.arrow_direction == 'last' and index_coord_start < index_coord_end) or (
                    wire_.arrow_direction == 'first' and index_coord_start > index_coord_end)

        if wire not in self.own_wires:
            print('Непредвиденная ошибка! Данного провода нет в списке проводов данной ветви')
        else:
            if flag_direction_wire_and_branch_coincide(wire):
                arrow_direction = wire.arrow_direction
            elif wire.arrow_direction == 'last':
                arrow_direction = 'first'
            else:
                arrow_direction = 'last'

            return arrow_direction

    def set_directions_of_wires_in_direction_of_branch(self):
        """Метод изменяет направление всех проводов ветви согласно направлению ветви"""

        def flag_direction_wire_and_branch_coincide(wire_):
            """Подпрограмма отрабатывает функцию флага совпадения направления провода и ветви"""
            coord_start = wire_.clamp_start.coord
            coord_end = wire_.clamp_end.coord
            index_coord_start = self.own_coords.index(coord_start)
            index_coord_end = self.own_coords.index(coord_end)

            return (wire_.arrow_direction == 'last' and index_coord_start < index_coord_end) or (
                    wire_.arrow_direction == 'first' and index_coord_start > index_coord_end)

        for wire in self.own_wires:
            if flag_direction_wire_and_branch_coincide(wire_):
                wire.arrow_direction = self.arrow_direction
            elif wire.arrow_direction == 'last':
                wire.arrow_direction = 'first'
            else:
                wire.arrow_direction = 'last'

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

    def __del__(self):
        del self


def reload_branches(branches, wire):
    """Подпрограмма перезагружает массив ветвей, добавляя новые, удаляю исчезнувшие и обновляя необходимые"""

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

    def define_branch_of_wire(wire_, branches_):
        """Подпрограмма определяет ветвь, в которой содержится данный провод"""

        def flag_one_of_wire_clamp_is_start_or_end_clamp_of_branch(wire_x, brch_):
            """Подпрограмма отрабатывает флаг, показывающий, что один из концов провода является началом/концом ветви"""
            return (wire_x.clamp_start.coord == brch_.start_coord or wire_x.clamp_start.coord == brch_.end_coord) or (
                    wire_x.clamp_end.coord == brch_.start_coord or wire_x.clamp_end.coord == brch_.end_coord)

        branch_of_wire_ = None

        num_brch = 0
        while branch_of_wire_ is None:
            if flag_one_of_wire_clamp_is_start_or_end_clamp_of_branch(wire_, branches_[num_brch]):
                branch_of_wire_ = branches_[num_brch]
            else:
                num_brch += 1

        return branch_of_wire_

    def add_wire_in_branch(branch_, wire_):
        """Подпрограмма добавляет провод, который только что был нарисован в массив own_wires с учетом его направления"""
        if branch_.start_coord == wire_.clamp_start.coord or branch_.start_coord == wire_.clamp_end.coord:
            branch_.own_wires.insert(0, wire)
        else:
            branch_.own_wires.append(wire)

    def add_coords_of_wire_in_branch(wire_start_coord, wire_end_coord, branch_):
        """Подпрограмма добавляет координаты зажимов нового провода в массив own_coords ветви с учетом всех факторов"""

        def flag_coords_not_in_own_coords():
            return wire_start_coord not in branch_.own_coords and wire_end_coord not in branch_.own_coords

        def flag_only_one_coord_in_own_coords():
            return (wire_start_coord in branch_.own_coords and wire_end_coord not in branch_.own_coords) or (
                    wire_start_coord not in branch_.own_coords and wire_end_coord in branch_.own_coords)

        def add_one_coord_in_branch(branch_x, wire_start_coord_, wire_end_coord_):
            """Подпрограмма отвечает за добавление координаты, которой нет в массиве ветви own_coords"""
            if wire_start_coord_ in branch_.own_coords and wire_end_coord_ not in branch_.own_coords:
                new_coord = wire_end_coord_
                common_clamp = wire_start_coord_
            else:
                new_coord = wire_start_coord_
                common_clamp = wire_end_coord_

            if common_clamp == branch_.start_coord:
                branch_.own_coords.insert(0, new_coord)
            else:
                branch_x.own_coords.append(new_coord)

        if flag_coords_not_in_own_coords():
            branch_.own_coords += [wire_start_coord, wire_end_coord]

        elif flag_only_one_coord_in_own_coords():
            add_one_coord_in_branch(branch_, wire_start_coord, wire_end_coord)

    def divided_branch(branches_, division_coord):
        """Подпрограмма разделяет ветвь на две дочерние, одна из которых будет новой, а другая останется старой с учетом
        приоритетности"""

        def search_for_old_branch(coord, branches_x):
            """Подпрограмма ищет ветвь, которая будет разделяться на дочерние ветви по данному зажиму"""
            num_brch = 0
            old_branch_ = None
            flag_branch_found = False
            while not flag_branch_found:
                if coord in branches_x[num_brch].own_coords:
                    flag_branch_found = True
                    old_branch_ = branches_x[num_brch]
                else:
                    num_brch += 1
            return old_branch_

        def define_priority_child_branch(old_branch_, own_wires, own_coords):
            """Подпрограмма определяет приоритет дочерней ветви"""
            if old_branch_.start_coord in own_coords:
                priority = 1
            else:
                priority = 0

            if old_branch_.main_wire in own_wires:
                priority += 2
            return priority

        old_branch = search_for_old_branch(division_coord, branches_)
        index_division_coord = old_branch.own_coords.index(division_coord)

        own_wires_first_branch = old_branch.own_wires[:index_division_coord]
        own_coords_first_branch = old_branch.own_coords[:index_division_coord + 1]
        priority_first_branch = define_priority_child_branch(old_branch, own_wires_first_branch,
                                                             own_coords_first_branch)

        own_wires_second_branch = old_branch.own_wires[index_division_coord:]
        own_coords_second_branch = old_branch.own_coords[index_division_coord:]
        priority_second_branch = define_priority_child_branch(old_branch, own_wires_second_branch,
                                                              own_coords_second_branch)

        if priority_first_branch > priority_second_branch:
            first_branch = old_branch
            first_branch.own_wires = own_wires_first_branch
            first_branch.own_coords = own_coords_first_branch

            second_branch = Branch(own_coords_second_branch[0], own_coords_second_branch[-1])
            branches_.append(second_branch)
            second_branch.own_wires = own_wires_second_branch
            second_branch.own_coords = own_coords_second_branch
        else:
            first_branch = Branch(own_coords_first_branch[0], own_coords_first_branch[-1])
            branches_.append(first_branch)
            first_branch.own_wires = own_wires_first_branch
            first_branch.own_coords = own_coords_first_branch

            second_branch = old_branch
            second_branch.own_wires = own_wires_second_branch
            second_branch.own_coords = own_coords_second_branch

    def merging_branches(wire_, branches_):
        """Подпрограмма объединяет две отдельные ветви, которые соединяются новым проводом в одну ветвь"""

        def search_for_connected_branches(wire_x, branches_x):
            """Подпрограмма ищет ветви, которые соединятся в одну новым проводом"""
            start_coord_of_wire = wire_x.clamp_start.coord
            end_coord_of_wire = wire_x.clamp_end.coord
            num_brch = 0
            first_branch_ = None
            flag_branch_found = False
            while not flag_branch_found:
                first_branch_ = branches_x[num_brch]
                if start_coord_of_wire in branch_.own_coords:
                    flag_branch_found = True
                else:
                    num_brch += 1

            second_branch_ = None
            flag_branch_found = False
            while not flag_branch_found:
                second_branch_ = branches_x[num_brch]
                if end_coord_of_wire in branch_.own_coords:
                    flag_branch_found = True
                else:
                    num_brch += 1
            return first_branch_, second_branch_

        def define_priority_merged_branch(wire_x, branch_x):
            """Подпрограмма определяет приоритет объединяемой ветви"""
            if wire_x.start_coord in own_coords:
                priority = 1
            else:
                priority = 0

            if branch_x.main_wire is not None:
                priority += 2
            return priority

        def connect_branches(main_branch, attached_branch,
                             wire_x):  # В Теоретических материалах есть пояснение данной подпрограммы
            """Подпрограмма отвечает за процесс слияния двух ветвей, где первая ветвь - та, которая останется, а вторая -
             исчезнет"""

            if main_branch.end_coord == wire_x.clamp_start.coord:
                main_branch.own_wires.append(wire_x)
                main_branch.own_coords.append(wire_x.clamp_end.coord)

                if wire_x.clamp_end.coord == attached_branch.start_coord:
                    main_branch.own_wires += attached_branch.own_wires
                    main_branch.own_coords += attached_branch.own_coords[1:]
                    main_branch.end_coord = main_branch.own_coords[-1]

                else:
                    main_branch.own_wires += attached_branch.own_wires[::-1]
                    main_branch.own_coords += attached_branch.own_coords[::-1][1:]
                    main_branch.end_coord = main_branch.own_coords[-1]

            elif main_branch.end_coord == wire_x.clamp_end.coord:
                main_branch.own_wires.append(wire_x)
                main_branch.own_coords.append(wire_x.clamp_start.coord)

                if wire_x.clamp_start == attached_branch.start_coord:
                    main_branch.own_wires += attached_branch.own_wires
                    main_branch.own_coords += attached_branch.own_coords[1:]
                    main_branch.end_coord = main_branch.own_coords[-1]
                else:
                    main_branch.own_wires += attached_branch.own_wires[::-1]
                    main_branch.own_coords += attached_branch.own_coords[::-1][1:]
                    main_branch.end_coord = main_branch.own_coords[-1]

            elif main_branch.start_coord == wire_x.clamp_start.coord:
                main_branch.own_wires.insert(0, wire_x)
                main_branch.own_coords.insert(0, wire_x.clamp_end.coord)

                if wire_x.clamp_end.coord == attached_branch.start_coord:
                    main_branch.own_wires = attached_branch.own_wires[::-1] + main_branch.own_wires
                    main_branch.own_coords = attached_branch.own_coords[1:][::-1] + main_branch.own_coords
                    main_branch.start_coord = main_branch.own_coords[0]
                else:
                    main_branch.own_wires = attached_branch.own_wires + main_branch.own_wires
                    main_branch.own_coords = attached_branch.own_coords[
                                             :len(attached_branch.own_coords) - 1] + main_branch.own_coords
                    main_branch.start_coord = main_branch.own_coords[0]
            else:
                main_branch.own_wires.insert(0, wire_x)
                main_branch.own_coords.insert(0, wire_x.clamp_start.coord)

                if wire_x.clamp_start.cord == attached_branch.start_coord:
                    main_branch.own_wires = attached_branch.own_wires + main_branch.own_wires
                    main_branch.own_coords = attached_branch.own_coords[
                                             :len(attached_branch.own_coords) - 1] + main_branch.own_coords
                    main_branch.start_coord = main_branch.own_coords[0]
                else:
                    main_branch.own_wires = attached_branch.own_wires[::-1] + main_branch.own_wires
                    main_branch.own_coords = attached_branch.own_coords[1:][::-1] + main_branch.own_coords
                    main_branch.start_coord = main_branch.own_coords[0]

            branches_.remove(attached_branch)
            attached_branch.__del__()

        first_branch, second_branch = search_for_connected_branches(wire_, branches_)
        priority_first_branch = define_priority_merged_branch(wire_, first_branch)
        priority_second_branch = define_priority_merged_branch(wire_, second_branch)
        if priority_first_branch > priority_second_branch:
            connect_branches(first_branch, second_branch, wire_)
        else:
            connect_branches(second_branch, first_branch, wire_)

    def reload_start_and_end_coord_of_all_branches(branches_):
        """Подпрограмма обновляет все начальные и конечные координаты зажимов для всех ветвей"""
        for brch in branches_:
            brch.start_coord = brch.own_coords[0]
            brch.end_coord = brch.own_coords[-1]

    clamp_start = wire.clamp_start
    clamp_end = wire.clamp_end

    type_clamp_start = define_type_clamp(clamp_start)
    type_clamp_end = define_type_clamp(clamp_end)

    if type_clamp_start == 'empty':

        if type_clamp_end == 'empty':
            branch = Branch(clamp_start.coord, clamp_end.coord)
            branches.append(branch)
            add_coords_of_wire_in_branch(clamp_start.coord, clamp_end.coord, branch)
            branch.own_wires.append(wire)

        elif type_clamp_end == 'unconnected_end':
            branch = define_branch_of_wire(wire, branches)
            add_wire_in_branch(branch, wire)
            add_coords_of_wire_in_branch(clamp_start.coord, clamp_end.coord, branch)

        elif type_clamp_end == 'connection':
            branch = Branch(clamp_start.coord, clamp_end.coord)
            branches.append(branch)
            add_coords_of_wire_in_branch(clamp_start.coord, clamp_end.coord, branch)
            branch.own_wires.append(wire)
            divided_branch(branches, clamp_end.coord)

        else:
            branch = Branch(clamp_start.coord, clamp_end.coord)
            branches.append(branch)
            add_coords_of_wire_in_branch(clamp_start.coord, clamp_end.coord, branch)
            branch.own_wires.append(wire)

    elif type_clamp_start == 'unconnected_end':

        if type_clamp_end == 'empty':
            branch = define_branch_of_wire(wire, branches)
            add_wire_in_branch(branch, wire)
            add_coords_of_wire_in_branch(clamp_start.coord, clamp_end.coord, branch)
        elif type_clamp_end == 'unconnected_end':
            merging_branches(wire, branches)

    reload_start_and_end_coord_of_all_branches(branches)
    i = 0
    for branch in branches:
        print('_________Ветвь номер {0:2d}_________'.format(i))
        for attr in ['start_coord', 'end_coord', 'own_coords', 'own_wires']:
            print(attr, getattr(branch, attr))
        print('____________________________________')
        i += 1
    print('\n\n')

def reload_nodes(nodes):
    """Подпрограмма перезагружает массив узлов, добавляя новые, удаляю исчезнувшие и обновляя необходимые"""
    pass
