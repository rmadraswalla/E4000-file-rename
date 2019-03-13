import shutil, os, datetime, argparse, re

A_STATION_IDS = ['a', 'A']
B_STATION_IDS = ['b', 'B']
C_STATION_IDS = ['c', 'C']

def rename(img_src_folder, img_dest_folder, starting_filename, station_id, session_number, distance_travelled, date_str, parse_ds, wrong_way):
    if date_str is not None:
        test_date = datetime.datetime.strptime(date_str, r'%Y.%m.%d')
    else:
        test_date = datetime.date.test_date()

    try:
        os.mkdir(img_dest_folder)
    except FileExistsError as e:
        pass

    all_files = os.listdir(img_src_folder)
    all_files.sort() # Sorts alphabetically

    if starting_filename is not None:
        if not starting_filename in all_files:
            print ("Filename " + starting_filename + " not found in current directory")
            return False
        else:
            start_idx = all_files.index(starting_filename)
    else:
        start_idx = 0

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
    year = '{:04d}'.format(test_date.year)
    month = '{:02d}'.format(test_date.month)
    day = '{:02d}'.format(test_date.day)

    files_copied = []

    idx = start_idx
    if wrong_way:
        for tsh in TSH_NUMS:
            for state in ['BEFORE', 'AFTER']:
                new_name = "%s.%s.%s_%s_%d_%d_TSH%d-%s.jpg" % (year, month, day, station_id.upper(), session_number, distance_travelled, tsh, state)
                shutil.copyfile(img_src_folder + all_files[idx], img_dest_folder + new_name)
                files_copied.append(all_files[idx])
                idx += 1
    else:
        for state in ['BEFORE', 'AFTER']:
            for tsh in TSH_NUMS:
                new_name = "%s.%s.%s_%s_%d_%d_TSH%d-%s.jpg" % (year, month, day, station_id.upper(), session_number, distance_travelled, tsh, state)
                shutil.copyfile(img_src_folder + all_files[idx], img_dest_folder + new_name)
                files_copied.append(all_files[idx])
                idx += 1

    ds_num = 0
    for idx in range(0, len(all_files)):
        if all_files[idx] in files_copied: continue
        if parse_ds:
            if station_id in A_STATION_IDS or station_id in B_STATION_IDS:
                ds_num += 1
                new_name = "%s.%s.%s_%s_%d_%d_DS_%d.jpg" % (year, month, day, station_id.upper(), session_number, distance_travelled, ds_num)
                shutil.copyfile(img_src_folder + all_files[idx], img_dest_folder + new_name)
            else:
                shutil.copyfile(img_src_folder + all_files[idx], img_dest_folder + all_files[idx])
        else:
            shutil.copyfile(img_src_folder + all_files[idx], img_dest_folder + all_files[idx])
        files_copied.append(all_files[idx])

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File renaming utility for wear station photos')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-f', '--starting_filename', help='Filename of first TSH picture', type=str)
    requiredNamed.add_argument('-l', '--station_letter', help='Station A/B/C', type=str)
    requiredNamed.add_argument('-n', '--session_number', help='Number of Session', type=int)
    requiredNamed.add_argument('-d', '--distance_travelled', help='Filename of first TSH picture', type=int)
    parser.add_argument('-a', '--date', help='Date of test (YYYY.MM.DD), defaults to today', type=str)
    parser.add_argument('-s', '--ds', help='Rename extra files under the DS naming scheme', action='store_true')
    parser.add_argument('-r', '--recursive', help='Run renaming inside SUBFOLDERS in \'unconverted\' folder', action='store_true')
    parser.add_argument('-w', '--wrong', help='If you do the long way and do Pre/Post of each TSH rather than all Pre then all Post', action='store_true')

    args = parser.parse_args()

    if args.recursive:
        all_folders = os.listdir('data/unconverted/')

        for folder in all_folders:
            try:
                img_src_folder = "data/unconverted/" + folder + "/"
                img_dest_folder = "data/converted/" + folder + "/"
                matches = re.match(r'(\d{4}\.\d{2}\.\d{2})\_([ABC])_(\d{1,3})_(\d*)', folder)
                if not matches:
                    print("Skipping unexpected file: %s" % (img_src_folder))
                    continue
                doMe = rename(img_src_folder, img_dest_folder, None, matches.group(2), int(matches.group(3)), int(matches.group(4)), matches.group(1), args.ds, args.wrong)
            except Exception as e:
                print (e)
                pass
    else:
        doMe = rename(img_src_folder, img_dest_folder, args.starting_filename, args.station_letter, args.session_number, args.distance_travelled, args.date, args.ds, args.wrong)

    if (doMe):
        print ("Renaming Complete!")
    else:
        print ("Error encountered.")
