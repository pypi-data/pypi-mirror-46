from microlab.signals import Signal_2D, Signal_1D, Intersection, Interpolation_Cubic
from microlab.geometry import create_line
from shapely.ops import snap
from shapely.ops import shared_paths
from microlab.images import create_mask, show_mask, draw_phase_on_mask, create_representation, export_mask

from microlab import plots

import os


class Sinusoidal:
    x = []
    y = []
    coordinates = {'s1': {'p1': [[], []],
                          'p2': [[], []]},
                   's2': {'p1': [[], []],
                          'p2': [[], []]}}
    edges = {'s1': [],
             's2': []}
    tunned = {'s1': [[], []],
              's2': [[], []]
              }

    closest = []

    def __init__(self, user_id, record_id, joint, signal_1=Signal_2D(), signal_2=Signal_2D(), intersections=Intersection(), report_file='',images_directory=''):
        """
        :param user_id:         the user id as string
        :param record_id:       the record id as string
        :param joint:           the joint as string
        :param signal_1:        the first signal as Signal 2D object
        :param signal_2:        the second signas as Signal 2D object
        :param intersections:   the intersection signal as Intersection object
        :param verbose:         boolean to show info messages
        :param debug:           boolean to show debug messages
        """
        self.user_id = user_id
        self.record_id = record_id
        self.reportFile = report_file
        self.images_directory = images_directory
        self.joint = joint
        self.intersections = intersections
        self.signal_1 = signal_1
        self.signal_2 = signal_2

        # generate the cordinates
        self.clear_memory()
        self.clear_edges()
        self.clear_coordinates()

    # clear
    def clear_memory(self):
        self.x = []
        self.y = []
        self.closest = []
    def clear_edges(self):
        # clear edges
        for s in self.edges:
            self.edges[s] = []


        # clear coordinates
        for signal_name, phases in self.coordinates.items():
            self.coordinates[signal_name] = {'p1': [[], []],
                                             'p2': [[], []]}
    def clear_coordinates(self):
        # clear coordinates
        for signal_name, phases in self.coordinates.items():
            self.coordinates[signal_name] = {'p1': [[], []],
                                             'p2': [[], []]}

    # Tuning
    def fine_tune(self, target_value, target_time, accuracy=0.5, verbose=False):
        self.clear_coordinates()
        self.clear_edges()
        # initialize only at first time
        if not self.edges['s1'] and not self.edges['s2']:
            self.edges['s1'] = self.closest.copy()
            self.edges['s2'] = self.closest.copy()

        first = [self.intersections.coordinates[0][0], self.intersections.coordinates[1][0]]
        second = [self.intersections.coordinates[0][1], self.intersections.coordinates[1][1]]
        third = [self.intersections.coordinates[0][2], self.intersections.coordinates[1][2]]
        diff_f_t = abs(first[1][0] - third[1][0])

        offset_value = target_value + first[1][0]
        offset_time = target_value -first[0][0]

        if verbose:
            print('[ time     ]   {}      Offset: {}'.format(target_time, offset_time))
            print('[ value    ]   {}      Offset: {}'.format(target_value, offset_value))

        # find the tuned valid points
        s1_valid = self.tune_s1(accuracy=accuracy, target_value=target_value)

        s2_valid = self.tune_s2(accuracy=accuracy, target_value=target_value)


        if len(s1_valid) > 0 :
            self.tunned['s1'] = [ [s1_valid[0][1], second[0][0], third[0][0]], [s1_valid[0][2], second[1][0], third[1][0]]]
            self.edges['s1'][0] = {'info': [s1_valid[0][0],0,0],
                                   's1': s1_valid[0]}
        else:
            print(' S1 not found')


        if len(s2_valid) > 0:
            self.tunned['s2'] = [ [s2_valid[0][1], second[0][0], third[0][0]], [s2_valid[0][2], second[1][0], third[1][0]]]
            self.edges['s2'][0] = {'info': [s2_valid[0][0], 0, 0],
                                   's2': s2_valid[0]}
        else:
            print(' S2 not found')


        self.find_edges(verbose=False)

        data = self.collect_data_between_tuned(verbose=False)

        for s_name, s in data.items():
            for axis in s:
                if len(axis) == 0:
                    return None

        self.s1_final = self.create_s1_representation(verbose=False)
        self.s2_final = self.create_s2_representation(verbose=False)


    def tune_s1(self, accuracy, target_value, verbose=False):
        first = [self.intersections.coordinates[0][0], self.intersections.coordinates[1][0]]
        second = [self.intersections.coordinates[0][1], self.intersections.coordinates[1][1]]
        third = [self.intersections.coordinates[0][2], self.intersections.coordinates[1][2]]

        offset_value = target_value + first[1][0]
        offset_time = target_value - first[0][0]

        first_closest = self.closest[0]['info'].copy()
        first_index = first_closest[0]

        second_closest = self.closest[1]['info'].copy()
        second_index = second_closest[0]

        s1_valid = []

        # Before first index
        for idx in range(0, first_index, 1):

            # get the point
            s1_time, s1_value = self.signal_1.get_point(index=idx)

            # check if its valid
            if abs(s1_value - offset_value) < accuracy and s1_value - offset_value > 0:
                s1_valid.append([idx, s1_time, s1_value])
        if len(s1_valid) == 0:

            # look for point after the first s1 point
            for idx in range(first_index, second_index, 1):
                s1_time, s1_value = self.signal_1.get_point(index=idx)

                if offset_value - s1_value < accuracy and offset_value - s1_value > 0:
                    s1_valid.append([idx, s1_time, s1_value])

            if verbose:
                print('\n S1 TUNE FOUND AFTER FIRST PHASE | {}'.format(s1_valid[0]))

        else:
            if verbose:
                print('\n S1 TUNE FOUND BEFORE FIRST PHASE | {}'.format(s1_valid[0]))

        return s1_valid
    def tune_s2(self, accuracy, target_value, verbose=False):
        first = [self.intersections.coordinates[0][0], self.intersections.coordinates[1][0]]
        second = [self.intersections.coordinates[0][1], self.intersections.coordinates[1][1]]
        third = [self.intersections.coordinates[0][2], self.intersections.coordinates[1][2]]

        offset_value = target_value + first[1][0]
        offset_time = target_value - first[0][0]

        first_closest = self.closest[0]['info'].copy()
        first_index = first_closest[0]

        second_closest = self.closest[1]['info'].copy()
        second_index = second_closest[0]

        s2_valid = []

        # Before first index
        for idx in range(0, first_index, 1):

            # get the point
            s2_time, s2_value = self.signal_2.get_point(index=idx)

            # check if its valid
            if abs(s2_value - offset_value) < accuracy and s2_value - offset_value > 0:
                s2_valid.append([idx, s2_time, s2_value])
        if len(s2_valid) == 0:

            # look for point after the first s1 point
            for idx in range(first_index, second_index, 1):

                s2_time, s2_value = self.signal_2.get_point(index=idx)

                if offset_value - s2_value < accuracy and offset_value - s2_value > 0:
                    s2_valid.append([idx, s2_time, s2_value])
            if verbose:
                print('\n S2 TUNE FOUND AFTER FIRST PHASE ')

        else:
            if verbose:
                print('\n S2 TUNE FOUND BEFORE FIRST PHASE')

        return s2_valid
    def find_edges(self, verbose=False):
        """
           Find the closed one to tunned points

        :param value:
        :param verbose:
        :return:
        """
        if verbose:
            print('\n   ------ Find Closest datum using tuned intersections -------')

        # S1
        first_idx = self.edges['s1'][0]['info'][0]
        second_idx = self.edges['s1'][1]['info'][0]
        third_idx = self.edges['s1'][2]['info'][0]
        for ideal_x, ideal_y in zip(self.tunned['s1'][0], self.tunned['s1'][1]):

            edge = {'info': [0, 0, 0],
                    's1': [[], []],
                    's2': [[], []]
                    }

            time_error = 2
            value_error = 0.1

            # Before Phase 1
            for idx in range(0, first_idx, 1):
                l_x, l_y = self.signal_1.get_point(index=idx)
                r_x, r_y = self.signal_2.get_point(index=idx)

                l_error_form_ideal_time = abs(l_x - ideal_x)
                r_error_form_ideal_time = abs(r_x - ideal_x)

                l_error_form_ideal_value = abs(ideal_y - l_y)
                r_error_form_ideal_value = abs(ideal_y - r_y)

                if l_error_form_ideal_value < value_error :

                    edge = {'info': [idx, l_error_form_ideal_value, r_error_form_ideal_value, l_error_form_ideal_time, r_error_form_ideal_time],
                            's1': [l_x, l_y],
                            's2': [r_x, r_y]}

            # Phase 1
            for idx in range(first_idx, second_idx, 1):
                l_x, l_y = self.signal_1.get_point(index=idx)
                r_x, r_y = self.signal_2.get_point(index=idx)

                l_error_form_ideal_time = abs(l_x - ideal_x)
                r_error_form_ideal_time = abs(r_x - ideal_x)

                l_error_form_ideal_value = abs(ideal_y - l_y)
                r_error_form_ideal_value = abs(ideal_y - r_y)

                if r_error_form_ideal_time < time_error and l_error_form_ideal_value < value_error and l_error_form_ideal_value < value_error:

                    edge = {'info': [idx, l_error_form_ideal_value, r_error_form_ideal_value, l_error_form_ideal_time, r_error_form_ideal_time],
                            's1': [l_x, l_y],
                            's2': [r_x, r_y]}

            self.edges['s1'].append(edge)

            if verbose:
                print('- S1 Intersection ----------------------------------------')
                print(' Index   : {}'.format(edge['info'][0]))
                print(' Ideal   : X = {}  Y = {}'.format(ideal_x, ideal_y))
                print(' value error | {}'.format(edge['info'][1]))
                print(' time  error | {}'.format(edge['info'][2]))
                print(' S1      : X = {}  Y = {}'.format(edge['s1'][0], edge['s1'][1]))
                print(' s2      : X = {}  Y = {}'.format(edge['s2'][0], edge['s2'][1]))
                print('---------------------------------------------------------\n')

        # S2
        first_idx = self.edges['s2'][0]['info'][0]
        second_idx = self.edges['s2'][1]['info'][0]
        third_idx = self.edges['s2'][2]['info'][0]
        for ideal_x, ideal_y in zip(self.tunned['s2'][0], self.tunned['s2'][1]):

            edge = {'info': [0, 0, 0],
                    's1': [[], []],
                    's2': [[], []]
                    }

            time_error = 2
            value_error = 0.1

            # Before Phase 1
            for idx in range(0, first_idx, 1):
                l_x, l_y = self.signal_1.get_point(index=idx)
                r_x, r_y = self.signal_2.get_point(index=idx)

                l_error_form_ideal_time = abs(l_x - ideal_x)
                r_error_form_ideal_time = abs(r_x - ideal_x)

                l_error_form_ideal_value = abs(ideal_y - l_y)
                r_error_form_ideal_value = abs(ideal_y - r_y)

                if l_error_form_ideal_value < value_error:
                    edge = {'info': [idx, l_error_form_ideal_value, r_error_form_ideal_value, l_error_form_ideal_time,
                                     r_error_form_ideal_time],
                            's1': [l_x, l_y],
                            's2': [r_x, r_y]}

            # Phase 1
            for idx in range(first_idx, second_idx, 1):
                l_x, l_y = self.signal_1.get_point(index=idx)
                r_x, r_y = self.signal_2.get_point(index=idx)

                l_error_form_ideal_time = abs(l_x - ideal_x)
                r_error_form_ideal_time = abs(r_x - ideal_x)

                l_error_form_ideal_value = abs(ideal_y - l_y)
                r_error_form_ideal_value = abs(ideal_y - r_y)

                if r_error_form_ideal_time < time_error and l_error_form_ideal_value < value_error and l_error_form_ideal_value < value_error:
                    edge = {'info': [idx, l_error_form_ideal_value, r_error_form_ideal_value, l_error_form_ideal_time,
                                     r_error_form_ideal_time],
                            's1': [l_x, l_y],
                            's2': [r_x, r_y]}

            # Phase 2
            # for idx in range(second_idx, third_idx, 1):
            #     # if idx < 6129:
            #     #     print(idx)
            #     l_x, l_y = self.signal_1.get_point(index=idx)
            #     r_x, r_y = self.signal_2.get_point(index=idx)
            #
            #     l_error_form_ideal_time = abs(l_x - ideal_x)
            #     r_error_form_ideal_time = abs(r_x - ideal_x)
            #
            #     l_error_form_ideal_value = abs(ideal_y - l_y)
            #     r_error_form_ideal_value = abs(ideal_y - r_y)
            #
            #     if  r_error_form_ideal_time < time_error and l_error_form_ideal_value < value_error and l_error_form_ideal_value < value_error:
            #
            #         edge = {'info': [idx, l_error_form_ideal_value, r_error_form_ideal_value, l_error_form_ideal_time, r_error_form_ideal_time],
            #                 's1': [l_x, l_y],
            #                 's2': [r_x, r_y]}

            self.edges['s2'].append(edge)

            if verbose:
                print('- S2 Intersection ----------------------------------------')
                print(' Index   : {}'.format(edge['info'][0]))
                print(' Ideal   : X = {}  Y = {}'.format(ideal_x, ideal_y))
                print(' value error | {}'.format(edge['info'][1]))
                print(' time  error | {}'.format(edge['info'][2]))
                print(' S1      : X = {}  Y = {}'.format(edge['s1'][0], edge['s1'][1]))
                print(' s2      : X = {}  Y = {}'.format(edge['s2'][0], edge['s2'][1]))
                print('---------------------------------------------------------\n')

    # choose the final intersected points

    def find_closest_datum_to_intersection(self, verbose=False):
        if verbose:
            print('\n   ------ Find Closest datum -------')
        self.closest = []

        # Find the closed point one to ideal intersection points
        for point in self.intersections.points:
            ideal_x, ideal_y = point.xy[0].tolist()[0], point.xy[1].tolist()[0]

            edge = {'info': [0, 0, 0],
                    's1': [[], []],
                    's2': [[], []]
                    }

            time_error = 2
            value_error = 0.1

            for idx in range(self.signal_1.length_x()):
                l_x, l_y = self.signal_1.get_point(index=idx)
                r_x, r_y = self.signal_2.get_point(index=idx)

                l_ideal_time__offset = abs(l_x - ideal_x)
                r_ideal_time_offset = abs(r_x - ideal_x)

                l_ideal_value__offset = abs(ideal_y - l_y)
                r_ideal_value__offset = abs(ideal_y - r_y)

                if l_ideal_time__offset < time_error and r_ideal_time_offset < time_error and l_ideal_value__offset < value_error and l_ideal_value__offset < value_error:

                    edge = {'info': [idx, l_ideal_value__offset, r_ideal_value__offset, l_ideal_time__offset, r_ideal_time_offset],
                            's1': [l_x, l_y],
                            's2': [r_x, r_y]}

            self.closest.append(edge)

            if verbose:
                print('- Intersection {} ----------------------------------------'.format(len(self.closest)))
                print(' Index   : {}'.format(edge['info'][0]))
                print(' Ideal   : X = {}  Y = {}'.format(ideal_x, ideal_y))
                print(' value error | {}'.format(edge['info'][1]))
                print(' time  error | {}'.format(edge['info'][2]))
                print(' S1      : X = {}  Y = {}'.format(edge['s1'][0], edge['s1'][1]))
                print(' s2      : X = {}  Y = {}'.format(edge['s2'][0], edge['s2'][1]))
                print('---------------------------------------------------------\n')


    # collect
    def collect_data_between_closest(self, verbose=False):
        """
            collect the data between final intersected points

        :param verbose:
        :return:
        """
        point1 = self.intersections.points[0]
        point2 = self.intersections.points[1]
        point3 = self.intersections.points[2]

        point1_x, point1_y = point1.xy[0].tolist()[0], point1.xy[1].tolist()[0]
        point2_x, point2_y = point2.xy[0].tolist()[0], point1.xy[1].tolist()[0]
        point3_x, point3_y = point3.xy[0].tolist()[0], point1.xy[1].tolist()[0]

        one_time = self.closest[0]['info'][0]
        two_time = self.closest[1]['info'][0]
        three_time = self.closest[2]['info'][0]

        if verbose:
            print('\n~1-2 one:{} two:{} three:{}'.format(one_time, two_time, three_time))

        s1_time_1_2 = self.signal_1.x[one_time:two_time]
        s1_1_2 = self.signal_1.y[one_time:two_time]
        self.s1_s_1_2 = Signal_2D(values=s1_1_2, time=s1_time_1_2, verbose=False)

        s2_time_1_2 = self.signal_2.x[one_time:two_time]
        s2_1_2 = self.signal_2.y[one_time:two_time]
        self.s2_s_1_2 = Signal_2D(values=s2_1_2, time=s2_time_1_2, verbose=False)

        if verbose:
            print('\n~2-3')
        s1_time_2_3 = self.signal_1.x[two_time:three_time]
        s1_2_3 = self.signal_1.y[two_time:three_time]
        self.s1_s_2_3 = Signal_2D(values=s1_2_3, time=s1_time_2_3, verbose=False)

        s2_time_2_3 = self.signal_2.x[two_time:three_time]
        s2_2_3 = self.signal_2.y[two_time:three_time]
        self.s2_s_2_3 = Signal_2D(values=s2_2_3, time=s2_time_2_3, verbose=False)

        return {'S1': [s1_time_1_2, s1_time_2_3],
                'S2': [s2_time_1_2, s2_time_2_3]}
    def collect_data_between_tuned(self, verbose=False):

        s1_one_time = self.edges['s1'][0]['info'][0]
        s1_two_time = self.edges['s1'][1]['info'][0]
        s1_three_time = self.edges['s1'][2]['info'][0]
        # two_cycle = self.edges['s1'][1]['s1'][1]


        s2_one_time = self.edges['s2'][0]['info'][0]
        s2_two_time = self.edges['s2'][1]['info'][0]
        s2_three_time = self.edges['s2'][2]['info'][0]
        # three_cycle = self.edges['s1'][2]['s1'][1]

        if verbose:
            print('S1 1', self.edges['s1'][0])
            print('S1 2', self.edges['s1'][1])
            print('S1 3', self.edges['s1'][2])

            print('\nS2 1', self.edges['s2'][0])
            print('S2 2', self.edges['s2'][1])
            print('S2 3', self.edges['s2'][2])

            print('\n S1  Phase 1  | one:{} two:{} three:{}'.format(s1_one_time, s1_two_time, s1_three_time))
            print(' S2  Phase 2  | one:{} two:{} three:{}'.format(s2_one_time, s2_two_time, s2_three_time))

        s1_time_1_2 = self.signal_1.x[s1_one_time:s1_two_time]
        s1_1_2 = self.signal_1.y[s1_one_time:s1_two_time]
        self.s1_s_1_2 = Signal_2D(values=s1_1_2, time=s1_time_1_2, verbose=False)


        s2_time_1_2 = self.signal_2.x[s2_one_time:s2_two_time]
        s2_1_2 = self.signal_2.y[s2_one_time:s2_two_time]
        self.s2_s_1_2 = Signal_2D(values=s2_1_2, time=s2_time_1_2, verbose=False)

        if verbose:
            print('\n~2-3')
        s1_time_2_3 = self.signal_1.x[s1_two_time:s1_three_time]
        s1_2_3 = self.signal_1.y[s1_two_time:s1_three_time]
        self.s1_s_2_3 = Signal_2D(values=s1_2_3, time=s1_time_2_3, verbose=False)

        s2_time_2_3 = self.signal_2.x[s2_two_time : s2_three_time]
        s2_2_3 = self.signal_2.y[s2_two_time : s2_three_time]
        self.s2_s_2_3 = Signal_2D(values=s2_2_3, time=s2_time_2_3, verbose=False)

        return {'S1': [s1_time_1_2, s1_time_2_3],
                'S2': [s2_time_1_2, s2_time_2_3]}

    # create
    def create_s1_representation(self, verbose=False):

        point1 = self.intersections.points[0]
        point2 = self.intersections.points[1]
        point3 = self.intersections.points[2]

        point1_x, point1_y = point1.xy[0].tolist()[0], point1.xy[1].tolist()[0]
        point2_x, point2_y = point2.xy[0].tolist()[0], point2.xy[1].tolist()[0]
        point3_x, point3_y = point3.xy[0].tolist()[0], point3.xy[1].tolist()[0]
        if verbose:
            print('P1 : {},{}'.format(point1_x, point1_y))
            print('P2 : {},{}'.format(point2_x, point2_y))
            print('P3 : {},{}'.format(point3_x, point3_y))
        s1_values = []
        s1_time = []

        # Collect 1 - 2
        for y in self.s1_s_1_2.y:
            x = len(s1_time) + 1
            i = self.s1_s_1_2.y.index(y)
            j = self.s1_s_1_2.x[i]

            s1_values.append(y)
            s1_time.append(x)

        self.coordinates['s1']['p1'][1].extend(s1_values)
        self.coordinates['s1']['p1'][0].extend(s1_time)

        s12 = Signal_2D(values=s1_values, time=s1_time ,verbose=False)

        # Collect 2 - 3
        s1_max_idx = len(s1_time)
        s1_values = []
        s1_time = []
        collect = True
        for y in self.s1_s_2_3.y:
            i = self.s1_s_2_3.y.index(y)
            j = self.s1_s_2_3.x[i]
            # print(y-one_time, two_cycle)
            a = len(s1_time)
            x = s1_max_idx - a
            if y > point1_y or x > 0 and collect:
                # print(x,point1_x,point1_y, j, y,)
                # print(i,x,j,point1_x ,y,point1_y,)
                s1_values.append(y)
                s1_time.append(x)
            # else:
            #     collect = False
            # print(s1_max_idx-a)
            # print(a)

            # print(x, j, y, 'left needs ', j - point2_x, y - point2_y)

        # create signal 1 sinusoidal representation
        self.coordinates['s1']['p2'][1].extend(s1_values)
        self.coordinates['s1']['p2'][0].extend(s1_time)

        s23 = Signal_2D(values=s1_values, time=s1_time,verbose=False)
        return [s12, s23]

    def create_s2_representation(self, verbose=False):

        point1 = self.intersections.points[0]
        point2 = self.intersections.points[1]
        point3 = self.intersections.points[2]

        point1_x, point1_y = point1.xy[0].tolist()[0], point1.xy[1].tolist()[0]
        point2_x, point2_y = point2.xy[0].tolist()[0], point1.xy[1].tolist()[0]
        point3_x, point3_y = point3.xy[0].tolist()[0], point1.xy[1].tolist()[0]

        if verbose:
            print('P1 : {},{}'.format(point1_x, point1_y))
            print('P2 : {},{}'.format(point2_x, point2_y))
            print('P3 : {},{}'.format(point3_x, point3_y))

        # Collect 1 - 2
        s2_values = []
        s2_time = []
        for y in self.s2_s_1_2.y:
            i = self.s2_s_1_2.y.index(y)
            j = self.s2_s_1_2.x[i]
            x = len(s2_time) + 1
            s2_values.append(y)
            s2_time.append(x)
        self.coordinates['s2']['p1'][1].extend(s2_values)
        self.coordinates['s2']['p1'][0].extend(s2_time)

        # Collect 2 - 3
        s2_max_idx = len(s2_time)
        s2_values = []
        s2_time = []
        collect = True
        for y in self.s2_s_2_3.y:
            a = len(s2_time)
            x = s2_max_idx - a

            i = self.s2_s_2_3.y.index(y)
            j = self.s2_s_2_3.x[i]

            # if abs(j-point1_y) > 0:

            # if y > point1_y or x > 0 and collect:
            s2_values.append(y)
            s2_time.append(x)

            # print(a, x, j, y)
            # print(j, x, y, 'right needs ', y - point1_y)

        # create signal 1 sinusoidal representation

        self.coordinates['s2']['p2'][1].extend(s2_values)
        self.coordinates['s2']['p2'][0].extend(s2_time)

    # visualize
    def draw_plot(self):
        # self.figure = plots.plt.figure()
        #
        # self.figure.suptitle('{} Gait Analysis on record {} on {}'.format(self.user_id,self.record_id, self.joint), fontsize=16)
        #
        # plots.plt.plot(self.signal_1.x,self.signal_1.y)
        # plots.plt.show()


        # prepair the figure

        point1 = self.intersections.points[0]
        point2 = self.intersections.points[1]
        point3 = self.intersections.points[2]

        point1_x, point1_y = point1.xy[0].tolist()[0], point1.xy[1].tolist()[0]
        point2_x, point2_y = point2.xy[0].tolist()[0], point1.xy[1].tolist()[0]
        point3_x, point3_y = point3.xy[0].tolist()[0], point1.xy[1].tolist()[0]




        plt = plots.plt
        plt.close('all')
        fig = plt.figure()
        fig.suptitle('Analysis for user {} , record {} , joint {}'.format(self.user_id, self.record_id, self.joint), fontsize=16)

        # Signal 1
        s1_intersects = [
            [self.closest[0]['s1'][0], self.closest[1]['s1'][0], self.closest[2]['s1'][0]],
            [self.closest[0]['s1'][1], self.closest[1]['s1'][1], self.closest[2]['s1'][1]]
        ]
        plt.subplot(2, 4, 1)
        plt.title('S1 (X:{}, Y:{}) '.format(len(self.signal_1.x), len(self.signal_1.y)))
        plt.plot(self.signal_1.x, self.signal_1.y, '.', color='black')
        plt.plot(s1_intersects[0], s1_intersects[1], '.-g')
        plt.plot(s1_intersects[0], s1_intersects[1], 'or')

        if len(self.tunned['s1'][0]) > 1:
            plt.plot(self.tunned['s1'][0][0], self.tunned['s1'][1][0], 'o', color='blue')

        plt.grid()


        plt.subplot(2, 4, 2)
        plt.title('S1 phases (A:{}, B:{})'.format(len(self.s1_s_1_2.x), len(self.s1_s_2_3.x)))
        plt.plot(self.s1_s_1_2.x, self.s1_s_1_2.y, '.-', color='orange')
        plt.plot(self.s1_s_2_3.x, self.s1_s_2_3.y, '.-', color='magenta')

        if len(self.tunned['s1'][0]) > 1:
            plt.plot(self.tunned['s1'][0][0], self.tunned['s1'][1][0], 'o', color='blue')
            plt.plot(s1_intersects[0][1], s1_intersects[1][1], 'o-', color='blue')
            plt.plot(s1_intersects[0][2], s1_intersects[1][2], 'o-', color='blue')

        # plt.plot(self.edges['s1'][0]['s1'][0], self.edges['s1'][0]['s1'][0], '.-g')
        # plt.plot(self.edges['s1'][0]['s1'][0], self.edges['s1'][0]['s1'][1], 'or')

        # plt.plot(self.edges[0]['s1'][0], self.edges[0]['s1'][1], '.-g')
        # plt.plot(self.edges[0]['s1'][0], self.edges[0]['s1'][1], 'or')

        plt.grid()


        plt.subplot(2, 4, 3)
        plt.title('S1 Sinusoidal (X:{}, Y:{})'.format(len(self.coordinates['s1']['p1'][0]), len(self.coordinates['s1']['p1'][1])))
        plt.plot(self.coordinates['s1']['p1'][0], self.coordinates['s1']['p1'][1], '.', color='black')
        plt.plot(self.coordinates['s1']['p2'][0], self.coordinates['s1']['p2'][1], '.', color='black')

        # plt.plot(self.coordinates[''].x, self.F.y, '.', color='magenta')

        # plt.plot(s1_intersects[0], s1_intersects[1], '.-', color='black', markersize=8)
        # plt.plot(s1_intersects[0], s1_intersects[1], 'o', color='red', markersize=3)
        plt.grid()

        # Signal 2
        s2_intersects = [
            [self.closest[0]['s2'][0], self.closest[1]['s2'][0], self.closest[2]['s2'][0]],
            [self.closest[0]['s2'][1], self.closest[1]['s2'][1], self.closest[2]['s2'][1]]
        ]
        plt.subplot(2, 4, 5)
        plt.title('S2 (X:{}, Y:{}) '.format(len(self.signal_2.x), len(self.signal_2.y)))
        plt.plot(self.signal_2.x, self.signal_2.y, '.', color='black')
        # print(len(self.closest))
        plt.plot(s2_intersects[0], s2_intersects[1], '.-g')
        plt.plot(s2_intersects[0], s2_intersects[1], 'or')

        if len(self.tunned['s2'][0]) > 1:
            plt.plot(self.tunned['s2'][0][0], self.tunned['s2'][1][0], 'o', color='blue')

        plt.grid()


        plt.subplot(2, 4, 6)
        plt.title('S2 phases (A:{}, B:{})'.format(len(self.s2_s_1_2.x), len(self.s2_s_2_3.x)))
        plt.plot(self.s2_s_1_2.x, self.s2_s_1_2.y, '.', color='orange')
        plt.plot(self.s2_s_2_3.x, self.s2_s_2_3.y, '.', color='magenta')
        if len(self.tunned['s2'][0]) > 1:
            plt.plot(self.tunned['s2'][0][0], self.tunned['s2'][1][0], 'o', color='blue')
            plt.plot(s2_intersects[0][1], s2_intersects[1][1], 'o', color='blue')
            plt.plot(s2_intersects[0][2], s2_intersects[1][2], 'o', color='blue')

        plt.grid()


        plt.subplot(2, 4, 7)
        plt.title('S2 Sinusoidal (X:{}, Y:{})'.format(len(self.coordinates['s2']['p1'][0]), len(self.coordinates['s2']['p1'][1])))
        plt.plot(self.coordinates['s2']['p1'][0], self.coordinates['s2']['p1'][1], '.', color='black')
        plt.plot(self.coordinates['s2']['p2'][0], self.coordinates['s2']['p2'][1], '.', color='black')
        # plt.plot(s2_intersects[0], s2_intersects[1], '.-', color='black', markersize=8)

        # plt.plot(s2_intersects[0], s2_intersects[1], '.-', color='black', markersize=8)
        # plt.plot(s2_intersects[0], s2_intersects[1], 'o', color='red', markersize=3)

        plt.grid()

        fig.set_size_inches(20, 10)

    def draw_masks(self, verbose=False):
        width = 5000
        height = 2000
        self.s1_mask = create_representation(phase1=self.coordinates['s1']['p1'],
                                            phase2=self.coordinates['s1']['p2'],
                                            width=width,
                                            height=height,
                                            verbose=verbose)

        self.s2_mask = create_representation(phase1=self.coordinates['s2']['p1'],
                                            phase2=self.coordinates['s2']['p2'],
                                            width=width,
                                            height=height,
                                            verbose=verbose)

    def show_mask(self, mask):
        show_mask(mask=mask)

    def export_masks(self, verbose=False):
        file_name = os.path.join(self.images_directory, 's1_{}.jpg'.format(self.joint))
        export_mask(mask=self.s1_mask, file_name=file_name, verbose=verbose)

        file_name = os.path.join(self.images_directory, 's2_{}.jpg'.format(self.joint))
        export_mask(mask=self.s2_mask, file_name=file_name, verbose=verbose)

    def show(self):
        plt = plots.plt
        plt.show()

    # export
    def export_plot(self):
        print('[ results ]  saving to {}'.format(self.reportFile))
        plt = plots.plt
        plt.savefig(fname=self.reportFile, dpi=100, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None, metadata=None)

        # close the plt to release memory
        plt.close('all')
