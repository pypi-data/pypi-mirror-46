from os import path
import tecplot as tp
from tecplot.constant import PlotType, Color, FillMode, GeomShape

examples_dir = tp.session.tecplot_examples_directory()
infile = path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
dataset = tp.data.load_tecplot(infile)

frame = tp.active_frame()
frame.plot_type = PlotType.XYLine
plot = frame.plot()
#{DOC:highlight}[
plot.show_symbols = True
#]

for lmap in list(plot.linemaps())[:3]:
#{DOC:highlight}[
    lmap.symbols.show = True
    lmap.symbols.symbol().shape = GeomShape.Square
    lmap.symbols.size = 2.5
    lmap.symbols.color = Color.Blue
    lmap.symbols.line_thickness = 0.4
    lmap.symbols.fill_mode = FillMode.UseSpecificColor
    lmap.symbols.fill_color = Color.Azure
#]

# save image to file
tp.export.save_png('linemap_symbols.png', 600, supersample=3)
