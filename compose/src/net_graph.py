import io
import networkx as nx
import matplotlib.pyplot as plt
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral11
from bokeh.models import (BoxZoomTool, Circle, HoverTool, SaveTool,
                          MultiLine, Plot, Range1d, ResetTool, PanTool)


def draw_graph(shelf):
    G = nx.DiGraph(directed=True)

    keys = list(shelf.keys())
    for key in keys:
        G.add_node(shelf[key]['jobname'],
               jobname=shelf[key]['jobname'],
                version = shelf[key]['version'],
                jarid = shelf[key]['jarid'],
                jobid = shelf[key]['jobid'],
                location = shelf[key]['location'],
                source_mqtt = shelf[key]['source_mqtt'],
                sink_mqtt=shelf[key]['sink_mqtt'],
                source_topic = shelf[key]['source_topic'],
                sink_topic = shelf[key]['sink_topic'],
                entry_class = shelf[key]['class']
               )
        jobs = list(shelf.keys())
        for job in jobs:
            if shelf[job]['source'] == shelf[key]['sink']:
                G.add_edge(shelf[key]['jobname'], shelf[job]['jobname'])

    node_color = Spectral11[2]
    edge_color = 'black'


    # Show with Bokeh
    plot = Plot(plot_width=1000, plot_height=800, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = "Job Graph"
    # what to show on hover
    node_hover_tool = HoverTool(tooltips=[("jobname", "@jobname"), ("version", "@version"), ("location", "@location"), ("source mqtt", "@source_mqtt"),
                                          ("sink mqtt", "@sink_mqtt"),
                                          ("source topic", "@source_topic"), ("sink topic", "@sink_topic")])

    #fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']

    # what tools to show on the side
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool(), SaveTool(), PanTool())
    # set up the graph to show, scale up and down when initially drawn
    graph_viz = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
    # visibility of nodes and edges
    graph_viz.node_renderer.glyph = Circle(size=25, fill_color=node_color)
    graph_viz.edge_renderer.glyph = MultiLine(line_color=edge_color, line_alpha=0.8, line_width=1)
    # append the graph to plotting
    plot.renderers.append(graph_viz)
    plot.legend.location = "top_left"

    return plot