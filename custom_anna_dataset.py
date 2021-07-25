"""
This script organizes a given anomaly detection dataset into the structure of the dataset 
found at https://www.research-collection.ethz.ch/handle/20.500.11850/389950?show=full, 
in order for it to be used within the ANNA framework https://github.com/leggedrobotics/anomaly_navigation.

A subset of the data, S (in which anomalies are detected in both the EO and its corresponding IR frame)
is created, and the dataset is split into train and test/validation sets from this subset of data.

:arg eo_normal: path to the folder containing the EO frames which did not contain maritime objects
:arg eo_anomalous: path to the folder containing the EO frames which contained maritime objects
:arg ir_normal: path to the folder containing the IR frames which did not contain maritime objects
:arg ir_anomalous: text file containing the file names of the IR frames which contained maritime objects
:arg train_size: number of EO/IR train images taken from S. The default value of 1200 was used in the Run #1 dataset.
:arg test_size: number of EO/IR test images taken from S. The default value of 100 was used in the Run #1 dataset.
"""

import argparse
from os import listdir
from random import shuffle
from shutil import copy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-eo_normal", default="image_folder/EO_0/", help="path to normal EO frames")
    parser.add_argument("-eo_anomalous", default="image_folder/EO_1/", help="path to anomalous EO frames")
    parser.add_argument("-ir_normal", default="image_folder/IR_0/", help="path to normal IR frames")
    parser.add_argument("-ir_anomalous", default="image_folder/IR_1/", help="path to anomalous IR frames")
    parser.add_argument("-train_size", type=int, default=1200, help="number of EO/IR train images")
    parser.add_argument("-test_size", type=int, default=100, help="number of EO/IR test images")
    args = parser.parse_args()

    eo_0_file = listdir(args.eo_normal)
    eo_1_file = listdir(args.eo_anomalous)
    ir_0_file = listdir(args.ir_normal)
    ir_1_file = listdir(args.ir_anomalous)

    eo0_frame_list = []
    eo1_frame_list = []
    ir0_frame_list = []
    ir1_frame_list = []

    with open(eo_0_file) as f:
        eo0_list = f.readlines()

    for item in eo0_list:
        fid = item.split('_')[1]
        eo0_frame_list.append(fid)

    with open(ir_0_file) as f:
        ir0_list = f.readlines()

    for item in ir0_list:
        fid = item.split('_')[1]
        ir0_frame_list.append(fid)

    with open(eo_1_file) as f:
        eo1_list = f.readlines()

    for item in eo1_list:
        fid = item.split('_')[1]
        eo1_frame_list.append(fid)

    with open(ir_1_file) as f:
        ir1_list = f.readlines()

    for item in ir1_list:
        fid = item.split('_')[1]
        ir1_frame_list.append(fid)

    zero_intersection_list = [frame for frame in eo0_frame_list if frame in ir0_frame_list]
    one_intersection_list = [frame for frame in eo1_frame_list if frame in ir1_frame_list]

    shuffle(zero_intersection_list)
    shuffle(one_intersection_list)

    train_list = zero_intersection_list[0 : args.train_size]
    val_pos_list = zero_intersection_list[args.train_size : args.train_size + args.test_size]
    val_neg_list = one_intersection_list[0 : args.test_size]

    for tl in train_list:
        tl_source_eo = args.eo_normal + "frame_" + str(tl) + "_rgb.png"
        tl_dest_eo = "data/full/train/frame_" + str(tl) + "_rgb.png"

        tl_source_ir = args.ir_normal + "frame_" + str(tl) + "_ir.png"
        tl_dest_ir = "data/full/train/frame_" + str(tl) + "_ir.png"

        copy(tl_source_eo, tl_dest_eo)
        copy(tl_source_ir, tl_dest_ir)

    for vp in val_pos_list:
        vp_source_eo = args.eo_normal + "frame_" + str(vp) + "_rgb.png"
        vp_dest_eo = "data/full/val/oe_pos/frame_" + str(vp) + "_rgb.png"

        vp_source_ir = args.ir_normal + "frame_" + str(vp) + "_ir.png"
        vp_dest_ir = "data/full/val/oe_pos/frame_" + str(vp) + "_ir.png"

        copy(vp_source_eo, vp_dest_eo)
        copy(vp_source_ir, vp_dest_ir)

    for vn in val_neg_list:
        vn_source_eo = args.eo_anomalous + "frame_" + str(vn) + "_rgb.png"
        vn_dest_eo = "data/full/val/oe_neg/frame_" + str(vn) + "_rgb.png"

        vn_source_ir = args.ir_anomalous + "frame_" + str(vn) + "_rgb.png"
        vn_dest_ir = "data/full/val/oe_neg/frame_" + str(vn) + "_ir.png"

        copy(vn_source_eo, vn_dest_eo)
        copy(vn_source_ir, vn_dest_ir)