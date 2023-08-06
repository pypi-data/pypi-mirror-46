import pkg_resources as pkg
import tifffile
import pickle
import sys

# Should avoid following error in python3
#   UnicodeDecodeError: 'ascii' codec can't decode byte 0xba in position 1: ordinal not in range(128)
# Generic functions


def loadtiff(filepath):
    data_file_path = 'data/' + filepath
    if (pkg.resource_exists('spam', data_file_path)):
        f = pkg.resource_filename('spam', data_file_path)
        return tifffile.imread(f)
    else:
        # raise IOError("File %s not found" % data_file_path)
        print(IOError("File %s not found" % data_file_path))
        return 0


def load(filepath):
    data_file_path = 'data/' + filepath
    if (pkg.resource_exists('spam', data_file_path)):
        f = pkg.resource_filename('spam', data_file_path)
        return open(f, 'rb')
    else:
        # raise IOError("File %s not found" % data_file_path)
        print(IOError("File %s not found" % data_file_path))
        return 0


def loadPickle(filepath):
    data_file_path = 'data/' + filepath
    if (pkg.resource_exists('spam', data_file_path)):
        f = pkg.resource_filename('spam', data_file_path)
        # Different pickle-loading options for different python versions
        if sys.version[0] == '2':
            return pickle.load(open(f, 'r'))
        else:
            return pickle.load(open(f, 'rb'), encoding='latin1')
    else:
        # raise IOError("File %s not found" % data_file_path)
        print(IOError("File %s not found" % data_file_path))
        return 0


# Usage example ##

# def loadtiffexample():
#    print("print something funny")
#    return loadtiff('image.tiff')


# def loadsomething():
#     print("print something funny")
#     return load('placeholder.txt')


def loadSnow():
    # print("spam.datasets.snow(): Brrr, enjoy this cold data")
    return loadtiff("snow/snow.tif")


def loadStructuredMesh():
    return loadPickle("mesh/structuredMesh.p")


def loadUnstructuredMesh():
    return loadPickle("mesh/unstructuredMesh.p")


def loadConcreteXr():
    return loadtiff("concrete/concrete_x-ray-bin16.tif")


def loadConcreteNe():
    return loadtiff("concrete/concrete_neutron-bin16.tif")
