import svgwrite
from svgwrite import rgb
from cairosvg import svg2png
from PIL import Image
from math import log, floor, ceil
from collections import OrderedDict
import warnings
from io import BytesIO
import cairosvg
__version__ = "0.0.5"

def smart_limits(data):
    rounding_factor = .4
    head_room = .3
    true_max = max(abs(min(data)), abs(max(data)))
    num_zeros = log(rounding_factor * true_max, 10)
    limits = [0, 0]
    if max(data) == 0:
        limits[1] = 0
    else:
        limits[1] = round(max(data) + head_room * true_max, floor(num_zeros) * (-1))
    if limits[1] > 0 and max(data) < 0:
        limits[1] = 0
    if min(data) == 0:
        limits[0] = 0
    else:
        limits[0] = round(min(data) - head_room * true_max, floor(num_zeros) * (-1))
    if limits[0] < 0 and min(data) > 0:
        limits[0] = 0
    return limits


def smart_ticks(data, limits=None):
    if limits is None:
        limits = smart_limits(data)
    # print('Limits are: %s'%limits)
    # Ticks should only be in divisers of 1, 2, 2.5 or 5 and any 10x multiple of those, e.g. 10, 20, 25
    # We will start with ~ 5 ticks, but later adjust for axis size. We will also move this function to be an axis
    # class function

    # first, determine how many orders of magnitude our data spans
    magnitudes = floor(log(limits[1]-limits[0], 10))

    # next divide our limits by that
    div_limits = [limit/(10**magnitudes) for limit in limits]

    # manual, verbose checking potential limits to see how many ticks we would get
    potential_ticks = [.1, .2, .25, .5, 1, 2, 25, 50, 100]
    num_ticks = [floor((div_limits[1]-div_limits[0])/pt) for pt in potential_ticks]


    for i, num_tick in enumerate(num_ticks):
        # even though it says 3 to 5 allowed ticks, it could actually be actually 4 to 8
        if (num_tick >= 4) & (num_tick <= 6):
            tick = potential_ticks[i]
            break

    # print("Tick value: %s %s times"%(tick*10**magnitudes, num_tick))
    # next, find the minimum tick value that matches out convention of allowable tick numbers
    tick = tick*10**magnitudes

    # check if our limit falls directly on the first tick. This would give a float rounding error
    # if the difference between the tick and modulo is 3 orders of magnitude smaller than we expect, it's a rounding error

    if log(tick - limits[0] % tick, 10) < (magnitudes-3):
        first_tick = limits[0]

    else:
        first_tick = limits[0] - limits[0] % tick
    if first_tick < limits[0]:

        first_tick += tick

    #print('first tick is as such: ', limits, first_tick)
    #propogate our ticks from there
    ticks = [first_tick]
    max_tick = first_tick

    while True:
        max_tick += tick
        #print(max_tick, limits[1])
        if max_tick > limits[1]:
            break
        else:
            ticks.append(max_tick)
    #print(ticks)
    return ticks


