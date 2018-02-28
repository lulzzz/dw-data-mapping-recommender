import plotly


class plotly_graph(object):
    def __init__(self, traces, layout):
        self.traces = traces
        self.layout = layout

    def graph(self):
        fig = dict(data=self.traces, layout=self.layout)
        plotly.offline.plot(fig, filename='asd.html')
