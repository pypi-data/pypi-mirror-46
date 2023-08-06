#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A module that defines some widgets for GUI based selection/interaction
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from itertools import cycle
import numpy as np


class DraggableArtist:
    """Base class for a draggable artist"""
    lock = None

    def __init__(self, ax, coords):
        """Initialise a draggableartist instance given x and y coordinate
        Parameters
        ----------
        ax: axes to be drawn on

        coord: coorindates

        size: size of the artist
        """

        self.ax = ax
        self.figure = self.ax.figure
        self.canvas = self.figure.canvas
        self.coords = np.asarray(coords, dtype=float)
        self.background = None

    def _init_artist(self, *args, **kwargs):
        """Initialise the artist"""
        raise NotImplementedError

    def connect(self):

        self.cidpress = self.artist.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.artist.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.artist.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def _basic_check(self, event):
        if event.inaxes != self.artist.axes:
            return False
        else:
            return True

    def _lock(self):
        DraggableArtist.lock = self

    def _unlock(self):
        DraggableArtist.lock = None

    def _on_press_draw(self):
        """Drawing after on_press event. Turns on bliting"""
        # Drawing
        canvas = self.artist.figure.canvas
        axes = self.artist.axes
        self.artist.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.artist.axes.bbox)

        # Redraw just the rectangle
        axes.draw_artist(self.artist)

        # and bilt just the redrawn area
        canvas.blit(axes.bbox)

    def on_press(self, event):

        raise NotImplementedError

    def _on_motion_draw(self):

        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.artist)
        self.canvas.blit(self.ax.bbox)

    def on_motion(self, event):

        raise NotImplementedError

    def _on_release_draw(self):

        self.artist.set_animated(False)
        self.background = None
        # redraw the full figure
        self.artist.figure.canvas.draw()

    def on_release(self, event):

        if self._basic_check(event) is False:
            return
        self._unlock()
        self.save_coords()
        self._on_release_draw()

    def save_coords(self):
        """Save coordinates from the artist"""
        raise NotImplementedError

    def disconnect(self):
        'disconnect all the stored connection ids'

        self.artist.figure.canvas.mpl_disconnect(self.cidpress)
        self.artist.figure.canvas.mpl_disconnect(self.cidrelease)
        self.artist.figure.canvas.mpl_disconnect(self.cidmotion)

    def remove(self):

        self.artist.remove()

    def set_coords(self, coor):
        self.coor = coor
        self.artist.center = coor.tolist()

    def redraw(self):

        self.artist.figure.canvas.draw()

    def __repr__(self):
        string = "DraggableArtist(coords={})".format(self.coords)
        return string

    def __del__(self):
        self.disconnect()
        self.remove()

    def set_size(self, size):
        self.artist.set_radius(size)

    @property
    def size(self):
        return self.artist.get_radius()


class DraggablePoint(DraggableArtist):
    """Class for a draggable point"""

    def __init__(self, ax, coord, size=0.1, color='r'):
        """Initialise a draggablepoint instance given x and y coordinate
        Parameters
        ----------
        ax: axes to be drawn on

        coord: coorindates

        size: size of the point
        """
        super().__init__(ax, coord)
        self._init_artist(coord, size, color)
        self.connect()
        self.press = None

    def _init_artist(self, coord, size, color):
        self.artist = patches.Circle(self.coords.tolist(),
                                     size,
                                     fc=color,
                                     edgecolor=color,
                                     alpha=0.5)
        self.ax.add_patch(self.artist)

    def on_press(self, event):
        if self._basic_check(event) is False:
            return
        if self.lock is not None:
            return
        contains, attrd = self.artist.contains(event)
        if not contains:
            return
        self.press = (self.artist.center, event.xdata, event.ydata)
        self._lock()
        self._on_press_draw()

    def on_motion(self, event):

        if self._basic_check(event) is False:
            return
        if self.lock is not self:
            return

        self.artist.center, xpress, ypress = self.press
        dx, dy = event.xdata - xpress, event.ydata - ypress
        self.artist.center = (self.artist.center[0] + dx,
                              self.artist.center[1] + dy)
        self._on_motion_draw()

    def on_release(self, event):
        if self._basic_check(event) is False:
            return
        if self.press is None:
            return
        self._unlock()
        self.press = None
        self.save_coords()
        self._on_release_draw()

    def save_coords(self):
        self.coords[0] = self.artist.center[0]
        self.coords[1] = self.artist.center[1]


