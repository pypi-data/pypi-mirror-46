import sys
import os
import getpass

from os import stat
from pwd import getpwuid

# important constants:

# colors
CBRED = '\033[38;5;196;1m'
CBORANGE = '\033[38;5;202;1m'
CBGREEN = '\033[38;5;40;1m'
CBYELLOW = '\033[1;33m'
CBWHITE = '\033[1;37m'
CBPURPLE = '\033[1;35m'
CLIGHTBLUE = '\033[94m'
CBBLUE = '\033[1;34m'
CBASE = '\033[0m'

COCCURRENCES = CBPURPLE
CFILE_PATHS = CBBLUE
CTEXT_FILES = CBWHITE


# indicator strings
INIT_STRINGS = ["--initial", "--init"]
LOWERCASE_STRINGS = ["--lowercase", "--lower"]
UPPERCASE_STRINGS = ["--uppercase", "--upper"]
DESTINATION_STRINGS = ["--destination"]
SPECIFIC_STRINGS = ["--specific"]
LOCAL_STRINGS = ["--local"]
RECURSIVE_STRINGS = ["--recursive"]
PATHS_STRINGS = ["--paths"]
END_FLAG_STRINGS = ["--end_param", "--end"]

# supported short indicators
SUPPORTED_SHORT_INDICATORS = ['i', 'd', 's', 'l', 'r', 'p']


def check_help_request(arguments):
    if len(arguments) == 1 and (arguments[0] == "-h" or arguments[0] == "--help"):
        README_path = "/usr/lib/modfname/README.md"

        f = open(README_path, 'r')
        print(CFILE_PATHS + "\n\t#######      modfname documentation      #######\n" + CBWHITE)

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
    # print(CBWHITE + "\n\t[INFO] " + CBASE, end='')
    print(CBWHITE + "\n\t[INFO] " + CBASE + msg)


def WARNING(msg=""):
    print(CBORANGE + "\n\t[WARNING] " + CBASE + msg)


def ERROR(msg=""):
    print(CBRED + "\n\t[ERROR] " + CBASE + msg)


def skipped():
    print(CBBLUE + "\n\t\t\tskipped\n\n" + CBASE)


def check_nb_parameters(args):
    if len(args) < 3:
        ERROR("no enough arguments")
        raise ValueError("no enough arguments. Needs at least the initial string, the destination string and "
                         "one file/folder path such as:\nmodfname -r \" \" \"_\" \"$MHOME/dev/tests/this is a test\"")


def initiate_values():
    lowercase = False
    uppercase = False
    specific = True
    local = False
    recursive = False
    init_strs = []
    dest_str = None
    fpaths = []
    nb_occs = [0, 0]  # 0: found, 1: replaced
    return lowercase, uppercase, specific, local, recursive, init_strs, dest_str, fpaths, nb_occs


