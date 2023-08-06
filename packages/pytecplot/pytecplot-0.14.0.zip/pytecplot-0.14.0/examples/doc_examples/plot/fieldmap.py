import os
import numpy
import tecplot

examples_dir = tecplot.session.tecplot_examples_directory()
infile = os.path.join(examples_dir, 'SimpleData', 'F18.lay')
tecplot.load_layout(infile)
frame = tecplot.active_frame()
plot = frame.plot()
dataset = frame.dataset

plot.contour(0).colormap_name = 'GrayScale'
plot.contour(0).legend.show = False

for zone_name in ['left wing', 'right wing']:
    fmap = frame.plot().fieldmap(dataset.zone(zone_name))
    fmap.contour.flood_contour_group = plot.contour(1)

plot.contour(1).colormap_name = 'Sequential - Yellow/Green/Blue'
plot.contour(1).levels.reset_levels(numpy.linspace(-0.07, 0.07, 50))

tecplot.export.save_png('F18_wings.png', 600, supersample=3)
