import shutil


def create_folder(folder_path):
    save_directory = folder_path
    import os
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)
    for filename in os.listdir(save_directory):
        file_path = os.path.join(save_directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return save_directory


import os, shutil
def clear_folder(path):
    folder = path
    for filename in os.listdir(folder):
        if filename[-3:]=="plt" or filename[0:3]=="goals":
            continue
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_uav1_and2(uav_list):
    uav1=None
    uav2=None
    for uav in uav_list:
        if uav.index==0:
            uav1=uav
        else:
            uav2=uav
    return (uav1,uav2)
# def print_line(file,list):
#     for element in list:
#         file.write(f'{element:<12s})
#     file.write("\n")