class DraggableMarkers(DraggableArtist):
    """Class for a draggable marker"""

    def __init__(self, ax, coords, size=36, colors=None, msize=5):
        """Initialise a draggablepoint instance given x and y coordinate
        Parameters
        ----------
        ax: axes to be drawn on

        coord: coorindates

        size: size of the point
        """
        super().__init__(ax, coords)
        self.msize = msize
        self._init_artist(size, colors)
        self.connect()

    def _init_artist(self, size, colors):
        coords = self.coords
        if colors is None:
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        ccolors = cycle(colors)
        colors = [next(ccolors) for i in range(len(coords))]
        self.artist = self.ax.scatter(coords[:, 0],
                                      coords[:, 1],
                                      marker='+',
                                      color=colors,
                                      s=size)

    def on_press(self, event):

        if self._basic_check(event) is False:
            return
        if self.lock is not None:
            return

        # Test if the point is picked up in pixels
        x = event.x
        y = event.y
        # marker's x,y coordiantes in pixels
        offsets = self.artist.get_offsets()
        xyartist = self.ax.transData.transform(offsets)
        # Linear distance in pixels
        # N array of distances
        r = np.sqrt(((xyartist - [x, y])**2).sum(axis=1))
        if np.min(r) < self.msize:
            # save figure background:
            self._on_press_draw()
            # store index of draggable marker:
            self.draggable = np.argmin(r)
            # Save location of the markers
            mloc = offsets[self.draggable]
            self.press = (mloc[0], mloc[1], event.xdata, event.ydata)
            # Lock any other instances
            self._lock()
        else:
            self.draggable = None

    def on_motion(self, event):

        if DraggableArtist.lock is not self or self._basic_check(
                event) is False:
            return
        if self.draggable is not None:
            if event.xdata and event.ydata:
                # get markers coordinate in data units:
                xydata = self.artist.get_offsets()
                # change the coordinate of the marker that is
                # being dragged to the ones of the mouse cursor:
                # Calculate displacement
                dx, dy = event.xdata - \
                    self.press[2], event.ydata - self.press[3]
                xydata[self.draggable] = [
                    self.press[0] + dx, self.press[1] + dy
                ]
                # update the plot:
                self._on_motion_draw()

    def on_release(self, event):

        if self.lock is not self or self._basic_check(event) is False:
            return
        self._unlock()
        self.press = None
        self.save_coords()
        self._on_release_draw()

    def save_coords(self):
        self.coords[self.draggable] = self.artist.get_offsets()[self.draggable]

    def set_coords(self, coords):
        self.coords = coords
        self.artist.set_offsets(coords)


# Need to get this compatible with ndarrays!
class DraggablePoints:
    """Collection of draggable points"""

    def __init__(self, ax, coords, size, colors=None):
        """Initialise a DraggablePoints object from a series of coordinates"""
        self.figure = ax.figure
        self.ax = ax
        self.dpoints = []
        self.size = size
        self.coords = coords
        if colors is None:
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        colors = cycle(colors)
        for coor in coords:
            self.dpoints.append(
                DraggablePoint(ax, coor, size, color=next(colors)))

    def set_xy(self, index, x, y):

        point = self.dpoints[index]
        point.set_xy(x, y)

    def set_sizes(self, size):
        for dpt in self.dpoints:
            dpt.set_size(size)

    def redraw(self):
        self.figure.canvas.draw()

    def set_coords(self, coords):
        """Set coordinates using a Nx2 numpy array"""

        # Refector: Update only those needed
        for coor, dpoint in zip(coords, self.dpoints):
            dpoint.set_coord(coor)

    def check_integrity(self):
        """Check the coor of points are views of self.coords"""
        for dpt in self.dpoints:
            assert dpt.coord.base is self.coords
        print("all points associated: pass")

    def __getitem__(self, index):
        return self.dpoints[index]

    def __setitem__(self, index, item):
        self.dpoints[index] = item

    def __len__(self):
        return len(self.dpoints)

    def __repr__(self):
        string = "<DraggablePoints object at {} with {} points>".format(
            id(self), len(self.dpoints))
        return string

    def __delitem__(self, index):

        dot = self.dpoints.pop(index)
        del dot


if __name__ == "__main__":
    # Drop in tests
    ax = plt.subplot(211)
    ax2 = plt.subplot(212)
    import numpy as np
    coords = np.random.random((50, 2))
    print(coords)
    dot = DraggableMarkers(ax, coords)
    pts = DraggablePoint(ax, [1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.show()
