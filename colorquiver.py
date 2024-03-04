# -*- coding: utf-8 -*-

#============================================================================================#
# Copyright (C) 2022-2024 Earthlight <earthlight2187@hotmail.com>                            #
#                                                                                            #
# Permission is hereby granted, free of charge, to any person obtaining a copy of this       #
# software and associated documentation files (the "Software"), to deal in the Software      #
# without restriction, including without limitation the rights to use, copy, modify, merge,  #
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons #
# to whom the Software is furnished to do so, subject to the following conditions:           #
#                                                                                            #
# The above copyright notice and this permission notice shall be included in all copies or   #
# substantial portions of the Software.                                                      #
#                                                                                            #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,        #
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR   #
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE  #
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR       #
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER     #
# DEALINGS IN THE SOFTWARE.                                                                  #
#============================================================================================#

from typing import Iterable

import numpy as np
import matplotlib.pyplot as plt


def _hsv_to_rgb(h: float, s: float, v: float) -> tuple[float]:
    """ Exactly the same as colorsys.hsv_to_rgb """
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0) # XXX assume int() truncates!
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0-f))
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q
    # Cannot get here


def _arr_hsv_to_rgb(h: np.ndarray, s: float | np.ndarray, v: float | np.ndarray) -> np.ndarray:
    """ The hsv_to_rgb function that processes multiple inputs in a numpy array. """
    i = (h * 6.0).astype(int)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0-f))
    i = i % 6
    return np.array([(mask := (i == 0)) * v, mask * t, mask * p]) \
         + np.array([(mask := (i == 1)) * q, mask * v, mask * p]) \
         + np.array([(mask := (i == 2)) * p, mask * v, mask * t]) \
         + np.array([(mask := (i == 3)) * p, mask * q, mask * v]) \
         + np.array([(mask := (i == 4)) * t, mask * p, mask * v]) \
         + np.array([(mask := (i == 5)) * v, mask * p, mask * q])


def _get_arg(vec: Iterable[float | np.ndarray]) -> float | np.ndarray:
    """ Return the argument of a 2d vector, normalized from 0 to 1.

        e.g. `_getArg([1,  1]) == 0.125`
             `_getArg([1, -1]) == 0.875`
    """
    return np.angle(-vec[0] - vec[1] * 1j) / 2 / np.pi + 0.5


def _vec_to_color(vec: Iterable[float], mapping: Iterable[float], mode: int = 1) -> Iterable[float]:
    """ Return a 3d vector represents the color of the given 2d vector normalized in the given
        mapping [min, max].

        - mode 1: black -> full colors indicates min -> max
        - mode 2: black -> full colors -> white indicates min -> max
        - mode 3: black -> full colors -> white indicates min -> threshold (= mean + std), and
        data bigger than the threshold would be clipped.

        An exception would be raised if the mode argment is other than 1, 2 or 3.
    """
    norm = np.linalg.norm(vec)
    if mode == 1:
        return _hsv_to_rgb(
            _get_arg(vec),
            1,
            (norm - mapping[0]) / (mapping[1] - mapping[0])
        )
    elif mode == 2 or mode == 3:
        mapped = (norm - mapping[0]) / (mapping[1] - mapping[0])
        return _hsv_to_rgb(
            _get_arg(vec),
            min(1, 2 - mapped * 2),
            min(1, mapped * 2)
        )
    else:
        raise Exception(f"Color mode {mode} not surportted.")


def _arr_vec_to_color(vec: Iterable[np.ndarray], mapping: Iterable[float], mode: int = 1) -> Iterable[float]:
    """ The _vec_to_color function that processes multiple inputs in a numpy array.
        See more in `_vec_to_color()`.
    """
    norm = np.sqrt(vec[0]**2 + vec[1]**2)
    if mode == 1:
        return _arr_hsv_to_rgb(
            _get_arg(vec),
            1,
            (norm - mapping[0]) / (mapping[1] - mapping[0])
        )
    elif mode == 2 or mode == 3:
        mapped = (norm - mapping[0]) / (mapping[1] - mapping[0])
        return _arr_hsv_to_rgb(
            _get_arg(vec),
            min(1, 2 - mapped * 2),
            min(1, mapped * 2)
        )
    else:
        raise Exception(f"Color mode {mode} not surportted.")


