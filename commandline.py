#python commandline.py --type single --input test1.jpg --method square --output result_test1.jpg --category 1
#python commandline.py --type batch --input "H:/brinell images/MP-4/Camera2 Images/1" --method square --output "H:/brinell images/MP-4/Result/1" --category 1
#python commandline.py --type single --input test4.tif --method square --output result_test4.tif --indentor 10 --load 3000 --hbv 288.4 --calibration 3.6
# 1st --> 0.8694 # 2nd --> 1.069 #  
#python commandline.py --type single --input ./10-3000-288.4BHN/0010.tif --output 0001.tif --indentor 10 --load 3000 --hbv 288.4 --method square --calibration 0.0076 --lower 285 --upper 291
#python commandline.py --type batch --input ./5-750-282.0BHN/ --output ./5-750-282.0BHN/Result/ --indentor 5 --load 750 --hbv 282 --method square --calibration 0.00780 --lower 279 --upper 285
import argparse
from ast import arg
import imp
from batch import batch
from single import single
import sys

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", required=True,
	help="Type of Excecution Single Or Batch Process")
ap.add_argument("-i", "--input", required=True,
	help="path of input file")
# ap.add_argument("-m", "--method", required=True,
#  	help="Square method or Circle method")
ap.add_argument("-o", "--output", required=True,
	help="Output Path")
# ap.add_argument("-ca", "--category", required=True,
# 	help="Category Type")
ap.add_argument("-in", "--indentor",required=True,help="diameter_of_indenter")
ap.add_argument("-ld", "--load",required=True,help="applied_load") 
ap.add_argument("-hd", "--hbv",required=True,help="HB_value")
ap.add_argument("-cb", "--calibration",required=True,help="calibration_value")
ap.add_argument("-mh", "--method",required=True,help="method")
ap.add_argument("-lb", "--lower",required=True,help="lower_value")
ap.add_argument("-ub", "--upper",required=True,help="upper_value")     
args = vars(ap.parse_args())
print(args)
type = args["type"]
input = args["input"]
output = args["output"]
indentor = float(args["indentor"])
load = float(args["load"])
hbvalue = float(args["hbv"])
calibration=float(args["calibration"])
method = args["method"]
lower=float(args["lower"])
upper=float(args["upper"])
std_mean_diameter=45

# if category == "1":
#     #diameter_calculated = 0.8694
#     HB_value = 99.6
#     diameter_of_indenter = 2.5
#     applied_load = 62.5
#     std_mean_diameter = 89.909425
#     calibration = 0.8694
# elif category == "2":
#     #diameter_calculated = 1.069
#     HB_value = 198.6
#     diameter_of_indenter = 2.5
#     applied_load = 187.5
#     std_mean_diameter = 73.27161
#     calibration = 1.069
# elif category == "3":
#     #diameter_calculated = 2.1115
#     HB_value = 200.4
#     diameter_of_indenter = 5
#     applied_load = 750
#     std_mean_diameter = 218.19523
#     #std_mean_diameter = 220.02669
#     calibration = 2.1115
# elif category == "4":
#     #diameter_calculated = 4.0783
#     HB_value = 220
#     diameter_of_indenter = 10
#     applied_load = 3000
#     std_mean_diameter = 429.08119
#     # std_mean_diameter = 429.44697
#     calibration = 4.0783
# elif category == "5":
#     #diameter_calculated = 4.0783
#     HB_value = 288.4
#     diameter_of_indenter = 10
#     applied_load = 3000
#     std_mean_diameter = 429.08119
#     # std_mean_diameter = 429.44697
#     calibration = 3.5795

if(type == "single"):
    #single(input,calibration,output,diameter_of_indenter,applied_load,HB_value,method,std_mean_diameter)
    single(input,calibration,output,indentor,load,hbvalue,method,lower,upper)

if(type == "batch"):
    batch(input,calibration,output,indentor,load,hbvalue,method,lower,upper)
