from CGATReport.Plugins.HoloviewsPlotter import HoloviewsPlot
from CGATReport.DataTree import path2str
from CGATReport.ResultBlock import ResultBlock, ResultBlocks

try:
    import holoviews as hv
    import bokeh
    HAS_HOLOVIEW = True
except ImportError:
    HAS_HOLOVIEW = False


class HvPlotScatterWithLabels(HoloviewsPlot):

    def render(self, data, path):

        layout = hv.Scatter(data)
        points = hv.Labels(
            {('x', 'y'): data,
             "text": ["label{}".format(x) for x in range(len(data))]},
            ['x', 'y'],
            'text')
        layout *= points
        return self.endPlot(layout, None, path)


class HvPlotScatterWithHover(HoloviewsPlot):

    def render(self, data, path):

        data["name"] = ["label{}".format(x) for x in range(len(data))]
        layout = hv.Scatter(data)
        tooltips = {"Function": "@gene_function",
                    "Name": "@name"}
        hover = bokeh.models.HoverTool(tooltips=tooltips)
        layout.opts(tools=[hover], width=600, height=400)
        return self.endPlot(layout, None, path)
    
