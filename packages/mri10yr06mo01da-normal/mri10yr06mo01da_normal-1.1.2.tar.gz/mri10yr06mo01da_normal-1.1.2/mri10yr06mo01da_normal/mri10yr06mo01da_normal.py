#!/usr/bin/env python
#                                                            _
# mri10yr06mo01da_normal fs app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import  os
from    os                      import listdir, sep
from    os.path                 import abspath, basename, isdir
from    distutils.dir_util      import copy_tree
import  shutil
import  pudb
import  sys
import  time
import  glob

Gstr_title = """
     
___  _________ _____      __  _____  _____  ____  _____  __  
|  \/  || ___ \_   _|    /  ||  _  ||  _  |/ ___||  _  |/  | 
| .  . || |_/ / | |______`| || |/' || |/' / /___ | |/' |`| | 
| |\/| ||    /  | |______|| ||  /| ||  /| | ___ \|  /| | | | 
| |  | || |\ \ _| |_     _| |\ |_/ /\ |_/ / \_/ |\ |_/ /_| |_
\_|  |_/\_| \_|\___/     \___/\___(_)\___/\_____(_)___/ \___/
                                                                                          
"""

Gstr_synopsis = """

    NAME

        mri10yr06mo01da_normal.py

    SYNOPSIS

        python mri10yr06mo01da_normal.py                                \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--splash <splash>]                                         \\
            [--dir <dir>]                                               \\
            <outputDir> 

    BRIEF EXAMPLE

        * Copy the (container) internal data to the output directory:

            mkdir out && chmod 777 out
            python mri10yr06mo01da_normal.py out

    DESCRIPTION

        `mri10yr06mo01da_normal.py` simply copies internal MRI data to the
        <outputDir>. If an optional [--dir <dir>] is passed, then contents
        of <dir> are copied instead.
        
    ARGS

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number. 
        
        [--man]
        If specified, print (this) man page.

        [--meta]
        If specified, print plugin meta data.

        [--splash <splash>]
        An optional splash message to print on startup.

        [--dir <dir>]
        An optional override directory to copy to the <outputDir>.
        Note, if run from a containerized version, this will copy 
        a directory from the *container* file system.

    EXAMPLES

    Copy the embedded MRI data to the ``out`` directory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Note: this command assumes that a directory called ``../data`` exists
    relative to the current directory (as is the case in containerized
    versions of this app).

        mkdir out && chmod 777 out
        mri10yr06mo01da_normal.py out

    Copy a user specified directory to the ``out`` directory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        mkdir out && chmod 777 out
        mri10yr06mo01da_normal.py --dir /usr/src/data out

"""

# import the Chris app superclass
from chrisapp.base import ChrisApp


class MRI10yr06mo01da_normal(ChrisApp):
    """
    This application simply copies from embedded data a reference normal anonymized MRI of a subject aged 10 years, 06 months, 01 days..
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'Anonymized reference MRI'
    CATEGORY                = 'Raw Data'
    TYPE                    = 'fs'
    DESCRIPTION             = 'This application simply copies from embedded data a reference normal anonymized MRI of a subject aged 10 years, 06 months, 01 days.'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '1.1.2'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictinary is saved when plugin is called with a ``--saveoutputmeta`` 
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}
 
    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """
        self.add_argument('--splash',
                            help        = 'a splash message to print',
                            type        = str,
                            dest        = 'splash',
                            optional    = True,
                            default     = '')
        self.add_argument('--dir', 
                          dest          ='dir', 
                          type          = str, 
                          default       = '', 
                          optional      = True,
                          help          = 'directory override')

    def manPage_show(self):
        """
        Print some quick help.
        """
        print(Gstr_synopsis)

    def metaData_show(self):
        """
        Print the plugin meta data
        """
        l_metaData  = dir(self)
        l_classVar  = [x for x in l_metaData if x.isupper() ]
        for str_var in l_classVar:
            str_val = getattr(self, str_var)
            print("%20s: %s" % (str_var, str_val))

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % MRI10yr06mo01da_normal.VERSION)

        if len(options.splash):
            print(options.splash)

        if len(options.dir):
            copy_tree(options.dir, options.outputdir)
        else:
            str_srcDir  = '../data'
            l_files = os.listdir(str_srcDir)
            for str_file in l_files:
                str_filename = os.path.join(str_srcDir, str_file)
                if (os.path.isfile(str_filename)):
                    print('Copying %s...' % str_filename)
                    shutil.copy(str_filename, options.outputdir)    

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)                    

# ENTRYPOINT
if __name__ == "__main__":
    app = MRI10yr06mo01da_normal()
    app.launch()
