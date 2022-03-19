import argparse
from single import single

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", required=True,
	help="Type of Excecution Single Or Batch Process")
ap.add_argument("-i", "--input", required=True,
	help="path of input file")
ap.add_argument("-c", "--calibration", required=True,
	help="Calibration value")
ap.add_argument("-m", "--method", required=True,
	help="Square method or Circle method")
ap.add_argument("-o", "--output", required=True,
	help="Output Path")
ap.add_argument("-ca", "--category", required=True,
	help="Category Type")
args = vars(ap.parse_args())
print(args)
type = args["type"]
input = args["input"]
calibration = args["calibration"]
method = args["method"]
output = args["output"]
category = args["category"]

if category == "1":
    diameter_of_indenter = 2.5
    applied_load = 62.5
elif category == "2":
    diameter_of_indenter = 2.5
    applied_load = 187.5
elif category == "3":
    diameter_of_indenter = 5
    applied_load = 750
elif category == "4":
    diameter_of_indenter = 10
    applied_load = 3000

if(type == "single"):
    single(input,calibration,output,diameter_of_indenter,applied_load)