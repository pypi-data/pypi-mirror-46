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
#{DOC:highlight}[
plot.show_scatter = True
#]

for i,fmap in enumerate(plot.fieldmaps()):
    points = fmap.points
    points.points_to_plot = PointsToPlot.SurfaceCellCenters
    points.step = (2,2)

#{DOC:highlight}[
    scatter = fmap.scatter
    scatter.color = Color(i)
    scatter.fill_mode = FillMode.UseSpecificColor
    scatter.fill_color = Color(i+plot.num_fieldmaps)
    scatter.size = 2
    scatter.line_thickness = 0.5
    scatter.symbol_type = SymbolType.Geometry
    scatter.symbol().shape = GeomShape(i%7)
#]

tp.export.save_png('fieldmap_scatter_geometry.png', 600, supersample=3)
