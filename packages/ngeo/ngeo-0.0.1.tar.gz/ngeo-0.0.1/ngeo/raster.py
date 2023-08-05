import numpy as np
from numba import njit
from functools import partial

import math
import xarray


# /* 2.0.10: before the drawing routines, some code to clip points that are
#  * outside the drawing window.  Nick Atty (nick@canalplan.org.uk)
#  *
#  * This is the Sutherland Hodgman Algorithm, as implemented by
#  * Duvanenko, Robbins and Gyurcsik - SH(DRG) for short.  See Dr Dobb's
#  * Journal, January 1996, pp107-110 and 116-117
#  *
#  * Given the end points of a line, and a bounding rectangle (which we
#  * know to be from (0,0) to (SX,SY)), adjust the endpoints to be on
#  * the edges of the rectangle if the line should be drawn at all,
#  * otherwise return a failure code */
#
# /* this does "one-dimensional" clipping: note that the second time it
#    is called, all the x parameters refer to height and the y to width
#    - the comments ignore this (if you can understand it when it's
#    looking at the X parameters, it should become clear what happens on
#    the second call!)  The code is simplified from that in the article,
#    as we know that gd images always start at (0,0) */
#
# /* 2.0.26, TBB: we now have to respect a clipping rectangle, it won't
# 	necessarily start at 0. */

@njit
def clip_1d(x0, y0, x1, y1, mindim, maxdim):
    if x0 < mindim:
        # start of line is left of window
        if x1 < mindim:
            return 0, x0, y0, x1, y1

        # gradient of line
        # calculate the slope of the line
        m = (y1 - y0) / float(x1 - x0)
        # adjust x0 to be on the left boundary (ie to be zero), and y0 to match
        y0 -= int(m * (x0 - mindim))
        x0 = mindim
        # now, perhaps, adjust the far end of the line as well
        if x1 > maxdim:
            y1 += m * (maxdim - x1)
            x1 = maxdim
        return 1, x0, y0, x1, y1

    if x0 > maxdim:
        # start of line is right of window - complement of above
        if x1 > maxdim:
            # as is the end, so the line misses the window
            return 0, x0, y0, x1, y1

        # gradient of line
        # calculate the slope of the line
        m = (y1 - y0) / float(x1 - x0)
        # adjust so point is on the right boundary
        y0 += int(m * (maxdim - x0))
        x0 = maxdim
        # now, perhaps, adjust end of the line
        if x1 < mindim:
            y1 -= int(m * (x1 - mindim))
            x1 = mindim
        return 1, x0, y0, x1, y1

    # the final case - the start of the line is inside the window
    if x1 > maxdim:
        # other end is outside to the right
        m = (y1 - y0) / float(x1 - x0)
        y1 += int(m * (x1 - mindim))
        x1 = mindim
        return 1, x0, y0, x1, y1

    # only get here if both points are inside the window
    return 1, x0, y0, x1, y1


@njit
def rasterize_V_line_local(im, x, y1, y2, col, thick=1):
    if thick > 1:
        # thick_haft = thick >> 1
        # gdImageFilledRectangle
        return
    else:
        if y2 < y1:
            t = y1
            y1 = y2
            y2 = t
        for i in range(y1, y2+1):
            im[i][x] = col
    return


@njit
def rasterize_H_line_local(im, y, x1, x2, col, thick=1):
    if thick > 1:
        # thick_haft = thick >> 1
        # gdImageFilledRectangle
        return
    else:
        if x2 < x1:
            t = x1
            x1 = x2
            x2 = t
        for i in range(x1, x2+1):
            im[y][i] = col
    return


#  Function: gdImageLine
#  Bresenham as presented in Foley & Van Dam.