def treat_input_parms(input_parms, lowercase, uppercase, specific, local, recursive, init_strs, dest_str, fpaths):

    nb_args = len(input_parms)
    args_not_used_indexes = list(range(nb_args))
    for arg_index, arg in enumerate(input_parms):
        if arg.startswith("--"):
            if arg in INIT_STRINGS + DESTINATION_STRINGS + LOWERCASE_STRINGS + UPPERCASE_STRINGS + \
                    SPECIFIC_STRINGS + LOCAL_STRINGS + RECURSIVE_STRINGS + PATHS_STRINGS + END_FLAG_STRINGS:
                if arg in LOWERCASE_STRINGS:
                    lowercase = True
                if arg in UPPERCASE_STRINGS:
                    uppercase = True
                if arg in SPECIFIC_STRINGS:
                    specific = True
                elif arg in LOCAL_STRINGS:
                    local = True
                    specific = False
                elif arg in RECURSIVE_STRINGS:
                    recursive = True
                    specific = False
                elif arg in END_FLAG_STRINGS:
                    pass

                elif arg_index < nb_args - 1:
                    if arg in INIT_STRINGS:
                        get_arg_list(input_parms, arg_index, args_not_used_indexes, init_strs)

                    if arg in DESTINATION_STRINGS:
                        dest_str = input_parms[arg_index + 1]
                        args_not_used_indexes.remove(arg_index + 1)

                    if arg in PATHS_STRINGS:
                        get_arg_list(input_parms, arg_index, args_not_used_indexes, fpaths)

                else:
                    ERROR("no parameter after %s indicator" % arg)
                    raise ValueError("needs a parameter after the %s indicator" % arg)

                args_not_used_indexes.remove(arg_index)

            else:
                ERROR("the indicator %s is not supported" % arg)
                raise ValueError("please remove the %s parameter from the command" % arg)
        elif arg.startswith("-"):
            for short_ind in arg[1:]:
                if short_ind not in SUPPORTED_SHORT_INDICATORS:
                    ERROR("the short indicator -%s is not supported" % short_ind)
                    raise ValueError("please remove the -%s short indicator from the command" % short_ind)
                elif short_ind == 'i':
                    get_arg_list(input_parms, arg_index, args_not_used_indexes, init_strs)
                elif short_ind == 'd':
                    dest_str = input_parms[arg_index + 1]
                    args_not_used_indexes.remove(arg_index + 1)
                elif short_ind == 's':
                    specific = True
                elif short_ind == 'l':
                    local = True
                    specific = False
                elif short_ind == 'r':
                    recursive = True
                    specific = False
                elif short_ind == 'p':
                    get_arg_list(input_parms, arg_index, args_not_used_indexes, fpaths)

            args_not_used_indexes.remove(arg_index)
    return lowercase, uppercase, specific, local, recursive, dest_str, args_not_used_indexes


def get_arg_list(input_parms, ref_arg_index, args_not_used_indexes, input_list):
    for arg_index, arg in enumerate(input_parms[ref_arg_index + 1:]):
        if not arg.startswith("-"):
            input_list.append(arg)
            args_not_used_indexes.remove(ref_arg_index + 1 + arg_index)
        else:
            return input_list


def get_final_params(input_parms, args_not_used_indexes, lowercase, uppercase, init_strs, dest_str, fpaths):

    if not lowercase and not uppercase and not init_strs and not dest_str and len(args_not_used_indexes) > 2:
        init_strs.append(input_parms[0])
        dest_str = input_parms[1]
        for arg_left in input_parms[2:]:
            fpaths.append(arg_left)
        args_not_used_indexes = []

    elif not fpaths:
        if not args_not_used_indexes:
            ERROR("arguments are missing ... please review the command syntax")
            raise ValueError("the file path arg is not defined")
        for arg_not_used_index in args_not_used_indexes:
            fpaths.append(input_parms[arg_not_used_index])
            args_not_used_indexes.pop()
    elif not lowercase and not uppercase and not dest_str:
        if not args_not_used_indexes:
            ERROR("arguments are missing ... please review the command syntax")
            raise ValueError("the destination string arg is not defined")
        dest_str = input_parms[-1]
        args_not_used_indexes.pop()
    elif not lowercase and not uppercase and not init_strs:
        if not args_not_used_indexes:
            ERROR("arguments are missing ... please review the command syntax")
            raise ValueError("the initial strings arg is not defined")
        for arg_not_used_index in args_not_used_indexes:
            init_strs.append(input_parms[arg_not_used_index])
            args_not_used_indexes.pop()

    if args_not_used_indexes:
        ERROR("too much arguments entered ... please review the command syntax")
        raise ValueError("the args %s have not been used" % args_not_used_indexes)

    return dest_str


def check_user_permissions(file_path):
    current_user = getpass.getuser()
    owner_file = getpwuid(stat(file_path).st_uid).pw_name
    if owner_file != current_user:
        WARNING("the file " + CFILE_PATHS + "%s" % file_path + CBASE + " is owned by " + CFILE_PATHS + "%s"
                % owner_file + CBASE + ", might be necessary to manage its permissions")


def concatenate_paths(root_path, final_path):
    if root_path.endswith('/') and final_path.startswith('/'):
        global_path = root_path[:-1] + final_path
    elif (root_path.endswith('/') and not final_path.startswith('/')) or (not root_path.endswith('/') and final_path.startswith('/')):
        global_path = root_path + final_path
    else:
        global_path = root_path + '/' + final_path
    return global_path


