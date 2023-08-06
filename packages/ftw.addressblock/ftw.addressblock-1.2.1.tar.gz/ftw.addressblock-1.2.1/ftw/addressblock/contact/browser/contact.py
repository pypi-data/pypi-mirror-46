from email.header import Header
from email.mime.text import MIMEText

import pkg_resources

from ftw.addressblock import _
from ftw.addressblock.interfaces import IAddressBlock
from ftw.subsite.interfaces import ISubsite
from plone import api
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from plone.registry.interfaces import IRegistry
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import WidgetActionExecutionError
from z3c.schema import email as emailfield
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import Invalid

IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'


class IContactView(Interface):
    """
    Interface for z3c.form.
    """
    sender = schema.TextLine(
        title=_(u'Sender_Name', default=u'Name'),
        required=True,
    )
    email = emailfield.RFC822MailAddress(
        title=_(u'mail_address', default='Email'),
        required=True,
    )
    subject = schema.TextLine(
        title=_(u'label_subject', default='Subject'),
        required=True,
    )
    message = schema.Text(
        title=_(u'label_message', default='Message'),
        required=True,
    )
    captcha = schema.TextLine(
        title=u'ReCaptcha',
        required=False,
    )


class ContactForm(form.Form):
    label = _(u'label_send_feedback', default=u'Send Feedback')
    fields = field.Fields(IContactView)

    # don't use context to get widget data
    ignoreContext = True

    def updateWidgets(self):
        captcha_enabled = self.recaptcha_enabled()
        if captcha_enabled:
            self.fields['captcha'].widgetFactory = ReCaptchaFieldWidget

        super(ContactForm, self).updateWidgets()

        if not captcha_enabled:
            # Simply delete the widget instead of trying to set hidden mode,
            # which caused a `ComponentLookupError` in a special case. Please
            # see `test_captcha_no_component_lookup_error`.
            del self.widgets['captcha']

    def recaptcha_enabled(self):
        registry = getUtility(IRegistry, context=self)
        private_key = registry.get(
            'plone.formwidget.recaptcha.interfaces.IReCaptchaSettings.private_key',
            u''
        )
        public_key = registry.get(
            'plone.formwidget.recaptcha.interfaces.IReCaptchaSettings.public_key',
            u''
        )
        return public_key and private_key and api.user.is_anonymous()

    @button.buttonAndHandler(_(u'Send Email'))
    def handleApply(self, action):
        data, errors = self.extractData()

        if self.recaptcha_enabled():
            captcha = getMultiAdapter((aq_inner(self.context), self.request),
                                      name='recaptcha')
            if not captcha.verify():
                raise WidgetActionExecutionError(
                    'captcha',
                    Invalid(
                        _('The captcha code you entered was wrong, '
                          'please enter the new one.')
                    )
                )

        if errors:
            return

        message = data.get('message')
        email = data.get('email')
        subject = data.get('subject')
        sender = data.get('sender').replace(',', ' ')
        self.send_feedback(email, subject, message, sender)
        msg = _(u'info_email_sent', default=u'The email was sent.')
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        return self.redirect()

    @button.buttonAndHandler(_(u'button_cancel', default=u'Cancel'))
    def handle_cancel(self, action):
        return self.redirect()

    def redirect(self):
        url = self.context.aq_parent.absolute_url()
        return self.request.RESPONSE.redirect(url)

    def get_to_address(self):
        """
        Check if the call came from addressblock, subsite or something else and
        change email recipient accordingly
        """
        portal = api.portal.get()
        to_email = portal.getProperty('email_from_address', '')

        if IS_PLONE_5:
            reg = api.portal.get_tool('portal_registry')
            from_email_field = reg._records.get('plone.email_from_address')
            if not from_email_field.value and not to_email:
                # especially for testing reasons we need to set a value here
                # if none is registered on the page in plone5
                from_email_field._set_value('test@localhost')
                to_email = from_email_field.value
            else:
                to_email = from_email_field.value

        nav_root = api.portal.get_navigation_root(self.context)
        if ISubsite.providedBy(nav_root):
            to_email = self.context.from_email or to_email
        elif self.is_addressblock():
            to_email = self.context.email or to_email

        return to_email

    def is_addressblock(self):
        return IAddressBlock.providedBy(self.context)

    def send_feedback(self, recipient, subject, message, sender):
        """Send a feedback email to the email address defined in
        the addressblock.
        """
        mh = getToolByName(self.context, 'MailHost')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        msg_body = translate(
            _(
                u'feedback_email_text',
                default='${sender} sends you a message:\n\n${msg}',
                mapping={
                    'sender': u'{0} ({1})'.format(sender, recipient),
                    'msg': message,
                },
            ),
            context=self.request,
        )

        msg = MIMEText(msg_body.encode('utf-8'), 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')

        if IS_PLONE_5:
            from plone import api
            reg = api.portal.get_tool('portal_registry')
            from_email_field = reg._records.get('plone.email_from_address')
            from_name_field = reg._records.get('plone.email_from_name')
            from_name = from_name_field.value
            if not from_email_field.value:
                # especially for testing reasons we need to set a value here
                # if none is registered on the page in plone5
                from_email_field._set_value('test@localhost')
                from_email = from_email_field.value
            else:
                from_email = from_email_field.value
        else:
            from_name = safe_unicode(portal.getProperty('email_from_name'))
            from_email = safe_unicode(portal.getProperty('email_from_address'))
        msg['From'] = Header(u'{0} <{1}>'.format(from_name, from_email), 'utf-8')

        msg['Reply-To'] = Header(u'{0} <{1}>'.format(
            safe_unicode(sender),
            safe_unicode(recipient),
        ), 'utf-8')

        msg['To'] = self.get_to_address()

        mh.send(msg)


ContactView = wrap_form(ContactForm)