#  gdImageLineLocal
def rasterize_line_local(im, x1, y1, x2, y2, color, cx1, cx2, cy1, cy2):

    # 2.0.10: Nick Atty: clip to edges of drawing rectangle, return if no
    # 	   points need to be drawn. 2.0.26, TBB: clip to edges of clipping
    # 	   rectangle. We were getting away with this because gdImageSetPixel
    # 	   is used for actual drawing, but this is still more efficient and opens
    # 	   the way to skip per-pixel bounds checking in the future.

    draw, x1, y1, x2, y2 = clip_1d(x1, y1, x2, y2, cx1, cx2)
    if draw == 0:
        return
    draw, y1, x1, y2, x2 = clip_1d(y1, x1, y2, x2, cy1, cy2)
    if draw == 0:
        return

    thick = 1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    if dx == 0:
        rasterize_V_line_local(im, x1, y1, y2, color)
        return im
    elif dy == 0:
        rasterize_H_line_local(im, y1, x1, x2, color)
        return

    if dy <= dx:
        #  More-or-less horizontal. use wid for vertical stroke
        #  Doug Claar: watch out for NaN in atan2 (2.0.5)
        #  2.0.12: Michael Schwartz: divide rather than multiply;
        # 	  TBB: but watch out for /0!
        ac = math.cos(math.atan2(dy, dx))
        if ac != 0:
            wid = thick / ac
        else:
            wid = 1

        if wid == 0:
            wid = 1

        d = 2 * dy - dx
        incr1 = 2 * dy
        incr2 = 2 * (dy - dx)
        if x1 > x2:
            x = x2
            y = y2
            ydirflag = -1
            xend = x1

        else:
            x = x1
            y = y1
            ydirflag = 1
            xend = x2

        # Set up line thickness
        wstart = y - wid / 2
        for w in range(wstart, wstart + wid):
            im[w][x] = color

        if (y2 - y1) * ydirflag > 0:
            while x < xend:
                x += 1
                if d < 0:
                    d += incr1
                else:
                    y += 1
                    d += incr2

                wstart = y - wid / 2
                for w in range(wstart, wstart + wid):
                    im[w][x] = color

        else:
            while x < xend:
                x += 1
                if d < 0:
                    d += incr1
                else:
                    y -= 1
                    d += incr2

                wstart = y - wid / 2
                for w in range(wstart, wstart + wid):
                    im[w][x] = color

    else:
        # More-or-less vertical. use wid for horizontal stroke
		# 2.0.12: Michael Schwartz: divide rather than multiply;
		#         TBB: but watch out for /0!
        asin = math.sin(math.atan2 (dy, dx))
        if asin != 0:
            wid = thick / asin
        else:
            wid = 1
        if wid == 0:
            wid = 1

        d = 2 * dx - dy
        incr1 = 2 * dx
        incr2 = 2 * (dx - dy)
        if y1 > y2:
            y = y2
            x = x2
            yend = y1
            xdirflag = -1
        else:
            y = y1
            x = x1
            yend = y2
            xdirflag = 1

        # Set up line thickness
        wstart = x - wid / 2
        for w in range(wstart, wstart + wid):
            im[y][w] = color
        if (x2 - x1) * xdirflag > 0:
            while y < yend:
                y += 1
                if d < 0:
                    d += incr1
                else:
                    x += 1
                    d += incr2

                wstart = x - wid / 2
                for w in range(wstart, wstart + wid):
                    im[y][w] = color
        else:
            while y < yend:
                y += 1
                if d < 0:
                    d += incr1
                else:
                    x -= 1
                    d += incr2
                wstart = x - wid / 2
                for w in range(wstart, wstart + wid):
                    im[y][w] = color
    return


