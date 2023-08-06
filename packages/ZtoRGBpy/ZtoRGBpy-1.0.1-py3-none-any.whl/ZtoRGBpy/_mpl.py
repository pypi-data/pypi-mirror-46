# -*- coding: utf-8 -*-
# =================================================================================
#  Copyright 2019 Glen Fletcher <mail@glenfletcher.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  All documentation this file as docstrings or comments are licensed under the
#  Creative Commons Attribution-ShareAlike 4.0 International License; you may
#  not use this documentation except in compliance with this License.
#  You may obtain a copy of this License at
#
#    https://creativecommons.org/licenses/by-sa/4.0
#
# =================================================================================
"""
ZtoRGB Matplotlib Module

Provides extension functions for matplotlib

.. moduleauthor:: Glen Fletcher <mail@glenfletcher.com>
"""
from collections.abc import Mapping

import matplotlib.colorbar as cbar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import SubplotBase

from ZtoRGBpy._core import remap


def colorbar(mappable=None, ax=None, cax=None, scale=None, profile=None, use_gridspec=True, **kw):
    """Generate a Matplotlib Colorbar

    Renders a special colorbar showing phase rotation on the opposite
    axis to the magnitude (no axis labels)

    Parameters
    ----------
    mappable: `AxesImage <matplotlib.image.AxesImage>` with ZtoRGBpy meta data, optional, default: `None`
        An `AxesImage <matplotlib.image.AxesImage>` as returned by `imshow` or `colorwheel`.
        Defaults to the current image, if `None`.

    ax : `Axes <matplotlib.axes.Axes>`, list of Axes, optional, default: `None`
        Parent axes from which space for a new colorbar axes will be stolen.
        If a list of axes is given they will all be resized to make room for the colorbar axes.

    cax : `Axes <matplotlib.axes.Axes>`,  optional, default: `None`
        Axes into which the colorbar will be drawn.

    scale : `Scale`, optional, default: `None`
        `Scale` used by the mapping that the colorbar represents. Defaults to the scale include
        in the ZtoRGBpy meta data for the mappable being used,

    profile : `RGBColorProfile`, optional, default: `None`
        `RGBColorProfile` used by the mapping that the colorbar represents. Defaults to the profile
        include in the ZtoRGBpy meta data for the mappable being used,

    use_gridspec : `bool`, optional, default: `True`
        If ``cax`` is `None`, a new ``cax`` is created as an instance of Axes.
        If ``ax`` is an instance of `Subplot <matplotlib.pyplot.subplot>` and ``use_gridspec`` is `True`,
        ``cax`` is created as an instance of Subplot using the
        `grid_spec <matplotlib.colorbar.make_axes_gridspec>` module.

    Other Parameters
    ----------------
    **kwargs : `matplotlib.colorbar.make_axes` parameters
        These parameters are passed to the underlying matplotlib function, used to generate the colorbar axes

    Returns
    -------
    image : `AxesImage <matplotlib.image.AxesImage>`
        image object representing the colorbar
    axes : `Axes <matplotlib.axes.Axes>`
        axes for the image object representing the colorbar


    Example
    -------

    .. plot::
        :format: doctest

        >>> import ZtoRGBpy
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> r = np.linspace(-5,5, 2001)
        >>> x,y = np.meshgrid(r,r)
        >>> z = x + 1j*y
        >>> ZtoRGBpy.imshow(np.cos(z), extent=[-5,5,-5,5])
        >>> ZtoRGBpy.colorbar()
        >>> plt.show()
    """
    if mappable is None:
        mappable = plt.gci()
    current_ax = plt.gca()
    if cax is None:
        if ax is None:
            ax = current_ax
        if use_gridspec and isinstance(ax, SubplotBase):
            cax, kw = cbar.make_axes_gridspec(ax, **kw)
        else:
            cax, kw = cbar.make_axes(ax, **kw)
    metadata = {}
    if mappable is not None:
        print(mappable)
        if hasattr(mappable, '_ZtoRGBpy__meta'):
            # noinspection PyProtectedMember
            metadata = mappable._ZtoRGBpy__meta
            if not isinstance(metadata, Mapping):
                metadata = {}
    if scale is None and 'scale' in metadata:
        scale = metadata['scale']
    if profile is None and 'profile' in metadata:
        profile = metadata['profile']
    if scale is None or profile is None:
        raise RuntimeError('No scale and profile was '
                           'found to use for colorbar creation. '
                           'Either define them as parameters, or'
                           'use a mappable created by `ZtoRBGpy.imshow`.')
    try:
        ticks, labels = scale.ticks()
    except NotImplementedError:
        raise NotImplementedError("{0!r:s} dose not support the rendering of a colorbar.".format(scale))
    if "ticklocation" not in kw or kw["ticklocation"] == 'auto':
        ticklocation = 'bottom' if kw["orientation"] == 'horizontal' else 'right'
    else:
        ticklocation = kw["ticklocation"]
    if "orientation" not in kw or kw["orientation"] == 'vertical':
        phase = np.linspace(-np.pi, np.pi, 45)
        magnitude = np.linspace(1, 0, 1000)
        phase, magnitude = np.meshgrid(phase, magnitude)
        extent = [0, np.pi * 2, 0, 1.0]
        long_axis, short_axis = cax.yaxis, cax.xaxis
    else:
        phase = np.linspace(np.pi, -np.pi, 45)
        magnitude = np.linspace(0, 1, 1000)
        magnitude, phase = np.meshgrid(magnitude, phase)
        extent = [0, 1.0, 0, np.pi * 2]
        long_axis, short_axis = cax.xaxis, cax.yaxis
    z_cb = cax.imshow(remap(magnitude * np.exp(1j * phase), profile=profile),
                      aspect="auto",
                      extent=extent)
    short_axis.set_visible(False)
    long_axis.set_ticks(ticks)
    long_axis.set_ticklabels(str(label) for label in labels)
    long_axis.set_ticks_position(ticklocation)
    long_axis.set_label_position(ticklocation)
    plt.sca(current_ax)
    return z_cb, cax


