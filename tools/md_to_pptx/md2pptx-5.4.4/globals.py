"""

globals.py

"""

import re

from processingOptions import ProcessingOptions

global processingOptions
processingOptions = ProcessingOptions()

global spanClassRegex
spanClassRegex = re.compile("<span( )*class=")

global spanStyleRegex
spanStyleRegex = re.compile("<span( )*style=")

global href_runs
href_runs = {}

global indirectAnchors
indirectAnchors = []
######################################################################################
#                                                                                    #
#  Prime for style. metadata                                                         #
#                                                                                    #
######################################################################################

# Background colour class correspondence
global bgcolors
bgcolors = {}

# Foreground colour class correspondence
global fgcolors
fgcolors = {}

# Emphases class correspondence
global emphases
emphases = {}

# Font size class correspondence
global fontsizes
fontsizes = {}

# Cell background class correspondence
global cellcolors
cellcolors = {}
