# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collective.portlet.existingcontent import _
from plone import api
from plone import schema
# from plone.app.contenttypes.behaviors.leadimage import ILeadImage
# from plone.app.contenttypes.behaviors.leadimage import ILeadImageBehavior
from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.app.contenttypes.behaviors.richtext import IRichTextBehavior
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.portlets.portlets import base
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope.interface import implementer


class IExistingContentPortlet(IPortletDataProvider):
    """Schema for the Existing Content Portlet."""

    content_uid = schema.Choice(
        title=_(u'Select existing content'),
        required=False,
        vocabulary='plone.app.vocabularies.Catalog',
    )
    form.widget(
        'content_uid',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'recentlyUsed': True,
            'selectableTypes': ['Document'],
            'basePath': make_relation_root_path,
        },
    )

    show_title = schema.Bool(
        title=_(u'Show content title'),
        default=False,
        required=False,
    )

    show_description = schema.Bool(
        title=_(u'Show content description'),
        default=False,
        required=False,
    )

    show_text = schema.Bool(
        title=_(u'Show content text'),
        default=False,
        required=False,
    )

    # let's think about another time
    # show_image = schema.Bool(
    #     title=_(u'Show content image (if available)'),
    #     default=False,
    #     required=False,
    # )

    # show_image_caption = schema.Bool(
    #     title=_(u'Show image caption (if leadimage available)'),
    #     default=False,
    #     required=False,
    # )

    # allow_image_popup = schema.Bool(
    #     title=_(u'Allow image popup (if leadimage available)'),
    #     default=False,
    #     required=False,
    # )

    # image_scale = schema.Choice(
    #     title=_(u'Image scale'),
    #     vocabulary='plone.app.vocabularies.ImagesScales',
    #     required=False,
    # )

    portlet_class = schema.TextLine(
        title=_(u'Portlet additional styles'),
        default=u'',
        required=False,
    )


@implementer(IExistingContentPortlet)
class Assignment(base.Assignment):

    def __init__(
        self,
        content_uid=None,
        show_title=False,
        show_description=False,
        show_text=False,
        # show_image=False,
        # show_image_caption=False,
        # allow_image_popup=False,
        # image_scale='mini',
        portlet_class='',
    ):
        self.content_uid = content_uid
        self.show_title = show_title
        self.show_description = show_description
        self.show_text = show_text
        # self.show_image = show_image
        # self.show_image_caption = show_image_caption
        # self.allow_image_popup = allow_image_popup
        # self.image_scale = image_scale
        self.portlet_class = portlet_class

        self.existing_content_title = ''
        self.existing_content_type = ''

        if self.content_uid:
            brains = api.content.find(UID=self.content_uid)
            if brains:
                self.existing_content_title = brains[0].Title
                self.existing_content_type = brains[0].Type

    @property
    def title(self):
        if self.content_uid:
            return _(
                u'Existing ${content_type} "${content_title}"',
                mapping={
                    'content_type': self.existing_content_type,
                    'content_title': self.existing_content_title,
                },
            )
        return _(u'Existing Content')


class AddForm(base.AddForm):
    schema = IExistingContentPortlet
    form_fields = field.Fields(IExistingContentPortlet)
    label = _(u'Add an existing content portlet')
    description = _(u'This portlet displays data of existing content.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    schema = IExistingContentPortlet
    form_fields = field.Fields(IExistingContentPortlet)
    label = _(u'Edit an existing content portlet')
    description = _(u'This portlet displays data of existing content.')


class Renderer(base.Renderer):
    schema = IExistingContentPortlet
    _template = ViewPageTemplateFile('portlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def render(self):
        return self._template()

    @property
    def available(self):
        if self.data.content_uid:
            return True
        return False

    @property
    def existing_content_brain(self):
        brain = None
        if self.data.content_uid:
            brains = api.content.find(UID=self.data.content_uid)
            if len(brains):
                brain = brains[0]
        return brain

    @property
    @memoize
    def existing_content_item(self):
        item = None
        if self.existing_content_brain:
            item = self.existing_content_brain.getObject()
        return item

    @property
    @memoize
    def title(self):
        title = ''
        if self.data.show_title:
            title = self.existing_content_brain.Title
        return title

    @property
    @memoize
    def description(self):
        description = ''
        if self.data.show_description:
            description = self.existing_content_brain.Description
        return description

    @property
    @memoize
    def text(self):
        text = None
        if self.data.show_text:
            item = self.existing_content_item
            if IRichText.providedBy(item) and IRichTextBehavior(item).text:
                text = IRichTextBehavior(item).text.output
        return text

    # let's think about that another time
    # @property
    # @memoize
    # def has_image(self):
    #     has_image = False
    #     if self.data.show_image:
    #         item = self.existing_content_item
    #         if ILeadImage.providedBy(item):
    #             if ILeadImageBehavior(item).image:
    #                 has_image = True
    #     return has_image

    # @property
    # @memoize
    # def has_image(self):
    #     has_image = False
    #     if self.data.show_image:
    #         item = self.existing_content_item
    #         if ILeadImage.providedBy(item):
    #             if ILeadImageBehavior(item).image:
    #                 has_image = True
    #     return has_image

    # @property
    # @memoize
    # def image_caption(self):
    #     image_caption = ''
    #     if self.has_image and self.data.show_image_caption:
    #         item = self.existing_content_item
    #         if ILeadImage.providedBy(item):
    #             return ILeadImageBehavior(item).image_caption
    #     return image_caption
