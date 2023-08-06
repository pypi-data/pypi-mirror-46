# @Author: Tang Yubin <tangyubin>
# @Date:   2019-05-26T12:04:11+08:00
# @Email:  tang-yu-bin@qq.com
# @Last modified by:   tangyubin
# @Last modified time: 2019-05-26T12:47:19+08:00

import numpy as np
import matplotlib.pyplot as plt

def plot_learning_curve():
    x = np.arange(10)
    y = x ** 2
    plt.plot(x, y)
