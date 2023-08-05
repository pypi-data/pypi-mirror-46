import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from ipywidgets import interact, FloatLogSlider
from sklearn.svm import SVC

from jcopml.plot.svc_decision import plot_svc
from luwiji.dataset.svm import gen_data_1, gen_data_2, gen_data_3

import os
from IPython.display import Image


class BaseDemoSVM:
    def __init__(self):
        pass

    @staticmethod
    def C():
        def _simul(C=10):
            model = SVC(kernel='linear', C=C).fit(X, y)
            plot_svc(X, y, model)
        df = gen_data_1()
        X = df.drop(columns="label")
        y = df.label
        interact(_simul, C=FloatLogSlider(value=100, base=10, min=-2, max=1, step=0.25, description='C'))


    @staticmethod
    def rbf():
        def _simul(elevation=90, sigma=0):
            r = np.exp(-(X ** 2).sum(1)/2/sigma**2)
            plt.figure(figsize=(8, 8))
            ax = plt.subplot(projection='3d')
            ax.scatter3D(X.x_1, X.x_2, r, c=y, s=50, cmap='bwr')
            ax.view_init(elev=elevation, azim=30)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('r')
        df = gen_data_2()
        X = df.drop(columns="label")
        y = df.label
        interact(_simul, elevation=(0, 90, 15), sigma=(0, 2, 0.2))


    @staticmethod
    def gamma():
        def _simul(gamma=0.01, plot_3d=False):
            model = SVC(kernel='rbf', C=1, gamma=gamma).fit(X, y)
            if plot_3d:
                plt.figure(figsize=(8, 8))
                val = model.decision_function(X_grid)
                Z = val.reshape(X1.shape)

                ax = plt.subplot(projection='3d')
                ax.plot_surface(X1, X2, Z, cstride=2, rstride=2, antialiased=False)
            else:
                plot_svc(X, y, model, support=False)
        df = gen_data_3()
        X = df.drop(columns="label")
        y = df.label

        xx = np.linspace(-0.4, 0.4, 100)
        yy = np.linspace(-0.4, 0.4, 100)
        X1, X2 = np.meshgrid(xx, yy)

        X_grid = np.c_[X1.ravel(), X2.ravel()]

        interact(_simul, gamma=FloatLogSlider(value=1, base=10, min=0, max=4, step=0.25, description='gamma'))


class BaseIllustrationSVM:
    def __init__(self):
        here = os.path.dirname(__file__)
        self.choose_one = Image(f"{here}/assets/choose_one.png", width=900)
        self.maximum_margin = Image(f"{here}/assets/maximum_margin.png", width=900)
