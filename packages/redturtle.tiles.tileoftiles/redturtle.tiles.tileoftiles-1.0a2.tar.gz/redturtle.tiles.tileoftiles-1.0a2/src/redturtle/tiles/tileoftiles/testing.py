# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import redturtle.tiles.tileoftiles


class RedturtleTilesTileoftilesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=redturtle.tiles.tileoftiles)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'redturtle.tiles.tileoftiles:default')


REDTURTLE_TILES_TILEOFTILES_FIXTURE = RedturtleTilesTileoftilesLayer()


REDTURTLE_TILES_TILEOFTILES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDTURTLE_TILES_TILEOFTILES_FIXTURE,),
    name='RedturtleTilesTileoftilesLayer:IntegrationTesting'
)


REDTURTLE_TILES_TILEOFTILES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDTURTLE_TILES_TILEOFTILES_FIXTURE,),
    name='RedturtleTilesTileoftilesLayer:FunctionalTesting'
)


REDTURTLE_TILES_TILEOFTILES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        REDTURTLE_TILES_TILEOFTILES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='RedturtleTilesTileoftilesLayer:AcceptanceTesting'
)