def colorquiver(
    ax: plt.Axes,
    rect: tuple,
    X: np.ndarray,
    Y: np.ndarray,
    mode: int = 1
) -> tuple[float]:
    """ Draw a color quiver on a given plt.Axes

        # Args
        - ax: The plt.Axes you want to draw color quiver on.
        - rect: The area to draw, in the format of (xmin, xmax, ymin, ymax)
        - X, Y: data, must be in the same shape

            - mode 1: black -> full colors indicates min -> max
            - mode 2: black -> full colors -> white indicates min -> max
            - mode 3: black -> full colors -> white indicates min -> threshold (= mean + std),
            and data bigger than the threshold would be clipped.
        
        # Returns
        Return two float numbers in a tuple.
        - The first one is the maximum vector length.
        - The second one is the threshold if the color mode is 3, otherwise it would be 0.

        # Raises
        - An exception would be raised there are different shapes of X and Y.
        - An exception would be raised if the mode argment is other than 1, 2 or 3.
    """
    if X.shape != Y.shape:
        raise Exception(f"{X.shape = }, {Y.shape = }, Shape not match.")

    ma = 0
    maxValue = 0

    if mode == 1 or mode == 2:
        ma = np.sqrt((X**2 + Y**2).max())
    elif mode == 3:
        norms = np.sqrt(X**2 + Y**2)
        ma = norms.sum() / norms.size + norms.std()
        maxValue = norms.max()
    
    im = _arr_vec_to_color(np.array([-X, Y]), [0, ma], mode)

    ax.imshow(im.transpose(1, 2, 0), extent=rect)
    
    return ma, maxValue


def colorlabel(
    fig: plt.figure,
    labelGrid: int,
    mapping: Iterable[float],
    colorMode: int = 1,
    fDict: dict = {'family':'Times New Roman', 'weight':'normal'},
    maxValue = None
) -> None:
    """ Add a graph to indicate how the colors match with the vectors.

        # Args
        - fig: The plt.figure to draw the color lable.
        - labelGrid: The pixel number of each side of the graph (won't affect the graph size),
        results in the fineness of the graph.
        - mapping: [minValue, maxValue], usually the actrual range of vector norms.
        - colorMode: 1~3 supported
        - fDict: Text format on the label
        - maxValue: Required when colorMode == 3
    """

    ax2 = fig.add_axes([0.75, 0.7, 0.2, 0.25], facecolor="#fff")

    ax2.axis([-1, 1, -1, 1])
    ax2.axis("off")

    labelGridLen = 2 / labelGrid

    for i in range(labelGrid):
        for j in range(labelGrid):
            labelGridRec = (
                -1 + i * labelGridLen,
                -1 + j * labelGridLen,
                -1 + (i+1) * labelGridLen,
                -1 + (j+1) * labelGridLen
            )
            labelGridCenter = np.array([
                -1 + (i+0.5) * labelGridLen,
                -1 + (j+0.5) * labelGridLen
            ])
            if np.linalg.norm(labelGridCenter) <= 1:
                ax2.fill(
                    [labelGridRec[0], labelGridRec[0], labelGridRec[2], labelGridRec[2]],
                    [labelGridRec[1], labelGridRec[3], labelGridRec[3], labelGridRec[1]],
                    color = _vec_to_color(labelGridCenter, (0, 1), colorMode),
                    lw = 0
                )

    offsetX = 0.1
    offsetY = -0.15
    labelWid = 0.1
    
    ax2.plot([0, 0], [0, 1], c='w', lw=1)
    ax2.plot([-labelWid/2, labelWid/2], [0, 0], c='w', lw=1)
    ax2.text(0 + offsetX, 0 + offsetY, str(mapping[0]), c='w', fontdict=fDict)
    
    ax2.plot([-labelWid/2, labelWid/2], [0.5, 0.5], c='w', lw=1)
    ax2.text(
        0 + offsetX,
        0.5 + offsetY,
        str((mapping[0] + mapping[1]) / 2),
        c='w' if colorMode==1 else 'k',
        fontdict=fDict
    )
    
    ax2.plot([-labelWid/2, labelWid/2], [1, 1], c='w', lw=1)
    ax2.text(0 + offsetX, 1 + offsetY, str(mapping[1]), c = 'k', fontdict=fDict)

    if colorMode == 3:
        ax2.set_title("max_value = " + str(maxValue), fontdict=fDict)
