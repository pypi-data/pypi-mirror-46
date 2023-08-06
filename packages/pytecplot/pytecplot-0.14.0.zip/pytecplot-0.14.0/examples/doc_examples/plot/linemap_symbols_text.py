from os import path
import tecplot as tp
from tecplot.constant import PlotType, Color, SymbolType, FillMode

examples_dir = tp.session.tecplot_examples_directory()
infile = path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
dataset = tp.data.load_tecplot(infile)

frame = tp.active_frame()
frame.plot_type = PlotType.XYLine
plot = frame.plot()
plot.show_symbols = True

cols = [Color.DeepRed, Color.Blue, Color.Fern]
chars = ['S','D','M']

for lmap,color,character in zip(plot.linemaps(), cols, chars):
    lmap.show = True
    lmap.line.color = color

    syms = lmap.symbols
    syms.show = True
#{DOC:highlight}[
    syms.symbol_type = SymbolType.Text
#]
    syms.size = 2.5
    syms.color = Color.White
    syms.fill_mode = FillMode.UseSpecificColor
    syms.fill_color = color
#{DOC:highlight}[
    syms.symbol().text = character
#]

plot.view.fit()

# save image to file
tp.export.save_png('linemap_symbols_text.png', 600, supersample=3)
