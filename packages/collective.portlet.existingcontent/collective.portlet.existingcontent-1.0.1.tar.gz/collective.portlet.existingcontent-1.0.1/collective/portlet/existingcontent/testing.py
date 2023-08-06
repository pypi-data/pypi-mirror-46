# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import collective.portlet.existingcontent


class CollectivePortletExistingContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.portlet.existingcontent)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.portlet.existingcontent:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        doc = api.content.create(
            container=portal,
            type='Document',
            title=u'Content for Portlet',
            id='doc',
        )
        api.content.transition(doc, transition='publish')


COLLECTIVE_PORTLET_EXISTINGCONTENT_FIXTURE = CollectivePortletExistingContentLayer()


COLLECTIVE_PORTLET_EXISTINGCONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PORTLET_EXISTINGCONTENT_FIXTURE,),
    name='CollectivePortletExistingContentLayer:IntegrationTesting',
)


COLLECTIVE_PORTLET_EXISTINGCONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PORTLET_EXISTINGCONTENT_FIXTURE,),
    name='CollectivePortletExistingContentLayer:FunctionalTesting',
)


COLLECTIVE_PORTLET_EXISTINGCONTENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_PORTLET_EXISTINGCONTENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectivePortletExistingContentLayer:AcceptanceTesting',
)