def check_folder_path_exists(folderpath):
    if not os.path.isdir(folderpath):
        WARNING(CFILE_PATHS + " %s " % folderpath + CBASE + "folder doesn't exist")
        raise ValueError("the directory path to apply %s doesn't exist, you may review it" % folderpath)


def check_path_exists(path):
    if not os.path.exists(path):
        WARNING(CFILE_PATHS + " %s " % path + CBASE + "path doesn't exist")
        return False
    return True


def abort_process():
    print(CBYELLOW + "\n\n\t\t\taborted ...\n\t\t\t\tSee you later\n" + CBASE)
    exit()


def init_strs_to_dest_str(init_path, lowercase, uppercase, init_strs, dest_str, nb_occs):
    base_path = os.path.dirname(init_path)
    fname = os.path.basename(init_path)
    fname_origin = fname

    if lowercase or uppercase:
        nb_occs[0] += 1
        fpath = concatenate_paths(base_path, fname)
        print(CFILE_PATHS + "%s" % fpath + CBWHITE)
        new_fname = None
        if lowercase:
            new_fname = fname.lower()
        if uppercase:
            new_fname = fname.upper()

        mod_fname_check = input("\tchange " + COCCURRENCES + "%s" % fname + CBWHITE + " to " + COCCURRENCES +
            "%s" % new_fname + CBWHITE + " ?\n\t[ENTER] to proceed\t[sS] to skip\t[aA] to abort process\n")

        if mod_fname_check == "":
            fname = new_fname
            nb_occs[1] += 1
        elif mod_fname_check in ["a", "A"]:
            abort_process()
        else:
            INFO(CFILE_PATHS + "%s" % fpath + CBWHITE + " not changed")

    elif init_strs:
        for init_str in init_strs:
            if init_str in fname:
                nb_occs[0] += 1
                fpath = concatenate_paths(base_path, fname)
                print("\nthere is " + COCCURRENCES + "\"%s\"" % init_str + CBASE + " in " + CFILE_PATHS + "%s" % fpath + CBWHITE)

                new_fname = fname.replace(init_str, dest_str)
                mod_fname_check = input("\tchange " + COCCURRENCES + "%s" % fname + CBWHITE + " to " + COCCURRENCES +
                    "%s" % new_fname + CBWHITE + " ?\n\t[ENTER] to proceed\t[sS] to skip\t[aA] to abort process\n")

                if mod_fname_check == "":
                    fname = new_fname
                    nb_occs[1] += 1
                elif mod_fname_check in ["a", "A"]:
                    abort_process()
                else:
                    INFO(CFILE_PATHS + "%s" % fpath + CBWHITE + " not changed")

    else:
        conf_error_message(lowercase, uppercase, init_strs, dest_str)

    if fname != fname_origin:
        new_path = concatenate_paths(base_path, fname)
        os.rename(init_path, new_path)
        OK(CFILE_PATHS + "%s/" % os.path.dirname(new_path) + COCCURRENCES + "%s" % fname + CFILE_PATHS + "\tdone")
        return new_path

    return init_path


def check_integrity_inputs(modes, lowercase, uppercase, init_strs, dest_str):
    check_mode_integrity(modes)
    check_modifier_integrity(lowercase, uppercase, init_strs, dest_str)


def check_mode_integrity(modes):
    nb_mode_on = 0
    for mode in modes:
        if mode:
            nb_mode_on += 1
    if nb_mode_on != 1:
        ERROR("the current modfname mode is not correct:\n\tspecific: %s\n\tlocal: %s\n\trecursive: %s" % (modes[0], modes[1], modes[2]))
        raise ValueError("check the input parameters to get a correct modfname mode")


def check_modifier_integrity(lowercase, uppercase, init_strs, dest_str):
    if lowercase:
        if uppercase or init_strs or dest_str:
            conf_error_message(lowercase, uppercase, init_strs, dest_str)
    elif uppercase:
        if lowercase or init_strs or dest_str:
            conf_error_message(lowercase, uppercase, init_strs, dest_str)

    elif init_strs:
        if lowercase or uppercase or not dest_str:
            conf_error_message(lowercase, uppercase, init_strs, dest_str)

    elif dest_str:
        if lowercase or uppercase or not init_strs:
            conf_error_message(lowercase, uppercase, init_strs, dest_str)
    else:
        conf_error_message(lowercase, uppercase, init_strs, dest_str)


