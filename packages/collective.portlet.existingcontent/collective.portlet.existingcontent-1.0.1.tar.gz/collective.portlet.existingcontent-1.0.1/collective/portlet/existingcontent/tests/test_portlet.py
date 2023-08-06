# -*- coding: utf-8 -*-
from collective.portlet.existingcontent import portlet as existing_content_portlet
from collective.portlet.existingcontent.testing import COLLECTIVE_PORTLET_EXISTINGCONTENT_INTEGRATION_TESTING
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.textfield import RichTextValue
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from Products.GenericSetup.utils import _getDottedName
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class TestPortletBase(unittest.TestCase):

    layer = COLLECTIVE_PORTLET_EXISTINGCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.doc = self.portal.doc


class TestPortlet(TestPortletBase):

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='portlets.ExistingContent')
        self.assertEqual(portlet.addview, 'portlets.ExistingContent')

    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name='portlets.ExistingContent')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEqual(
            ['plone.app.portlets.interfaces.IDefaultPortletManager'],
            registered_interfaces,
        )

    def testInterfaces(self):
        portlet = existing_content_portlet.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='portlets.ExistingContent')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn',
        )
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(
            isinstance(
                mapping.values()[0],
                existing_content_portlet.Assignment,
            ),
        )

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.portal.REQUEST

        mapping['foo'] = existing_content_portlet.Assignment(
            content_uid=self.doc.UID(),
        )
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertTrue(
            isinstance(
                editview,
                existing_content_portlet.EditForm,
            ),
        )

    def testRenderer(self):
        context = self.portal
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager,
            name='plone.leftcolumn',
            context=self.portal,
        )
        assignment = existing_content_portlet.Assignment(
            content_uid=self.doc.UID(),
        )

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment),
            IPortletRenderer,
        )
        self.assertTrue(
            isinstance(
                renderer,
                existing_content_portlet.Renderer,
            ),
        )


class TestRenderer(TestPortletBase):

    def renderer(
        self,
        context=None,
        request=None,
        view=None,
        manager=None,
        assignment=None,
    ):
        context = self.portal
        request = request or self.portal.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager,
            name='plone.leftcolumn',
            context=self.portal,
        )
        assignment = assignment or existing_content_portlet.Assignment(
            content_uid=self.doc.UID(),
        )

        return getMultiAdapter(
            (context, request, view, manager, assignment),
            IPortletRenderer,
        )

    def test_availability(self):
        """an empty portlet may exist, but it's not displayed."""
        renderer = self.renderer(
            assignment=existing_content_portlet.Assignment(),
        )
        self.assertFalse(renderer.available)

        renderer = self.renderer(
            assignment=existing_content_portlet.Assignment(
                content_uid=self.doc.UID(),
            ),
        )
        self.assertTrue(renderer.available)

    def test_portlet_title(self):
        renderer = self.renderer(
            assignment=existing_content_portlet.Assignment(
                content_uid=self.doc.UID(),
                show_title=True,
            ),
        )

        self.assertEqual(
            renderer.title,
            self.doc.title,
        )

        self.doc.title = 'a changed title'
        self.doc.reindexObject()

        renderer = self.renderer(assignment=renderer.data)

        self.assertEqual(
            renderer.title,
            self.doc.title,
        )

    def test_portlet_description(self):
        renderer = self.renderer(
            assignment=existing_content_portlet.Assignment(
                content_uid=self.doc.UID(),
                show_description=True,
            ),
        )
        self.assertEqual(
            renderer.description,
            self.doc.description,
        )
        self.doc.description = 'a description'
        self.doc.reindexObject()

        renderer = self.renderer(assignment=renderer.data)

        self.assertEqual(
            renderer.description,
            self.doc.description,
        )

    def test_portlet_text(self):
        renderer = self.renderer(
            assignment=existing_content_portlet.Assignment(
                content_uid=self.doc.UID(),
                show_text=True,
            ),
        )

        self.assertEqual(
            renderer.text,
            self.doc.text,
        )

        self.doc.text = RichTextValue(
            '<p>lorem ipsum dolor ...</p>',
            mimeType='text/html',
            outputMimeType='text/x-html-safe',
        )
        self.doc.reindexObject()

        renderer = self.renderer(assignment=renderer.data)

        self.assertEqual(
            renderer.text,
            self.doc.text.output,
        )

    def test_portlet_rendering(self):
        self.doc.description = 'a description'
        self.doc.text = RichTextValue(
            '<p>lorem ipsum dolor ...</p>',
            mimeType='text/html',
            outputMimeType='text/x-html-safe',
        )
        self.doc.reindexObject()

        renderer = self.renderer(
            assignment=existing_content_portlet.Assignment(
                content_uid=self.doc.UID(),
                show_title=True,
                show_description=True,
                show_text=True,
            ),
        )

        renderer_output = renderer.render()
        self.assertIn(self.doc.title, renderer_output)
        self.assertIn(self.doc.description, renderer_output)
        self.assertIn(self.doc.text.output, renderer_output)
