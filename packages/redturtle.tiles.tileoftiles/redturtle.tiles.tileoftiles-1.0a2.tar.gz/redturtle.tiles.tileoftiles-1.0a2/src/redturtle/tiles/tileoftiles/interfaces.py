# -*- coding: utf-8 -*-
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from redturtle.tiles.management.interfaces import (
    IRedturtleTilesManagementLayer,
)
from redturtle.tiles.tileoftiles import _
from zope import schema


class IRedturtleTilesTileoftilesLayer(IRedturtleTilesManagementLayer):
    """Marker interface that defines a browser layer."""


class ITileOfTiles(model.Schema):
    """ """

    title = schema.TextLine(
        title=_("label_tile_title", u"Tile title"), required=False
    )

    background_color = schema.TextLine(
        title=_("Background color"),
        description=_(
            "Please set a hex code. This property will be overriden by the background image."
        ),
        required=False,
    )

    text_color = schema.TextLine(
        title=_("Text color"),
        description=_("Please set a hex code."),
        required=False,
    )

    background_image = NamedBlobFile(
        title=_("Background image"),
        description=_("Upload an image to be used as tile background"),
        required=False,
    )

    min_height = schema.TextLine(
        title=_("Minimum height"),
        description=_(
            "Set a minimum height for the tile, in pixels. e.g. 200px"
        ),
        default=u"50px",
        required=False,
    )

    css_class = schema.TextLine(
        title=_("Additional classes"),
        description=_(
            "Write here a class or list of classes that will be added to the tile"
        ),
        required=False,
    )
