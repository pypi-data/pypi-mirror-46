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
ZtoRGB core module

Provides all core functions

.. moduleauthor:: Glen Fletcher <mail@glenfletcher.com>
"""
from collections.abc import Sequence, Mapping
from copy import copy
from inspect import getfullargspec

import numpy as np


class Scale(object):
    """Abstract base class for defining a scaling function for the remapping of complex values to RGB colors.

    Automatically generates `repr` of subclasses (see **attributes** to define parameters from subclasses).

    Attributes
    ----------

    __args: `Sequence <collections.abc.Sequence>`
        List of Positional argument values for specific subclass
    __kwargs: `Mapping <collections.abc.Mapping>`
        Mapping of keyword only argument values for specific subclass

    See Also
    --------
       `custom_scale`

    """
    def __init__(self):
        pass

    def __call__(self, value):
        """Transform value with scaling function

        This method must be overridden by the subclass to define the transformation.

        Parameters
        ----------
        value: `array_like <numpy.asarray>` [...]
            Array of value to be transformed, by the scaling function.

        Returns
        -------
        scaled: `array <numpy.ndarray>` [ ``value.shape`` ]
            Scaled transformation (:math:`T(v)`) of ``value`` such that :math:`0 \le |T(v)| \le 1`.
        """
        raise NotImplementedError()

    def ticks(self):
        """Returns a list of tick marks suitable for a colorbar

        This method must be overridden by the subclass to define how tick should be displayed on the colorbar.

        Returns
        -------
        offsets: `Sequence <collections.abc.Sequence>` [ `float` ]
            Positions in the scaled interval :math:`[0.0, 1.0]` at which tick marks should be drawn.
        labels: `Sequence <collections.abc.Sequence>` [ `str` ]
            Labels to be displayed for each tick mark, non `str` types will be converted to `str`.
        """
        raise NotImplementedError()

    def _format_param(self, arg, cls=None, name=None):
        if name is not None and isinstance(name, str):
            kw = name.strip() + "="
        else:
            kw = ""
        return kw + self.format_arg(arg, cls, name)

    def format_arg(self, arg, cls=None, name=None):
        """Format argument

        Parameters
        ----------
        arg: `object`
            argument to be formatted
        cls: `type`
            class that uses the argument
        name: `str`
            name of argument

        Returns
        -------
        repr: `str`
            String representation of argument
        """
        if isinstance(arg, float):
            return "{0:g}".format(arg)
        else:
            return repr(arg)

    def __repr__(self):
        args = []
        arg_class = []
        kwargs = {}
        kwarg_names = []
        kwarg_class = {}
        for subclass in type(self).__mro__:
            if subclass == Scale:
                break
            if subclass.__init__ != subclass.__mro__[1].__init__:
                spec = getfullargspec(subclass.__init__)
                subclass_args = []
                subclass_kwargs = {}
                if hasattr(self, '_{0:s}__args'.format(subclass.__name__)):
                    subclass_args = getattr(self, '_{0:s}__args'.format(subclass.__name__))
                    if not isinstance(subclass_args, Sequence):
                        subclass_args = []
                if hasattr(self, '_{0:s}__kwargs'.format(subclass.__name__)):
                    subclass_kwargs = getattr(self, '_{0:s}__kwargs'.format(subclass.__name__))
                    if not isinstance(subclass_args, Mapping):
                        subclass_kwargs = {}
                num_args = len(spec.args) - 1
                if spec.defaults is not None:
                    num_defaults = len(spec.defaults)
                else:
                    num_defaults = 0
                num_values = len(subclass_args)
                if num_values + num_defaults < num_args:
                    raise RuntimeError("{0:s} dose not define __args "
                                       "for non-default arguments".format(subclass.__name__))
                for i in range(num_args):
                    if num_values > i:
                        args.append(subclass_args[i])
                    else:
                        args.append(spec.defaults[i - (num_args - num_defaults)])
                    arg_class.append(subclass)
                for kwname in spec.kwonlyargs:
                    if kwname not in kwarg_names:
                        if kwname in subclass_kwargs:
                            kwargs[kwname] = subclass_kwargs[kwname]
                        elif spec.kwonlydefaults is not None and kwname in spec.kwonlydefaults:
                            kwargs[kwname] = spec.kwonlydefaults[kwname]
                        else:
                            raise RuntimeError("{0:s} dose not define __kwargs "
                                               "for non-default keyword arguments".format(subclass.__name__))
                        kwarg_names.append(kwname)
                        kwarg_class[kwname] = subclass
        arglist = ', '.join(self._format_param(arg, cls) for arg, cls in zip(args, arg_class))
        if len(arglist) > 0 and len(kwarg_names) > 0:
            arglist += ', '
        arglist += ', '.join(self._format_param(kwargs[kwname], kwarg_class[kwname], kwname) for kwname in kwarg_names)
        if type(self).__module__ == '__main__':
            return "{0:s}({1:s})".format(type(self).__name__, arglist)
        else:
            return "{0:s}.{1:s}({2:s})".format(type(self).__module__, type(self).__name__, arglist)


class LinearScale(Scale):
    """Linear Scaling
    
    Provides a transformation representing a simple linear transformation,
    mapping the interval``[0.0, vmax]`` into the interval ``[0.0, 1.0]``, when invoked."""
    _divisors = [5, 10, 20, 25]

    def __init__(self, vmax=1.0):
        self.__args = [vmax]
        Scale.__init__(self)
        self.mag = float(vmax)

    def __call__(self, value):
        return np.asarray(value) / self.mag

    def ticks(self):
        """Returns a list of tick marks suitable for a colorbar

        Generates 4 to 10 linear steps where the steps are :math:`S = 10^m \\cdot \\{ 5, 10, 20, 25 \\}` with
        :math:`m \\in \\mathbb{Z}` and starting at 0 to give :math:`N` steps.

        Returns
        -------
        offsets: `Sequence <collections.abc.Sequence>` [ `float` ]
            Returns the `Sequence` :math:`0, \\frac{S}{vmax}, \\dots, \\frac{(N - 1) \\cdot S}{vmax}`
        labels: `Sequence <collections.abc.Sequence>` [ `str` ]
            Returns the `Sequence` :math:`0, S, \\dots, (N-1) \\cdot S`, formatted using the
            `General format <formatspec>` (``'g'``).
        """
        divisor = 0
        dfactor = 1.0
        while True:
            maxsteps = np.ceil(self.mag / (LinearScale._divisors[divisor]
                                           * dfactor))
            if maxsteps < 4:
                if divisor == 0:
                    dfactor /= 10
                    divisor = len(LinearScale._divisors) - 1
                else:
                    divisor -= 1
            elif maxsteps > 10:
                if divisor == len(LinearScale._divisors) - 1:
                    dfactor *= 10
                    divisor = 0
                else:
                    divisor += 1
            else:
                break
        stepsize = LinearScale._divisors[divisor] * dfactor
        steps = np.arange(stepsize, self.mag, stepsize)
        offsets = steps / self.mag
        steps = ["{:g}".format(step) for step in steps]
        return offsets, steps


class LogScale(Scale):
    """Logarithmic Scaling
    
    Provides a transformation representing a logarithmic transformation,
    mapping interval :math:`[v_{min}, v_{max}]` into the interval :math:`[1-l_{max}, 1]`.
    """

    def __init__(self, vmin=0.01, vmax=1.0, *, lmax=0.9):
        self.__args = [vmin, vmax]
        self.__kwargs = {'lmax': lmax}
        Scale.__init__(self)
        self.logmin = np.log10(vmin)
        self.logmax = np.log10(vmax)
        self.lightness_max = lmax
        self.lightness_buf = 1.0 - lmax
        self.factor = self.lightness_max/(self.logmax-self.logmin)

    def __call__(self, value):
        """Transform value with scaling function

        Parameters
        ----------
        value: `array_like <numpy.asarray>` [...]
            Array of values to be transformed, by the scaling function.

        Returns
        -------
        scaled: `array <numpy.ndarray>` [ ``value.shape`` ]
            Scaled transformation (:math:`T(v)`) of ``value``

        Notes
        -----
        Performs a logarithmic transformation, mapping the interval :math:`[v_{min}, v_{max}]` into the interval
        :math:`[1-l_{max}, 1]` using the transformation:

        .. math::
            T(v) = (1 - l_{max}) + \\frac{v \\cdot log_{10} ( |v| - log_{10} ( v_{min} ) \cdot l_{max} }
                                         {|v| \\cdot ( log_{10} ( v_{max} ) - log_{10} ( v_{min} ) )}

        """
        value = np.asarray(value)
        avalue = abs(value)
        return self.lightness_buf+(value*(np.log10(avalue) -
                                          self.logmin)/avalue)*self.factor

    def ticks(self):
        """Returns a list of tick marks suitable for a colorbar

        Generates 3 to 6 logarithmic steps such that the steps are all powers of 10 and bound by the interval
        ``[vmin, vmax]``

        Returns
        -------
        offsets: `Sequence <collections.abc.Sequence>` [ `float` ]
            Returns the `Sequence` :math:`T(10^{t_{min}}), \\dots, T(10^{t_{max}})`
        labels: `Sequence <collections.abc.Sequence>` [ `str` ]
            Returns the `Sequence` :math:`10^{t_{min}}, \\dots, 10^{t_{max}}`, as strings using latex math,
            as supported by `matplotlib`\ 's maths rendering.
        """
        lmax = np.floor(self.logmax)
        lmin = np.ceil(self.logmin)
        logrange = int(lmax - lmin) + 1
        while logrange > 6:
            for n in range(5, 2, -1):
                if (logrange - 1) % n == 0:
                    logrange = n + 1
                    break
            else:
                if self.logmax - lmax > lmin - self.logmin:
                    lmin += 1
                else:
                    lmax -= 1
                logrange = int(lmax - lmin) + 1
        steps = np.linspace(lmin, lmax, logrange)
        values = ["$10^{{{0:.0f}}}$".format(s) for s in steps]
        offsets = self(10 ** steps)
        return offsets, values


class RGBColorProfile(object):
    """
    Defines a color profile in a given RGB color space by conversion factors for
    red, green and blue to the Y component of the XYZ color space, i.e. the white point.

    Parameters
    ----------
    weights: `tuple` [ `float`, `float`, `float` ], optional, default: (2126.0, 7152.0, 772.0)
        Color component weight triple (:math:`W_R, W_G, W_B`) for conversion to the XYZ color space
        Defaults to the sRGB color space defined by IEC\ :cite:`RGBColorProfile-IECsRGB`.

    gamma: `float`, optional, defaults: 0.5
        Gamma (:math:`\gamma`) correction.
    """
    def __init__(self, weights=(2126.0, 7152.0, 722.0), gamma=0.5):
        self.weights = weights
        self.gamma = gamma

    def get_ratios(self):
        """Returns the relative ratios for red and blue

        Returns
        -------
        red_ratio: `float`
            Relative ratio of red (:math:`K_R`)

        blue_ratio: `float`
            Relative ratio of blue (:math:`K_B`)

        Notes
        -----
        Ratios for red (:math:`K_R`) and blue (:math:`K_B`) are defined by:

        .. math::

            K_R =& \\frac{W_R}{W_R + W_G + W_B}\\\\
            K_B =& \\frac{W_B}{W_R + W_G + W_B}
        """
        red_ratio = self.weights[0] / (self.weights[0] +
                                       self.weights[1] + self.weights[2])
        blue_ratio = self.weights[2] / (self.weights[0] +
                                        self.weights[1] + self.weights[2])
        return red_ratio, blue_ratio

    # noinspection PyPep8Naming
    def remove_gamma(self, RGB):
        """Removes gamma correction from color

        Parameters
        ----------
        RGB : `array_like <numpy.asarray>` [...]
            gamma corrected RGB color values

        Returns
        -------
        rgb : `array <numpy.ndarray>` [ ``RGB.shape`` ]
            non-gamma corrected RGB color values

        Notes
        -----
        Equivalent to :math:`{rgb} = {RGB}^{\\frac{1}{\\gamma}}`
        """
        return np.asarray(RGB) ** (1.0 / self.gamma)

    def apply_gamma(self, rgb):
        """Applies gamma correction to color

        Parameters
        ----------
        rgb : `array_like <numpy.asarray>` [...]
            non-gamma corrected RGB color values

        Returns
        -------
        RGB : `array <numpy.asarray>` [ ``rgb.shape`` ]
            gamma corrected RGB color values

        Notes
        -----
        Equivalent to :math:`{RGB} = {rgb}^{\\gamma}`"""
        return np.asarray(rgb) ** self.gamma

    def get_limits(self):
        """Returns :math:`U_{max}` and :math:`V_{max}`

        Returns
        -------
        Vmax: `float`
            V channel magnitude limit (:math:`V_{max}`)

        Umax: `float`
            U channel magnitude limit (:math:`U_{max}`)

        Notes
        -----

        :math:`U_{max}` and :math:`V_{max}` represent the limits of the UV color space,
        as defined by\ :cite:`RGBColorProfile-fletcher2019`:

        .. math::

            V_{max} =& \\frac{\\sqrt[3]{K_R}}{\\sqrt[3]{K_R} + \\sqrt[3]{K_B}}\\\\
            U_{max} =& \\frac{\\sqrt[3]{K_B}}{\\sqrt[3]{K_R} + \\sqrt[3]{K_B}}
        """
        red_ratio, blue_ratio = self.get_ratios()
        blue_ratio_cuberoot = blue_ratio ** (1 / 3.0)
        red_ratio_cuberoot = red_ratio ** (1 / 3.0)
        # Get U, V trans_matrix based on color ratios
        vmax = red_ratio_cuberoot / (red_ratio_cuberoot + blue_ratio_cuberoot)
        umax = blue_ratio_cuberoot / (red_ratio_cuberoot + blue_ratio_cuberoot)
        return umax, vmax

    def get_transform(self):
        """Returns the UV to RGB transformation matrix :math:`\\mathbf{K_Q}`.

        Returns
        -------
        transformation: `array <numpy.ndarray>` [3, 2, dtype = `float`]
            transformation matrix :math:`\\mathbf{K_Q}`

        Notes
        -----
        The transformation matrix :math:`\\mathbf{K_Q}` is defined by\ :cite:`RGBColorProfile-fletcher2019`:

        .. math::

            \\mathbf{K_Q} &=
            \\left[\\begin{matrix}
                    0 & \\frac{1-K_R}{V_{max}} \\\\
                    \\frac{K_B\\left( 1-K_B \\right)}{U_{max}\\left( K_B+K_R-1 \\right)} &
                    \\frac{K_R\\left( 1-K_R \\right)}{V_{max}\\left( K_B+K_R-1 \\right)}\\\\
                    \\frac{1-K_B}{U_{max}} & 0 \\\\
            \\end{matrix}\\right]
        """
        red_ratio, blue_ratio = self.get_ratios()
        umax, vmax = self.get_limits()
        trans_matrix = np.zeros((3, 2))
        trans_matrix[0, 1] = (1 - red_ratio / vmax)
        trans_matrix[1, 0] = (blue_ratio * (1 - blue_ratio) /
                              (umax * (blue_ratio + red_ratio - 1)))
        trans_matrix[1, 1] = (red_ratio * (1 - red_ratio) /
                              (vmax * (blue_ratio + red_ratio - 1)))
        trans_matrix[2, 0] = (1 - blue_ratio / umax)
        return trans_matrix

    def get_chroma_limit(self):
        """Return the limiting chroma

        Returns
        -------
        chroma_limit: `float`
            Limiting Chroma for the colorspace

        Notes
        -----
        The limiting chroma is computed from the transformation matrix
        as described in Fletcher 2019\ :cite:`RGBColorProfile-fletcher2019`.
        """
        trans_matrix = self.get_transform()
        chroma_limit = [trans_matrix[0, 1], trans_matrix[2, 0]]
        kg2 = (trans_matrix[1, 0] ** 2 + trans_matrix[1, 1] ** 2)
        chroma_limit.append(- ((trans_matrix[1, 0] + np.sqrt(kg2)) * kg2 /
                               (kg2 + trans_matrix[1, 0] * np.sqrt(kg2))))
        chroma_limit.append(- ((trans_matrix[1, 0] - np.sqrt(kg2)) * kg2 /
                               (kg2 - trans_matrix[1, 0] * np.sqrt(kg2))))
        return 1 / max(chroma_limit)

    def __repr__(self):
        return "{0:s}.{1:s}({2!r:s}, {3:g})".format(type(self).__module__,
                                                    type(self).__name__,
                                                    self.weights, self.gamma)


# pylint: disable=C0103
# These constants should start with lowercase s, as this is the correct
# usage, for writing sRGB
sRGB_HIGH = RGBColorProfile((2126.0, 7152.0, 722.0), 0.5)
sRGB_LOW = RGBColorProfile((2126.0, 7152.0, 722.0), 1)
sRGB = copy(sRGB_HIGH)
# pylint: enable=C0103


def remap(data, scale=None, profile=None, return_int=False, return_metadata=False, **kwargs):
    """Converts an array of complex values to RGB triples

    For 2d arrays of complex numbers the returned array is suitable
    for passing to `pyplot.imshow <matplotlib.pyplot.imshow>` from matplotlib.

    Parameters
    ----------
    data : `array_like <numpy.asarray>` [...]
        Complex input data.

    scale : {`Scale`, 'linear', 'log'}, optional, default: `None`
        Use to define the magnitude scaling of the data. Data is transformed by this object to a interval
        of :math:`[0.0, 1.0]`

        If passed an instance of `Scale`, then this instance is use to scale the data.

        If passed a subclass of `Scale`, an instance is then created of this subclass, as
        ``scale([min(abs(data)),] max(abs(data)), **kwargs)``.

        'linear' or `None` are equivalent to passing `LinearScale`, while 'log' is equivalent to passing `LogScale`

    profile: {`RGBColorProfile`, 'srgb', 'srgb_high', 'srgb_low'}, optional, default: `None`
        ColorProfile representing the RGB colorspace to convert the complex data to.

        'srgb' or `None` are equivalent to passing `sRGB`, while 'srgb_high' or 'srgb_low' are respectively
        equivalent to passing `sRGB_HIGH` or `sRGB_LOW`.

    return_int : `bool`, optional, default: `False`
        If true, returns integers in the interval :math:`[0, 255]`
        rather than floats in the interval :math:`[0.0, 1.0]`.

    return_metadata : `bool`, optional, default: `False`
        Return the scale and profile instance used to generate the mapping.

    Other Parameters
    ----------------
    **kwargs :
        These parameters are passed to the ``scale`` class when creating an automatic instance for scaling.

    Returns
    -------
    rgb : `array <numpy.ndarray>` [ ``data.shape``, 3]
        Array containing RGB color values with the last dimension representing the RGB triplets.

        If ``return_int`` is `False` then the values are floating point in the interval :math:`[0.0, 1.0]`.

        If ``return_int`` is `True` then the values are integers in the interval :math:`[0, 255]`.

    scale : `Scale`
        Present only if ``return_metadata`` = `True`. The actual `Scale` instance used to generate the mapping.

    profile : `RGBColorProfile`
        Present only if ``return_metadata`` = `True`. The actual `RGBColorProfile`
        instance used to generate the mapping.
    """
    data = np.asarray(data, complex)
    if profile is None or isinstance(profile, str) and profile.lower() == 'srgb':
        profile = sRGB
    elif isinstance(profile, str) and profile.lower() == 'srgb_high':
        profile = sRGB_HIGH
    elif isinstance(profile, str) and profile.lower() == 'srgb_low':
        profile = sRGB_LOW
    if not isinstance(profile, RGBColorProfile):
        raise ValueError("profile can't be converted to an instance of RGBColorProfile.")

    if scale is None or isinstance(scale, str) and scale.lower() == 'linear':
        scale = LinearScale
    elif isinstance(scale, str) and scale.lower() == 'log':
        scale = LogScale
    if isinstance(scale, type) and issubclass(scale, Scale):
        spec = getfullargspec(scale)
        num_args = len(spec.args) - 1
        if num_args == 0:
            scale = scale(**kwargs)
        elif num_args == 1:
            scale = scale(np.nanmax(np.abs(data)), **kwargs)
        elif num_args > 1:
            scale = scale(np.nanmin(np.abs(data)), np.nanmax(np.abs(data)), **kwargs)
    if not isinstance(scale, Scale):
        raise ValueError("scale can't be converted to an instance of Scale.")

    trans_matrix = profile.get_transform()
    chroma_limit = profile.get_chroma_limit()
    lightness_cutoff = (4 ** (1 / 3.0)) / 2
    data = np.asarray(scale(data), complex)
    nan = np.isnan(data)
    data[nan] = 0
    magnitude = np.abs(data).reshape(*(data.shape + (1,)))
    data = data.view(float).reshape(*(data.shape + (2,)))
    luminance = (1-(1-lightness_cutoff)*np.clip(magnitude, 0, 1))**3
    chrome = chroma_limit*(1-luminance)
    rbg = np.einsum('qz,...z->...q', trans_matrix, data)
    rbg /= (magnitude > 0)*magnitude + (magnitude == 0)
    rbg *= chrome
    rbg += luminance
    rbg = profile.remove_gamma(rbg)
    rbg[nan, :] = 0
    if return_int:
        ret = (rbg * 255).astype('i8')
    else:
        ret = rbg
    if return_metadata:
        return ret, scale, profile
    else:
        return ret
