import svgwrite
from svgwrite import rgb
from .helpers import smart_ticks, smart_limits
from itertools import cycle


class Axis:
    defaults = {
        'dim': 0,
        'pos': [],  # [x, y] svg pixel coordinates of bottom left of chart
        'lim': None,  # [min, max] limits of our axis
        'color': (0, 0, 0),  # color of our axis line

        'axis_offset': -1,
        'axis_linewidth': 1,

        'major_tick_values': None,
        'major_tick_linewidth': 1,
        'major_tick_length': 5,
        'major_tick_color': (0, 0, 0),
        'major_tick_labels': None,
        'major_tick_font': 'arial',

        'minor_tick_linewidth': 1,
        'minor_tick_color': (0, 0, 0),

        'labels': [],  # labels for our major ticks
        'label_font_size': 10,  # font size of the axis labels
        'label_offset_x': 0,  # how far away the axis labels are away from the end of the ticks, y axis.
        'label_offset_y': 0,  # how far away the axis labels are away from the end of the ticks, x axis.

        'title': None,
        'title_font_size': 12,
        'title_offset': 0,
        'title_font': 'arial'
    }

    def __init__(self, name, link_to):
        defaults = self.defaults
        self.name = name
        self.type = 'Axis'
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
        self.major_tick_labels = defaults['major_tick_labels']
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
        if self.major_tick_labels:
            tick_labels = [tick_label for (tick_coord, tick_label) in zip(tick_coords, cycle(self.major_tick_labels))]
        else:
            tick_labels = [tick_coord[0] for tick_coord in tick_coords]

        for coord, label in zip(tick_coords, tick_labels):
            subfigure.add(subfigure.text('%s' % label,
                                         insert=(coord[1]+1, coord[2])),)
        # add the axis title

        subfigure.add(subfigure.text('%s' % self.title,
                                     insert=title_coords,
                                     style=title_style,
                                     transform=title_transform
                      ), )

        return subfigure


class YAxis(Axis):
    def __init__(self, name=None, link_to=None, kwargs={}):
        super().__init__(name, link_to)
        self.subtype = 'y'
        self.associated_drawable = ''
        self.side = 'left'
        self.setattrs(**kwargs)

    def get_y_res(self, data, main_figure):
        if self.lim is None:
            return main_figure.drawables[self.link_to].get_y_res(data)

        return (self.dim-1) / (self.lim[1] - self.lim[0])

    def draw(self, main_figure=None):
        # grab any linked plot values
        # if there is a linked_chart and the values are not defined,
        # grab its data, its position, its dimensions and its limits
        lim = None
        if self.link_to:
            linked_chart = main_figure.drawables[self.link_to]
            if not self.pos:
                self.pos = main_figure.drawables[self.link_to].pos
            if self.lim is None:
                lim = main_figure.drawables[self.link_to].ylim
            else:
                lim = self.lim
            if not self.dim:
                self.dim = main_figure.drawables[self.link_to].dim[1]

        # find min and max of main figure data. These could be in multiple datasets
        print(self.link_to)
        data = linked_chart.get_y_range(main_figure)

        # data_min = min([min(main_figure.data[key][1]) for key in main_figure.drawables[self.link_to].data_name])
        # data_max = max([max(main_figure.data[key][1]) for key in main_figure.drawables[self.link_to].data_name])
        # data = [data_min, data_max]

        if lim is None:
            lim = smart_limits(data)
        if not self.major_tick_values:
            major_tick_values = smart_ticks(data, lim)

        # this may defer to the linked chart, so we need to pass main_figure
        y_res = self.get_y_res(data, main_figure)

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
                    round(self.pos[0] - self.axis_offset),
                    round(self.pos[1] + self.dim - y_res * (major_tick_value - lim[0])),
                    round(self.pos[0] - self.major_tick_length - self.axis_offset - self.axis_linewidth),
                    round(self.pos[1] + self.dim - y_res * (major_tick_value - lim[0])))

                x = self.pos[0] - self.major_tick_length - self.label_offset_x - self.axis_offset - self.axis_linewidth
                y = self.pos[1] + self.dim - y_res * (major_tick_value - lim[0]) + self.label_offset_y

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
                major_tick_path += " %s %s L %s %s M" % (
                    round(self.pos[0] + self.axis_offset + linked_chart.dim[0]),
                    round(self.pos[1] + self.dim - y_res * (major_tick_value - lim[0])),
                    round(self.pos[0] + self.axis_offset + linked_chart.dim[0] + self.major_tick_length + self.axis_linewidth/2),
                    round(self.pos[1] + self.dim - y_res * (major_tick_value - lim[0]))
                )

                x = self.pos[0] + self.major_tick_length + self.label_offset_x + self.axis_offset + \
                    linked_chart.dim[0] + self.axis_linewidth
                y = self.pos[1] + self.dim - y_res * (major_tick_value - lim[0]) + self.label_offset_y
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

    def get_tick_positions(self, main_figure):
        data_min = min([min(main_figure.data[key][1]) for key in main_figure.drawables[self.link_to].data_name])
        data_max = max([max(main_figure.data[key][1]) for key in main_figure.drawables[self.link_to].data_name])
        data = [data_min, data_max]
        # if self.lim is not defined, pull the limits from the main figure
        # if it's also None, then the smart_ticks will just do its thing
        if self.lim is None:
            lim = main_figure.drawables[self.link_to].ylim
        else:
            lim = self.lim
        if lim is None:
            lim = smart_limits(data)

        if self.major_tick_values is None:
            major_tick_values = smart_ticks(data, lim)
        else:
            major_tick_values = self.major_tick_values

        y_res = self.get_y_res(data, main_figure)
        return [(major_tick_value - lim[0]) * y_res for major_tick_value in major_tick_values]


