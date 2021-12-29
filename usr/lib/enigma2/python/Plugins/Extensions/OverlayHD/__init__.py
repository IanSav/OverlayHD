from gettext import bindtextdomain, dgettext, gettext, install, textdomain

from Components.Language import language
from Tools.Directories import SCOPE_PLUGINS, resolveFilename

PluginLanguageDomain = "OverlayHD"
PluginLanguagePath = "Extensions/OverlayHD/locale"


def localeInit():
	languagePath = resolveFilename(SCOPE_PLUGINS, PluginLanguagePath)
	# install(PluginLanguageDomain, languagePath, names=("ngettext", "pgettext"))
	bindtextdomain(PluginLanguageDomain, languagePath)
	# textdomain(PluginLanguageDomain)


def _(txt):
	if dgettext(PluginLanguageDomain, txt):
		return dgettext(PluginLanguageDomain, txt)
	else:
		print("[%s] Falling back to default translation for '%s'." % (PluginLanguageDomain, txt))
		return gettext(txt)


language.addCallback(localeInit)