def colorwheel(ax=None, scale=None, profile=None, rotation=0, grid=False):
    """Renders a colorwheel, showing the colorspace, with optional grid

    Parameters
    ----------
    ax : `Axes <matplotlib.axes.Axes>`, optional, default: `None`
        The axes to plot to. If `None`, use the current axes like `pyplot.imshow <matplotlib.pyplot.imshow>`\

    scale : `Scale`, optional, default: `None`
        This parameter is passed directly to `remap`\ ``(Z, scale=scale, profile=profile)``

    profile : `RGBColorProfile`, optional, default: `None`
        This parameter is passed directly to `remap`\ ``(Z, scale=scale, profile=profile)``

    rotation: `float`, optional, default: ``0``
        This is the angle in radians by which the colorwheel is rotated

    grid: `bool`, optional, default: `False`
        Boolean indicating if the grid should be drawn

    Returns
    -------
    image : `AxesImage <matplotlib.image.AxesImage>`
        Extra metadata about the complex mapping is added to this object
    grid_axes : `Axes <matplotlib.axes.Axes>`
        Present only if ``grid`` = `True`. The polar axes on which the grid is drawn

    Example
    -------

    .. plot::
        :format: doctest

        >>> import ZtoRGBpy
        >>> import matplotlib.pyplot as plt
        >>> ZtoRGBpy.colorwheel()
        >>> plt.show()
    """
    rline = np.linspace(-1, 1, 1001)
    xmesh, ymesh = np.meshgrid(rline, rline)
    zmesh = xmesh+1j*ymesh
    zmesh *= np.exp(1j*rotation)
    rgba = np.ones(zmesh.shape + (4,))
    rgba[..., 3] = abs(zmesh) <= 1
    rgba[..., 0:3], scale, profile = remap(zmesh, scale=scale, profile=profile,
                                           return_metadata=True)
    current_ax = plt.gca()
    if ax is None:
        ax = current_ax
    z_im = ax.imshow(rgba, extent=[-1, 1, 1, -1])
    z_im._ZtoRGBpy__meta = {"scale": scale, "profile": profile}
    ax.axis('off')
    if grid:
        pax = ax.figure.add_axes(ax.figbox, projection='polar', frameon=False)
        ticks = scale.ticks()
        pax.set_rticks(ticks[0]), pax.set_yticklabels(ticks[1])
        pax.set_theta_zero_location("N")
        pax.set_rlabel_position(290)
        pax.yaxis.grid(True, which='major', linestyle='-')
        pax.xaxis.grid(True, which='major', linestyle='-')
        ret = z_im, pax
    else:
        ret = z_im
    plt.sca(current_ax)
    plt.sci(z_im)
    return ret


def imshow(z, ax=None, scale=None, profile=None, **kwargs):
    """Displays a complex image on the ax or the current axes.

    Invokes `matplotlib.axes.Axes.imshow` on the results of
    `remap`\ (z, scale, profile) and attachs scale and profile
    to the returned object as metadata.
    
    Parameters
    ----------
    z : `array_like <numpy.asarray>` [N, M]
        The complex data. This is mapped to colors based on
        `remap`\ (z, scale=scale, profile=profile)
        
    ax : `Axes <matplotlib.axes.Axes>`, optional, default: `None`
        The `axes <matplotlib.axes.Axes>` to plot to. If `None` use the current axes like `pyplot.imshow <matplotlib.pyplot.imshow>`
        
    scale : `Scale`, optional, default: `None`
        This parameter is passed directly to `remap`\ ``(z, scale=scale, profile=profile)``
        
    profile : `RGBColorProfile`, optional, default: `None`
        This parameter is passed directly to `remap`\ ``(z, scale=scale, profile=profile)``

    Other Parameters
    ----------------
    **kwargs : `matplotlib.axes.Axes.imshow` parameters
        These parameters are passed to the underlying matplotlib function

    Returns
    -------
    image : `matplotlib.image.AxesImage`
        Extra metadata about the complex mapping is added to this object

    Example
    -------

    .. plot::
        :format: doctest

        >>> import ZtoRGBpy
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> r = np.linspace(-5,5, 2001)
        >>> x,y = np.meshgrid(r,r)
        >>> z = x + 1j*y
        >>> ZtoRGBpy.imshow(np.cos(z), extent=[-5,5,-5,5])
        >>> plt.show()
    """
    current_ax = plt.gca()
    if ax is None:
        ax = current_ax
    rgb, scale, profile = remap(z, scale=scale, profile=profile,
                                return_metadata=True)
    z_im = ax.imshow(rgb, **kwargs)
    # add meta data so ZtoRGBpy.colorbar can pull
    #   scale and profile automatically
    z_im._ZtoRGBpy__meta = {"scale": scale, "profile": profile}
    plt.sca(ax)
    plt.sci(z_im)
    return z_im