class XAxis(Axis):
    def __init__(self, name=None, link_to=None, kwargs={}):
        super().__init__(name, link_to)
        self.subtype = 'x'
        self.associated_drawable = ''
        self.side = 'bottom'
        self.setattrs(**kwargs)


    def get_x_res(self, data, main_figure):
        # if the axis limits or dimensions were never specified, pull from its linked chart
        if self.lim is None:
            return main_figure.drawables[self.link_to].get_x_res(data)
        return (self.dim-1) / (self.lim[1] - self.lim[0])


    def draw(self, main_figure):
        # write a function to grabbed any linked plot values
        # if there is a linked_chart and the values are not defined,
        # grab its data, its position, its dimensions and its limits
        chart_height = 0
        lim = None
        if self.link_to:
            if not self.pos:
                self.pos = [main_figure.drawables[self.link_to].pos[0],
                            main_figure.drawables[self.link_to].pos[1] + main_figure.drawables[self.link_to].dim[1]
                            ]
            if self.lim is None:
                lim = main_figure.drawables[self.link_to].xlim
            else:
                lim = self.lim

            if not self.dim:
                self.dim = main_figure.drawables[self.link_to].dim[0]

            chart_height = main_figure.drawables[self.link_to].dim[1]

        # do some work to get where our ticks will be
        # tick_values - labels
        # tick_positions - x coordinates for the tick
        if main_figure.drawables[self.link_to].subtype == 'Scatter':
            # find min and max of main figure data. These could be in multiple datasets
            data_min = min([min(main_figure.data[key][0]) for key in main_figure.drawables[self.link_to].data_name])
            data_max = max([max(main_figure.data[key][0]) for key in main_figure.drawables[self.link_to].data_name])
            data = [data_min, data_max]

            if lim is None:
                lim = smart_limits(data)

            if not self.major_tick_values:
                tick_values = smart_ticks(data, lim)
            else:
                tick_values = self.major_tick_values

            x_res = self.get_x_res(data, main_figure)
            tick_positions = [x_res * (tick_value-lim[0]) for tick_value in tick_values]

        elif main_figure.drawables[self.link_to].subtype == 'Bar':
            try:
                # see if we have data for a bar chart. If so, we'll grpah the Y values and use the X for labels
                data = main_figure.data[self.data_name[0]][1]
                tick_values = main_figure.data[self.data_name[0]][0]
            except:
                data = main_figure.data[self.data_name[0]]
                tick_values = [i+1 for i in range(len(main_figure.data[self.data_name[0]]))]
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
                    round(self.pos[0] + tick_position) + 1,
                    round(self.pos[1] + self.axis_offset),
                    round(self.pos[0] + tick_position) + 1,
                    round(self.pos[1] + self.major_tick_length + self.axis_offset + self.axis_linewidth)
                )
                x = round(self.pos[0] + tick_position + self.label_offset_x)
                y = round(self.pos[1] + self.major_tick_length + self.axis_offset + self.label_offset_y + self.axis_linewidth)
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


    def get_tick_positions(self, main_figure):
        data_min = min([min(main_figure.data[key][0]) for key in main_figure.drawables[self.link_to].data_name])
        data_max = max([max(main_figure.data[key][0]) for key in main_figure.drawables[self.link_to].data_name])
        data = [data_min, data_max]
        # if self.lim is not defined, pull the limits from the main figure
        # if it's also None, then the smart_ticks will just do its thing
        if self.lim is None:
            lim = main_figure.drawables[self.link_to].xlim
        else:
            lim = self.lim
        if lim is None:
            lim = smart_limits(data)

        if self.major_tick_values is None:
            major_tick_values = smart_ticks(data, lim)
        else:
            major_tick_values = self.major_tick_values
        x_res = self.get_x_res(data, main_figure)
        return [(major_tick_value-lim[0]) * x_res for major_tick_value in major_tick_values]


