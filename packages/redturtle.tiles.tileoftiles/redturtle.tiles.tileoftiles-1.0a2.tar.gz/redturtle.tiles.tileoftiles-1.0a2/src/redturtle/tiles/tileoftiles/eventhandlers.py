# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_hasattr

from plone.tiles.interfaces import ITileDataStorage
from zope.annotation import IAnnotations
from zope.component import getMultiAdapter

import logging

logger = logging.getLogger('Redturtle TileOfTiles')

def delete_tile_of_tiles(tile, event):
    """
    Here things are quite tricky.
    We have nothing to do if we are not a tile of tiles; in this case skip
    everything.
    Otherwise in tile.context.tiles_list we have the list of tiles grouped
    by tilemanager. So we can get ids of the tiles in this tilemanager id
    (tile.id in the function)
    """
    if tile.__name__ != 'redturtle.tiles.tileoftiles':
        return

    managerid = u'managerId_{}'.format(tile.id)
    if not safe_hasattr(tile.context, 'tiles_list'):
        logger.info('Unable to delete this "tile of tiles" tiles list')
        return

    if managerid not in tile.context.tiles_list:
        logger.info('Tile of tiles it\'s probably empty; nothing to do')
        return

    tiles_list = tile.context.tiles_list[managerid]
    tile_ids_to_delete = [(innertile['tile_type'], innertile['tile_id']) for innertile in tiles_list]

    # Right now we have the list of tiles we have store in the tile of tiles
    # we can find it in two kind of store: in context annotations (persistent
    # tiles) or in a TileDataManager (transient tiles).
    # We will delete it manually. It ain't much but it's honest work.
    persistent_storage = IAnnotations(tile.context)
    traverser = tile.context.restrictedTraverse
    for tile_type, tile_id in tile_ids_to_delete:

        id_for_pstorage = 'plone.tiles.data.{}'.format(tile_id)

        # IF tile is stored in annotations, clean it. We don't need to remove
        # from the manager list of tiles, 'cause we'll remove the entire list
        if id_for_pstorage in persistent_storage:
            del persistent_storage[id_for_pstorage]
            logger.info('Remove tile {} with id {} at {} from persistent storage'.format(tile_type, tile_id, tile.context.absolute_url()))
            continue

        # If the tile is stored in transient storage, get it, get the storage
        # delete the tile. The transient storage is an adapter adapting also the
        # tile
        tile_view = traverser('@@{}/{}'.format(tile_type, tile_id))
        transient_storage = getMultiAdapter(
            (tile.context, tile.request, tile_view), ITileDataStorage)
        if tile_id in transient_storage:
            # XXX don't know why we can't delete it, but plone.tiles do this.
            transient_storage[tile_id] = {}
            logger.info('Remove tile {} with id {} at {} from transient storage'.format(tile_type, tile_id, tile.context.absolute_url()))
            continue
    if managerid in tile.context.tiles_list:
        del tile.context.tiles_list[managerid]
        logger.info('Remove the tile of tiles with id {} from {}'.format(managerid, tile.context.absolute_url()))
