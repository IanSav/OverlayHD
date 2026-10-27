from gettext import bindtextdomain, dgettext, gettext  # , install, textdomain

from Components.International import international
from Tools.Directories import SCOPE_PLUGINS, resolveFilename

__version__ = "2.03"

PluginLocaleDomain = "OverlayHD"
PluginLocalePath = "Extensions/OverlayHD/locale"


def _(text):
	if (translation := dgettext(PluginLocaleDomain, text)) == text:
		translation = gettext(text)
		# print("[%s] Falling back to default translation for '%s'." % (PluginLocaleDomain, text))
	return translation


def localeInit():
	bindtextdomain(PluginLocaleDomain, resolveFilename(SCOPE_PLUGINS, PluginLocalePath))


localeInit()
international.addCallback(localeInit)