class YHist(Axis):
    def __init__(self, name=None, link_to=None, kwargs={}):
        super().__init__(name, link_to)
        self.num_bins = 10
        self.side = 'right'
        self.subtype = 'YHist'
        self.inside_border_width = 1
        self.inside_border_color = (0, 0, 0)
        self.offset = 0
        self.dim = [None, None]
        self.setattrs(**kwargs)

    def draw(self, main_figure):
        # calculate the bins
        # get all linked Y values in a flattened list
        linked_chart = main_figure.drawables[self.link_to]

        dim = [0, 0]
        if self.dim[0] is None:
            dim[0] = 50
        if self.dim[1] is None:
            dim[1] = linked_chart.dim[1]


        all = []
        for data_name in linked_chart.data_name:
            for datapoint in main_figure.data[data_name][1]:
                all.append(datapoint)

        # get the chart limits in order to bin the points
        if linked_chart.ylim is None:
            data = linked_chart.get_y_range(main_figure)
            ylim = smart_limits(data)
        else:
            ylim = linked_chart.ylim

        # start the binning process
        bin_size = (ylim[1]-ylim[0])/self.num_bins
        bin_amount = []
        for i in range(self.num_bins):
            bin_amount.append(len([j for j in all if (ylim[0] + i*bin_size) <= j < (ylim[0] + (i+1)*bin_size)]))
        subfigure = svgwrite.Drawing(size=(main_figure.dim[0],
                                           main_figure.dim[1]),
                                     )
        top_left = linked_chart.pos
        top_left[0] = top_left[0] + linked_chart.dim[0] + self.offset
        top_left[1] = top_left[1]+1

        # draw the outline
        if self.inside_border_width:
            subfigure.add(
                subfigure.rect(
                    shape_rendering='crispEdges',
                    insert=top_left,
                    size=(dim[0], dim[1] - 1),
                    stroke=rgb(*self.inside_border_color),
                    stroke_width=self.inside_border_width,
                    fill='none'
                )
            )
        bar_max = max(bin_amount)
        for i, bar_length in enumerate(bin_amount[::-1]):
            bar_top = top_left[1] + i*((dim[1]-1)/self.num_bins)
            bar_pixel_length = (bar_length / bar_max) * dim[0]
            subfigure.add(subfigure.rect(
                shape_rendering='crispEdges',
                insert=(top_left[0], bar_top),
                size=(bar_pixel_length, (dim[1]-1)/self.num_bins),
                stroke=rgb(0, 0, 0),
                stroke_width=1,
                fill=rgb(50, 50, 255)

            ))


        # draw the axis line
        """
        subfigure.add(subfigure.path(border_path,
                                     fill="none",
                                     stroke=rgb(*self.color),
                                     stroke_width=self.axis_linewidth, shape_rendering='crispEdges'))

        # draw the major ticks
        subfigure.add(subfigure.path(major_tick_path,
                                     fill="none",
                                     stroke=rgb(*self.color),
                                     stroke_width=self.major_tick_linewidth, shape_rendering='crispEdges'))

        """
        return subfigure









