from zipfile import ZipFile

import os


def prune(path):
    '''
    Deletes a file or a directory

    Parameters:
    path    (str): Path to be removed
    '''

    if os.path.isdir(path):
        # Empty the contents of the folder before removing the directory
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

        os.rmdir(path)
    else:
        os.remove(path)

def zip_file(content, path, clean=True):
    '''
    Archives a file or the contents of a directory as a zip

    Parameters:
    content (str): Input path to the file or directory
    path    (str): Output path for the zip file

    Returns:
    (str): Path to the zipped file
    '''

    with ZipFile(path, 'w') as f:
        if os.path.isdir(content):
            for item in os.listdir(content):
                f.write(os.path.join(content, item), arcname=item)
        else:
            f.write(content)

    if clean:
        prune(content)

    return path
