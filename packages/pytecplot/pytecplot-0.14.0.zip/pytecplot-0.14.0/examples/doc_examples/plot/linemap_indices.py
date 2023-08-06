from os import path
import tecplot as tp
from tecplot.constant import PlotType, IJKLines

examples_dir = tp.session.tecplot_examples_directory()
infile = path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
dataset = tp.data.load_tecplot(infile)

frame = tp.active_frame()
frame.plot_type = PlotType.XYLine
plot = frame.plot()

for lmap in list(plot.linemaps())[:3]:
    lmap.show = True
#{DOC:highlight}[
    lmap.indices.varying_index = IJKLines.I
    lmap.indices.i_range = 0,0,3
#]

# save image to file
tp.export.save_png('linemap_indices.png', 600, supersample=3)
