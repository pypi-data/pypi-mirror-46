from microlab import sotware


if __name__ == '__main__':
    print(' ~ TEST SOFWARE ')
    sw = sotware.statistics()
    for software_name, software_details in sw.items():
        print('\n{}'.format(software_name))
        for detail, value in software_details.items():
            print('  -', detail, value)