def rasterize_polygon(data, height, width, xrange, yrange, dtype):
    out = np.zeros(shape=(height, width), dtype=dtype)
    n = int(len(data)/2)
    if n == 0:
        return out

    c = 1

    xs = np.array(data[0::2])
    ys = np.array(data[1::2])

    xconv = partial(map_x_to_screen_x, xrange=xrange, width=width)
    yconv = partial(map_y_to_screen_y, yrange=yrange, height=height)

    xs = list(map(xconv, xs))
    ys = list(map(yconv, ys))

    miny = min(ys)
    maxy = max(ys)

    miny = int(miny)
    maxy = int(maxy)

    cx1 = 0
    cx2 = width - 1
    cy1 = 0
    cy2 = height - 1

    #  /* necessary special case: horizontal line */
    if n > 1 and miny == maxy:
        x1 = x2 = xs[0]
        for i in range(1, n):
            if xs[i] < x1:
                x1 = xs[i]
            elif xs[i] > x2:
                x2 = xs[i]
        rasterize_line_local(out, x1, miny, x2, miny, c, cx1, cx2, cy1, cy2)
        return out

    pmaxy = maxy

    #  /* 2.0.16: Optimization by Ilia Chipitsine -- don't waste time offscreen */
    #  /* 2.0.26: clipping rectangle is even better */
    if miny < cy1:
        miny = cy1

    if maxy > cy2:
        maxy = cy2

    #  /* Fix in 1.3: count a vertex only once */
    for y in range(miny, maxy + 1):
        polyInts = []
        ints = 0
        for i in range(n):
            if not i:
                ind1 = n - 1
                ind2 = 0
            else:
                ind1 = i - 1
                ind2 = i

            y1 = ys[ind1]
            y2 = ys[ind2]

            if y1 < y2:
                x1 = xs[ind1]
                x2 = xs[ind2]
            elif y1 > y2:
                y2 = ys[ind1]
                y1 = ys[ind2]
                x2 = xs[ind1]
                x1 = xs[ind2]
            else:
                continue

            #  /* Do the following math as float intermediately, and round to ensure
            #   * that Polygon and FilledPolygon for the same set of points have the
            #   * same footprint. */

            if (y >= y1) and (y < y2):
                polyInts.append(int(float((y - y1) * (x2 - x1)) / float(y2 - y1) + 0.5 + x1))
                ints += 1
            elif (y == pmaxy) and (y == y2):
                polyInts.append(int(x2))
                ints += 1

        # 2.0.26: polygons pretty much always have less than 100 points,
        # and most of the time they have considerably less. For such trivial
        # cases, insertion sort is a good choice. Also a good choice for
        # future implementations that may wish to indirect through a table.

        for i in range(1, ints):
            index = polyInts[i]
            j = i
            while (j > 0) and (polyInts[j - 1] > index):
                polyInts[j] = polyInts[j - 1]
                j -= 1
            polyInts[j] = index

        for i in range(0, ints-1, 2):
            # 2.0.29: back to gdImageLineLocal to prevent segfaults when
            # 		  performing a pattern fill
            rasterize_line_local(out, polyInts[i], y, polyInts[i+1], y, c, cx1, cx2, cy1, cy2)

    return out

@njit
def map_x_to_screen_x(xs, xrange, width):
    return int((xs - xrange[0]) / (xrange[1] - xrange[0]) * width)

@njit
def map_y_to_screen_y(ys, yrange, height):
    return int((ys - yrange[0]) / (yrange[1] - yrange[0]) * height)


def rasterize_func(part_data, part_coords, height, width, xrange, yrange, dtype):
    feature_idx = part_coords[0, 0]
    polygon_idx = part_coords[1, 0]
    part_idx = part_coords[2, 0]
    return feature_idx, polygon_idx, part_idx, \
           rasterize_polygon(part_data, height, width, xrange, yrange, dtype)


def rasterize(fc, height, width, xrange, yrange, dtype=np.uint8):
    '''
    rasterize turns a feature collection into a regularly gridded array (image)


    Parameters
    ----------
    feature_collection: geomarray.FeatureCollection
    out_height: int
    out_width: int

    Returns
    -------
    out: numpy.array((out_height, out_width), dtype=dtype)

    Example
    -------

    fc = FeatureCollection()
    result = rasterize(fc, 800, 600)

    >>> array([[0, 1, 0, 0],
               [0, 1, 1, 0],
               [0, 1, 1, 0]])
    '''

    out = np.zeros((height, width), dtype=dtype)

    geom_gen = fc.geometry.map(rasterize_func, axis=2,
                               height=height, width=width,
                               xrange=xrange, yrange=yrange,
                               dtype=dtype)

    for feature_id, polygon_id, part_id, part_raster in geom_gen:
        if part_id > 0:
            out -= part_raster
        else:
            out += part_raster

    return out
