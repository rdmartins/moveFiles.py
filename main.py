#!python

import getopt
import os
import pathlib
import shutil
import sys
from tqdm import tqdm


def findMP3(path):
    mp3Files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.mp3'):
                mp3Files.append(os.path.join(root, file))
    return mp3Files


def makeDict(src, dest, srcMP3):
    newDict = {}

    for item in srcMP3:
        newItem = item.removeprefix(src._str + '/')
        newItem = newItem.replace('/', '_')
        newItem = os.path.join(dest, newItem)

        newDict.update({newItem: item})

    return newDict


def syncDest(srcFiles, destFiles):
    pbDestFiles = tqdm(destFiles)
    pbDestFiles.set_description('Sincronizando')
    for file in pbDestFiles:
        if file in srcFiles:
            del srcFiles[file]
        else:
            os.remove(file)
    return srcFiles


def copyMP3(srcMP3, destPath):
    pbSrcMP3Items = tqdm(srcMP3.items())
    pbSrcMP3Items.set_description('Copiando')
    for destFile, srcFile in pbSrcMP3Items:
        shutil.copyfile(srcFile, destFile)


def printHelp():
    print('main.py -s <source dir> -d <destiny dir> [--sync]')


def main(argv):
    src = None
    dest = None
    sync = False
    try:
        opts, args = getopt.getopt(
            argv,
            'hs:d:',
            ['help', 'source=', 'destiny=', 'sync']
        )
    except getopt.GetoptError:
        printHelp()
        exit(1)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            exit()
        elif opt in ('-s', '--source'):
            src = pathlib.Path(arg)
        elif opt in ('-d', '--destiny'):
            dest = pathlib.Path(arg)
        elif opt == '--sync':
            sync = True

    if src is None or dest is None:
        printHelp()
        exit(2)

    srcMP3 = findMP3(src)
    srcMP3 = makeDict(src, dest, srcMP3)

    if sync:
        destMP3 = findMP3(dest)
        srcMP3 = syncDest(srcMP3, destMP3)

    copyMP3(srcMP3, dest)


if __name__ == '__main__':
    main(sys.argv[1:])
