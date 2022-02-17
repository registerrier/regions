# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This module defines text regions in both pixel and sky coordinates.
"""

from astropy.wcs.utils import pixel_to_skycoord, skycoord_to_pixel

from .point import PointPixelRegion, PointSkyRegion
from ..core import PixCoord
from ..core.attributes import ScalarPixCoord, ScalarSkyCoord

__all__ = ['TextSkyRegion', 'TextPixelRegion']


class TextPixelRegion(PointPixelRegion):
    """
    A text string in pixel coordinates.

    Parameters
    ----------
    center : `~regions.PixCoord`
        The leftmost point of the text string before rotation.
    text : str
        The text string.
    meta : `~regions.RegionMeta`, optional
        A dictionary that stores the meta attributes of this region.
    visual : `~regions.RegionVisual`, optional
        A dictionary that stores the visual meta attributes of this
        region.

    Examples
    --------
    .. plot::
        :include-source:

        from regions import PixCoord, TextPixelRegion, RegionVisual
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 1)

        center = PixCoord(x=15, y=10)
        visual = RegionVisual({'textangle': 30})
        reg = TextPixelRegion(center=center, text="Hello World!",
                              visual=visual)
        reg.plot(ax=ax)

        ax.set_xlim(10, 30)
        ax.set_ylim(2.5, 20)
        ax.set_aspect('equal')
    """

    _params = ('center', 'text')
    center = ScalarPixCoord('center',
                            description=('The leftmost pixel position before '
                                         'rotation.'))
    mpl_artist = 'Text'

    def __init__(self, center, text, meta=None, visual=None):
        super().__init__(center, meta, visual)
        self.text = text

    def to_sky(self, wcs):
        center = pixel_to_skycoord(self.center.x, self.center.y, wcs=wcs)
        return TextSkyRegion(center, self.text, meta=self.meta.copy(),
                             visual=self.visual.copy())

    def as_artist(self, origin=(0, 0), **kwargs):
        """
        Return a matplotlib Text object for this region
        (`matplotlib.text.Text`).

        Parameters
        ----------
        origin : array_like, optional
            The ``(x, y)`` pixel position of the origin of the displayed
            image.

        **kwargs : dict
            Any keyword arguments accepted by `~matplotlib.text.Text`.
            These keywords will override any visual meta attributes of
            this region.

        Returns
        -------
        artist : `~matplotlib.text.Text`
            A matplotlib Text object.
        """
        from matplotlib.text import Text

        mpl_kwargs = self.visual.define_mpl_kwargs(self.mpl_artist)
        mpl_kwargs.update(kwargs)

        return Text(self.center.x - origin[0], self.center.y - origin[1],
                    self.text, **mpl_kwargs)


class TextSkyRegion(PointSkyRegion):
    """
    A text string in sky coordinates.

    Parameters
    ----------
    center : `~astropy.coordinates.SkyCoord`
        The leftmost position of the text string before rotation.
    text : str
        The text string.
    meta : `~regions.RegionMeta`, optional
        A dictionary that stores the meta attributes of this region.
    visual : `~regions.RegionVisual`, optional
        A dictionary that stores the visual meta attributes of this
        region.
    """

    _params = ('center', 'text')
    center = ScalarSkyCoord('center',
                            description=('The leftmost position before '
                                         'rotation as a sky coordinate.'))

    def __init__(self, center, text, meta=None, visual=None):
        super().__init__(center, meta, visual)
        self.text = text

    def to_pixel(self, wcs):
        center_x, center_y = skycoord_to_pixel(self.center, wcs=wcs)
        center = PixCoord(center_x, center_y)
        return TextPixelRegion(center, self.text, meta=self.meta.copy(),
                               visual=self.visual.copy())
