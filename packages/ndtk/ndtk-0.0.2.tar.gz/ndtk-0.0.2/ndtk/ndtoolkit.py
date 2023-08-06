import warnings
warnings.filterwarnings("ignore")

from control_chart.control_chart import *
from multi_dimension.multi_dimension import *

from optparse import OptionParser
import pandas as pd
import json
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")
#parser.add_option("-q", "--quiet",
#                  action="store_false", dest="verbose", default=True,
#                  help="don't print status messages to stdout")
parser.add_option("-m", "--method", dest="method",
                  help="[Shewhart,EWMA,CUSUM,PCA,SVDD,KMeans]", metavar="METHOD",choices=['Shewhart','EWMA','CUSUM','PCA','SVDD','KMeans'])

(options, args) = parser.parse_args()
#print options
A = pd.read_excel(options.filename)
figfilename = eval(options.method)(A)
output = {'figfilename':figfilename}
print json.dumps(output)
