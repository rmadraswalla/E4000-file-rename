import shutil, os, datetime, argparse

A_STATION_IDS = ['a', 'A']
B_STATION_IDS = ['b', 'B']
C_STATION_IDS = ['c', 'C']

def rename(starting_filename, station_id, session_number, distance_travelled):
    target_folder = "data/"
    all_files = os.listdir(target_folder)
    all_files.sort() # Sorts alphabetically
    if not starting_filename in all_files:
        print ("Filename " + starting_filename + " not found in current directory")
        return False
    else:
        start_idx = all_files.index(starting_filename)

    if station_id in A_STATION_IDS:
        TSH_NUMS = range(1, 14 + 1) # Add 1 to include last index
    elif station_id in B_STATION_IDS:
        TSH_NUMS = range(15, 28 + 1) # Add 1 to include last index
    elif station_id in C_STATION_IDS:
        TSH_NUMS = range(29, 38 + 1) # Add 1 to include last index
    else:
        print ("Invalid station: %s", station_id)
        return False

    # Make parts for newname
    today = datetime.date.today()
    year = '{:04d}'.format(today.year)
    month = '{:02d}'.format(today.month)
    day = '{:02d}'.format(today.day)


    idx = start_idx
    for state in ['BEFORE', 'AFTER']:
        for tsh in TSH_NUMS:
            new_name = "%s.%s.%s_%s_%d_%d_TSH%d-%s.jpg" % (year, month, day, station_id, session_number, distance_travelled, tsh, state)
            os.rename(target_folder + all_files[idx], target_folder + new_name)
            idx += 1

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File renaming utility for wear station photos')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-f', '--starting_filename', help='Filename of first TSH picture', required=True, type=str)
    requiredNamed.add_argument('-l', '--station_letter', help='Station A/B/C', required=True, type=str)
    requiredNamed.add_argument('-n', '--session_number', help='Number of Session', required=True, type=int)
    requiredNamed.add_argument('-d', '--distance_travelled', help='Filename of first TSH picture', required=True, type=int)
    args = parser.parse_args()

    doMe = rename(args.starting_filename, args.station_letter, args.session_number, args.distance_travelled)

    if (doMe):
        print ("Renaming Complete!")
    else:
        print ("Error encountered.")
