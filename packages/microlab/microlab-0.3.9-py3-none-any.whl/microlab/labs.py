from microlab.files import read_json, create_folder
from microlab.signals import Signal_1D, Signal_2D, Interpolation_Cubic, Intersection
from microlab.analysis import Sinusoidal

import os


class Representation:
    __version__ = '0.2'

    # Joints selection
    selected_joints = []
    selected_users = []
    metrics = {}
    calculated = {}

    # Flags
    verbose = False
    debug = False
    info = False

    # Data
    user_id = None
    record_id = None
    joint = None
    filename = None
    cycles = None

    def __init__(self, verbose=False, debug=False, info=False, selected_joints=[], selected_users=[], records_directory='', results_directory='', images_directory=''):
        # Flags
        self.verbose = verbose
        self.debug = debug
        self.info = info

        # Input
        self.records_dir = records_directory

        # Output
        self.results_directory = results_directory
        create_folder(results_directory, verbose=False)

        self.images_directory = images_directory

        # Joints
        self.selected_joints = selected_joints
        for joint in self.selected_joints:
            self.metrics[joint] = 0

        # Users
        if 'all' in selected_users:
            self.selected_users = os.listdir(records_directory)
        else:
            self.selected_users = selected_users


    def screen(self):
        print('  - - - - - - - - - - - - - - - - - -')
        print('     Representation Generator  v.{}'.format(self.__version__))
        print('  - - - - - - - - - - - - - - - - - -')
        for user_id in self.calculated:
            print('\n------ User: {} ---------'.format(user_id))
            joints = self.calculated[user_id]
            for joint in joints:
                counter = self.calculated[user_id][joint]
                print(joint, counter)

    def mark_as_finished(self):
        # already known user
        if self.user_id in self.calculated:
            self.calculated[self.user_id][self.joint] += 1

        # new user
        else:
            self.calculated[self.user_id] = dict(self.metrics)

    def set(self, user_id, record_id, filename, report_file):
        self.user_id = str(user_id)
        self.record_id = str(record_id)
        self.filename = filename
        self.report_file = report_file
        self.load_data()

    def load_data(self):
        path_to_file = os.path.join(self.records_dir, self.user_id, self.record_id, self.filename)
        if os.path.isfile(path_to_file):
            self.filename = path_to_file
            self.cycles = read_json(path=self.filename, verbose=self.verbose)

    def data_is_valid(self, data):
        for s_name, s in data.items():
            for axis in s:
                if len(axis) == 0:
                    return True
        return True

    def exetasis(self):
        for joint in self.cycles:

            if self.verbose:
                print('User:{}  Record:{}  Joint:{} '.format(self.user_id, self.record_id, joint), end=' .....')

            """ Data Selection """
            left_distance = self.cycles[joint]['Left']['Distance'][:-1]
            left_frames = self.cycles[joint]['Left']['Frames']

            right_distance = self.cycles[joint]['Right']['Distance'][:-1]
            right_frames = self.cycles[joint]['Right']['Frames']

            if self.verbose:
                print('User:{}  Record:{}  Joint:{} '.format(self.user_id, self.record_id, joint), end=' .....')

            """ Data validation """
            if joint in self.selected_joints and len(left_distance) > 0 and len(right_distance) > 0:
                self.joint = joint

                print(' -----------')
                print('  {}-{}-{}'.format(self.user_id, self.record_id, self.joint))
                """ Convert Data to 2D Signal """
                left_signal = Signal_2D(values=left_frames, time=left_distance, verbose=False)
                # left_signal.show(title=' {} Left Cycle Data'.format(joint), marker='ob')

                right_signal = Signal_2D(values=right_frames, time=right_distance, verbose=False)
                # right_signal.show(title='  {} Right Cycle Data'.format(joint), marker='ob')

                """ Intersect the Signals """
                intersections = Intersection(name=joint, signal_a=left_signal, signal_b=right_signal, verbose=False)

                """ Needed 3 intersections """
                if len(intersections.points) == 3:

                    """ Interpolate the 1D Signals """
                    temp_left = Signal_1D(values=left_signal.x, serialized=True, verbose=False)
                    temp_right = Signal_1D(values=right_signal.x, serialized=True, verbose=False)

                    total_number = 10000
                    left_interpolated = Interpolation_Cubic(signal=temp_left, total_number=total_number, verbose=False)
                    # left_interpolated.show(title=' {} Left Interpolated'.format(joint), marker='.')

                    right_interpolated = Interpolation_Cubic(signal=temp_right, total_number=total_number,
                                                             verbose=False)
                    # right_interpolated.show(title='{} Right interpolated'.format(joint), marker='.')

                    if self.verbose:
                        print('[ OK ]')

                    """ Analysis Report """
                    gait = Sinusoidal(user_id=self.user_id,
                                      record_id=self.record_id,
                                      joint=joint,
                                      signal_1=left_interpolated,
                                      signal_2=right_interpolated,
                                      intersections=intersections,
                                      report_file=os.path.join(self.report_file, '{}.jpg'.format(self.joint)),
                                      images_directory=self.record_images_directory
                                      )

                    # choose the final intersected points
                    closest = gait.find_closest_datum_to_intersection(verbose=self.verbose)

                    # collect the data between final intersected points
                    data = gait.collect_data_between_closest(verbose=self.verbose)

                    # when a signal is empty , stop the analysis
                    if self.data_is_valid(data):

                        # create with out tolerance
                        gait.create_s1_representation(verbose=self.verbose)
                        gait.create_s2_representation(verbose=self.verbose)

                        if len(gait.intersections.coordinates[0]) == 3:
                            first = [gait.intersections.coordinates[0][0], gait.intersections.coordinates[1][0]]
                            second = [gait.intersections.coordinates[0][1], gait.intersections.coordinates[1][1]]
                            third = [gait.intersections.coordinates[0][2], gait.intersections.coordinates[1][2]]
                            diff_f_t = abs(first[1][0] - third[1][0])
                            diff_f_y = abs(first[0][0] - third[0][0])
                            # print('first {}'.format(first))
                            # print('second {}'.format(second))
                            # print('third {}'.format(third))
                            # pass without tolerance
                            # print('its {}'.format(diff_f_t))

                            # fine tune the representation , using tolerance
                            if diff_f_t > 0:
                                if self.info:
                                    print('[  1 -3    ] has offset {} , auto fine tune'.format(diff_f_t))
                                gait.fine_tune(target_value=diff_f_t, target_time=diff_f_y, accuracy=0.3, verbose=False)
                            else:
                                if self.info:
                                    print('[  1 -3    ] has offset {}'.format(diff_f_t))

                            self.mark_as_finished()
                            # Report
                            gait.draw_plot()
                            # gait.show()
                            gait.export_plot()

                            # Masks
                            gait.draw_masks()
                            gait.export_masks(verbose=True)


                else:
                    print('[ rejected ] {} has {} intersection points'.format(self.joint, len(intersections.points)))
                    print(' -----------')

            else:
                if self.info:
                    print('[ invalid  ] lengths of the signals S1:{}  S2:{}'.format(len(left_distance), len(right_distance)))

    def start(self):
        for dirName, subdirList, fileList in os.walk(self.records_dir):
            if len(subdirList) == 0:
                user_id = dirName.split('/')[-2]
                record_id = dirName.split('/')[-1]



                # print(dirName)
                # print(user_id)
                # print(record_id)

                if user_id in self.selected_users:
                    if self.info:
                        print('\n[ record   ] {}'.format(os.path.join(dirName, record_id)))
                    # user results
                    print(dirName)
                    user_directory = os.path.join(self.results_directory, user_id)
                    create_folder(user_directory, verbose=False)
                    # record results
                    report_file = os.path.join(self.results_directory, user_id, record_id)
                    create_folder(report_file, verbose=False)

                    # user masks
                    user_images_directory = os.path.join(self.images_directory, user_id)
                    create_folder(user_images_directory, verbose=False)
                    # record masks
                    self.record_images_directory = os.path.join(self.images_directory, user_id, record_id)
                    create_folder(self.record_images_directory, verbose=False)

                    # set the data
                    self.set(user_id=user_id, record_id=record_id, filename='cycle.json', report_file=report_file)

                    try:
                        self.exetasis()

                    except:
                        if self.info:
                            print('[!] Failed')

            # for folder in subdirList:
            #     for userDir, recordFolders, recordFiles in os.walk(os.path.join(records, folder)):
            #         user_id = userDir.split('/')[-1]
            #         if user_id in self.selected_users:
            #             for a, b, f in os.walk(userDir):
            #                 for record_id in b:
            #                     if self.info:
            #                         print('\n[ record   ] {}'.format(os.path.join(userDir, record_id)))
            #                     # report_file = os.path.join(self.records_dir, user_id, record_id)
            #                     # self.set(user_id=user_id, record_id=record_id, filename='cycle.json', report_file=report_file)
            #
            #                     try:
            #                         self.exetasis()
            #
            #                     except:
            #                         if self.info:
            #                             print('[!] Failed')
