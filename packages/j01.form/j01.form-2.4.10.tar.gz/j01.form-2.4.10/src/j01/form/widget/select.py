###############################################################################
#
# Copyright (c) 2014 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Select widget
$Id: select.py 4977 2019-05-09 05:28:48Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import zope.component
import zope.interface
import zope.i18n
import zope.i18nmessageid
import zope.schema.interfaces

import z3c.form.interfaces
import z3c.form.widget
import z3c.form.browser.widget

from j01.form import interfaces
from j01.form.layer import IFormLayer
from j01.form.widget.widget import WidgetMixin

_ = zope.i18nmessageid.MessageFactory('p01')


class SelectWidgteBase(WidgetMixin, z3c.form.browser.widget.HTMLSelectWidget,
    z3c.form.widget.SequenceWidget):
    """Select widget base class"""

    klass = u'select-control form-control'
    css = u'select'
    prompt = False

    noValueMessage = _('No value')
    promptMessage = _('Select a value ...')

    # Internal attributes
    _adapterValueAttributes = \
        z3c.form.widget.SequenceWidget._adapterValueAttributes + \
        ('noValueMessage', 'promptMessage', 'prompt')

    def isSelected(self, term):
        return term.token in self.value

    @property
    def items(self):
        if self.terms is None:  # update() has not been called yet
            return ()
        items = []
        if (not self.required or self.prompt) and self.multiple is None:
            message = self.noValueMessage
            if self.prompt:
                message = self.promptMessage
            items.append({
                'id': self.id + '-novalue',
                'value': self.noValueToken,
                'content': message,
                'selected': self.value == []
                })

        ignored = set(self.value)

        def addItem(idx, term, prefix=''):
            selected = self.isSelected(term)
            if selected and term.token in ignored:
                ignored.remove(term.token)
            id = '%s-%s%i' % (self.id, prefix, idx)
            content = term.token
            if zope.schema.interfaces.ITitledTokenizedTerm.providedBy(term):
                content = zope.i18n.translate(
                    term.title, context=self.request, default=term.title)
            items.append(
                {'id': id, 'value': term.token, 'content': content,
                 'selected': selected})

        for idx, term in enumerate(self.terms):
            addItem(idx, term)

        if ignored:
            # some values are not displayed, probably they went away from the vocabulary
            for idx, token in enumerate(sorted(ignored)):
                try:
                    term = self.terms.getTermByToken(token)
                except LookupError:
                    # just in case the term really went away
                    continue

                addItem(idx, term, prefix='missing-')
        return items

################################################################################
#
# select widget

class SelectWidget(SelectWidgteBase):
    """Select widget"""

    zope.interface.implementsOnly(interfaces.ISelectWidget)


class MultiSelectWidget(SelectWidget):
    """Select widget implementation."""

    zope.interface.implementsOnly(interfaces.IMultiSelectWidget)

    prompt = False
    size = 5
    multiple = 'multiple'


################################################################################
#
# select picker, see http://silviomoreto.github.io/bootstrap-select/ for options

JAVASCRIPT = """<script type="text/javascript">
$(document).ready(function(){
    $('#%(id)s').selectpicker();
});
</script>
"""

class SelectPickerOptions(object):
    """SelectPicker options"""

#    options = {
#        style: 'btn-default',
#        size: 'auto',
#        title: null,
#        selectedTextFormat : 'values',
#        noneSelectedText : 'Nothing selected',
#        noneResultsText : 'No results match',
#        countSelectedText: '{0} of {1} selected',
#        maxOptionsText: ['Limit reached ({n} {var} max)', 'Group limit reached ({n} {var} max)', ['items','item']],
#        width: false,
#        container: false,
#        hideDisabled: false,
#        showSubtext: false,
#        showIcon: true,
#        showContent: true,
#        dropupAuto: true,
#        header: false,
#        liveSearch: false,
#        actionsBox: false,
#        multipleSeparator: ', ',
#        iconBase: 'glyphicon',
#        tickIcon: 'glyphicon-ok',
#        maxOptions: false,
#        }

