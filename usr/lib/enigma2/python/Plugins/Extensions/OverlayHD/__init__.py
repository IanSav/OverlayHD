from gettext import bindtextdomain, dgettext, gettext  # , install, textdomain

from Components.International import international
from Tools.Directories import SCOPE_PLUGINS, resolveFilename

PluginLocaleDomain = "OverlayHD"
PluginLocalePath = "Extensions/OverlayHD/locale"

__version__ = "2.01"


def _(text):
	translation = dgettext(PluginLocaleDomain, text)
	if translation == text:
		translation = gettext(text)
		print("[%s] Falling back to default translation for '%s'." % (PluginLocaleDomain, text))
	return translation


def localeInit():
	localePath = resolveFilename(SCOPE_PLUGINS, PluginLocalePath)
	# install(PluginLocaleDomain, localePath, names=("ngettext", "pgettext"))
	bindtextdomain(PluginLocaleDomain, localePath)
	# textdomain(PluginLocaleDomain)


international.addCallback(localeInit)
