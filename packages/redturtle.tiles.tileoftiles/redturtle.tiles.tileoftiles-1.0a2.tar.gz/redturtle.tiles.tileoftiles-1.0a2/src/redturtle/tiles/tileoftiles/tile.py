# -*- encoding:utf-8 *-
from plone import tiles
import base64


class TileOfTiles(tiles.PersistentTile):
    """
    """

    def get_style(self):
        style = []
        bgcolor = self.data.get("background_color") or ""
        if bgcolor:
            style.append("background-color: {}".format(bgcolor))
        bgimage = self.data.get("background_image") or None
        if bgimage:
            b64 = base64.b64encode(bgimage.data)
            style.append(
                'background-image: url("data:image/png;base64,{}")'.format(b64)
            )
        color = self.data.get("text_color") or ""
        if color:
            style.append("color: {}".format(color))
        style.append(
            "min-height: {}".format(self.data.get("min_height") or "0")
        )
        return "; ".join(style)
