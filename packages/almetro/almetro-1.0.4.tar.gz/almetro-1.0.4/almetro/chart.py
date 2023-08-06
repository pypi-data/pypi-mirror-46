from matplotlib import pyplot as plt
from collections.abc import Iterable
from .spec import experimental_with_ratio_spec


class ChartLine:
    def __init__(self, data={}, label=None, color=None):
        self.data = data
        self.label = label
        self.color = color
        self.plt_line = None

    def setup(self, plt_axis):
        lines = plt_axis.plot(self.data.keys(), self.data.values(), self.color, label=self.label)
        if isinstance(lines, Iterable):
            self.plt_line = lines[0]
        else:
            self.plt_line = lines

    @staticmethod
    def new(data={}, label=None, color=None):
        return ChartLine(data, label, color)


class ChartAxis:
    legend_loc = "upper left"
    grid = True

    def __init__(self, title=None, chart_lines=[]):
        self.title = title
        self.chart_lines = chart_lines
        self.plt_axis = None

    def setup(self, plt_axis):
        self.plt_axis = plt_axis
        self.plt_axis.set_title(self.title)
        self.plt_axis.grid(ChartAxis.grid)
        for chart_line in self.chart_lines:
            chart_line.setup(self.plt_axis)
        self.plt_axis.legend(loc=ChartAxis.legend_loc)
        self.plt_axis.label_outer()

    @staticmethod
    def new(title=None, chart_lines=[]):
        return ChartAxis(title, chart_lines)


class Chart:
    def __init__(self, title=None, chart_axes=[]):
        self.title = title
        self.chart_axes = chart_axes
        self.plt_figure = None

    def show(self):
        fig, axes = plt.subplots(1, len(self.chart_axes), sharex=True, sharey=False, figsize=(18, 10))
        self.plt_figure = fig
        self.plt_figure.suptitle(self.title)
        for i, chart_axis in enumerate(self.chart_axes):
            if isinstance(axes, Iterable):
                axis = axes[i]
            else:
                axis = axes
            chart_axis.setup(axis)
        plt.close()
        return fig

    @staticmethod
    def new(title=None, chart_axes=[]):
        return Chart(title, chart_axes)


def build_chart(metro, spec_builder=experimental_with_ratio_spec):
    spec = spec_builder(metro, metro.complexity)
    chart_axes = []
    for axis_spec in spec['axes']:
        chart_lines = []
        for line_spec in axis_spec['lines']:
            chart_lines.append(ChartLine.new(**line_spec))
        chart_axes.append(ChartAxis.new(axis_spec['title'], chart_lines))

    return Chart.new(spec['title'], chart_axes)