class SelectPickerWidget(SelectWidget):
    """SelectPickerWidget"""

    zope.interface.implementsOnly(interfaces.ISelectPickerWidget)

    klass = u'select-picker-control form-control'
    css = u'select-picker'

    @property
    def javascript(self):
        return JAVASCRIPT % {'id': self.id}


class MultiSelectPickerWidget(MultiSelectWidget):
    """MultiSelectPickerWidget"""

    zope.interface.implementsOnly(interfaces.IMultiSelectPickerWidget)

    klass = u'select-picker-control form-control'
    css = u'select-picker'

    @property
    def javascript(self):
        return JAVASCRIPT % {'id': self.id}


################################################################################
#
# group select

class GroupSelectWidget(SelectWidget):
    """Select widget with optgroup support"""

    zope.interface.implementsOnly(interfaces.IGroupSelectWidget)

    def appendSubTerms(self, groupName, items, subTerms, count):
        """Append collected sub terms as optgroup subItems"""
        subItems = []
        for subTerm in subTerms:
            id = '%s-%i' % (self.id, count)
            content = zope.i18n.translate(subTerm.title,
                context=self.request, default=subTerm.title)
            subItems.append(
                {'id': id,
                 'value': subTerm.token,
                 'content': content,
                 'selected': self.isSelected(subTerm)})
        items.append({'isGroup': True,
                      'content': groupName,
                      'subItems': subItems})

    @property
    def items(self):
        if self.terms is None:
            # update() has not been called yet
            return ()
        items = []
        if (not self.required or self.prompt) and self.multiple is None:
            message = self.noValueMessage
            if self.prompt:
                message = self.promptMessage
            items.append({
                'isGroup': False,
                'id': self.id + '-novalue',
                'value': self.noValueToken,
                'content': message,
                'selected': self.value == []
                })

        # setup optgroup and option items
        groupName = None
        subTerms = []
        for count, term in enumerate(self.terms):
            if term.isGroup:
                if groupName is not None and subTerms:
                    self.appendSubTerms(groupName, items, subTerms, count)
                     # set empty subTerms list
                    subTerms = []
                # set as next groupName
                groupName = zope.i18n.translate(term.title,
                    context=self.request, default=term.title)
            else:
                # collect sub item terms
                subTerms.append(term)

        # render the last collected sub terms with the latest groupName
        if groupName is not None:
            self.appendSubTerms(groupName, items, subTerms, count)

        return items


################################################################################
#
# html select
# https://github.com/jsmodules/ddslick

# NOTE: this requires the mCustomScrollbar javascript
#       http://manos.malihu.gr/jquery-custom-content-scroller/
DDSLICK_SCROLLBAR_JAVASCRIPT = """
    $('#%(id)s .dd-options').mCustomScrollbar({
        alwaysShowScrollbar: 0,
        scrollInertia: 100,
        mouseWheel: {
            enable: true,
            preventDefault: true
        },
        theme: 'dark-3',
        scrollButtons:{
            enable: true
        }
    });
"""

