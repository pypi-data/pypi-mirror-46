from os import path
import tecplot as tp
from tecplot.constant import (Color, PlotType, PointsToPlot, SymbolType,
                                  GeomShape, FillMode)

examples_dir = tp.session.tecplot_examples_directory()
infile = path.join(examples_dir, 'SimpleData', 'HeatExchanger.plt')
dataset = tp.data.load_tecplot(infile)

frame = tp.active_frame()
frame.plot_type = PlotType.Cartesian2D
plot = frame.plot()
plot.show_shade = True
#{DOC:highlight}[
plot.show_scatter = True
#]

for i,fmap in enumerate(plot.fieldmaps()):
    fmap.points.points_to_plot = PointsToPlot.SurfaceCellCenters
    fmap.points.step = (4,4)

#{DOC:highlight}[
    fmap.scatter.color = Color((i%4)+13)
    fmap.scatter.fill_mode = FillMode.UseSpecificColor
    fmap.scatter.fill_color = Color.Yellow
    fmap.scatter.size = 3
    fmap.scatter.symbol_type = SymbolType.Text
    fmap.scatter.symbol().text = hex(i)[-1]
#]

    fmap.shade.color = Color.LightBlue

tp.export.save_png('fieldmap_scatter_text.png', 600, supersample=3)
