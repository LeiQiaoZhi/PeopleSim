from turtle import title
import matplotlib.pyplot as plt
from typing import *
import os


class PlotData:
    def __init__(self, xlabel, ylabel) -> None:
        self.X = []
        self.Y = []
        self.xlabel = xlabel
        self.ylabel = ylabel

    def add_entry(self, x, y):
        self.X.append(x)
        self.Y.append(y)

    def plot(self):
        pass


class LineData(PlotData):

    def plot(self, title=""):
        fig, ax = plt.subplots()
        ax.plot(self.X, self.Y)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(title)

        current_dir = os.path.dirname(os.path.realpath(__file__))
        save_path = os.path.join(os.path.dirname(current_dir), 'plots',
                                 f'{self.xlabel}_vs_{self.ylabel}.png')
        plt.savefig(save_path)
        print(f"{title} saved to {save_path}")


class ScatterData(PlotData):

    def plot(self, title=""):
        fig, ax = plt.subplots()
        ax.scatter(self.X, self.Y, s=2)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(title)

        current_dir = os.path.dirname(os.path.realpath(__file__))
        save_path = os.path.join(os.path.dirname(current_dir), 'plots',
                                 f'{self.xlabel}_vs_{self.ylabel}.png')
        plt.savefig(save_path)
        print(f"{title} saved to {save_path}")


class Plotter:
    def __init__(self) -> None:
        self.plot_data: Dict[str, PlotData] = {}

    def add_scatter(self, graph_name, x, y, xlabel="", ylabel="") -> None:
        if graph_name not in self.plot_data.keys():
            self.plot_data[graph_name] = ScatterData(xlabel, ylabel)
        self.plot_data[graph_name].add_entry(x, y)

    def add_scalar(self, graph_name, x, y, xlabel="", ylabel="") -> None:
        '''
        for normal line plots
        '''
        if graph_name not in self.plot_data.keys():
            self.plot_data[graph_name] = LineData(xlabel, ylabel)
        self.plot_data[graph_name].add_entry(x, y)

    def plot(self) -> None:
        print(f"\n***** Plotting Graphs *****\n")
        for name, data in self.plot_data.items():
            data.plot(title=name)
        print("Graphs Saved")
