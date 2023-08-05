from microlab.signals import Signal_2D, Signal_1D, Intersection, Interpolation_Cubic
from microlab.geometry import create_line
from shapely.geometry.polygon import Polygon


ideal_time_limit = 1.5
ideal_value_limit = 1.2


class Sinusoidal:

    def __init__(self, user_id, record_id, joint, signal_1=Signal_2D(), signal_2=Signal_2D(), intersections=Intersection(), verbose=False):
        self.user_id = user_id
        self.record_id = record_id
        self.joint = joint
        self.intersections = intersections
        self.signal_1 = signal_1
        self.signal_2 = signal_2

        accepted = []

        # Find the closed one to ideal intersection points
        for point in intersections.points:
            ideal_x, ideal_y = point.xy[0].tolist()[0], point.xy[1].tolist()[0]
            if verbose:
                print('\nIdeal point | X:{} , Y:{} '.format(ideal_x, ideal_y))

            accepted_info = [0, 0, 0]
            accepted_left = [[], []]
            accepted_right = [[], []]

            collecting = False
            time_error = 1.2
            value_error = 1.5
            for idx in range(0, len(signal_1.x), 1):
                l_x = signal_1.x[idx]
                l_y = signal_1.y[idx]

                r_x = signal_2.x[idx]
                r_y = signal_2.y[idx]

                error_form_ideal_time = abs(l_x - ideal_x)
                error_form_ideal_value = abs(ideal_y - l_y)

                if error_form_ideal_time < time_error and error_form_ideal_value < value_error:
                    time_error = error_form_ideal_time
                    value_error = error_form_ideal_value
                    collecting = True

                    # diff_y is the error from ideal intersection
                    accepted_info = [idx, error_form_ideal_value, error_form_ideal_time]
                    accepted_left = [l_x, l_y]
                    accepted_right = [r_x, r_y]

            accepted.append({'info': accepted_info,
                             'Left': accepted_left,
                             'Right': accepted_right
                             })

            if verbose:
                print('Index: {}'.format(accepted_info[0]))
                print('Ideal value error  :', accepted_info[1])
                print('Ideal time  error  :', accepted_info[2])
                print('Left:  {}, {}'.format(accepted_left[0], accepted_left[1]))
                print('Right: {}, {}'.format(accepted_right[0], accepted_right[1]))
                print('----------------------------')


        one_time = accepted[0]['info'][0]
        one_cycle = accepted[0]['Left'][0]

        two_time = accepted[1]['info'][0]
        two_cycle = accepted[1]['Left'][1]

        three_time = accepted[2]['info'][0]
        three_cycle = accepted[2]['Left'][1]

        if verbose:
            print('\n~1-2 one:{} two:{} three:{}'.format(one_time,two_time,three_time))

        left_time_1_2 = signal_1.x[one_time:two_time]
        left_1_2 = signal_1.y[one_time:two_time]
        left_s_1_2 = Signal_2D(values=left_1_2, time=left_time_1_2, verbose=True)

        right_time_1_2 = signal_2.x[one_time:two_time]
        right_1_2 = signal_2.y[one_time:two_time]
        right_s_1_2 = Signal_2D(values=right_1_2, time=right_time_1_2, verbose=True)

        print('\n~ 2-3')
        left_time_2_3 = signal_1.x[two_time:three_time]
        left_2_3 = signal_1.y[two_time:three_time]
        left_s_2_3 = Signal_2D(values=left_2_3, time=left_time_2_3, verbose=True)

        right_time_2_3 = signal_2.x[two_time:three_time]
        right_2_3 = signal_2.y[two_time:three_time]
        right_s_2_3 = Signal_2D(values=right_2_3, time=right_time_2_3, verbose=True)


        left_gaitprint = []
        left_time = []
        for y in left_s_1_2.y.copy():
            # if (y - one_time ) > 0:
                left_gaitprint.append(y)
                left_time.append(len(left_time) + 1)
        left_max_idx = len(left_time)

        # print('last left', left_max_idx)

        for y in left_s_2_3.y.copy():
            # print(y-one_time, two_cycle)
            a = len(left_time) - left_max_idx
            left_gaitprint.append(y)
            # print(left_max_idx-a)
            # print(a)
            left_time.append(left_max_idx - a)

        right_gaitprint = []
        right_time = []
        for y in right_s_1_2.y.copy():
            right_gaitprint.append(y)
            right_time.append(len(right_time) + 1)
        right_max_idx = len(right_time)

        # print('last right', right_max_idx)

        for y in right_s_2_3.y.copy():
                # print(abs(y-ideal_y))
                a = len(right_time) - right_max_idx
                right_gaitprint.append(y)
                right_time.append(right_max_idx - a)

        if len(left_time_1_2) > 0 and len(left_time_2_3) > 0 and len(right_time_1_2) > 0 and len(right_time_2_3):
            # intersections.show(title='User:{} Record:{} Joint:{} Intersections'.format(user_id, record_id, joint), marker='og')
            # intersections.show_coordinates()
            left_g = Signal_2D(values=left_time, time=left_gaitprint, verbose=True)
            left_g.show(title='User:{} Record:{} Joint:{} Signal 1 '.format(user_id,record_id,joint), marker='.')

            poly = Polygon([[0,0],[1,0],[1,1],[0,1]])

            # import numpy
            # from PIL import Image, ImageDraw
            # img = Image.new('L', (1800, 1000), 0)
            # ImageDraw.Draw(img).polygon([(0,0),(1,0),(1,1),(0,1)], outline=1, fill=1)
            # mask = numpy.array(img)
            # import cv2
            # cv2.imshow('mask', mask)
            # cv2.waitKey(0)

            right_g = Signal_2D(values=right_time, time=right_gaitprint, verbose=True).show(title='User:{} Record:{} Joint:{} Signal 2 '.format(user_id,record_id,joint), marker='-')

