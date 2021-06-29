import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse



def plot(dir, maw):
    file_list = os.listdir(dir)
    altitude_list = []
    for fi in file_list:
        with open(dir + "/" + fi) as f:
            params_list = f.readlines()
        print(params_list[64].split(':')[1].split(' ')[1])
        altitude_list.append(params_list[64].split(':')[1].split(' ')[1])

    altitude_array = np.array(altitude_list, dtype=np.float64)
    filtered_array = np.convolve(altitude_array, np.ones(maw), "valid") / maw

    sns.set()
    N = len(filtered_array)
    x = np.arange(N)

    plt.plot(x, filtered_array)
    plt.savefig("altitude_plot_" + dir + "_maw" + str(maw) + ".png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", default="raw_1125", help="folder name")
    parser.add_argument("-maw", type=int, help="moving average window")
    args = parser.parse_args()

    plot(args.path, args.maw)
