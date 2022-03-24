#python commandline.py --type single --input test1.jpg --method square --output result_test1.jpg --category 1
#python commandline.py --type batch --input "H:/brinell images/MP-4/Camera2 Images/1" --method square --output "H:/brinell images/MP-4/Result/1" --category 1
# 1st --> 0.8694 # 2nd --> 1.069 #  
import argparse
from batch import batch
from single import single

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", required=True,
	help="Type of Excecution Single Or Batch Process")
ap.add_argument("-i", "--input", required=True,
	help="path of input file")
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
method = args["method"]
output = args["output"]
category = args["category"]

if category == "1":
    #diameter_calculated = 0.8694
    HB_value = 99.6
    diameter_of_indenter = 2.5
    applied_load = 62.5
    std_mean_diameter = 89.909425
    calibration = 0.8694
elif category == "2":
    #diameter_calculated = 1.069
    HB_value = 198.6
    diameter_of_indenter = 2.5
    applied_load = 187.5
    std_mean_diameter = 73.27161
    calibration = 1.069
elif category == "3":
    #diameter_calculated = 2.1115
    HB_value = 200.4
    diameter_of_indenter = 5
    applied_load = 750
    std_mean_diameter = 218.19523
    #std_mean_diameter = 220.02669
    calibration = 2.1115
elif category == "4":
    #diameter_calculated = 4.0783
    HB_value = 220
    diameter_of_indenter = 10
    applied_load = 3000
    std_mean_diameter = 429.08119
    # std_mean_diameter = 429.44697
    calibration = 4.0783

if(type == "single"):
    single(input,calibration,output,diameter_of_indenter,applied_load,HB_value,method,std_mean_diameter)

if(type == "batch"):
    batch(input,calibration,output,diameter_of_indenter,applied_load,HB_value,method,std_mean_diameter)
