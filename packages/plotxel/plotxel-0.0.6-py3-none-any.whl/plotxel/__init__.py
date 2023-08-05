import svgwrite
from svgwrite import rgb
from cairosvg import svg2png
from PIL import Image
from math import log, floor, ceil
from collections import OrderedDict
import warnings
from io import BytesIO
from .charts import Scatter, Bar, Chart
from .axes import YAxis, XAxis, Axis
import cairosvg
__version__ = "0.0.6"


class Plotxel:
    def __init__(self, dim):
        self.dim = dim  # list, dimensions, in pixels, [width, height]
        self.data = {}  # dictionary to store all data values. will be referenced by data name
        self.drawables = OrderedDict()  # keep track of the drawable items (charts, axes) in the figure. each drawable has a name
        self.background_color = rgb(255, 255, 255)
        self.anti_aliasing = True

    def add_data(self, name, x, y):
        self.data[name] = [x, y]  # add some data. Drawables are linked to the data

    def add_drawable(self, drawable_name, drawable_type, data_name=None, link_to=None, **kwargs):
        """
        specify a data series name (in self.data), what kind of item, and its name
        """
        if drawable_type == "Scatter":
            self.drawables[drawable_name] = Scatter(data_name, drawable_name, kwargs)

        elif drawable_type == "YAxis":
            if data_name is None:
                data_name = self.drawables[link_to].data_name
            self.drawables[drawable_name] = YAxis(data_name, drawable_name, link_to, kwargs)

        elif drawable_type == "XAxis":
            if data_name is None:
                data_name = self.drawables[link_to].data_name
            self.drawables[drawable_name] = XAxis(data_name, drawable_name, link_to, kwargs)

        elif drawable_type == 'XHist':
            print("XHist not implemented yet.")

        elif drawable_type == 'YHist':
            print("YHist not implemented yet.")

        elif drawable_type == 'Bar':
            self.drawables[drawable_name] = Bar(data_name, drawable_name, kwargs)

        else:
            warnings.warn("Could not create a drawable of '%s'. Acceptable inputs are 'Scatter', 'Bar', 'YAxis', 'XAxis', 'YHist', and 'XHist'"%drawable_type, Warning)

        return self.drawables[drawable_name]

    def draw(self):
        """
        Converts the object to SVG HTML
        :return:
        """
        if self.anti_aliasing:
            svg_html = svgwrite.Drawing(size=(self.dim[0], self.dim[1]), shape_rendering='auto')
        else:
            svg_html = svgwrite.Drawing(size=(self.dim[0], self.dim[1]), shape_rendering='crispEdges')

        #svg_html = svgwrite.Drawing(size=(self.dim[0], self.dim[1]), shape_rendering='crispEdges')
        svg_html.add(svg_html.rect(size=(self.dim[0], self.dim[1]), fill=self.background_color, ))
        for figure_object_key in self.drawables:

            figure_object = self.drawables[figure_object_key]
            # check for our highest level objects. Chart, Axis, and we'll see what else in the future!!
            if figure_object.type == 'Chart':
                # print('Drawing a chart.')
                # if we encounter a Chart, it will have a subtype(e.g. Scatter) where 'draw' is defined.
                # we'll pass the object itself to the draw function so that we can extract the figure properties
                svg_html.add(figure_object.draw(self))
            if figure_object.type == 'Axis':
                # print('Drawing an axis.')
                svg_html.add(figure_object.draw(self))

        svg_html = svg_html.tostring()
        svg_html = svg_html.replace('><', '><')

        return svg_html

    def render(self, filename=None):
        """
        converts the svg to either a png file or a BytesIO object
        :param filename: str -- option filename
        :return:
        """
        if filename:
            if filename[-4:] == '.png':
                pass
            else:
                filename += '.png'
            svg2png(bytestring=self.draw(), write_to=filename)
            return filename
        #print(self.draw())
        mem_file = BytesIO()
        svg2png(self.draw(), write_to=mem_file)
        return mem_file

    def show(self):
        """
        Shows the image in whatever viewing software you have
        :return: None
        """
        image = Image.open(self.render())
        image.show()




