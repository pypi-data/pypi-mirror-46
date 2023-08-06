#!/usr/bin/env python                                             
#                                                             _
# pacscopy fs app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import  os
import  sys

# import the Chris app superclass
from    chrisapp.base          import ChrisApp
from    distutils.dir_util     import copy_tree

Gstr_synopsis = """

    NAME

        pacscopy.py

    SYNOPSIS

        python pacscopy.py                                              \\
            --dir <dir>                                                 \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            [--man]                                                     \\
            [--meta]                                                    \\
            <outputDir> 

    BRIEF EXAMPLE

        * To copy some directory in open storage to an output directory:

            mkdir out
            python pacscopy.py      --dir <someDirInOpenStorage>        \\
                                    out

    DESCRIPTION

        `pacscopy.py` simply copies a directory specified with the 
        `--dir <dir>` flag-value pair to the output directory.

    ARGS

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number. 
        
        [--man]
        If specified, print (this) man page.

        [--meta]
        If specified, print plugin meta data.

        --dir <dir>
        The directory to copy to the <outputDir>.

"""

class Pacscopy(ChrisApp):
    """
    This is a simple application that is really just the `dircopy` plugin with a new name..
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'PACS copy '
    CATEGORY                = 'PACS'
    TYPE                    = 'fs'
    DESCRIPTION             = 'This is a simple application that is really just the `dircopy` plugin with a new name.'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '1.0.4'
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

    # Fill out this with key-value output descriptive info (such as an output file path
    # relative to the output dir) that you want to save to the output meta file when
    # called with the --saveoutputmeta flag
    OUTPUT_META_DICT = {}
 
    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """
        self.add_argument('--dir', 
                          dest          ='dir', 
                          type          = ChrisApp.path, 
                          default       = './', 
                          optional      = True,
                          help          = 'directory in PACS openstorage to be copied')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        copy_tree(options.dir, options.outputdir)

# ENTRYPOINT
if __name__ == "__main__":
    app = Pacscopy()
    app.launch()