class Chart:
    defaults = {
        'dim': [300, 150],
        'xlim': [],
        'ylim': [],
        'marker_shape': 'circle',
        'marker_size': 10,
        'pos': [0, 0],
        'inside_border_width': 1,
        'inside_border': [[1], [1], [1], [1]],
        'inside_border_color': 'black',
        'title': 'Title',
        'title_offset': 10,
        'title_font': 'arial',
        'title_font_size': 20,
        'line_width': 1,
        'line_color': (0, 0, 0)
    }

    def __init__(self, data_name):

        defaults = self.defaults
        self.type = 'Chart'
        self.data_name = data_name  # the data we link our chart to

        # chart properties
        self.dim = defaults['dim']  # [x, y] pixel size of graph. Does not include axes. Border will be truncated
        self.pos = defaults['pos']  # [x, y] pixels from top left corner
        self.xlim = defaults['xlim']  # [min, max] limits of our x data
        self.ylim = defaults['ylim']  # [min, max] limits of our y data

        self.inside_border_width = defaults['inside_border_width']
        self.inside_border = defaults['inside_border']  # top, right, bottom, left widths for the border
        self.inside_border_color = defaults['inside_border_color']  # border color

        self.title = defaults['title']
        self.title_font = defaults['title_font']
        self.title_offset = defaults['title_offset']
        self.title_font_size = defaults['title_font_size']

        # marker properties
        self.marker_shape = defaults['marker_shape']
        self.marker_size = defaults['marker_size']
        self.marker_fill_color = (50, 50, 200)  # color of the markers
        self.marker_border_color = (0, 0, 0)  # color of the marker border
        self.marker_border_width = 1  # thickness of the marker border. 0 means no border

        # line connector properties
        self.line_width = defaults['line_width']
        self.line_color = defaults['line_color']

    def get_x_res(self):
        return (self.dim[0]-1) / (self.xlim[1] - self.xlim[0])

    def get_y_res(self):
        return (self.dim[1]-1) / (self.ylim[1] - self.ylim[0])

    def setattrs(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def draw_border(self):
        if self.inside_border is not None and (type(self.inside_border) == list or type(self.inside_border) == set):
            border_path = 'M '
            border_strokes = []
            for border_instruction in self.inside_border:
                if border_instruction[0] == 1 or border_instruction[0] == True:
                    border_strokes.append('L')
                else:
                    border_strokes.append('M')
            border_positions = []

            border_positions.append([0,
                                     int(self.inside_border_width / 2) + self.inside_border_width % 2,
                                     ])

            border_positions.append(
                [self.dim[0] - int(self.inside_border_width / 2),  # + self.inside_border_width%2-1,
                 int(self.inside_border_width / 2) + self.inside_border_width % 2,
                 ])

            border_positions.append(
                [self.dim[0] - int(self.inside_border_width / 2),  # + self.inside_border_width % 2-1,
                 self.dim[1] - int(self.inside_border_width / 2)  # + self.inside_border_width % 2-1
                 ])

            border_positions.append([int(self.inside_border_width / 2) + self.inside_border_width % 2,
                                     self.dim[1] - int(self.inside_border_width / 2)
                                     # + self.inside_border_width % 2-1
                                     ])

            border_positions.append([int(self.inside_border_width / 2) + self.inside_border_width % 2,
                                     0
                                     ])

            border_strokes.append('M')

            for stroke, border_position in zip(border_strokes, border_positions):
                border_path += "%s %s %s" % (border_position[0], border_position[1], stroke)

            border_path += "%s %s" % (border_positions[0][0], border_positions[0][1])

        return svgwrite.path.Path(border_path,
                               shape_rendering='crispEdges',
                               fill="none",
                               stroke=self.inside_border_color,
                               stroke_width=self.inside_border_width)


    def draw_title(self):
        return svgwrite.text.Text('%s' % self.title,
                                     insert=(
                                         round(self.pos[0] + (self.dim[0] - 1) / 2),
                                         round(self.pos[1] - self.title_offset)
                                     ),
                                     style="text-anchor:middle;font-size:%spx;font-style:%s;alignment-baseline:bottom"%(self.title_font_size, self.title_font))


class Scatter(Chart):
    def __init__(self, data_name, kwargs={}):
        super().__init__(data_name)
        self.subtype = 'Scatter'
        self.setattrs(**kwargs)


    def SetDefaults(self, data):
        pass

    def draw(self, main_figure):

        x_data = main_figure.data[self.data_name][0]
        y_data = main_figure.data[self.data_name][1]

        if not self.xlim:
            self.xlim = smart_limits(x_data)

        if not self.ylim:
            self.ylim = smart_limits(y_data)

        # make a figure the size of the main figure
        # we may need to draw outside of the actual chart area and into the main figure (for borders and such)
        # we also need to extract data series and other things
        subfigure = svgwrite.Drawing(size=(main_figure.dim[0], main_figure.dim[1]))

        # determine how many pixels/value in our chart
        x_res = self.get_x_res()
        y_res = self.get_y_res()


        # establish our chart drawing area, such that the points are truncated if they fall outside the range
        # our chart points and circles will be added in here
        chart_area = svgwrite.Drawing(
            size=(self.dim[0], self.dim[1]),
            x=self.pos[0], y=self.pos[1])

        # each circle's position is calculated based on the chart size and it's data values
        # the points are plotted relative to our chart_area, which is then affixed to the main figure
        # x is plotted left to right. We calculate it by determining X's value relative to the chart minimum, then
        # multiplying it by the resolution to get it in pixels
        # y is plotted top to bottom, so same thing except we subtract the calculated value by the figure size
        # to get its proper position
        # future support: square, asterisk, dash, plus, custom svg

        data_coordinates = []

        for x, y in zip(x_data, y_data):
            # add coordinates
            data_coordinates.append(
                (
                    ((x - self.xlim[0]) * x_res),
                    (self.dim[1] - (y - self.ylim[0]) * y_res)
                )
            )

        # draw a line, if present
        if self.line_width > 0:
            line_path = "M "
            for center in data_coordinates:
                line_path +="%s %s L "%(center[0], center[1])
            line_path = line_path[:-2]
            chart_area.add(
                chart_area.path(line_path,
                                shape_rendering='geometricPrecision',
                                fill="none",
                                stroke=rgb(self.line_color[0], self.line_color[1], self.line_color[2]),
                                stroke_width=self.line_width))

        # draw our makers
        if self.marker_size > 0:

            for center in data_coordinates:
                if self.marker_shape == 'circle':
                    chart_area.add(
                        chart_area.circle(
                            #shape_rendering='crispEdges',
                            center=(center),
                            r=self.marker_size/2,
                            fill=rgb(self.marker_fill_color[0], self.marker_fill_color[1], self.marker_fill_color[2]),
                            stroke=rgb(self.marker_border_color[0], self.marker_border_color[1], self.marker_border_color[2],),
                            stroke_width=self.marker_border_width
                        )
                    )
                elif self.marker_shape == 'square':
                    chart_area.add(
                        chart_area.rect(
                            insert=(center[0] - self.marker_size/2, center[1] - self.marker_size/2),
                            size=(self.marker_size, self.marker_size),
                            fill=rgb(self.marker_fill_color[0], self.marker_fill_color[1], self.marker_fill_color[2]),
                            stroke=rgb(self.marker_border_color[0], self.marker_border_color[1],
                                       self.marker_border_color[2], ),
                            stroke_width=self.marker_border_width
                        )
                    )

                elif self.marker_shape == 'rectangle' or self.marker_shape == 'rect':
                    chart_area.add(
                        chart_area.rect(
                            insert=(center[0] - self.marker_size/2, center[1] - self.marker_size/4),
                            size=(self.marker_size, self.marker_size/2),
                            fill=rgb(self.marker_fill_color[0], self.marker_fill_color[1], self.marker_fill_color[2]),
                            stroke=rgb(self.marker_border_color[0], self.marker_border_color[1],
                                       self.marker_border_color[2], ),
                            stroke_width=self.marker_border_width
                        )
                    )
                elif self.marker_shape == '-' or self.marker_shape == 'dash':
                    pass
                elif self.marker_shape == '*' or self.marker_shape == 'star':
                    pass

        # inside of our chart area we will add a border.
            if self.inside_border is not None and (type(self.inside_border) == list or type(self.inside_border) == set):
                border_path = 'M '
                border_strokes = []
                for border_instruction in self.inside_border:
                    if border_instruction[0] == 1 or border_instruction[0] == True:
                        border_strokes.append('L')
                    else:
                        border_strokes.append('M')
                border_positions = []

                border_positions.append([0,
                                         int(self.inside_border_width / 2) + self.inside_border_width % 2,
                                         ])

                border_positions.append(
                    [self.dim[0] - int(self.inside_border_width / 2),  # + self.inside_border_width%2-1,
                     int(self.inside_border_width / 2) + self.inside_border_width % 2,
                     ])

                border_positions.append(
                    [self.dim[0] - int(self.inside_border_width / 2),  # + self.inside_border_width % 2-1,
                     self.dim[1] - int(self.inside_border_width / 2)  # + self.inside_border_width % 2-1
                     ])

                border_positions.append([int(self.inside_border_width / 2) + self.inside_border_width % 2,
                                         self.dim[1] - int(self.inside_border_width / 2)
                                         # + self.inside_border_width % 2-1
                                         ])

                border_positions.append([int(self.inside_border_width / 2) + self.inside_border_width % 2,
                                         0
                                         ])

                border_strokes.append('M')

                for stroke, border_position in zip(border_strokes, border_positions):
                    border_path += "%s %s %s" % (border_position[0], border_position[1], stroke)

                border_path += "%s %s" % (border_positions[0][0], border_positions[0][1])

            chart_area.add(chart_area.path(border_path,
                                         shape_rendering='crispEdges',
                                         fill="none",
                                         stroke=self.inside_border_color,
                                         stroke_width=self.inside_border_width))


        chart_area.add(self.draw_border())
        subfigure.add(self.draw_title())
        subfigure.add(chart_area)

        return subfigure


class Bar(Chart):

    def __init__(self, data_name, kwargs={}):
        super().__init__(data_name)
        self.subtype = 'Bar'
        self.style = 'grouped'
        self.group_spacing = 5
        self.bar_spacing = 5
        self.margins = [5, 5]
        self.bar_line_width = 1
        self.bar_fill_color = (0, 0, 0)
        self.bar_line_color = (0, 0, 0)
        self.ylim = None
        self.setattrs(**kwargs)

    def draw(self, main_figure):
        # get the data series
        data = []
        for series in main_figure.data[self.data_name]:
            data.append(series)

        # for a bar chart, pull the Y data
        data = data[1]

        subfigure = svgwrite.Drawing(size=(main_figure.dim[0], main_figure.dim[1]))
        chart_area = svgwrite.Drawing(
            size=(self.dim[0], self.dim[1]),
            x=self.pos[0], y=self.pos[1])

        # calculate bar widths. ensuring fidelity with respect to margin and bar spacing

        widths = self.get_widths(data)

        # get the top-middle coordinate of each bar. We'll use this for our rectangles
        bar_y_coords = []
        heights = []
        for i, y in enumerate(data):
            # add coordinates
            bar_y_coords.append(self.dim[1] - (y - self.ylim[0]) * self.get_y_res())
            heights.append((y - self.ylim[0]) * self.get_y_res())

        # get the left x value for our rectangles
        bar_x_coords = self.get_x_coords(widths)

        for x, y, width, height in zip(bar_x_coords, bar_y_coords, widths, heights):
            chart_area.add(
                chart_area.rect(
                    shape_rendering='crispEdges',
                    insert=(x-int(width/2), y),
                    size=(width, height),
                    fill=rgb(self.bar_fill_color[0], self.bar_fill_color[1], self.bar_fill_color[2]),
                    stroke=rgb(self.bar_line_color[0], self.bar_line_color[1],
                               self.bar_line_color[2], ),
                    stroke_width=self.bar_line_width
                )
            )
        chart_area.add(self.draw_border())
        subfigure.add(self.draw_title())
        subfigure.add(chart_area)

        return subfigure

    def get_x_coords(self, widths):
        bar_x_coords = [self.margins[0]]
        for width in widths[:-1]:
            bar_x_coords.append(bar_x_coords[-1] + width + self.group_spacing)
        for i, (width, bar_x_coord) in enumerate(zip(widths, bar_x_coords)):
            bar_x_coords[i] += int(width/2)
        return bar_x_coords

    def get_widths(self, data):
        widths = [(self.dim[0] - sum(self.margins) - self.group_spacing*(len(data)-1))//len(data)]*len(data)
        remainder = (self.dim[0] - sum(self.margins) - self.group_spacing*(len(data)-1))%len(data)

        for i, width in zip(range(remainder), widths):
            widths[i] += 1

        return widths


class Axis:
    defaults = {
        'dim': 0,
        'pos': [],  # [x, y] svg pixel coordinates of bottom left of chart
        'lim': [],  # [min, max] limits of our axis
        'color': (0, 0, 0),  # color of our axis line

        'axis_offset': 0,
        'axis_linewidth': 1,

        'major_tick_values': None,
        'major_tick_linewidth': 1,
        'major_tick_length': 5,
        'major_tick_color': (0, 0, 0),
        'major_ticks': [],
        'major_tick_font': 'arial',

        'minor_tick_linewidth': 1,
        'minor_tick_color': (0, 0, 0),

        'labels': [],  # labels for our major ticks
        'label_font_size': 10,  # font size of the axis labels
        'label_offset_x': 0,  # how far away the axis labels are away from the end of the ticks, y axis.
        'label_offset_y': 0,  # how far away the axis labels are away from the end of the ticks, x axis.

        'title': 'Axis',
        'title_font_size': 12,
        'title_offset': 0,
        'title_font': 'arial'
    }

    def __init__(self, data_name, link_to):
        defaults = self.defaults
        self.type = 'Axis'
        self.data_name = data_name
        self.link_to = link_to

        self.dim = defaults['dim']
        self.pos = defaults['pos']  # [x, y] svg pixel coordinates of bottom left of chart
        self.lim = defaults['lim']  # [min, max] limits of our axis
        self.color = defaults['color']  # color of our axis line

        self.axis_offset = defaults['axis_offset']
        self.axis_linewidth = defaults['axis_linewidth']

        self.major_tick_values = defaults['major_tick_values']
        self.major_tick_linewidth = defaults['major_tick_linewidth']
        self.major_tick_length = defaults['major_tick_length']
        self.major_tick_color = defaults['major_tick_color']
        self.major_ticks = defaults['major_ticks']
        self.major_tick_font = defaults['major_tick_font']

        self.minor_tick_linewidth = defaults['minor_tick_linewidth']
        self.minor_tick_color = defaults['minor_tick_color']

        self.labels = defaults['labels']  # labels for our major ticks
        self.label_font_size = defaults['label_font_size']  # font size of the axis labels
        self.label_offset_x = defaults['label_offset_x']  # how far away the axis labels are away from the end of the ticks, y axis.
        self.label_offset_y = defaults['label_offset_y']  # how far away the axis labels are away from the end of the ticks, x axis.

        self.title = defaults['title']
        self.title_font_size = defaults['title_font_size']
        self.title_offset = defaults['title_offset']
        self.title_font = defaults['title_font']

    def setattrs(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def draw_axis(self, main_figure, label_style, border_path, major_tick_path, tick_coords, title_coords, title_style, title_transform="rotate(0, 0, 0)"):
        subfigure = svgwrite.Drawing(size=(main_figure.dim[0],
                                           main_figure.dim[1]),
                                     style=label_style)
        # draw the axis line
        subfigure.add(subfigure.path(border_path,
                                     fill="none",
                                     stroke=rgb(*self.color),
                                     stroke_width=self.axis_linewidth, shape_rendering='crispEdges'))

        # draw the major ticks
        subfigure.add(subfigure.path(major_tick_path,
                                     fill="none",
                                     stroke=rgb(*self.color),
                                     stroke_width=self.major_tick_linewidth, shape_rendering='crispEdges'))
        # label the ticks
        for coord in tick_coords:
            subfigure.add(subfigure.text('%s' % coord[0],
                                         insert=(coord[1]+1, coord[2])),)
        # add the axis title
        subfigure.add(subfigure.text('%s' % self.title,
                                     insert=title_coords,
                                     style=title_style,
                                     transform=title_transform
                      ), )

        return subfigure


class YAxis(Axis):
    def __init__(self, data_name=None, link_to=None, kwargs={}):
        super().__init__(data_name, link_to)
        self.subtype = 'y'
        self.associated_drawable = ''
        self.side = 'left'

        self.setattrs(**kwargs)

    def get_y_res(self):
        return (self.dim - 1) / (self.lim[1] - self.lim[0])

    def draw(self, main_figure=None):
        # grab any linked plot values
        # if there is a linked_chart and the values are not defined,
        # grab its data, its position, its dimensions and its limits

        if self.link_to:
            linked_chart = main_figure.drawables[self.link_to]
            if not self.data_name:
                self.data_name = main_figure.drawables[self.link_to].data_name
            if not self.pos:
                self.pos = main_figure.drawables[self.link_to].pos

            if not self.lim:
                self.lim = main_figure.drawables[self.link_to].ylim

            if not self.dim:
                self.dim = main_figure.drawables[self.link_to].dim[1]

        data = main_figure.data[self.data_name][1]
        if not self.major_tick_values:
            major_tick_values = smart_ticks(data, self.lim)


        y_res = self.get_y_res()

        # start the svg path for the major tick
        major_tick_path = "M"
        tick_coords = []

        if self.side == 'left':
            label_style = "text-anchor:end;font-size:%spx;font-style:%s;alignment-baseline:middle" % (
            self.label_font_size, self.major_tick_font)

            border_path = "M %s %s L %s %s" % (
                    self.pos[0] - self.axis_offset - self.axis_linewidth/2,
                    self.pos[1],
                    self.pos[0] - self.axis_offset - self.axis_linewidth/2,
                    self.pos[1] + self.dim)

            for major_tick_value in major_tick_values:
                major_tick_path += " %s %s L %s %s M"%(
                    self.pos[0] - self.axis_offset,
                    self.pos[1] + self.dim - y_res * major_tick_value,
                    self.pos[0] - self.major_tick_length - self.axis_offset - self.axis_linewidth,
                    self.pos[1] + self.dim - y_res * major_tick_value)

                x = self.pos[0] - self.major_tick_length - self.label_offset_x - self.axis_offset - self.axis_linewidth
                y = self.pos[1] + self.dim - y_res * major_tick_value + self.label_offset_y

                tick_coords.append([major_tick_value, x, y])

            major_tick_path = major_tick_path[:-2]

            # add the axis title
            text_x = round(self.pos[0] - self.major_tick_length - self.axis_offset - self.label_offset_y - self.axis_linewidth - self.title_offset)
            text_y = round(self.pos[1] + (self.dim-1)/2)
            title_coords = (text_x, text_y)
            title_style = "text-anchor:middle;font-size:%spx;font-style:%s;alignment-baseline:baseline" % (self.title_font_size, self.title_font)
            title_transform = "rotate(-90, %s, %s)" % (text_x, text_y)


        if self.side == 'right':
            label_style = "text-anchor:start;font-size:%spx;font-style:%s;alignment-baseline:middle" % (
            self.label_font_size, self.major_tick_font)

            border_path = "M %s %s L %s %s" % (
                self.pos[0] + self.axis_offset + linked_chart.dim[0] + self.axis_linewidth/2,
                self.pos[1],
                self.pos[0] + self.axis_offset + linked_chart.dim[0] + self.axis_linewidth/2,
                self.pos[1] + self.dim)

            for major_tick_value in major_tick_values:
                major_tick_path += " %s %s L %s %s M"%(
                    self.pos[0] + self.axis_offset + linked_chart.dim[0],
                    self.pos[1] + self.dim - y_res * major_tick_value,
                    self.pos[0] + self.axis_offset + linked_chart.dim[0] + self.major_tick_length + self.axis_linewidth/2,
                    self.pos[1] + self.dim - y_res * major_tick_value)

                x = self.pos[0] + self.major_tick_length + self.label_offset_x + self.axis_offset + \
                    linked_chart.dim[0] + self.axis_linewidth
                y = self.pos[1] + self.dim - y_res * major_tick_value + self.label_offset_y
                tick_coords.append([major_tick_value, x, y])

            major_tick_path = major_tick_path[:-2]
            text_x = round(self.pos[0] + self.major_tick_length + self.axis_offset + self.label_offset_y + self.axis_linewidth + self.title_offset + linked_chart.dim[0] + self.title_font_size)
            text_y = round(self.pos[1] + (self.dim-1)/2)
            title_coords = (text_x, text_y)
            title_style = "text-anchor:middle;font-size:%spx;font-style:%s;alignment-baseline:baseline" % (self.title_font_size, self.title_font)
            title_transform = "rotate(-90, %s, %s)"%(text_x, text_y)

        kwargs = {
            'main_figure': main_figure,
            'label_style': label_style,
            'border_path': border_path,
            'major_tick_path': major_tick_path,
            'tick_coords': tick_coords,
            'title_coords': title_coords,
            'title_style': title_style,
            'title_transform': title_transform
        }
        return self.draw_axis(**kwargs)

    def set_defaults(self, data):
        pass


class XAxis(Axis):
    def __init__(self, data_name=None, link_to=None, kwargs={}):
        super().__init__(data_name, link_to)
        self.subtype = 'x'
        self.associated_drawable = ''
        self.side = 'bottom'
        self.setattrs(**kwargs)
    def get_x_res(self):
        return (self.dim - 1) / (self.lim[1] - self.lim[0])

    def draw(self, main_figure):
        # write a function to grabbed any linked plot values
        # if there is a linked_chart and the values are not defined,
        # grab its data, its position, its dimensions and its limits
        chart_height = 0
        if self.link_to:
            if not self.data_name:
                self.data_name = main_figure.drawables[self.link_to].data_name

            if not self.pos:
                self.pos = [main_figure.drawables[self.link_to].pos[0],
                            main_figure.drawables[self.link_to].pos[1] + main_figure.drawables[self.link_to].dim[1]
                            ]

            if not self.lim:
                self.lim = main_figure.drawables[self.link_to].xlim

            if not self.dim:
                self.dim = main_figure.drawables[self.link_to].dim[0]

            chart_height = main_figure.drawables[self.link_to].dim[1]

        # do some work to get where our ticks will be
        # tick_values - labels
        # tick_positions - x coordinates for the tick
        if main_figure.drawables[self.link_to].subtype == 'Scatter':
            data = main_figure.data[self.data_name][0]
            x_res = self.get_x_res()
            tick_values = smart_ticks(data, self.lim)
            tick_positions = [x_res * tick_value for tick_value in tick_values]

        elif main_figure.drawables[self.link_to].subtype == 'Bar':
            try:
                # see if we have data for a bar chart. If so, we'll grpah the Y values and use the X for labels
                data = main_figure.data[self.data_name][1]
                tick_values = main_figure.data[self.data_name][0]
            except:
                data = main_figure.data[self.data_name]
                tick_values = [i+1 for i in range(len(main_figure.data[self.data_name]))]
            widths = main_figure.drawables[self.link_to].get_widths(data)
            tick_positions = main_figure.drawables[self.link_to].get_x_coords(widths)
            tick_positions = [position-1 for position in tick_positions]




        major_tick_path = "M"
        tick_coords = []

        if self.side == 'top':
            label_style = "text-anchor:middle;font-size:%spx;font-style:%s;alignment-baseline:bottom" % (self.label_font_size, self.major_tick_font)
            border_path = "M %s %s L %s %s" % (self.pos[0],
                                               self.pos[1] - chart_height - self.axis_offset - self.axis_linewidth / 2,
                                               self.pos[0] + self.dim,
                                               self.pos[1] - chart_height - self.axis_offset - self.axis_linewidth / 2)
            # draw the ticks
            for tick_value, tick_position in zip(tick_values, tick_positions):
                # print(self.pos[0], tick_position, 1)
                major_tick_path += " %s %s L %s %s M"%(
                    round(self.pos[0] + tick_position + 1),
                    round(self.pos[1] - chart_height - self.axis_offset),
                    round(self.pos[0] + tick_position + 1),
                    round(self.pos[1] - chart_height - self.major_tick_length - self.axis_offset - self.axis_linewidth))
                x = round(self.pos[0] + tick_position + self.label_offset_x)
                y = round(self.pos[
                              1] - chart_height - self.major_tick_length - self.axis_offset - self.label_offset_y - self.axis_linewidth)  # + self.font_size/2.5
                tick_coords.append([tick_value, x, y])

            major_tick_path = major_tick_path[:-2]
            title_style = "text-anchor:middle;font-size:%spx;font-style:%s;alignment-baseline:baseline" % (self.title_font_size, self.title_font)
            title_coords = [
                round(self.pos[0] + (self.dim-1)/2),
                round(self.pos[1] - chart_height - self.major_tick_length - self.axis_offset - self.label_offset_y - self.axis_linewidth - self.title_offset - self.label_font_size)
            ]

        # draw the main axis. Might simply overlap with the figure border
        if self.side =='bottom':
            label_style = "text-anchor:middle;font-size:%spx;font-style:arial;alignment-baseline:top" % self.label_font_size

            border_path = "M %s %s L %s %s"%(self.pos[0],
                                             self.pos[1] + self.axis_offset + self.axis_linewidth/2,
                                             self.pos[0] + self.dim,
                                             self.pos[1] + self.axis_offset + self.axis_linewidth/2)
            # draw the ticks
            for tick_value, tick_position in zip(tick_values, tick_positions):
                major_tick_path += " %s %s L %s %s M"%(
                    self.pos[0] + tick_position + 1,
                    self.pos[1] + self.axis_offset,# + self.axis_linewidth/2,
                    self.pos[0] + tick_position + 1,
                    self.pos[1] + self.major_tick_length + self.axis_offset + self.axis_linewidth)
                x = self.pos[0] + tick_position + self.label_offset_x
                y = self.pos[1] + self.major_tick_length + self.axis_offset + self.label_offset_y + self.axis_linewidth
                tick_coords.append([tick_value, x, y])

            major_tick_path = major_tick_path[:-2]
            title_coords = [
                round(self.pos[0] + (self.dim - 1) / 2),
                round(self.pos[
                          1] + self.major_tick_length + self.axis_offset + self.label_offset_y + self.axis_linewidth + self.title_offset + self.label_font_size + self.title_font_size)
            ]
            title_style = "text-anchor:middle;font-size:%spx;font-style:%s;alignment-baseline:baseline" % (
                                         self.title_font_size, self.title_font)

        # now do the drawing
        # make the subfigure

        kwargs = {
            'main_figure': main_figure,
            'label_style': label_style,
            'border_path': border_path,
            'major_tick_path': major_tick_path,
            'tick_coords': tick_coords,
            'title_coords': title_coords,
            'title_style': title_style
        }
        return self.draw_axis(**kwargs)


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
            self.drawables[drawable_name] = Scatter(data_name, kwargs)

        elif drawable_type == "YAxis":
            self.drawables[drawable_name] = YAxis(data_name, link_to, kwargs)

        elif drawable_type == "XAxis":
            self.drawables[drawable_name] = XAxis(data_name, link_to, kwargs)
        elif drawable_type == 'XHist':
            print("XHist not implemented yet.")

        elif drawable_type == 'YHist':
            print("YHist not implemented yet.")

        elif drawable_type == 'Bar':
            self.drawables[drawable_name] = Bar(data_name, kwargs)

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