def conf_error_message(lowercase, uppercase, init_strs, dest_str):
    ERROR("modfname conf is not correct:\n\tlowercase: %s\n\tuppercase: %s\n\tinit_strs: "
          "%s\n\tdest_str: %s" % (lowercase, uppercase, init_strs, dest_str))
    raise ValueError("check the input parameters to get a correct modfname conf")


def mod_fnames(fpath, lowercase, uppercase, init_strs, dest_str, recursive, nb_occs):

    check_user_permissions(fpath)

    if os.path.isfile(fpath):
        init_strs_to_dest_str(fpath, lowercase, uppercase, init_strs, dest_str, nb_occs)

    if os.path.isdir(fpath):
        fpath = init_strs_to_dest_str(fpath, lowercase, uppercase, init_strs, dest_str, nb_occs)
        if recursive:
            list_files_and_folders = os.listdir(fpath)
            for file_or_folder_name in list_files_and_folders:
                mod_fnames(concatenate_paths(fpath, file_or_folder_name), lowercase, uppercase, init_strs, dest_str, recursive, nb_occs)


def occs_summary(nb_occs, init_strs):
    if nb_occs[0] == 0:
        print(CFILE_PATHS + "\n\t0" + CBASE + " occurrence of " + COCCURRENCES + "%s" % init_strs + CBASE + " found")
    elif nb_occs[0] == 1:
        print(CFILE_PATHS + "\n\t1" + CBASE + " occurrence of " + COCCURRENCES + "%s" % init_strs +
              CBASE + " found and " + CFILE_PATHS + "%s" % nb_occs[1] + CBASE + " replaced")
    else:
        print(CFILE_PATHS + "\n\t%s" % nb_occs[0] + CBASE + " occurrences of " + COCCURRENCES + "%s" % init_strs
              + CBASE + " found and " + CFILE_PATHS + "%s" % nb_occs[1] + CBASE + " replaced")


def main():

    input_parms = sys.argv[1:]
    check_help_request(input_parms)
    check_nb_parameters(input_parms)
    lowercase, uppercase, specific, local, recursive, init_strs, dest_str, fpaths, nb_occs = initiate_values()

    lowercase, uppercase, specific, local, recursive, dest_str, args_not_used_indexes = \
        treat_input_parms(input_parms, lowercase, uppercase, specific, local, recursive, init_strs, dest_str, fpaths)

    check_mode_integrity([specific, local, recursive])

    dest_str = get_final_params(input_parms, args_not_used_indexes, lowercase, uppercase, init_strs, dest_str, fpaths)

    check_modifier_integrity(lowercase, uppercase, init_strs, dest_str)

    if recursive or local:
        if len(fpaths) != 1:
            ERROR("in recursive mode only one folder path must be given\ngiven %s" % fpaths)
            raise ValueError("please enter only one input folder path in recursive mode")

        folder_path = fpaths[0]
        check_folder_path_exists(folder_path)
        if not folder_path.startswith('/'):
            folder_path = concatenate_paths(os.getcwd(), folder_path)

        files_folders = os.listdir(folder_path)
        for file_or_folder_name in files_folders:
            mod_fnames(concatenate_paths(folder_path, file_or_folder_name), lowercase, uppercase, init_strs, dest_str, recursive, nb_occs)
    else:
        if len(fpaths) == 0:
            ERROR("needs at least one file/folder path")
            raise ValueError("please enter at least one path")

        for fpath in fpaths:
            if not fpath.startswith('/'):
                fpath = concatenate_paths(os.getcwd(), fpath)
            if not check_path_exists(fpath):
                skipped()
                continue
            mod_fnames(fpath, lowercase, uppercase, init_strs, dest_str, recursive, nb_occs)

    occs_summary(nb_occs, init_strs)


if __name__ == "__main__":
    main()
