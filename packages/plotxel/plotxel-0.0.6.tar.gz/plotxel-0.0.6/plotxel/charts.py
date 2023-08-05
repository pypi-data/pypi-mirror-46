import svgwrite
from svgwrite import rgb
from .helpers import smart_limits

class Chart:
    defaults = {
        'dim': (300, 150),
        'xlim': None,
        'ylim': None,
        'marker_shape': 'circle',
        'marker_size': 10,
        'pos': (0, 0),
        'inside_border_width': 1,
        'inside_border': [[1], [1], [1], [1]],
        'inside_border_color': 'black',
        'title': 'Title',
        'title_offset': 10,
        'title_font': 'arial',
        'title_font_size': 20,

        'line_width': 1,
        'line_color': (0, 0, 0),
        'line_style': None,

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
    }

    def __init__(self, data_name, name):

        defaults = self.defaults
        self.name = name
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
        print(xlim)
        return (self.dim[0]-1) / (xlim[1] - xlim[0])


    def get_y_res(self, data=None):
        if self.ylim is None:
            ylim = smart_limits(data)

        else:
            ylim = self.ylim

        return (self.dim[1]-1) / (ylim[1] - ylim[0])


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

        data = main_figure.data[self.data_name]
        major_ticks = None

        if self.x_major_ticks is not None:
            major_ticks = self.x_major_ticks
        else:
            for drawable in main_figure.drawables:
                if main_figure.drawables[drawable].subtype == 'x':
                    if main_figure.drawables[drawable].link_to == self.name:
                        major_ticks = main_figure.drawables[drawable].get_tick_positions(main_figure)
                        break

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

        data = main_figure.data[self.data_name]
        major_ticks = None

        if self.y_major_ticks is not None:
            major_ticks = self.y_major_ticks
        else:
            for drawable in main_figure.drawables:
                if main_figure.drawables[drawable].subtype == 'y':
                    if main_figure.drawables[drawable].link_to == self.name:
                        major_ticks = main_figure.drawables[drawable].get_tick_positions(main_figure)
                        break

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


class Scatter(Chart):
    def __init__(self, data_name, name, kwargs={}):
        super().__init__(data_name, name)
        self.subtype = 'Scatter'
        self.setattrs(**kwargs)


    def SetDefaults(self, data):
        pass


    def draw(self, main_figure):

        x_data = main_figure.data[self.data_name][0]
        y_data = main_figure.data[self.data_name][1]

        if not self.xlim:
            xlim = smart_limits(x_data)

        if not self.ylim:
            ylim = smart_limits(y_data)

        # make a figure the size of the main figure
        # we may need to draw outside of the actual chart area and into the main figure (for borders and such)
        # we also need to extract data series and other things
        subfigure = svgwrite.Drawing(size=(main_figure.dim[0], main_figure.dim[1]))

        # determine how many pixels/value in our chart
        x_res = self.get_x_res(x_data)
        y_res = self.get_y_res(y_data)


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


        data_coordinates = []
        for x, y in zip(x_data, y_data):
            # add coordinates
            data_coordinates.append(
                (
                    round((x - xlim[0]) * x_res + 1),
                    round(self.dim[1] - (y - ylim[0]) * y_res)
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

    def __init__(self, data_name, name, kwargs={}):
        super().__init__(data_name, name)
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