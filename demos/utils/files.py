import os
import shutil


def create_data_folder(folder_name, base_path=os.getenv("HOME")):
    path = base_path + '/' + folder_name
    if os.path.exists(path):
        print(path + " exists")
        ans = 'y'  # input("remove (y/n)")
        if ans == 'y':
            print("removing " + path)
            try:
                shutil.rmtree(path)
            except OSError:
                print("Error: %s : %s" % (path, os.strerror))
            else:
                print(path + " successfully removed")

    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)
        return path
    return path


def progress(i, total):
    percent = str(int(float(i / (total - 1)) * 100)) + '%'
    s = "Progress: " + percent + '\r'
    print(s, end='')
