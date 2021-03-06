
import os
import shutil
import urllib2
import hashlib
from time import sleep
 
#################
# USER SETTINGS #
#################
 
periodic = True  # Keep looping forever to monitor the websites?
t = 15  # Time period (in seconds) if periodic=True, otherwise ignored
 
paths = [
    'http://www.nationalparks.gov.uk/snwebcam/webcam1.jpg',
    'http://webcams.mathew-street.com/static/mathewst/webcam1_static.jpg',
    'http://www.wirralcam.org/csource/ph15jul.jpg',
    'http://www2.wirralcam.org/livesource/fslarge.jpg'
    ]
    
########################
# END OF USER SETTINGS #
########################


def get_file(path, filename):
    """Grab the file from the internet"""
    response = urllib2.urlopen(path)
    data = response.read()
    tmp_filename = 'tmp_{0}'.format(filename)
    f = open(tmp_filename, 'wb')
    f.write(data)
    f.close()
    return tmp_filename


def create_directory(dirname):
    """Create directory, if it doesn't already exist"""
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def is_duplicate(tmp_filename, filename):
    """Check if the latest file has already been downloaded"""
    # tmp_filename should always exist because it was downloaded
    f = open(tmp_filename)
    data1 = f.read()
    f.close()
    # filename may not exist if this is the first run, so perform a check
    if os.path.exists(filename):
        f = open(filename)
        data2 = f.read()
        f.close()
    else:
        data2 = ''
    
    hash1 = hashlib.sha512(data1).hexdigest()
    hash2 = hashlib.sha512(data2).hexdigest()
    
    if hash1 == hash2:
        return True
    else:
        return False


def get_last_file(directory, index_file):
    """Returns the last file to be stored in the directory"""
    if os.path.exists(os.path.join(directory, index_file)):
        f = open(os.path.join(directory, index_file))
        data = f.read()
        f.close()
        last_file = os.path.join(directory, data.split('\n')[-2])
    else:
        last_file = ''
    return last_file


def move_file(tmp_filename, dirname, last_file, index_file):
    """Moves the image file and appends to the index text file"""
    if last_file == '':
        f_num = 0
    else:
        f_num = int(os.path.split(os.path.splitext(last_file)[0])[-1])+1
    f_ext = os.path.splitext(tmp_filename)[-1]
    destination = '{0}{1}'.format(f_num, f_ext)
    shutil.move(tmp_filename, os.path.join(dirname, destination))
    f = open(os.path.join(dirname, index_file), 'a')
    f.write('{0}\n'.format(destination))
    f.close()


def process_paths(image_paths):
    """Download images and do the magic"""
    print('')
    print('Processing Paths')
    for path in image_paths:
        
        filename = os.path.split(path)[-1]
        dirname = os.path.join('IMAGES', os.path.splitext(filename)[0])
        index_file = 'index.txt'
        
        try:
            tmp_filename = get_file(path, filename)
            create_directory(dirname)

            last_file = get_last_file(dirname, index_file)
            if not is_duplicate(tmp_filename, last_file):
                print('Not a duplicate ({0})'.format(filename))
                move_file(tmp_filename, dirname, last_file, index_file)
            else:
                print('Is a duplicate ({0})'.format(filename))
                os.remove(tmp_filename)
        except urllib2.HTTPError:
            print('Unable to download ({0})'.format(filename))

    print('Processing Complete')


if __name__ == '__main__':
    while True:
        process_paths(paths)
        if not periodic:
            break
        sleep(t)
