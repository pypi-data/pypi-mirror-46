# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.portlet.existingcontent.testing import COLLECTIVE_PORTLET_EXISTINGCONTENT_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.portlet.existingcontent is properly installed."""

    layer = COLLECTIVE_PORTLET_EXISTINGCONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.portlet.existingcontent is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.portlet.existingcontent'))

    def test_browserlayer(self):
        """Test that ICollectivePortletExistingContentLayer is registered."""
        from collective.portlet.existingcontent.interfaces import (
            ICollectivePortletExistingContentLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectivePortletExistingContentLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_PORTLET_EXISTINGCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.portlet.existingcontent'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.portlet.existingcontent is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.portlet.existingcontent'))

    def test_browserlayer_removed(self):
        """Test that ICollectivePortletExistingContentLayer is removed."""
        from collective.portlet.existingcontent.interfaces import \
            ICollectivePortletExistingContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectivePortletExistingContentLayer,
            utils.registered_layers())
