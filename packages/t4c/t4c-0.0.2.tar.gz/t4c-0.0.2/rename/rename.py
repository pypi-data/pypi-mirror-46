from renamer import Renamer
import sys


def description():
    print('Should be :')
    print("\t", "python rename.py -action path")
    print()
    print("-action can be : ")
    print("\t", "-rename : rename all files in the given path")
    print("\t", "-restore : rename files at the given path with their former filename")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        description()
            
    else:
        action = sys.argv[1]
        path = sys.argv[2]

        if action == '-rename':
            r = Renamer(path)
            r.rename()
        elif action == '-restore':
            r = Renamer(path)
            r.restore()
        else:
            description()
