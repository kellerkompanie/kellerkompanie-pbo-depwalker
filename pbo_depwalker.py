#!/usr/bin/python

import os
import subprocess
import sys
import threading

import armaclassparser


def dokanpbo_mount_pbos(src_folder):
    dokanpbo_args = []
    for root, dirs, files in os.walk(src_folder):
        basename = os.path.basename(root)
        if not basename.startswith('@'):
            continue

        if 'addons' in dirs:
            dokanpbo_args.append(os.path.join(root, 'addons'))

    command = ' '.join(["DokanPbo.exe", "-f"] + ['"{}"'.format(arg) for arg in dokanpbo_args] + ["-o", "Q:"])
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    process.communicate()


def extract_dependencies(src_folder):
    # use dokan to mount pbo as drive Q
    threading.Thread(target=dokanpbo_mount_pbos, args=(src_folder,)).start()

    while os.system("vol %s: 2>nul>nul" % "Q") != 0:
        pass

    for root, dirs, files in os.walk("%s:\\" % "Q"):
        for file_name in files:
            if file_name.lower() == "config.cpp":
                file_path = os.path.join(root, file_name)
                try:
                    print(file_path)
                    print(armaclassparser.parse_from_file(file_path))
                except RuntimeError as e:
                    print(e, file=sys.stderr)

    # unmount when finished
    subprocess.run("DokanPbo.exe -U Q:")


def main():
    src_folder = "E:\\keksync2"
    extract_dependencies(src_folder)

    # threading.Thread(target=dokanpbo_mount_pbos, args=(src_folder,)).start()
    # while os.system("vol %s: 2>nul>nul" % "Q") != 0:
    #     pass
    # tokens = armaclassparser.parse_from_file("Q:\\x\\zen\\addons\\modules\\config.cpp")
    # print(armaclassparser.generator.from_tokens(tokens))
    #
    # # unmount when finished
    # subprocess.run("DokanPbo.exe -U Q:")


if __name__ == "__main__":
    main()
