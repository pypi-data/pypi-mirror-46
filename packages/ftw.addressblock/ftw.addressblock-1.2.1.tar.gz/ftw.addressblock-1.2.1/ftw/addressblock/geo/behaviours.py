from collective.geo.behaviour import MessageFactory as CGMF
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from zope import schema
from zope.interface import alsoProvides
from zope.interface import provider


@provider(IFormFieldProvider)
class IMapPreferencesSchema(form.Schema):
    """Additional map preferences
    """

    form.fieldset(
        'coordinates',
        label=CGMF(u'Coordinates'),
        fields=[
            'maplayer',
            'zoomlevel',
        ]
    )

    form.mode(zoomlevel='hidden')
    zoomlevel = schema.TextLine(
        title=u'Zoom',
        required=False,
    )

    form.mode(maplayer='hidden')
    maplayer = schema.TextLine(
        title=u'Maplayer',
        required=False
    )


alsoProvides(IMapPreferencesSchema, IFormFieldProvider)