DDSLICK_JAVASCRIPT = """<script type="text/javascript">
$(document).ready(function() {
    $('#%(id)s').ddslick({
        width: "%(width)s",
        background: "%(background)s",
        selectText: "%(label)s",
        showSelectedHTML: false
    });%(mCustomScrollbar)s
});
</script>
"""
class DDSlickSelectWidget(SelectWidgteBase):
    """DDSlick select widget

    Title, text and description mut get translated during vocbaulary setup.
    We don't provide term translation based in ITitledTokenizedTerm.
    """

    zope.interface.implementsOnly(interfaces.IDDSlickSelectWidget)

    klass = u'ddslick-control form-control'
    css = u'ddslick'
    width = "100%"
    background = "#FFFFFF"
    showScrollbar = False

    def addItem(self, idx, term, items, ignored, prefix=''):
        selected = self.isSelected(term)
        if selected and term.token in ignored:
            ignored.remove(term.token)
        id = '%s-%s%i' % (self.id, prefix, idx)
        items.append({
            'id': id,
            'value': term.token,
            'img': getattr(term, 'img', None),
            'text': getattr(term, 'text', None),
            'description': getattr(term, 'description', None),
            'content': term.title,
            'selected': selected,
            })

    @property
    def items(self):
        if self.terms is None:  # update() has not been called yet
            return ()
        items = []
        if (not self.required or self.prompt) and self.multiple is None:
            message = self.noValueMessage
            if self.prompt:
                message = self.promptMessage
            items.append({
                'id': self.id + '-novalue',
                'value': self.noValueToken,
                'content': message,
                'img': None,
                'text': message,
                'description': None,
                'selected': self.value == []
                })

        ignored = set(self.value)

        for idx, term in enumerate(self.terms):
            self.addItem(idx, term, items, ignored)

        if ignored:
            # some values are not displayed, probably they went away from the vocabulary
            for idx, token in enumerate(sorted(ignored)):
                try:
                    term = self.terms.getTermByToken(token)
                except LookupError:
                    # just in case the term really went away
                    continue
                self.addItem(idx, term, items, ignored, prefix='missing-')
        return items

    @property
    def javascript(self):
        if self.showScrollbar:
            mCustomScrollbar = DDSLICK_SCROLLBAR_JAVASCRIPT % {
                'id': self.id,
            }
        else:
            mCustomScrollbar = ''
        return DDSLICK_JAVASCRIPT % {
            'id': self.id,
            'label': self.label,
            'width': self.width,
            'background': self.background,
            'mCustomScrollbar': mCustomScrollbar,
            }




# adapter
@zope.component.adapter(zope.schema.interfaces.IChoice, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def ChoiceWidgetDispatcher(field, request):
    """Dispatch widget for IChoice based also on its source."""
    return zope.component.getMultiAdapter((field, field.vocabulary, request),
                                          z3c.form.interfaces.IFieldWidget)


@zope.component.adapter(zope.schema.interfaces.IChoice,
                        zope.interface.Interface, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def SelectFieldWidget(field, source, request):
    """IFieldWidget factory for SelectWidget."""
    return z3c.form.widget.FieldWidget(field, SelectWidget(request))


@zope.component.adapter(
    zope.schema.interfaces.IUnorderedCollection, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def CollectionSelectFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return z3c.form.widget.FieldWidget(field, MultiSelectWidget(request))


@zope.component.adapter(
    zope.schema.interfaces.IUnorderedCollection,
    zope.schema.interfaces.IChoice, IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def CollectionChoiceSelectFieldWidget(field, value_type, request):
    """IFieldWidget factory for SelectWidget."""
    return z3c.form.widget.FieldWidget(field, SelectWidget(request))


# get
def getSelectWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return z3c.form.widget.FieldWidget(field, SelectWidget(request))


def getMultiSelectWidget(field, request):
    """IFieldWidget factory for MultiSelectWidget."""
    return z3c.form.widget.FieldWidget(field, MultiSelectWidget(request))


def getSelectPickerWidget(field, request):
    """IFieldWidget factory for SelectPickerWidget."""
    return z3c.form.widget.FieldWidget(field, SelectPickerWidget(request))


def getMultiSelectPickerWidget(field, request):
    """IFieldWidget factory for MultiSelectPickerWidget."""
    return z3c.form.widget.FieldWidget(field, MultiSelectPickerWidget(request))


def getGroupSelectWidget(field, request):
    """IFieldWidget factory for GroupSelectWidget."""
    return z3c.form.widget.FieldWidget(field, GroupSelectWidget(request))


def getDDSlickSelectWidget(field, request):
    """IFieldWidget factory for DDSlickSelectWidget."""
    return z3c.form.widget.FieldWidget(field, DDSlickSelectWidget(request))


def getDDSlickScrollbarSelectWidget(field, request):
    """IFieldWidget factory for DDSlickSelectWidget."""
    widget = z3c.form.widget.FieldWidget(field, DDSlickSelectWidget(request))
    widget.showScrollbar = True
    return widget
