import sys
import os
import subprocess
import shutil
from subprocess import call
from datetime import datetime

CBRED = '\033[38;5;196;1m'
CBORANGE = '\033[38;5;202;1m'
CBGREEN = '\033[38;5;40;1m'

CBWHITE = '\033[1;37m'
# CBPURPLE = '\033[1;35m'
CBBLUE = '\033[1;34m'

CBASE = '\033[0m'


def check_help_request(args):
    if len(args) == 1 and (args[0] == "-h" or args[0] == "--help"):
        README_path = "/usr/lib/zipf/README.md"

        f = open(README_path, 'r')
        print(CBBLUE + "\n\t#######      zipf documentation      #######\n" + CBWHITE)

        for line in f:
            if line == "```sh\n" or line == "```\n" or line == "<pre>\n" or line == "</pre>\n":
                continue
            line = line.replace('```sh', '').replace('```', '').replace('<pre>', '').replace('</b>', '').\
                replace('<b>', '').replace('<!-- -->', '').replace('<br/>', '').replace('```sh', '').\
                replace('***', '').replace('***', '').replace('**', '').replace('*', '')

            print(" " + line, end='')
        print(CBASE)
        exit()


def OK(msg=""):
    print(CBGREEN + "\n\t[OK] " + CBASE + msg)


def INFO(msg=""):
    print(CBWHITE + "\n\t[INFO] " + CBASE + msg)


def WARNING(msg=""):
    print(CBORANGE + "\n\t[WARNING] " + CBASE + msg)


def ERROR(msg=""):
    print(CBRED + "\n\t[ERROR] " + CBASE + msg)


def skipped():
    print(CBBLUE + "\n\t\t\tskipped\n\n" + CBASE)


def path_exists(path):
    if not os.path.exists(path):
        return False
    return True


def get_abs_path(fpath):
    return os.path.normpath((os.path.join(os.getcwd(), os.path.expanduser(fpath))))


def error_man(init_msg, err_msg, folder_path, moved_folder_path):
    ERROR(init_msg + " error:\n\t\t" + str(err_msg))

    sudo_conf = input(CBWHITE + "\n\t\tuse sudo?\n\t\t\t[Enter] to proceed\t\t[any case] to skip\n")
    if sudo_conf == "":
        subprocess.check_call(['sudo', "mv", folder_path, moved_folder_path])
    else:
        skipped()


def check_f_moved(folder_path, moved_folder_path):
    if os.path.exists(folder_path) or not os.path.exists(moved_folder_path):
        if os.path.exists(folder_path):
            WARNING(CBBLUE + "%s" % folder_path + CBASE + " still exists")
        if not os.path.exists(moved_folder_path):
            WARNING(CBBLUE + "%s" % moved_folder_path + CBASE + " doesn't exist")
        return False
    return True


def check_archive_created(archive_name):
    archive_path = os.getcwd() + "/" + archive_name + ".zip"
    if os.path.isfile(archive_path):
        OK(CBBLUE + "%s" % archive_path + CBASE + "created")
        return True
    else:
        ERROR(CBBLUE + "%s" % archive_path + CBASE + "not created")
        return False


def zip_folder(folder_path, archive_name=None):

    if not archive_name:
        cdatetime = datetime.now()
        archive_name = cdatetime.strftime("%Y_%m_%d-%H_%M_%S")

    shutil.make_archive(archive_name, 'zip', folder_path)
    check_archive_created(archive_name)
    shutil.rmtree(folder_path)


def zip_files(flist, archive_name=None):

    cdatetime = datetime.now()
    ctime = cdatetime.strftime("%Y_%m_%d-%H_%M_%S")

    if not archive_name:
        archive_name = ctime

    cpath = os.getcwd()
    folder_path = cpath + "/" + archive_name

    if path_exists(folder_path):
        WARNING(CBBLUE + "%s" % folder_path + CBASE + " already exists" + CBASE)
        moved_folder_path = folder_path + "_" + ctime
        try:
            shutil.move(folder_path, moved_folder_path)

        except PermissionError as err_msg:
            error_man("permission", err_msg, folder_path, moved_folder_path)

        except OSError as err_msg:
            error_man("os", err_msg, folder_path, moved_folder_path)

        except Exception as err_msg:
            error_man("", err_msg, folder_path, moved_folder_path)

        if check_f_moved(folder_path, moved_folder_path):
            OK(CBBLUE + "%s" % folder_path + CBASE + " moved" + CBASE)
        else:
            ERROR("an issue occurred when moving file " + CBBLUE + "%s" % folder_path + CBASE)
            raise ValueError("not able to rename " + CBBLUE + "%s" % folder_path + CBASE)

    try:
        os.mkdir(folder_path)
    except Exception as err_msg:
        ERROR("an issue occurred when creating folder " + CBBLUE + "%s" % folder_path + CBASE + "\n%s" % err_msg)
        raise ValueError("not able to create " + CBBLUE + "%s" % folder_path + CBASE + " folder")

    for f in flist:
        fpath = get_abs_path(f)

        if os.path.isdir(fpath):
            call(['cp', '-a', fpath, folder_path])
        elif os.path.isfile(fpath):
            shutil.copy(fpath, folder_path)

    shutil.make_archive(archive_name, 'zip', folder_path)
    check_archive_created(archive_name)
    shutil.rmtree(folder_path)


def main():
    inputs = sys.argv[1:]
    check_help_request(inputs)

    if len(inputs) == 0:
        ERROR("needs at least one argument being a folder name or a list of files/folders")
        raise ValueError("no input ... no zip ...")

    elif len(inputs) == 1:
        fpath = get_abs_path(inputs[0])
        print(fpath)
        if path_exists(fpath):
            if os.path.isdir(fpath):
                zip_folder(fpath)
            else:
                zip_files([fpath])
        else:
            ERROR(CBBLUE + "%s" % fpath + CBASE + " path doesn't exist")
            raise ValueError("needs at least one existing path in argument being a folder name or a list of files/folders")
    else:
        last_arg = inputs[-1]
        if path_exists(get_abs_path(last_arg)):
            zip_files(inputs)
        else:
            zip_files(inputs[:-1], last_arg)


if __name__ == "__main__":
    main()
