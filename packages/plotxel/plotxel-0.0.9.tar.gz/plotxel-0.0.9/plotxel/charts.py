import svgwrite
from svgwrite import rgb
from .helpers import smart_limits, smart_ticks
from itertools import cycle

class Chart:

    series_attributes = {'line_width',
                         'line_color',
                         'marker_shape',
                         'marker_size',
                         'marker_fill_color',
                         'marker_border_color',
                         'marker_border_width',
                         'line_style',
                         'marker_opacity'}

    defaults = {
        'dim': (300, 150),
        'xlim': None,
        'ylim': None,

        'pos': (0, 0),
        'inside_border_width': 1,
        'inside_border': ([1], [1], [1], [1]),
        'inside_border_color': 'black',
        'title': 'Title',
        'title_offset': 10,
        'title_font': 'arial',
        'title_font_size': 20,

        'x_major_ticks': None,
        'y_major_ticks': None,

        'vertical_gridlines': False,
        'vertical_gridline_width': 1,
        'vertical_gridline_color': (175, 175, 175),
        'vertical_gridline_style': None,

        'horizontal_gridlines': False,
        'horizontal_gridline_width': 1,
        'horizontal_gridline_color': (175, 175, 175),
        'horizontal_gridline_style': None,

        # series attributes -- must be lists
        # these items are lists since they there may be multiple datasets
        'marker_shape': ['circle', 'square', 'rect'],
        'marker_size': [10],
        'marker_fill_color': [(50, 50, 200), (200, 50, 50), (50, 200, 50)],  # color of the markers
        'marker_opacity': [1],
        'marker_border_color': [(0, 0, 0)],  # color of the marker border
        'marker_border_width': [1],  # thickness of the marker border. 0 means no border

        'line_width': [1],
        'line_color': [(50, 50, 200), (200, 50, 50), (50, 200, 50)],
        'line_style': [None]

    }

    def __init__(self, name, data_name):

        defaults = self.defaults
        self.name = name
        self.type = 'Chart'
        if type(data_name) == str:
            data_name = [data_name]
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
        self.marker_fill_color = defaults['marker_fill_color'] # color of the markers
        self.marker_border_color = defaults['marker_border_color']  # color of the marker border
        self.marker_border_width = defaults['marker_border_width']  # thickness of the marker border. 0 means no border
        self.marker_opacity = defaults['marker_opacity']

        # line connector properties
        self.line_width = defaults['line_width']
        self.line_color = defaults['line_color']

        # ticks, mostly for gridlines
        self.x_major_ticks = defaults['x_major_ticks']
        self.y_major_ticks = defaults['y_major_ticks']

        # gridline stuff
        self.vertical_gridlines = defaults['vertical_gridlines']
        self.vertical_gridline_width = defaults['vertical_gridline_width']
        self.vertical_gridline_color = defaults['vertical_gridline_color']
        self.vertical_gridline_style = defaults['vertical_gridline_style']

        self.horizontal_gridlines = defaults['horizontal_gridlines']
        self.horizontal_gridline_width = defaults['horizontal_gridline_width']
        self.horizontal_gridline_color = defaults['horizontal_gridline_color']
        self.horizontal_gridline_style = defaults['horizontal_gridline_style']


    def get_x_res(self, data=None):
        if self.xlim is None:
            xlim = smart_limits(data)
        else:
            xlim = self.xlim
        return (self.dim[0]-1) / (xlim[1] - xlim[0])


    def get_y_res(self, data=None):
        if self.ylim is None:
            ylim = smart_limits(data)

        else:
            ylim = self.ylim
        return (self.dim[1]-1) / (ylim[1] - ylim[0])


    def setattrs(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.series_attributes:
                if type(v) is not list:
                    setattr(self, k, [v])
                else:
                    setattr(self, k, v)
            else:
                setattr(self, k, v)


    def draw_border(self):
        if self.inside_border is not None and (type(self.inside_border) == tuple):
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


    def draw_vertical_gridlines(self, main_figure):

        # Draw a gridline
        #
        # first, are major ticks defined for the chart?
        # if they are
        #  draw the grid line accordingly
        # else
        #  find any linked axes
        #  If any have have major ticks defined
        #    use those
        #  else
        #    Everything is using smart ticks

        major_ticks = None
        xlim = None
        data = self.get_x_range(main_figure)
        if self.xlim is not None:
            xlim = self.xlim
        if xlim is None:
            xlim = smart_limits(data)

        res = self.get_x_res(data)
        if self.x_major_ticks is not None:
            major_ticks = [(tick-xlim[0])*res for tick in self.x_major_ticks]
        else:
            for drawable in main_figure.drawables:
                if main_figure.drawables[drawable].subtype == 'x':
                    if main_figure.drawables[drawable].link_to == self.name:
                        major_ticks = main_figure.drawables[drawable].get_tick_positions(main_figure)
                        break
            else:
                major_ticks = smart_ticks(data, xlim)
                major_ticks = [(tick-xlim[0])*res for tick in major_ticks]


        path = 'M'
        for major_tick_value in major_ticks:
            path += " %s %s L %s %s M" % (
                round(major_tick_value) + 1,
                0,
                round(major_tick_value) + 1,
                self.dim[1])
        path = path[:-2]

        return svgwrite.path.Path(
            path,
            fill="none",
            stroke=rgb(*self.vertical_gridline_color),
            stroke_width=self.vertical_gridline_width,
            shape_rendering='crispEdges'
        )


    def draw_horizontal_gridlines(self, main_figure):

        # Draw a gridline
        #
        # first, are major ticks defined for the chart?
        # if they are
        #  draw the grid line accordingly
        # else
        #  find any linked axes
        #  If any have have major ticks defined
        #    use those
        #  else
        #    Everything is using smart ticks

        major_ticks = None

        data = self.get_y_range(main_figure)
        ylim = None
        if self.ylim is not None:
            ylim = self.ylim
        if ylim is None:
            ylim = smart_limits(data)

        res = self.get_y_res(data)


        if self.y_major_ticks is not None:
            major_ticks = [(tick-ylim[0])*res for tick in self.y_major_ticks]

        else:
            for drawable in main_figure.drawables:
                if main_figure.drawables[drawable].subtype == 'y':
                    if main_figure.drawables[drawable].link_to == self.name:
                        major_ticks = main_figure.drawables[drawable].get_tick_positions(main_figure)
                        break
            else:
                major_ticks = smart_ticks(data)
                major_ticks = [(tick-ylim[0])*res for tick in major_ticks]

        path = 'M'
        for major_tick_value in major_ticks:
            path += " %s %s L %s %s M" % (
                0,
                round(self.dim[1] - major_tick_value),
                self.dim[0],
                round(self.dim[1] - major_tick_value)
            )
        path = path[:-2]

        return svgwrite.path.Path(
            path,
            fill="none",
            stroke=rgb(*self.horizontal_gridline_color),
            stroke_width=self.horizontal_gridline_width,
            shape_rendering='crispEdges'
        )


    def get_x_range(self, main_figure):
        data_min = min([min(main_figure.data[key][0]) for key in self.data_name])
        data_max = max([max(main_figure.data[key][0]) for key in self.data_name])
        return [data_min, data_max]


    def get_y_range(self, main_figure):
        data_min = min([min(main_figure.data[key][1]) for key in self.data_name])
        data_max = max([max(main_figure.data[key][1]) for key in self.data_name])
        return [data_min, data_max]


class Scatter(Chart):
    def __init__(self, name, data_name, kwargs={}):
        super().__init__(name, data_name)
        self.subtype = 'Scatter'
        self.setattrs(**kwargs)


    def SetDefaults(self, data):
        pass


    def draw(self, main_figure):
        """
        All this function does is draw the actual points. Borders, axes, gridlines, are drawn in the Chart base class
        :param main_figure:
        :return:
        """

        # find the min and max of all the datasets. There is a way better way to do this I'm sure
        x_range = self.get_x_range(main_figure)
        y_range = self.get_y_range(main_figure)
        #min_x = min([min(main_figure.data[key][0]) for key in self.data_name])
        #min_y = min([min(main_figure.data[key][1]) for key in self.data_name])

        #max_x = max([max(main_figure.data[key][0]) for key in self.data_name])
        #max_y = max([max(main_figure.data[key][1]) for key in self.data_name])

        # establish our limits
        if not self.xlim:
            xlim = smart_limits(x_range)
        else:
            xlim = self.xlim
        if not self.ylim:
            ylim = smart_limits(y_range)
        else:
            ylim = self.ylim

        # make a figure the size of the main figure
        # we may need to draw outside of the actual chart area and into the main figure (for borders and such)
        # we also need to extract data series and other things
        subfigure = svgwrite.Drawing(size=(main_figure.dim[0], main_figure.dim[1]))

        # determine how many pixels/value in our chart
        x_res = self.get_x_res(x_range)
        y_res = self.get_y_res(y_range)

        # establish our chart drawing area, such that the points are truncated if they fall outside the range
        # our chart points and circles will be added in here
        chart_area = svgwrite.Drawing(
            size=(self.dim[0], self.dim[1]),
            x=self.pos[0], y=self.pos[1])

        # draw the gridlines from the parent Chart class
        chart_area.add(self.draw_vertical_gridlines(main_figure))
        chart_area.add(self.draw_horizontal_gridlines(main_figure))

        # each circle's position is calculated based on the chart size and it's data values
        # the points are plotted relative to our chart_area, which is then affixed to the main figure
        # x is plotted left to right. We calculate it by determining X's value relative to the chart minimum, then
        # multiplying it by the resolution to get it in pixels
        # y is plotted top to bottom, so same thing except we subtract the calculated value by the figure size
        # to get its proper position
        # future support: square, asterisk, dash, plus, custom svg

        for data_name, line_color, line_width, marker_size, marker_shape, marker_fill_color, marker_border_color, marker_border_width, marker_opacity  in zip(
            self.data_name,
            cycle(self.line_color),
            cycle(self.line_width),
            cycle(self.marker_size),
            cycle(self.marker_shape),
            cycle(self.marker_fill_color),
            cycle(self.marker_border_color),
            cycle(self.marker_border_width),
            cycle(self.marker_opacity)
            ):

            x_data = main_figure.data[data_name][0]
            y_data = main_figure.data[data_name][1]

            data_coordinates = []
            for x, y in zip(x_data, y_data):
                # add coordinates
                data_coordinates.append(
                    (
                        round((x - xlim[0]) * x_res + 1),
                        round((ylim[1] - y)/(ylim[1]-ylim[0]) * self.dim[1])
                    )
                )

            # draw a line, if present
            if line_width > 0:
                line_path = "M "
                for center in data_coordinates:
                    line_path +="%s %s L "%(center[0], center[1])
                line_path = line_path[:-2]
                chart_area.add(
                    chart_area.path(line_path,
                                    shape_rendering='geometricPrecision',
                                    fill="none",
                                    stroke=rgb(*line_color),
                                    stroke_width=line_width))

            # draw our makers
            if marker_size > 0:
                for center in data_coordinates:
                    if marker_shape == 'circle':
                        chart_area.add(
                            chart_area.circle(
                                center=(center),
                                r=marker_size/2,
                                fill=rgb(*marker_fill_color),
                                stroke=rgb(*marker_border_color),
                                stroke_width=marker_border_width,
                                opacity=marker_opacity
                            )
                        )
                    elif marker_shape == 'square':
                        chart_area.add(
                            chart_area.rect(
                                insert=(center[0] - marker_size/2, center[1] - marker_size/2),
                                size=(marker_size, marker_size),
                                fill=rgb(*marker_fill_color),
                                stroke=rgb(*marker_border_color),
                                stroke_width=marker_border_width,
                                opacity=marker_opacity
                            )
                        )

                    elif marker_shape == 'rectangle' or marker_shape == 'rect':
                        chart_area.add(
                            chart_area.rect(
                                insert=(center[0] - marker_size/2, center[1] - marker_size/4),
                                size=(marker_size, marker_size/2),
                                fill=rgb(*marker_fill_color),
                                stroke=rgb(*marker_border_color),
                                stroke_width=marker_border_width,
                                opacity=marker_opacity
                            )
                        )
                    elif marker_shape == '-' or marker_shape == 'dash':
                        pass
                    elif marker_shape == '*' or marker_shape == 'star':
                        pass

        # inside of our chart area we will add a border.
        if self.inside_border is not None and (type(self.inside_border) == tuple):
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

    def __init__(self, name, data_name, kwargs={}):
        super().__init__(name, data_name)
        self.subtype = 'Bar'
        self.style = 'grouped'
        self.group_spacing = 5
        self.bar_spacing = 3
        self.margins = [5, 5]
        self.bar_line_width = [2]
        self.bar_fill_color = [(50, 50, 250), (250, 50, 50), (50, 250, 50)]
        self.bar_line_color = [(0, 0, 0)]
        self.ylim = None
        self.setattrs(**kwargs)

    def draw(self, main_figure):
        # for a bar chart, pull the Y data
        data = [main_figure.data[data_name][1] for data_name in self.data_name]

        subfigure = svgwrite.Drawing(size=(main_figure.dim[0], main_figure.dim[1]))
        chart_area = svgwrite.Drawing(
            size=(self.dim[0], self.dim[1]),
            x=self.pos[0], y=self.pos[1])

        # calculate group widths. ensuring fidelity with respect to margin and bar spacing
        group_widths = self.get_group_widths(data)

        # returns a nested list of grouped bars
        bar_widths = self.get_bar_widths(data, group_widths)
        # returns the leftmost position of each bar in a nested format
        group_x_coords = self.get_x_coords(group_widths, bar_widths)

        # get the top-middle coordinate of each group. We'll use this for our rectangles
        bar_y_coords = []
        heights = []
        for group_data in data:
            temp_bar_y_coords = []
            temp_heights = []
            for i, y in enumerate(group_data):
                # add coordinates
                temp_bar_y_coords.append(self.dim[1] - (y - self.ylim[0]) * self.get_y_res())
                temp_heights.append((y - self.ylim[0]) * self.get_y_res())
            bar_y_coords.append(temp_bar_y_coords)
            heights.append(temp_heights)
        # get the left x value for our rectangles


        bar_y_coords =[list(x) for x in zip(*bar_y_coords)]
        heights = [list(x) for x in zip(*heights)]
        # now the exciting part -- let's draw some rectangles!!
        for x_coords, y_coords, widths, heights in zip(group_x_coords, bar_y_coords, bar_widths, heights):
            for x_coord, y_coord, width, height, bar_fill_color, bar_line_color, bar_line_width in zip(x_coords, y_coords, widths, heights, cycle(self.bar_fill_color), cycle(self.bar_line_color), cycle(self.bar_line_width)):
                chart_area.add(
                    chart_area.rect(
                        shape_rendering='crispEdges',
                        insert=(x_coord, y_coord),
                        size=(width, height),
                        fill=rgb(*bar_fill_color),
                        stroke=rgb(*bar_line_color),
                        stroke_width=bar_line_width,
                    )
                )

        chart_area.add(self.draw_border())
        subfigure.add(self.draw_title())
        subfigure.add(chart_area)

        return subfigure


    def get_x_coords(self, group_widths,  bar_widths):
        bar_x_coords = []
        # first calculate relatve group positionings
        for group in bar_widths:
            temp = [0]
            for individual in group[:-1]:
                temp.append(temp[-1] + individual + self.bar_spacing)
            bar_x_coords.append(temp)

        # next, calcualte our relative group coordinates
        group_x_coords = [self.margins[0]]
        for group_width in group_widths[:-1]:
            group_x_coords.append(group_x_coords[-1] + group_width + self.group_spacing)

        # now add them together for the left x coordinate of each bar
        temp = []
        for group_x_coord, bar_x_coord in zip(group_x_coords, bar_x_coords):
            temp.append([coord + group_x_coord for coord in bar_x_coord])
        bar_x_coords = temp
        return bar_x_coords


    def get_group_widths(self, data):
        num_groups = len(data[0])
        widths = [(self.dim[0] - sum(self.margins) - self.group_spacing*(num_groups-1))//num_groups]*num_groups
        remainder = (self.dim[0] - sum(self.margins) - self.group_spacing*(num_groups-1))%num_groups

        for i, width in zip(range(remainder), widths):
            widths[i] += 1

        return widths


    def get_bar_widths(self, data, group_widths):
        group_size = len(data)
        bar_widths = []
        # for each group, calculate the individual widths
        for group_width in group_widths:
            widths = [(group_width - self.bar_spacing*(group_size-1)) // group_size]*group_size
            remainder = (group_width - self.bar_spacing*(group_size-1)) % group_size
            for i, width in zip(range(remainder), widths):
                widths[i] += 1
            bar_widths.append(widths)
        return bar_widths






