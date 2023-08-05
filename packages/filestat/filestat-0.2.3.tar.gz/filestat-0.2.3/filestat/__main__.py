#!/usr/bin/python3

import argparse
from filestat import utils


def main():
    parser = argparse.ArgumentParser(description='A command line library for file monitoring')
    parser.add_argument(
        '-f',
        '--file',
        required=True,
        type=str,
        help='The name of the file filestat -f filestat.py',
    )

    args = parser.parse_args()
    if args.file is not None:
        file = args.file
        try:
            name_of_owner = utils.get_owner_info(file)
            name_of_group = utils.get_group_info(file)
            size_of_file = utils.get_size(file)
            update_time = utils.creation_time(file)
            last_access = utils.get_last_access_time(file)
            permissions = utils.get_permissions(file)
            readable = utils.readable(file)
            writable = utils.writable(file)
            executable = utils.executable(file)

            string = f'Location/Name:\t{file}\nOwner:\t{name_of_owner}\nGroup:\t{name_of_group}\n' \
                f'Size:\t{size_of_file} bytes\nUpdate Time: \t{update_time}\n' \
                f'Last Access:\t{last_access}\nPermissions:\t{permissions}\n' \
                f'Readable: \t{readable}\nWritable: \t{writable}\n' \
                f'Executable: \t{executable}'

            print(string)

        except Exception as e:
            print(e)
    else:
        print("Try with python3 -m filestat -f filename.py")
    return True


if __name__ == '__main__':
    main()
