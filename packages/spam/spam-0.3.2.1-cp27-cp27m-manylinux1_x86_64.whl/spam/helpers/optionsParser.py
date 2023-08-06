import argparse
import numpy
import os

# Nice str2bool suggestion from Maxim ( https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse )


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def ldicParser(parser):
    parser.add_argument('-nompi',
                        action="store_false",
                        dest='MPI',
                        help='Activate MPI parallelisation?')

    parser.add_argument('inFiles',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help="A space-separated list of two 3D greyscale tiff files to correlate, in order")

    parser.add_argument('-mf1',
                        '--maskFile1',
                        dest='MASK1',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to tiff file containing the mask of image 1 -- masks zones not to correlate, which should be == 0")

    #parser.add_argument('-mf2',
                        #'--maskFile2',
                        #dest='MASK2',
                        #default=None,
                        #type=argparse.FileType('r'),
                        #help="Path to tiff file containing the mask of image 2 -- masks correlation windows")

    parser.add_argument('-pf',
                        '-phiFile',
                        dest='PHIFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

    parser.add_argument('-pfb',
                        '--phiFile-bin-ratio',
                        type=int,
                        default=1,
                        dest='PHIFILE_BIN_RATIO',
                        help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    parser.add_argument('-glt',
                        '--grey-low-threshold',
                        type=float,
                        default=-numpy.inf,
                        dest='GREY_LOW_THRESH',
                        help="Grey threshold on mean of reference imagette BELOW which the correlation is not performed. Default = -infinity")

    parser.add_argument('-ght',
                        '--grey-high-threshold',
                        type=float,
                        default=numpy.inf,
                        dest='GREY_HIGH_THRESH',
                        help="Grey threshold on mean of reference imagette ABOVE which the correlation is not performed. Default = infinity")

    parser.add_argument('-reg',
                        '--registration',
                        action="store_true",
                        dest='REG',
                        help='Perform an initial registration? Default = False')

    parser.add_argument('-regb',
                        '--registration-binning',
                        type=int,
                        default=1,
                        dest='REG_BIN',
                        help='Binning to apply to input images for registration. Default = 1')

    parser.add_argument('-regm',
                        '--registration-margin',
                        type=float,
                        default=0.1,
                        dest='REG_MARGIN',
                        help='Registration margin in proportions of image size. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-regs',
                        '--subtract-registration',
                        action="store_true",
                        dest='REGSUB',
                        help='Subtract rigid part of initial registration from output displacements? Default = False')

    parser.add_argument('-ps',
                        '--pixel-search',
                        type=str,
                        default='auto',
                        dest='PS',
                        help="Pixel search option.Accepted values are:\n\t\"auto\": disactivate pixel search if registration works, or Ffile is given."+\
                             "\n\t\"on\": Force a pixel search in any case (rounds initial guess and can lose initial F).\n\t\"off\": block pixel search. \"auto\" is default")

    parser.add_argument('-psr',
                        '--pixel-search-range',
                        nargs=6,
                        type=int,
                        default=[-3, 3, -3, 3, -3, 3],
                        dest='PSR',
                        help='Z- Z+ Y- Y+ X- X+ ranges (in pixels) for the pxiel search. Requires pixel search to be activated. Default = +-3px')

    parser.add_argument('-psf',
                        '--pixel-search-filter',
                        type=int,
                        default=0,
                        dest='PS_FILTER',
                        help='Median filter pixel search results. Default = 0')

    # Default: node spacing equal in all three directions
    parser.add_argument('-ns',
                        '--node-spacing',
                        nargs=1,
                        type=int,
                        default=None,
                        dest='NS',
                        help="Node spacing in pixels (assumed equal in all 3 directions -- see -ns3 for different setting). Default = 10px")

    # Possible: node spacing different in all three directions
    parser.add_argument('-ns3',
                        '--node-spacing-3',
                        nargs=3,
                        type=int,
                        default=None,
                        dest='NS',
                        help="Node spacing in pixels (different in 3 directions). Default = 10, 10, 10px")

    # Default: window size equal in all three directions
    parser.add_argument('-hws',
                        '--half-window-size',
                        nargs=1,
                        type=numpy.uint,
                        default=None,
                        dest='HWS',
                        help="Half correlation window size, measured each side of the node pixel (assumed equal in all 3 directions -- see -hws3 for different setting). Default = 10px")

    # Possible: node spacing different in all three directions
    parser.add_argument('-hws3',
                        '--half-window-size-3',
                        nargs=3,
                        type=int,
                        default=None,
                        dest='HWS',
                        help="Half correlation window size, measured each side of the node pixel (different in 3 directions). Default = 10, 10, 10px")

    parser.add_argument('-nosp',
                        '--no-subpixel',
                        action="store_false",
                        dest='SUBPIXEL',
                        help='Disactivates subpixel refinement')

    parser.add_argument('-spm',
                        '--sub-pixel-margin',
                        nargs=1,
                        type=numpy.uint,
                        default=[3],
                        dest='SUBPIXEL_MARGIN',
                        help="Subpixel margin for subpixel interpolation. Default = 3px")

    parser.add_argument('-spm3',
                        '--sub-pixel-margin3',
                        nargs=3,
                        type=numpy.uint,
                        default=None,
                        dest='SUBPIXEL_MARGIN',
                        help="Subpixel margin for subpixel interpolation. Default = 3px")

    parser.add_argument('-spi',
                        '--sub-pixel-max-iterations',
                        type=numpy.uint,
                        default=50,
                        dest='SUBPIXEL_MAX_ITERATIONS',
                        help="Subpixel max iterations subpixel search. Default = 50")

    parser.add_argument('-spp',
                        '--sub-pixel-min-phi-change',
                        type=numpy.float,
                        default=0.001,
                        dest='SUBPIXEL_MIN_PHI_CHANGE',
                        help="Subpixel min change in Phi to stop subpixel search. Default = 0.001")

    parser.add_argument('-spo',
                        '--sub-pixel-interpolation-order',
                        type=numpy.uint,
                        default=1,
                        dest='SUBPIXEL_INTERPOLATION_ORDER',
                        help="Subpixel interpolation order. Default = 1")

    parser.add_argument('-sef',
                        '--series-Ffile',
                        action="store_true",
                        dest='SERIES_PHIFILE',
                        help='During a total analysis, activate use of previous Ffield for next correlation')

    parser.add_argument('-sei',
                        '--series-incremental',
                        action="store_true",
                        dest='SERIES_INCREMENTAL',
                        help='Perform incremental correlations between images')

    parser.add_argument('-cif',
                        '--correct-input-field',
                        action="store_true",
                        dest='CORRECT_FIELD',
                        help='Activates correction of the input F field')

    parser.add_argument('-cni',
                        '--correct-neighbours-for-field-interpolation',
                        type=numpy.uint,
                        default=12,
                        dest='CORRECT_NEIGHBOURS',
                        help="Neighbours for field interpolation. Default = 12")

    parser.add_argument('-cmf',
                        '--correct-median-filter',
                        action="store_true",
                        dest='CORRECT_MEDIAN_FILTER',
                        help="Activates an overall median filter on the input F field")

    parser.add_argument('-cmfr',
                        '--correct-median-filter-radius',
                        type=numpy.uint,
                        default=2,
                        dest='CORRECT_MEDIAN_FILTER_RADIUS',
                        help="Radius of median filter for correction of input F field. Default = 2")

    parser.add_argument('-cdf',
                        '--correct-delta-f-norm',
                        type=numpy.float,
                        default=0.001,
                        dest='CORRECT_DELTA_F_NORM',
                        help="Delta F norm for a return status = 1 correlation window to consider the point good. Default = 0.001")

    parser.add_argument('-cpscc',
                        '--correct-pixel-search-cc',
                        type=numpy.float,
                        default=0.98,
                        dest='CORRECT_PIXEL_SEARCH_CC',
                        help="Pixel search correlation coefficient to consider the point good. Default = 0.98")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files. Default is basename of input file (without extension)")

    parser.add_argument('-vtk',
                        '--VTKout',
                        action="store_true",
                        dest='VTK',
                        help='Activate VTK output format. Default = False')

    parser.add_argument('-tsv',
                        '--TSVout',
                        action="store_true",
                        dest='TSV',
                        help='Activate TSV output format. Default = False')

    parser.add_argument('-tif',
                        '-tiff',
                        '--TIFFout',
                        '--TIFout',
                        action="store_true",
                        dest='TIF',
                        help='Activate TIF output format. Default = False')

    args = parser.parse_args()

    # 2018-03-24 check for 2D without loading images
    #try:
    #except:
        #print("DICregularGrid: Input TIFF files need to be writeable in order to guess their dimensionality")
        #exit()
    # 2019-03-21 EA: better check for dimensions, doesn't depend on writability of files
    import tifffile
    tiff = tifffile.TiffFile(args.inFiles[0].name)
    imagejSingleSlice = True
    #if tiff.imagej_metadata is not None:
        #if 'slices' in tiff.imagej_metadata:
            #if tiff.imagej_metadata['slices'] > 1:
                #imagejSingleSlice = False

    # 2019-04-05 EA: 2D image detection approved by Christophe Golke
    if len(tiff.pages) == 1 and len(tiff.series[0]):
        twoD = True
    else:
        twoD = False
    tiff.close()


    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFiles[0].name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.inFiles[0].name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    # 2018-11-15 EA: Setting this in the client in order not to overwrite files in a series
    #if args.PREFIX is None:
        #args.PREFIX = os.path.splitext(os.path.basename(args.inFiles[0].name))[0]

    if args.PS != 'auto' and args.PS != 'on' and args.PS != 'off':
        print("\nInvalid option {} for pixel search. Setting \"auto\"".format(args.PS))
        args.PS = 'auto'

    # Catch interdependent node spacing and correlation window sizes
    if args.NS is None:
        print("\nUsing default node spacing: "),
        if args.HWS is None:
            print("2x default half window size"),
            args.HWS = [10]
            print("({}) which is".format(args.HWS[0])),
            args.NS = [args.HWS[0] * 2]
        else:
            print("2x user-set half window size"),
            if len(args.HWS) == 1:
                print("({}) which is".format(args.HWS[0])),
                args.NS = [int(args.HWS[0] * 2)]
            elif len(args.HWS) == 3:
                print("({} -- selecting smallest) which is".format(args.HWS)),
                args.NS = [int(min(args.HWS) * 2)]
        print(args.NS)

    # Catch 3D options
    if len(args.NS) == 1:
        args.NS = [args.NS[0], args.NS[0], args.NS[0]]
    if len(args.HWS) == 1:
        args.HWS = [args.HWS[0], args.HWS[0], args.HWS[0]]
    if len(args.SUBPIXEL_MARGIN) == 1:
        args.SUBPIXEL_MARGIN = [args.SUBPIXEL_MARGIN[0], args.SUBPIXEL_MARGIN[0], args.SUBPIXEL_MARGIN[0]]

    if type(args.SUBPIXEL_MAX_ITERATIONS) == list:
        args.SUBPIXEL_MAX_ITERATIONS = args.SUBPIXEL_MAX_ITERATIONS[0]

    # Catch and overwrite 2D options
    if twoD:
        args.NS[0] = 1
        args.HWS[0] = 0
        args.SUBPIXEL_MARGIN[0] = 0
        args.PSR[0] = 0
        args.PSR[1] = 0

    # Behaviour undefined for series run and im1 mask since im1 will change, complain and continue
    if args.MASK1 is not None and args.SERIES_INCREMENTAL:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: You set an im1 mask and an incremental      ###")
        print("###  series correlation, meaning that im1 will change...  ###")
        print("#############################################################")
        print("#############################################################")

    # Make sure at least one output format has been asked for
    if args.VTK + args.TSV + args.TIF == 0:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: No output type of VTK, TSV and TIF options  ###")
        print("###  Are you sure this is right?!                         ###")
        print("#############################################################")
        print("#############################################################")

    if args.REG_MARGIN > 0.45:
        print("Registration margin cannot be bigger than 0.45 since 0.5 would contain no data!!")

    if args.SERIES_PHIFILE:
        args.TSV = True

    # just keep the name for this one
    if args.PHIFILE is not None:
        args.PHIFILE = args.PHIFILE.name

    return args


def ddicParser(parser):
    parser.add_argument('im1',
                        metavar='im1',
                        type=argparse.FileType('r'),
                        help="Greyscale image of reference state for correlation")

    parser.add_argument('lab1',
                        metavar='lab1',
                        type=argparse.FileType('r'),
                        help="Labelled image of reference state for correlation")

    parser.add_argument('im2',
                        metavar='im2',
                        type=argparse.FileType('r'),
                        help="Greyscale image of deformed state for correlation")

    parser.add_argument('-ps',
                        '--pixel-search',
                        type=str,
                        default='auto',
                        dest='PS',
                        help="Pixel search option.Accepted values are:\n\t\"auto\": disactivate pixel search if registration works, or Ffile is given."+\
                             "\n\t\"on\": Force a pixel search in any case (rounds initial guess and can lose initial F).\n\t\"off\": block pixel search. \"auto\" is default")
    
    parser.add_argument('-nompi',
                        action="store_false",
                        dest='MPI',
                        help='Disactivate MPI parallelisation?')

    parser.add_argument('-nops',
                        '--no-pixel-search',
                        action="store_false",
                        dest='PS',
                        help='Disactivate pixel search?')

    parser.add_argument('-psr',
                        '--pixel-search-range',
                        nargs=6,
                        type=int,
                        default=[-3, 3, -3, 3, -3, 3],
                        dest='PSR',
                        help='Z- Z+ Y- Y+ X- X+ ranges (in pixels) for the pxiel search. Requires pixel search to be activated. Default = +-3px')

    parser.add_argument('-nosp',
                        '--no-subpixel',
                        action="store_false",
                        dest='SUBPIXEL',
                        help='Disactivate subpixel refinement?')

    parser.add_argument('-ld',
                        '--label-dilate',
                        type=int,
                        default=1,
                        dest='LABEL_DILATE',
                        help="Number of times to dilate labels. Default = 1")

    parser.add_argument('-vt',
                        '--volume-threshold',
                        type=numpy.uint,
                        default=100,
                        dest='VOLUME_THRESHOLD',
                        help="Volume threshold below which labels are ignored. Default = 100")

    parser.add_argument('-reg',
                        '--registration',
                        action="store_true",
                        dest='REG',
                        help='Perform an initial registration? Default = False')

    parser.add_argument('-regb',
                        '--registration-binning',
                        type=int,
                        default=1,
                        dest='REG_BIN',
                        help='Binning to apply to input images for registration. Default = 1')

    parser.add_argument('-regm',
                        '--registration-margin',
                        type=float,
                        default=0.1,
                        dest='REG_MARGIN',
                        help='Registration margin in proportions of image size. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-pf',
                        '-phiFile',
                        dest='PHIFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

    parser.add_argument('-pfb',
                        '--phiFile-bin-ratio',
                        type=int,
                        default=1,
                        dest='PHIFILE_BIN_RATIO',
                        help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    parser.add_argument('-cif',
                        '--correct-input-field',
                        action="store_true",
                        dest='CF',
                        help='Correction of the input F field. Default = True')

    parser.add_argument('-nfi',
                        '--neighbours-for-field-interpolation',
                        type=numpy.uint,
                        default=12,
                        dest='NEIGHBOURS',
                        help="Neighbours for field interpolation. Default = 12")

    parser.add_argument('-nomask',
                        '--no-mask',
                        action="store_false",
                        dest='MASK',
                        help='Don\'t mask each label\'s image')

    parser.add_argument('-spm',
                        '--sub-pixel-margin',
                        type=numpy.uint,
                        default=2,
                        dest='SUBPIXEL_MARGIN',
                        help="Subpixel margin for subpixel interpolation. Default = 3px")

    parser.add_argument('-spi',
                        '--sub-pixel-max-iterations',
                        type=numpy.uint,
                        default=50,
                        dest='SUBPIXEL_MAX_ITERATIONS',
                        help="Subpixel max iterations subpixel search. Default = 50")

    parser.add_argument('-spp',
                        '--sub-pixel-min-phi-change',
                        type=numpy.float,
                        default=0.001,
                        dest='SUBPIXEL_MIN_PHI_CHANGE',
                        help="Subpixel min change in Phi to stop subpixel search. Default = 0.001")

    parser.add_argument('-spo',
                        '--sub-pixel-interpolation-order',
                        type=numpy.uint,
                        default=1,
                        dest='SUBPIXEL_INTERPOLATION_ORDER',
                        help="Subpixel interpolation order. Default = 3")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files. Default is basename of input file (without extension)")

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.lab1.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    #  sub pixel margin must be at least as big as label dilate
    if args.LABEL_DILATE >= args.SUBPIXEL_MARGIN:
        print("Warning, \"label dilate\" is less than to \"sub pixel margin\", overriding")
        args.SUBPIXEL_MARGIN = args.LABEL_DILATE

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0]+"-"+os.path.splitext(os.path.basename(args.im2.name))[0]

    return args


def multiModalRegistrationParser(parser):
    import spam.DIC
    import numpy

    parser.add_argument('im1',
                        metavar='im1',
                        type=argparse.FileType('r'),
                        help="Greyscale image of reference state for correlation")

    parser.add_argument('im2',
                        metavar='im2',
                        type=argparse.FileType('r'),
                        help="Greyscale image of deformed state for correlation")

    parser.add_argument('-im1min',
                        type=float,
                        default=None,
                        dest='IM1_MIN',
                        help="Minimum of im1 for greylevel scaling. Default = im1.min()")

    parser.add_argument('-im1max',
                        type=float,
                        default=None,
                        dest='IM1_MAX',
                        help="Maximum of im1 for greylevel scaling. Default = im1.max()")

    parser.add_argument('-im2min',
                        type=float,
                        default=None,
                        dest='IM2_MIN',
                        help="Minimum of im2 for greylevel scaling. Default = im2.min()")

    parser.add_argument('-im2max',
                        type=float,
                        default=None,
                        dest='IM2_MAX',
                        help="Maximum of im2 for greylevel scaling. Default = im2.max()")

    parser.add_argument('-im1th',
                        '--im1-threshold',
                        type=int,
                        default=0,
                        dest='IM1_THRESHOLD',
                        help='Greylevel threshold for image 1. Below this threshold, peaks in the histogram are ignored.')

    parser.add_argument('-im2th',
                        '--im2-threshold',
                        type=int,
                        default=0,
                        dest='IM2_THRESHOLD',
                        help='Greylevel threshold for image 2. Below this threshold, peaks in the histogram are ignored.')

    parser.add_argument('-bin',
                        '--bin-levels',
                        type=int,
                        default=1,
                        dest='NBINS',
                        help='Number of binning levels to apply to the data (if given 3, the binning levels used will be 4 2 1). The -phase option is necessary and should define this many phases (i.e., 3 different numbers in this example)')

    parser.add_argument('-ph',
                        '--phases',
                        nargs='+',
                        type=int,
                        default=[2],
                        dest='PHASES',
                        help='Disactivate subpixel refinement?')

    parser.add_argument('-jhb',
                        '--joint-histogram-bins',
                        # nargs=1,
                        type=int,
                        default=128,
                        dest='JOINT_HISTO_BINS',
                        help='The number of greylevel bins for both images in the joint histogram')

    parser.add_argument('-dst',
                        '--dist-between-max',
                        type=int,
                        default=None,
                        dest='DIST_BETWEEN_MAX',
                        help='Minimal distance between two maxima in the histogram')

    parser.add_argument('-fdi',
                        '--fit-distance',
                        type=float,
                        default=None,
                        dest='FIT_DISTANCE',
                        help='Distance considered around a peak for the Gaussian ellipsoid fitting')

    parser.add_argument('-voc',
                        '--voxel-coverage',
                        type=float,
                        default=1.0,
                        dest='VOXEL_COVERAGE',
                        help='Percentage (between 0 and 1) of voxel coverage of the phases in the joint histogram')

    parser.add_argument('-int',
                        '--interactive',
                        action="store_true",
                        dest='INTERACTIVE',
                        help='Present live-updating plots to the user')

    parser.add_argument('-gra',
                        '--graphs',
                        action="store_true",
                        dest='GRAPHS',
                        help='Save graphs to file')

    parser.add_argument('-ssl',
                        '--show-slice-axis',
                        type=int,
                        default=0,
                        dest='SHOW_SLICE_AXIS',
                        help='Axis of the cut used for the plots')

    # parser.add_argument('-tmp',
    #                     '--writeTemporaryFiles',
    #                     action="store_true",
    #                     dest='DATA',
    #                     help='Save temporary files (joint histogram) to \"dat\" file')

    parser.add_argument('-loadprev',
                        '--load-previous-iteration',
                        action="store_true",
                        dest='LOADPREV',
                        help='Load output pickle files from previous iterations (2* coarser binning)')

    parser.add_argument('-mar',
                        '--margin',
                        type=float,
                        default=0.1,
                        dest='MARGIN',
                        help='Margin of both images. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-cro',
                        '--crop',
                        type=float,
                        default=0.1,
                        dest='CROP',
                        help='Initial crop of both images. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-pif',
                        default=None,
                        type=argparse.FileType('r'),
                        dest='FGUESS_PICKLE',
                        help="Pickle file name for initial guess. Should be in position 0 in the array and labeled as 'F' as for registration.")

    # Remove next two arguments for F input, and replace with displacement and rotation inputs on command line
    # parser.add_argument('-Ffile',
    # dest='PHIFILE',
    # default = None,
    # type=argparse.FileType('r'),
    # help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

    # parser.add_argument('-Ffb',
    # '--Ffile-bin-ratio',
    # type=int,
    # default=1,
    # dest='PHIFILE_BIN_RATIO',
    # help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    parser.add_argument('-tra',
                        '--translation',
                        nargs=3,
                        type=float,
                        default=None,
                        dest='TRA',
                        help="Z, Y, X initial displacements to apply at the bin 1 scale")

    parser.add_argument('-rot',
                        '--rotation',
                        nargs=3,
                        type=float,
                        default=None,
                        dest='ROT',
                        help="Z, Y, X components of rotation vector to apply at the bin 1 scale")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files. Default is basename of input file (without extension)")

    args = parser.parse_args()

    # The number of bin levels must be the same as the number of phases
    if (args.NBINS != len(args.PHASES)):
        print("\toptionsParser.multiModalRegistrationParser(): Number of bin levels and number of phases not the same, exiting")
        exit()

    # For back compatibility, generate list of bins
    args.BINS = []
    for i in range(args.NBINS)[::-1]:
        args.BINS.append(2**i)

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.im1.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.im1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Get initial guesses
    if args.TRA is not None or args.ROT is not None:
        transformation = dict({})
        if args.TRA is not None:
            transformation['t'] = args.TRA
        if args.ROT is not None:
            transformation['r'] = args.ROT
        Fguess = spam.DIC.computePhi(transformation)
        args.FGUESS = Fguess
    else:
        args.FGUESS = numpy.eye(4)

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0]+"-"+os.path.splitext(os.path.basename(args.im2.name))[0]

    return args


def DICglobalParser(parser):
        parser.add_argument('inFiles',
                            nargs='+',
                            type=argparse.FileType('r'),
                            help="A space-separated list of two 3D greyscale tiff files to correlate, in order")

        parser.add_argument('-mf1',
                            '--maskFile1',
                            dest='MASK1',
                            default=None,
                            type=argparse.FileType('r'),
                            help="Path to tiff file containing the mask of image 1 -- masks  zones not to correlate")

        parser.add_argument('-mf2',
                            '--maskFile2',
                            dest='MASK2',
                            default=None,
                            type=argparse.FileType('r'),
                            help="Path to tiff file containing the mask of image 2 -- masks correlation windows")

        parser.add_argument('-pf',
                            '-phiFile',
                            dest='PHIFILE',
                            default=None,
                            type=argparse.FileType('r'),
                            help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

        parser.add_argument('-pfb',
                            '--phiFile-bin-ratio',
                            type=int,
                            default=1,
                            dest='PHIFILE_BIN_RATIO',
                            help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

        # parser.add_argument('-glt',
        #                     '--grey-low-threshold',
        #                     type=float,
        #                     default=-numpy.inf,
        #                     dest='GREY_LOW_THRESH',
        #                     help="Grey threshold on mean of reference imagette BELOW which the correlation is not performed. Default = -infinity")
        #
        # parser.add_argument('-ght',
        #                     '--grey-high-threshold',
        #                     type=float,
        #                     default=numpy.inf,
        #                     dest='GREY_HIGH_THRESH',
        #                     help="Grey threshold on mean of reference imagette ABOVE which the correlation is not performed. Default = infinity")

        parser.add_argument('-reg',
                            '--registration',
                            action="store_true",
                            dest='REG',
                            help='Perform an initial registration? Default = False')

        parser.add_argument('-regb',
                            '--registration-binning',
                            type=int,
                            default=1,
                            dest='REG_BIN',
                            help='Binning to apply to input images for registration. Default = 1')

        parser.add_argument('-regm',
                            '--registration-margin',
                            type=float,
                            default=0.1,
                            dest='REG_MARGIN',
                            help='Registration margin in proportions of image size. Default = 0.1, which means 0.1 * image size from both sides')

        # parser.add_argument('-nops',
        #                     '--no-pixel-search',
        #                     action="store_false",
        #                     dest='PS',
        #                     help='Disactivate pixel search?')

        # parser.add_argument('-psr',
        #                     '--pixel-search-range',
        #                     nargs=6,
        #                     type=int,
        #                     default=[-3, 3, -3, 3, -3, 3],
        #                     dest='PSR',
        #                     help='Z- Z+ Y- Y+ X- X+ ranges (in pixels) for the pxiel search. Requires pixel search to be activated. Default = +-3px')

        # parser.add_argument('-psf',
        #                     '--pixel-search-filter',
        #                     type=int,
        #                     default=0,
        #                     dest='PS_FILTER',
        #                     help='Median filter pixel search results. Default = 0')

        parser.add_argument('-spi',
                            '--sub-pixel-max-iterations',
                            type=numpy.uint,
                            default=10,
                            dest='SUBPIXEL_MAX_ITERATIONS',
                            help="Subpixel max iterations subpixel search. Default = 10")

        parser.add_argument('-spp',
                            '--sub-pixel-min-phi-change',
                            type=numpy.float,
                            default=0.001,
                            dest='SUBPIXEL_MIN_PHI_CHANGE',
                            help="Subpixel min change in F to stop subpixel search. Default = 0.001")

        # parser.add_argument('-spo',
        #                     '--sub-pixel-interpolation-order',
        #                     type=numpy.uint,
        #                     default=1,
        #                     dest='SUBPIXEL_INTERPOLATION_ORDER',
        #                     help="Subpixel interpolation order. Default = 1")

        # parser.add_argument('-cif',
        #                     '--correct-input-field',
        #                     action="store_true",
        #                     dest='CF',
        #                     help='Correction of the input F field. Default = True')

        # parser.add_argument('-nfi',
        #                     '--neighbours-for-field-interpolation',
        #                     type=numpy.uint,
        #                     default=12,
        #                     dest='NEIGHBOURS',
        #                     help="Neighbours for field interpolation. Default = 12")

        parser.add_argument('-od',
                            '--out-dir',
                            type=str,
                            default=None,
                            dest='OUT_DIR',
                            help="Output directory, default is the dirname of input file")

        parser.add_argument('-pre',
                            '--prefix',
                            type=str,
                            default="GDIC_",
                            dest='PREFIX',
                            help="Prefix for output files. Default is basename of input file (without extension)")

        parser.add_argument('-Mfile',
                            dest='MESH_FILE',
                            default=None,
                            type=argparse.FileType('r'),
                            help="Path to pickle file containing mesh information needed for the correlation (coordinates, connectivity, labels and padding). Default = None.")

        parser.add_argument('-Mcube',
                            '--mesh-cuboid',
                            nargs=7,
                            type=numpy.float,
                            default=None,
                            dest='MESH_CUBOID',
                            help='7 floats parameters to mesh a cuboid. first 3 are position of the bottom corner (Z, Y X), next 3 are the lenghts of the cube (Z, Y X) and the last one is the average length between two nodes.')

        args = parser.parse_args()

        if args.MESH_FILE is None and args.MESH_CUBOID is None:
            print("\tgdic: a mesh is needed. Use one of this option: -Mcube or -Mfile.")
            print("\tgdic: exiting.")
            exit()

        # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
        if args.OUT_DIR is None:
            args.OUT_DIR = os.path.dirname(args.inFiles[0].name)
            # However if we have no dir, notice this and make it the current directory.
            if args.OUT_DIR == "":
                args.OUT_DIR = "./"
        else:
            # Check existence of output directory
            try:
                if args.OUT_DIR:
                    os.makedirs(args.OUT_DIR)
                else:
                    args.DIR_out = os.path.dirname(args.inFiles[0].name)
            except OSError:
                if not os.path.isdir(args.OUT_DIR):
                    raise

        # Output file name prefix
        if args.PREFIX is None:
            args.PREFIX = os.path.splitext(os.path.basename(args.inFiles[0].name))[0]

        if type(args.SUBPIXEL_MAX_ITERATIONS) == list:
            args.SUBPIXEL_MAX_ITERATIONS = args.SUBPIXEL_MAX_ITERATIONS[0]

        if args.REG_MARGIN > 0.45:
            print("Registration margin cannot be bigger than 0.45 since 0.5 would contain no data!!")

        return args

def regularStrainsCalcParser(parser):
    parser.add_argument('inFile',
                        metavar='inFile',
                        type=argparse.FileType('r'),
                        help='Path to TSV file containing the result of the correlation')

    parser.add_argument('-mask',
                        '--mask',
                        action="store_true",
                        dest='MASK',
                        help='Mask correlation points according to return status')

    parser.add_argument('-cif',
                        '--correct-input-field',
                        action="store_true",
                        dest='CORRECT_FIELD',
                        help='Activates correction of the input displacement field')

    parser.add_argument('-cni',
                        '--correct-neighbours-for-field-interpolation',
                        type=numpy.uint,
                        default=12,
                        dest='CORRECT_NEIGHBOURS',
                        help="Neighbours for field interpolation. Default = 12")

    parser.add_argument('-cmf',
                        '--correct-median-filter',
                        action="store_true",
                        dest='CORRECT_MEDIAN_FILTER',
                        help="Activates an overall median filter on the input displacement field")

    parser.add_argument('-cmfr',
                        '--correct-median-filter-radius',
                        type=numpy.uint,
                        default=2,
                        dest='CORRECT_MEDIAN_FILTER_RADIUS',
                        help="Radius of median filter for correction of input displacement field. Default = 2")

    parser.add_argument('-cdp',
                        '--correct-delta-phi-norm',
                        type=numpy.float,
                        default=None,
                        dest='CORRECT_DELTA_PHI_NORM',
                        help="Delta Phi norm for a return status = 1 correlation window to consider the point good. Default = 0")

    parser.add_argument('-cpscc',
                        '--correct-pixel-search-cc',
                        type=numpy.float,
                        default=0,
                        dest='CORRECT_PIXEL_SEARCH_CC',
                        help="Pixel search correlation coefficient to consider the point good. Default = 0")

    parser.add_argument('-ss',
                        '--small--strains',
                        action="store_true",
                        dest='SMALL_STRAINS',
                        help='Strain field is computed under the hypothesis of small strain. Default = False')

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help='Output directory, default is the dirname of input file')

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output files. Default is basename of input file (without extension)')

    parser.add_argument('-nos',
                        '--not-only-strain',
                        action="store_true",
                        dest='NOT_ONLY_STRAIN',
                        help='Return all the output matrices. Default = True')

    parser.add_argument('-tif',
                        '-tiff',
                        '--TIFFout',
                        '--TIFout',
                        action="store_true",
                        dest='TIF',
                        help='Activate TIF output format. Default = True')

    parser.add_argument('-vtk',
                        '--VTKout',
                        action="store_true",
                        dest='VTK',
                        help='Activate VTK output format. Default = True')

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFile.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise
     # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.inFile.name))[0]

     # Make sure at least one output format has been asked for
    if args.VTK + args.TIF == 0:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: No output type of VTK, TSV and TIF options  ###")
        print("###  Are you sure this is right?!                         ###")
        print("#############################################################")
        print("#############################################################")

    return args

def discreteStrainsCalcParser(parser):
    parser.add_argument('inFile',
                        metavar='inFile',
                        type=argparse.FileType('r'),
                        help='Path to TSV file containing the result of the correlation')

    parser.add_argument('-ss',
                        '--small--strains',
                        action="store_true",
                        dest='SMALL_STRAINS',
                        help='Strain field is computed under the hypothesis of small strain. Default = False')

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help='Output directory, default is the dirname of input file')

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output files. Default is basename of input file (without extension)')

    parser.add_argument('-nos',
                        '--not-only-strain',
                        action="store_true",
                        dest='NOT_ONLY_STRAIN',
                        help='Return all the output matrices. Default = True')

    parser.add_argument('-vtk',
                        '--VTKout',
                        action="store_true",
                        dest='VTK',
                        help='Activate VTK output format. Default = True')

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFile.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise
     # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.inFile.name))[0]

     # Make sure at least one output format has been asked for
    if args.VTK + args.TIF == 0:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: No output type of VTK, TSV and TIF options  ###")
        print("###  Are you sure this is right?!                         ###")
        print("#############################################################")
        print("#############################################################")

    return args


def BCFromDVCParser(parser):
    parser.add_argument('-gmshFile',
                        dest='GMSHFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help='Path to gmsh file containing the FE mesh. Default = None')

    parser.add_argument('-vtkFile',
                        dest='VTKFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help='Path to vtk file containing the FE mesh. Default = None')

    parser.add_argument('-tsvFile',
                        dest='TSVDVCFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to tsv file containing the result of a correlation. Default = None")

    parser.add_argument('-mask',
                        '--mask',
                        action="store_true",
                        dest='MASK',
                        help='Mask correlation points according to return status')

    parser.add_argument('-pixSize',
                        '--pixel-size',
                        type = numpy.float,
                        default = 1.0,
                        dest='PIXEL_SIZE',
                        help="Physical size of a pixel (i.e. mm/px). Default = 1")

    parser.add_argument('-tol',
                        '--tolerance',
                        type=numpy.float,
                        default=1e-6,
                        dest='TOL',
                        help="Numerical tolerance for floats. Default = 1e-6")

    parser.add_argument('-meshType',
                        '--mesh-type',
                        type=str,
                        default="cube",
                        dest='MESHTYPE',
                        help="The type of the input mesh (i.e. cube, cylinder etc). Default = cube")
    
    parser.add_argument('-topBottom',
                        '--top-bottom',
                        action="store_true",
                        dest='TOP_BOTTOM',
                        help="Apply BC only on top-bottom surfaces (i.e. z=zmin, z=zmax)")
    
    parser.add_argument('-cylCentre',
                        '--cylinder-centre',
                        nargs=2,
                        type=numpy.float,
                        default=[0, 0],
                        dest='CYLCENTRE',
                        help="The cente of the cylinder [x, y]. Default =[0, 0]")
    
    parser.add_argument('-cylRadius',
                        '--cylinder-radius',
                        type=numpy.float,
                        default=1.0,
                        dest='CYLRADIUS',
                        help="The radius of the cylinder. Default = 1")
    
    parser.add_argument('-ni',
                        '--neighbours-for-interpolation',
                        type=numpy.uint,
                        default=4,
                        dest='NEIGHBOURS_INT',
                        help="Neighbours for field interpolation. Default = 4")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of gmsh file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output files. Default is basename of mesh file (without extension)')

    parser.add_argument('-feapBC',
                        '--feap-boundary-conditions',
                        action="store_true",
                        dest='FEAPBC',
                        help='Write the boundary conditions in FEAP format. Default = True')
    
    parser.add_argument('-saveVTK',
                        '--VTKout',
                        action="store_true",
                        dest='SAVE_VTK',
                        help='Save the BC field as VTK. Default = True')

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        try:
            args.OUT_DIR = os.path.dirname(args.GMSHFILE.name)
        except:
            try:
                args.OUT_DIR = os.path.dirname(args.VTKFILE.name)
            except:
                print("\n***You need to input an unstructured mesh. Exiting...***")
                exit()
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                try:
                    args.DIR_out = os.path.dirname(args.GMSHFILE.name)
                except:
                    try:
                        args.DIR_out = os.path.dirname(args.VTKFILE.name)
                    except:
                        print("\n***You need to input an unstructured mesh. Exiting...***")

        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        try:
            args.PREFIX = os.path.splitext(os.path.basename(args.GMSHFILE.name))[0]
        except:
            try:
                args.DIR_out = os.path.dirname(args.VTKFILE.name)
            except:
                print("\n***You need to input an unstructured mesh. Exiting...***")
                exit()

    return args
