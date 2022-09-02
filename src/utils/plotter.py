from turtle import title
import matplotlib.pyplot as plt
from typing import *
import os
from utils.logger import Logger


class PlotData:
    def __init__(self, xlabel, ylabel, kwargs={}) -> None:
        self.X = []
        self.Y = []
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.kwargs = kwargs

    def add_entry(self, x, y):
        self.X.append(x)
        self.Y.append(y)

    def get_save_path(self) -> str:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        save_path = os.path.join(os.path.dirname(current_dir), 'plots',
                                 f'{self.ylabel}_vs_{self.xlabel}.png')
        return save_path

    def plot(self):
        pass


class LineData(PlotData):

    def plot(self, title=""):
        fig, ax = plt.subplots()
        ax.plot(self.X, self.Y, **self.kwargs)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(title)

        save_path = self.get_save_path()
        plt.savefig(save_path)
        Logger.info(f"{title} saved to {save_path}")


class ScatterData(PlotData):

    def plot(self, title=""):
        fig, ax = plt.subplots()
        ax.scatter(self.X, self.Y, **self.kwargs)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(title)

        save_path = self.get_save_path()
        plt.savefig(save_path)
        Logger.info(f"{title} saved to {save_path}")


class Plotter:
    def __init__(self) -> None:
        self.plot_data: Dict[str, PlotData] = {}

    def add_scatter(self, graph_name, x, y, xlabel="", ylabel="", kwargs={}) -> None:
        if graph_name not in self.plot_data.keys():
            self.plot_data[graph_name] = ScatterData(xlabel, ylabel, kwargs)
        self.plot_data[graph_name].add_entry(x, y)

    def add_scalar(self, graph_name, x, y, xlabel="", ylabel="", kwargs={}) -> None:
        '''
        for normal line plots
        '''
        if graph_name not in self.plot_data.keys():
            self.plot_data[graph_name] = LineData(xlabel, ylabel, kwargs)
        self.plot_data[graph_name].add_entry(x, y)

    def plot(self) -> None:
        Logger.print_title("Plotting Graphs")
        for name, data in self.plot_data.items():
            data.plot(title=name)
        Logger.important("Graphs Saved", color=Logger.GREEN)
