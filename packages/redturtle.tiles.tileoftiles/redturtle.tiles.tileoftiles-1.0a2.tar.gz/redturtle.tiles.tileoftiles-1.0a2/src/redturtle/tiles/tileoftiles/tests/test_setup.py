# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from redturtle.tiles.tileoftiles.testing import REDTURTLE_TILES_TILEOFTILES_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that redturtle.tiles.tileoftiles is properly installed."""

    layer = REDTURTLE_TILES_TILEOFTILES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if redturtle.tiles.tileoftiles is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'redturtle.tiles.tileoftiles'))

    def test_browserlayer(self):
        """Test that IRedturtleTilesTileoftilesLayer is registered."""
        from redturtle.tiles.tileoftiles.interfaces import (
            IRedturtleTilesTileoftilesLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IRedturtleTilesTileoftilesLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = REDTURTLE_TILES_TILEOFTILES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['redturtle.tiles.tileoftiles'])

    def test_product_uninstalled(self):
        """Test if redturtle.tiles.tileoftiles is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'redturtle.tiles.tileoftiles'))

    def test_browserlayer_removed(self):
        """Test that IRedturtleTilesTileoftilesLayer is removed."""
        from redturtle.tiles.tileoftiles.interfaces import \
            IRedturtleTilesTileoftilesLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           IRedturtleTilesTileoftilesLayer,
           utils.registered_layers())
