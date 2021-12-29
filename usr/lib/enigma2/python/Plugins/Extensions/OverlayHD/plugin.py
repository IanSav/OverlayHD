# ===========================================================================
#
# OverlayHD Skin Manager
#
# Version Date - 30-Dec-2021
# Remember to change version number variable below!!!
#
# Repository - https://github.com/IanSav/OverlayHD
# Coding by IanSav (c) 2015-2021
#
# This skin and plugin were originally developed for the Beyonwiz Australia
# distribution of Enigma2.  This skin and code is free to use and may be
# distributed and used on Beyonwiz and other Enigma2 based firmware.
#
# This skin and plugin are NOT free software, they are open source.  You are
# allowed to use and modify them so long as you attribute and acknowledge the
# source and original author.  That is, the license and original author
# details must be retained at all times.
#
# This skin and plugin was developed and enhanced as open source software
# they may not be commercially distributed or included in any commercial
# software or used for commercial benefit.
#
# If you wish to contribute fixes or enhancements to the skin or plugin then
# please drop me a line at IS.OzPVR (at) gmail.com.  If you wish to use this
# skin or plugin as part of a commercial product please contact me.
#
# ===========================================================================

from errno import ENOENT
from os import listdir, makedirs, readlink, remove, symlink, unlink
from os.path import dirname, exists, isdir, isfile, islink, join as pathjoin, splitext
from random import randrange
from shutil import copy2, move, rmtree
from xml.etree.cElementTree import Element, ElementTree, SubElement

try:
	from Components.SystemInfo import BoxInfo
	distro = BoxInfo.getItem("distro", "enigma2").lower()
	displayDistro = BoxInfo.getItem("displaydistro", "Enigma2")
except ImportError as err:
	print("[OverlayHD] Note: BoxInfo is not available.")
	try:
		from boxbranding import getImageDistro
		distro = getImageDistro().lower()
		displayDistro = distro
	except ImportError as err:
		print("[OverlayHD] Note: Boxbranding is not available, OpenPLi assumed.")
		distro = "openpli"
		displayDistro = "OpenPLi"

from enigma import eEnv, gRGB

from skin import colors, domScreens, fonts, reloadWindowStyles
from Components.ActionMap import HelpableActionMap
from Components.config import ConfigEnableDisable, ConfigSelection, ConfigSubsection, ConfigYesNo, config, configfile
from Components.Label import Label
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.HelpMenu import HelpableScreen
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Setup import Setup
from Screens.Standby import QUIT_RESTART, TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.BoundFunction import boundFunction
from Tools.Directories import SCOPE_CONFIG, SCOPE_GUISKIN, SCOPE_MEDIA, SCOPE_PLUGIN, SCOPE_SKINS, fileReadXML, resolveFilename

MODULE_NAME = __name__.split(".")[-1]
PLUGIN_VERSION_NUMBER = "1.92"

DISTRO_MENU_IDVAL = 0
DISTRO_SCREENLIST = 1

distroModes = {
	"beyonwiz": ("osd_menu", ("Beyonwiz")),
	"openatv": ("system", ("OpenATV", "Enigma2")),
	"openpli": ("gui", ("OpenPLi", "Enigma2")),
	"openvision": ("osd_menu", ("OpenVision", "Enigma2")),
	"openvix": ("skinsetup", ("OpenViX", "Enigma2"))
}

colorChoices = [
	("Arsenic", _("Arsenic")),
	("Black", _("Black")),
	("Blue", _("Blue")),
	("Charcoal", _("Charcoal")),
	("Coral", _("Coral")),
	("Cyan", _("Cyan")),
	("DarkerBlue", _("Darker Blue")),
	("DarkGrey", _("Dark Grey")),
	("DavysGrey", _("Davy's Grey")),
	("DeepBlue", _("Deep Blue")),
	("DeepGrey", _("Deep Grey")),
	("DeepPink", _("Deep Pink")),
	("DimGrey", _("Dim Grey")),
	("DodgerBlue", _("Dodger Blue")),
	("DullBlue", _("Dull Blue")),
	("DullGreen", _("Dull Green")),
	("DullRed", _("Dull Red")),
	("DullYellow", _("Dull Yellow")),
	("EerieBlack", _("Eerie Black")),
	("EgyptianBlue", _("Egyptian Blue")),
	("Gainsboro", _("Gainsboro")),
	("Gold", _("Gold")),
	("Green", _("Green")),
	("Grey", _("Grey")),
	("GreyBlue", _("Grey Blue")),
	("Gunmetal", _("Gunmetal")),
	("Indigo", _("Indigo")),
	("Jet", _("Jet")),
	("Licorice", _("Licorice")),
	("LightBlue", _("Light Blue")),
	("LightGrey", _("Light Grey")),
	("LightRed", _("Light Red")),
	("LightSlateBlue", _("Light Slate Blue")),
	("Magenta", _("Magenta")),
	("Maroon", _("Maroon")),
	("MediumBlue", _("Medium Blue")),
	("MidBlack", _("Mid Black")),
	("MidnightBlue", _("Midnight Blue")),
	("Mustard", _("Mustard")),
	("Navy", _("Navy")),
	("OffBlack", _("Off Black")),
	("Onyx", _("Onyx")),
	("Orange", _("Orange")),
	("OrangeRed", _("Orange Red")),
	("OuterSpace", _("Outer Space")),
	("OxfordBlue", _("Oxford Blue")),
	("Pink", _("Pink")),
	("PowderBlue", _("Powder Blue")),
	("Purple", _("Purple")),
	("Raven", _("Raven")),
	("Red", _("Red")),
	("RoyalBlue", _("Royal Blue")),
	("SaddleBrown", _("Saddle Brown")),
	("Silver", _("Silver")),
	("SmokyBlack", _("Smoky Black")),
	("Tan", _("Tan")),
	("Teal", _("Teal")),
	("WarmYellow", _("Warm Yellow")),
	("White", _("White")),
	("Yellow", _("Yellow")),
	("ButtonBlue", _("Button Blue")),
	("ButtonGreen", _("Button Green")),
	("ButtonRed", _("Button Red")),
	("ButtonYellow", _("Button Yellow")),
	("ButtonBack", _("Button Background")),
	# ("User1", _("User 1")),
	# ("User2", _("User 2")),
	# ("User3", _("User 3")),
	# ("User4", _("User 4")),
	# ("User5", _("User 5")),
	# ("User6", _("User 6")),
	# ("User7", _("User 7")),
	# ("User8", _("User 8")),
	# ("User9", _("User 9")),
	# ("User0", _("User 10"))
]

backgroundChoice = [("Background", _("Background"))]

transparencyChoices = [
	("0x00000000", _("0% (Opaque)")),
	("0x0c000000", _("5%")),
	("0x19000000", _("10%")),
	("0x26000000", _("15%")),
	("0x33000000", _("20%")),
	("0x3f000000", _("25%")),
	("0x4c000000", _("30%")),
	("0x59000000", _("35%")),
	("0x66000000", _("40%")),
	("0x72000000", _("45%")),
	("0x7f000000", _("50%")),
	("0x8c000000", _("55%")),
	("0x99000000", _("60%")),
	("0xa5000000", _("65%")),
	("0xb2000000", _("70%")),
	("0xbf000000", _("75%")),
	("0xcc000000", _("80%")),
	("0xd8000000", _("85%")),
	("0xe5000000", _("90%")),
	("0xf2000000", _("95%")),
	("0xff000000", _("100% (Transparent)"))
]

# Items with a color and transparency require two lines in the setup XML file.
# (One for ItemColor and one for ItemTransparency.)
#
colorElements = [
	("ScreenBackground", "Black", "0x3f000000"),  # As this can be used by other elements it must be processed first!
	("BannerBorder", "Black", None),
	("BannerClock", "White", None),
	("BannerClockBackground", "Background", "Background"),
	("BannerClockDate", "LightBlue", None),
	("BannerClockTime", "White", None),
	("BannerTitle", "White", None),
	("EPGBackground", "Black", None),
	("EPGGridBackground", "Orange", None),
	("EPGGridBorder", "Black", None),
	("EPGOverlayBorder", "Black", None),
	("EPGOverlayColor", "WarmYellow", None),
	("EPGProgressBackground", "DeepGrey", None),
	("EPGProgressBorder", "WarmYellow", None),
	("EPGProgressColor", "WarmYellow", None),
	("EPGTimeLine", "Yellow", None),
	("EPGTransparency", None, "Background"),
	("EPGEntryBackgroundColor", "MidBlack", None),
	("EPGEntryBackgroundColorNow", "Jet", None),
	("EPGEntryBackgroundColorNowSelected", "Silver", None),
	("EPGEntryBackgroundColorSelected", "Grey", None),
	("EPGEntryForegroundColor", "White", None),
	("EPGEntryForegroundColorNow", "White", None),
	("EPGEntryForegroundColorNowSelected", "Black", None),
	("EPGEntryForegroundColorSelected", "Black", None),
	("EPGRecordBackgroundColor", "DullRed", None),
	("EPGRecordBackgroundColorSelected", "Red", None),
	("EPGRecordForegroundColor", "White", None),
	("EPGRecordForegroundColorSelected", "Black", None),
	("EPGServiceBackgroundColor", "OffBlack", None),
	("EPGServiceBackgroundColorNow", "DavysGrey", None),
	("EPGServiceForegroundColor", "White", None),
	("EPGServiceForegroundColorNow", "White", None),
	("EPGZapBackgroundColor", "DullGreen", None),
	("EPGZapBackgroundColorSelected", "Green", None),
	("EPGZapForegroundColor", "White", None),
	("EPGZapForegroundColorSelected", "Black", None),
	("FAVMarked", "DullGreen", "0x26000000"),
	("FAVMarkedBackground", "Background", "Background"),
	("FAVService", "White", None),
	("FAVServiceFallback", "Blue", None),
	("FAVServiceMarked", "Green", None),
	("FAVServiceMarkedSelected", "White", None),
	("FAVServiceNotAvailable", "Grey", None),
	("FAVServiceSelected", "White", None),
	("FAVServiceSelectedFallback", "Cyan", None),
	("FindCharacter", "Gold", None),
	("FootnoteBackground", "Background", "Background"),
	("FootnoteText", "LightBlue", None),
	("HelpPress", "Yellow", None),
	("InfoBackground", "Background", "Background"),
	("InfobarMediaBackground", "Background", "Background"),
	("InfobarTVBackground", "Background", "Background"),
	("InfoBouquet", "LightBlue", None),
	("InfoBroadcaster", "LightBlue", None),
	("InfoChannel", "LightBlue", None),
	("InfoChannelSelected", "Blue", None),
	("InfoDetailsNext", "White", None),
	("InfoDetailsNow", "White", None),
	("InfoDiskStats", "DullYellow", None),
	("InfoDurationNext", "LightBlue", None),
	("InfoDurationNow", "LightBlue", None),
	("InfoGenreNext", "Grey", None),
	("InfoGenreNow", "Grey", None),
	("InfoLCN", "LightBlue", None),
	("InfoMediaFileSize", "LightBlue", None),
	("InfoMediaLength", "LightBlue", None),
	("InfoMediaName", "LightBlue", None),
	("InfoMediaPosition", "White", None),
	("InfoMediaRemaining", "White", None),
	("InfoProgramNext", "White", None),
	("InfoProgramNow", "White", None),
	("InfoProgramSelected", "White", None),
	("InfoProgressBackground", "DeepGrey", None),
	("InfoProgressBorder", "Grey", None),
	("InfoProgressColor", "Green", None),
	("InfoRatingNext", "Grey", None),
	("InfoRatingNow", "Grey", None),
	("InfoRecordingBackground", "DeepGrey", None),
	("InfoRecordingBorder", "Grey", None),
	("InfoRecordingColor", "OrangeRed", None),
	("InfoServiceData", "LightBlue", None),
	("InfoTimesNext", "Grey", None),
	("InfoTimesNow", "Grey", None),
	("InfoTimesSelected", "Silver", None),
	("KeyBack", "ButtonBack", "0x00000000"),
	("KeyBlue", "ButtonBlue", None),
	("KeyGreen", "ButtonGreen", None),
	("KeyRed", "ButtonRed", None),
	("KeyText", "White", None),
	("KeyYellow", "ButtonYellow", None),
	("MenuBackground", "Background", "Background"),
	("MenuDisabled", "Grey", None),
	("MenuSelected", "DodgerBlue", "0x26000000"),
	("MenuText", "White", None),
	("MenuTextSelected", "White", None),
	("PictureBackground", "Background", "Background"),
	("PictureLabel", "DullGreen", None),
	("PictureLabelBorder", "Black", None),
	("Pinstripe", "DavysGrey", None),
	("PinstripeKeyError", "DavysGrey", None),
	("PinstripeMute", "DavysGrey", None),
	("PinstripeVolume", "DavysGrey", None),
	("ProgressBackground", "DeepGrey", None),
	("ProgressBorder", "Grey", None),
	("ProgressColor", "White", None),
	("Resolution", "Silver", None),
	("ResolutionBackground", "Background", "Background"),
	("ScreenSaver", "Black", "0x19000000"),
	("Scrollbar", "Gainsboro", None),
	("SMSHelperBackground", "Background", "Background"),
	("SMSHelperLabel", "Grey", None),
	("SMSHelperText", "White", None),
	("Text", "White", None),
	("TextBackground", "Background", "Background"),
	("TextDisabled", "DimGrey", None),
	("TextIndented", "Grey", None),
	("TextIndentedSelected", "Silver", None),
	("TextLabel", "Grey", None),
	("TextSelected", "White", None),
	("TextWaiting", "Gold", None),
	("TimeShiftBackground", "DeepGrey", None),
	("TimeShiftBorder", "Grey", None),
	("TimeShiftColor", "Green", None),
	("TimeShiftData", "Silver", None),
	("TunerBackground", "Background", "Background"),
	("TunerBER", "OrangeRed", None),
	("TunerBorder", "Grey", None),
	("TunerCurrent", "DullGreen", None),
	("TunerData", "Silver", None),
	("TunerIdle", "DimGrey", None),
	("TunerLabel", "PowderBlue", None),
	("TunerRecording", "Orange", None),
	("VolumeBackground", "Black", None),
	("VolumeColor", "LightBlue", None),
	("WeatherData", "White", None),
	("WeatherLabel", "Grey", None),
	("WeatherProvider", "Orange", None)
]

derivedBackgroundElements = [
	"EPGEntryBackgroundColor",
	"EPGEntryBackgroundColorNow",
	"EPGEntryBackgroundColorNowSelected",
	"EPGEntryBackgroundColorSelected",
	"EPGRecordBackgroundColor",
	"EPGRecordBackgroundColorSelected",
	"EPGServiceBackgroundColor",
	"EPGServiceBackgroundColorNow",
	"EPGZapBackgroundColor",
	"EPGZapBackgroundColorSelected"
]

derivedForegroundElements = [
	"EPGEntryForegroundColor",
	"EPGEntryForegroundColorNow",
	"EPGEntryForegroundColorNowSelected",
	"EPGEntryForegroundColorSelected",
	"EPGRecordForegroundColor",
	"EPGRecordForegroundColorSelected",
	"EPGServiceForegroundColor",
	"EPGServiceForegroundColorNow",
	"EPGZapForegroundColor",
	"EPGZapForegroundColorSelected"
]

bannerFontChoices = [
	("ArialNarrow", _("Arial Narrow")),
	("DejaVuSans", _("DejaVu Sans")),
	("DejaVuSansBold", _("DejaVu Sans Bold")),
	("DejaVuSansCondensed", _("DejaVu Sans Condensed")),
	("DejaVuSansCondensedBold", _("DejaVu Sans Condensed Bold")),
	("DejaVuSerifCondensed", _("DejaVu Serif Condensed")),
	("DejaVuSerifCondensedBold", _("DejaVu Serif Condensed Bold")),
	("DroidSansBold", _("DroidSans Bold")),
	("GoodTimes", _("Good Times")),
	("KhammuRabi", _("Khammu Rabi")),
	("NemesisFlatline", _("Nemesis Flatline")),
	("RobotoBlack", _("Roboto Black")),
	("RobotoBold", _("Roboto Bold")),
	("ValisEnigma", _("Valis Enigma"))
]

textFontChoices = [
	("ArialNarrow", _("Arial Narrow")),
	("DejaVuSansCondensed", _("DejaVu Sans Condensed")),
	("DejaVuSansCondensedBold", _("DejaVu Sans Condensed Bold")),
	("DejaVuSerifCondensed", _("DejaVu Serif Condensed")),
	("DejaVuSerifCondensedBold", _("DejaVu Serif Condensed Bold")),
	("KhammuRabi", _("Khammu Rabi")),
	("NemesisFlatline", _("Nemesis Flatline")),
	("ValisEnigma", _("Valis Enigma"))
]

fixedFontChoices = [
	("AndaleMono", _("Andale Mono")),
	("DejaVuSansMono", _("DejaVu Sans Mono")),
	("DejaVuSansMonoBold", _("DejaVu Sans Mono Bold")),
	("MPluss1M", _("M+ 1M")),
	("VeraSansMono", _("Vera Sans Mono"))
]

fontElements = [
	("Body", "NemesisFlatline", textFontChoices),
	("ButtonFont", "NemesisFlatline", textFontChoices),
	("ChoiceList", "NemesisFlatline", textFontChoices),
	("ClockFont", "RobotoBlack", bannerFontChoices),
	("DescriptionFont", "NemesisFlatline", textFontChoices),
	("EPGEventFont", "NemesisFlatline", textFontChoices),
	("EPGServiceFont", "NemesisFlatline", textFontChoices),
	("EPGTimeLineFont", "NemesisFlatline", textFontChoices),
	("FAVEventFont", "NemesisFlatline", textFontChoices),
	("FAVLCNFont", "NemesisFlatline", textFontChoices),
	("FAVServiceFont", "NemesisFlatline", textFontChoices),
	("FileListFont", "NemesisFlatline", textFontChoices),
	("FileListMultiFont", "NemesisFlatline", textFontChoices),
	("FixedFont", "MPluss1M", fixedFontChoices),
	("HelpFont", "NemesisFlatline", textFontChoices),
	("InfoDescriptionFont", "NemesisFlatline", textFontChoices),
	("InfoEventFont", "NemesisFlatline", textFontChoices),
	("InfoOtherFont", "NemesisFlatline", textFontChoices),
	("InfoTimeFont", "NemesisFlatline", textFontChoices),
	("MenuFont", "NemesisFlatline", textFontChoices),
	("MovieSelectionFont", "NemesisFlatline", textFontChoices),
	("SMSHelperFont", "DejaVuSansCondensed", textFontChoices),
	("Regular", "NemesisFlatline", textFontChoices),
	("SelectionList", "NemesisFlatline", textFontChoices),
	("TextFont", "NemesisFlatline", textFontChoices),
	("TitleFont", "RobotoBlack", bannerFontChoices)
]

imageNames = {
	"BackgroundImage": "backdrop.mvi",
	"BootImage": "bootlogo.mvi",
	"RadioImage": "radio.mvi"
}

imageChoices = [
	("", _("Default")),
	("Random", _("Random"))
]

spinnerChoices = [
	("", _("Default"))
]

buttonBase = "ScreenTemplateButton%s"

buttonColors = [
	"Red",
	"Green",
	"Yellow",
	"Blue",
]

buttonChoices = [
	("Bar", _("Bar")),
	("Box", _("Box")),
	("Block", _("Block")),
	("Button", _("Button")),
	("Circle", _("Circle")),
	("Legacy", _("Legacy")),
	("LineBottom", _("Line Bottom")),
	("LineLeft", _("Line Left")),
	("LineRight", _("Line Right")),
	("LineTop", _("Line Top")),
	("Pill", _("Pill"))
]

optionElements = [
	("ButtonStyle", "Block", ConfigSelection, buttonChoices),  # As this is used by can AlwaysShowButtons it must be processed first!
	("AlwaysShowButtons", False, ConfigYesNo, None),
	("BackgroundImage", "", ConfigSelection, imageChoices),
	("BootImage", "", ConfigSelection, imageChoices),
	("EnhancedMenu", False, ConfigEnableDisable, None),
	("EPGSettings", False, ConfigYesNo, None),
	("EPGShowTicks", True, ConfigYesNo, None),
	("FAVSettings", False, ConfigYesNo, None),
	("FontSettings", False, ConfigYesNo, None),
	("GeneralSettings", False, ConfigYesNo, None),
	("InfoSettings", False, ConfigYesNo, None),
	("MenuSettings", False, ConfigYesNo, None),
	("PanelSettings", False, ConfigYesNo, None),
	("RadioImage", "", ConfigSelection, imageChoices),
	("RecordBlink", True, ConfigYesNo, None),
	("SortThemes", False, ConfigYesNo, None),
	("Spinner", "", ConfigSelection, spinnerChoices),
	("TextSettings", False, ConfigYesNo, None),
	("UpdateBlink", True, ConfigYesNo, None),
	("UseGroups", True, ConfigYesNo, None)
]

groups = [
	"EPGSettings",
	"FAVSettings",
	"FontSettings",
	"GeneralSettings",
	"InfoSettings",
	"MenuSettings",
	"PanelSettings",
	"TextSettings"
]

dontRestart = [
	"BackgroundImage",
	"BootImage",
	"RadioImage",
	"RecordBlink",
	"SortThemes",
	"UpdateBlink",
	"UseGroups"
] + groups


# debugSkin = config.crash.debugSkins.value
debugSkin = False
if not hasattr(config.plugins, "skin"):
	config.plugins.skin = ConfigSubsection()
config.plugins.skin.OverlayHD = ConfigSubsection()
config.plugins.skin.OverlayHD.ShowInExtensions = ConfigYesNo(default=False)


class OverlayHDSkinManager(Setup):
	def __init__(self, session):
		Setup.__init__(self, session=session, setup="OverlayHDSkinManager", plugin="Extensions/OverlayHD")
		self["key_yellow"] = StaticText(_("Themes"))
		self["key_blue"] = StaticText(_("Default"))
		self["OverlayHDActions"] = HelpableActionMap(self, "ColorActions", {
			"yellow": (self.theme, _("Manage themes")),
			"blue": (self.default, _("Apply the default skin settings"))
		}, prio=0, description=_("OverlayHD Actions"))
		config.plugins.skin.OverlayHD.UseGroups.addNotifier(self.changeGrouping, initial_call=False, immediate_feedback=True)

	def changeGrouping(self, configElement):
		grouping = not config.plugins.skin.OverlayHD.UseGroups.value
		for group in groups:
			getattr(config.plugins.skin.OverlayHD, group).value = grouping

	def theme(self):
		self.session.openWithCallback(self.themeClosed, OverlayHDThemeManager)

	def themeClosed(self):
		self.applySettings()

	def default(self):
		print("[OverlayHD] Setting OverlayHD skin to default settings.")
		for (label, color, transparency) in colorElements:
			if color is None or transparency is None:
				item = getattr(config.plugins.skin.OverlayHD, label)
				item.value = item.default
				if debugSkin:
					print("[OverlayHD] Defaulting color '%s' to '%s'." % (label, item.default))
			else:
				item = getattr(config.plugins.skin.OverlayHD, "%sColor" % label)
				item.value = item.default
				item = getattr(config.plugins.skin.OverlayHD, "%sTransparency" % label)
				item.value = item.default
				if debugSkin:
					print("[OverlayHD] Defaulting color '%sColor' to '%s'." % (label, item.default))
					print("[OverlayHD] Defaulting transparency '%sTransparency' to '%s'." % (label, item.default))
		for (label, font, fontTable) in fontElements:
			item = getattr(config.plugins.skin.OverlayHD, label)
			item.value = item.default
			if debugSkin:
				print("[OverlayHD] Defaulting font '%s' to '%s'." % (label, item.default))
		for (label, default, configType, optionTable) in optionElements:
			item = getattr(config.plugins.skin.OverlayHD, label)
			item.value = item.default
			if debugSkin:
				print("[OverlayHD] Defaulting option '%s' to '%s'." % (label, item.default))
		self.applySettings()
		self.setFootnote(_("Default OverlayHD skin settings applied."))

	def changedEntry(self):
		self.applySettings()
		Setup.changedEntry(self)

	def saveAll(self):  # Save all entries, both displayed and not currently displayed.
		restart = False
		for item in config.plugins.skin.OverlayHD.dict():
			if item in dontRestart:
				continue
			if getattr(config.plugins.skin.OverlayHD, item).isChanged():
				restart = True
				break
		config.plugins.skin.OverlayHD.UseGroups.removeNotifier(self.changeGrouping)
		config.plugins.skin.OverlayHD.save()
		configfile.save()
		# self.applySettings()
		return restart
		# Setup.saveAll(self, restart)

	def cancelConfirm(self, result):  # Cancel all changed entries, both displayed and not currently displayed.
		if not result:
			return
		config.plugins.skin.OverlayHD.UseGroups.removeNotifier(self.changeGrouping)
		config.plugins.skin.OverlayHD.cancel()
		self.applySettings()
		Setup.cancelConfirm(self, result)

	def applySettings(self):
		index = self["config"].getCurrentIndex()
		applySkinSettings(fullInit=False)
		self.applySkin()
		self.instance.invalidate()  # Remove this when the underlying bug is fixed!
		self["config"].setCurrentIndex(index)


class OverlayHDThemeManager(Screen, HelpableScreen):
	skin = """
	<screen name="OverlayHDThemeManager" title="OverlayHD Theme Manager" position="fill" backgroundColor="ScreenBackground" flags="wfNoBorder">
		<panel name="ScreenTemplate" />
		<ePixmap pixmap="menus/mainmenu_tv_channel.png" position="50,100" size="300,500" alphatest="on" transparent="1" />
		<widget source="themes" render="Listbox" position="400,80" size="830,420" backgroundColor="MenuBackground" backgroundColorSelected="MenuSelected" enableWrapAround="1" foregroundColor="MenuText" foregroundColorSelected="MenuTextSelected" scrollbarMode="showOnDemand" transparent="0">
			<convert type="TemplatedMultiContent">
				{
				"template":
					[
					MultiContentEntryText(pos = (20, 0), size = (790, 35), font = 0, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0),
					],
				"fonts": [parseFont("MenuFont;25)],
				"itemHeight": 35
				}
			</convert>
		</widget>
		<panel name="ScreenTemplateDescription4" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = OverlayHDThemeManager.skin
		# self.skinName = ["OverlayHDThemeManager"]
		HelpableScreen.__init__(self)
		self.setTitle(_("OverlayHD Theme Manager"))
		self["key_menu"] = StaticText(_("MENU"))
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Apply"))
		self["key_yellow"] = StaticText(_("Create"))
		self["key_blue"] = StaticText(_("Update"))
		self["key_help"] = StaticText(_("HELP"))
		self["actions"] = HelpableActionMap(self, ["OkCancelActions", "ColorActions", "MenuActions"], {
			"ok": (self.applyTheme, _("Apply the currently highlighted theme, return to OverlayHD Skin Manager")),
			"cancel": (self.cancelTheme, _("Cancel theme selection, return to OverlayHD Skin Manager")),
			"menu": (self.themeMenu, _("Menu of actions applicable to the currently highlighted theme")),
			"red": (self.cancelTheme, _("Cancel theme selection, return to OverlayHD Skin Manager")),
			"green": (self.applyTheme, _("Apply the currently highlighted theme, return to OverlayHD Skin Manager")),
			"yellow": (self.createTheme, _("Create a new theme using the current skin settings")),
			"blue": (self.updateTheme, _("Update the currently highlighted theme with the current skin settings"))
		}, prio=0, description=_("OverlayHD Theme Actions"))
		self["themes"] = List()
		self["description"] = Label()
		self.filename = resolveFilename(SCOPE_CONFIG, "OverlayHD_themes.xml")
		self.domThemes = Element("themes")
		self.createUpdateTheme(themeName="Current")
		if not isfile(self.filename):
			# self.saveThemes()  # Enable this call to always create the default themes settings file.
			print("[OverlayHD] Themes file does not exist, theme 'Current' created.")
		self.domThemes = fileReadXML(self.filename, default=self.domThemes, source=MODULE_NAME)
		self["themes"].updateList(self.listThemes())
		self["themes"].onSelectionChanged.append(self.clearDescription)

	def createUpdateTheme(self, themeName=None):
		if themeName is None:
			themeName = self["themes"].getCurrent()[0]
		theme = self.findTheme(themeName)
		if theme is None:
			theme = SubElement(self.domThemes, "theme", {"name": themeName})
		else:
			theme.clear()
			theme.set("name", themeName)
		for (label, color, transparency) in colorElements:
			if color is None or transparency is None:
				element = SubElement(theme, "color", {"name": label, "value": getattr(config.plugins.skin.OverlayHD, label).value})
			else:
				item = "%sColor" % label
				element = SubElement(theme, "color", {"name": item, "value": getattr(config.plugins.skin.OverlayHD, item).value})
				item = "%sTransparency" % label
				element = SubElement(theme, "color", {"name": item, "value": getattr(config.plugins.skin.OverlayHD, item).value})
		for (label, font, fontTable) in fontElements:
			element = SubElement(theme, "font", {"name": label, "value": getattr(config.plugins.skin.OverlayHD, label).value})
		for (label, default, configType, optionTable) in optionElements:
			if optionTable is None:
				element = SubElement(theme, "option", {"name": label, "type": "boolean", "value": str(getattr(config.plugins.skin.OverlayHD, label).value)})
			else:
				element = SubElement(theme, "option", {"name": label, "value": getattr(config.plugins.skin.OverlayHD, label).value})

	def findTheme(self, themeName):
		if self.domThemes:
			themes = self.domThemes.findall("theme")
			for theme in themes:
				name = theme.get("name")
				if name == themeName:
					return theme
		return None

	def listThemes(self):
		themeList = []
		if self.domThemes:
			themes = self.domThemes.findall("theme")
			for theme in themes:
				name = theme.get("name")
				if debugSkin:
					print("[OverlayHD] Theme '%s' found." % name)
				themeList.append((name, name))
			if config.plugins.skin.OverlayHD.SortThemes.value:
				themeList.sort(key=lambda item: item[0])
			if debugSkin:
				count = len(themes)
				print("[OverlayHD] %d %s found." % (ngettext("theme", "themes", count), count))
		return themeList

	def saveThemes(self):
		self["themes"].updateList(self.listThemes())
		self.xmlIndent(self.domThemes)
		ElementTree(self.domThemes).write(self.filename)

	def xmlIndent(self, element, level=0):
		indent = "\t" * level
		if len(element):
			if not element.text or not element.text.strip():
				element.text = "\n%s\t" % indent
			if not element.tail or not element.tail.strip():
				element.tail = "\n%s" % indent
			for element in element:
				self.xmlIndent(element, level + 1)
			if not element.tail or not element.tail.strip():
				element.tail = "\n%s" % indent
		else:
			if level and (not element.tail or not element.tail.strip()):
				element.tail = "\n%s" % indent

	def applyTheme(self):
		if self["themes"].count():
			themeName = self["themes"].getCurrent()[0]
		else:
			self["description"].setText(_("There are no themes to apply!"))
			return
		theme = self.findTheme(themeName)
		if theme is not None:
			print("[OverlayHD] Applying theme '%s'." % themeName)
			items = config.plugins.skin.OverlayHD.dict()
			colors = theme.findall("color")
			for color in colors:
				name = color.get("name")
				value = color.get("value")
				if name and value and name in items:
					getattr(config.plugins.skin.OverlayHD, name).value = value
					if debugSkin:
						print("[OverlayHD] Theme color '%s' value is '%s'." % (name, value))
				else:
					print("[OverlayHD] Theme color '%s' value '%s' is invalid!" % (name, value))
			fonts = theme.findall("font")
			for font in fonts:
				name = font.get("name")
				value = font.get("value")
				if name and value and name in items:
					getattr(config.plugins.skin.OverlayHD, name).value = value
					if debugSkin:
						print("[OverlayHD] Theme font '%s' value is '%s'." % (name, value))
				else:
					print("[OverlayHD] Theme font '%s' value '%s' is invalid!" % (name, value))
			options = theme.findall("option")
			for option in options:
				name = option.get("name")
				type = option.get("type")
				value = option.get("value")
				if name and value is not None and name in items:
					if type == "boolean":
						value = value.upper()
						if value in ("TRUE", "YES", "ON", "ENABLE", "ENABLED", "1"):
							value = True
						if value in ("FALSE", "NO", "OFF", "DISABLE", "DISABLED", "0"):
							value = False
					getattr(config.plugins.skin.OverlayHD, name).value = value
					if debugSkin:
						print("[OverlayHD] Theme option '%s' value is '%s'." % (name, value))
				else:
					print("[OverlayHD] Theme option '%s' value '%s' is invalid!" % (name, value))
			self.saveThemes()
		self.close()

	def cancelTheme(self):
		self.close()

	def themeMenu(self):
		themeActions = [
			(_("Create new theme"), self.createTheme),
			(_("Update theme"), self.updateTheme),
			(_("Rename theme"), self.renameTheme),
			(_("Delete theme"), self.deleteTheme),
			(_("Export theme"), self.exportTheme),
			(_("Import theme"), self.importTheme)
		]
		themeName = self["themes"].getCurrent()[0] if self["themes"].count() else "* %s *" % _("Undefined")
		self.session.openWithCallback(self.themeMenuAction, ChoiceBox, title=_("OverlayHD Theme: '%s'") % themeName, list=themeActions, skin_name="OverlayHDThemeMenu", windowTitle=self.getTitle())

	def themeMenuAction(self, choice):
		if choice is None:
			return
		themeName = self["themes"].getCurrent()[0] if self["themes"].count() else None
		choice[1](themeName)

	def createTheme(self, themeName=None):
		self.session.openWithCallback(self.createThemeAction, VirtualKeyBoard, title=_("Enter a name for this new theme:"), text="", windowTitle=self.getTitle())

	def createThemeAction(self, themeName):
		if self.checkThemeName(themeName):
			print("[OverlayHD] Creating theme '%s'." % themeName)
			self.createUpdateTheme(themeName=themeName)
			self["themes"].updateList(self.listThemes())
			self["description"].setText(_("Theme '%s' created.") % themeName)

	def updateTheme(self, themeName=None): # Fis me!
		if self["themes"].count():
			themeName = self["themes"].getCurrent()[0]
			print("[OverlayHD] Updating theme '%s'." % themeName)
			self.createUpdateTheme(themeName=themeName)
			self["themes"].updateList(self.listThemes())
			self["description"].setText(_("Theme '%s' updated.") % themeName)
		else:
			self.newTheme()

	def renameTheme(self, themeName):
		self.session.openWithCallback(self.renameThemeAction, VirtualKeyBoard, title=_("Enter new name for the '%s' theme:") % themeName, text=themeName, windowTitle=self.getTitle())

	def renameThemeAction(self, themeName):
		if self.checkThemeName(themeName):
			oldName = self["themes"].getCurrent()[0]
			theme = self.findTheme(oldName)
			if theme is not None:
				print("[OverlayHD] Renaming theme '%s' to '%s'." % (oldName, themeName))
				theme.set("name", themeName)
				self["themes"].updateList(self.listThemes())
				self["description"].setText(_("Theme '%s' renamed to '%s'.") % (oldName, themeName))

	def deleteTheme(self, themeName):
		if themeName == "Current":
			self["description"].setText(_("The '%s' theme may not be deleted!") % themeName)
		else:
			self.session.openWithCallback(self.deleteThemeAction, MessageBox, _("Do you really want to delete the '%s' theme?") % themeName, windowTitle=self.getTitle())

	def deleteThemeAction(self, answer):
		if answer:
			themeName = self["themes"].getCurrent()[0]
			theme = self.findTheme(themeName)
			if theme is not None:
				print("[OverlayHD] Deleting theme '%s'." % themeName)
				if isinstance(self.domThemes, ElementTree):
					self.domThemes = self.domThemes.getroot()
				self.domThemes.remove(theme)
				self["themes"].updateList(self.listThemes())
				self["description"].setText(_("Theme '%s' deleted.") % themeName)

	def exportTheme(self, themeName):
		print("[OverlayHD] Export theme.")
		self["description"].setText(_("Theme export not yet available!"))

	def importTheme(self, themeName):
		print("[OverlayHD] Import theme.")
		self["description"].setText(_("Theme import not yet available!"))

	def checkThemeName(self, themeName):
		valid = True
		if themeName is None:
			valid = False
			# self.session.open(MessageBox, _("Theme name can not be None!"), MessageBox.TYPE_ERROR, timeout=5, windowTitle=self.getTitle())
			# self["description"].setText(_("Theme name can not be None!"))
		elif themeName == "":
			valid = False
			self.session.open(MessageBox, _("Theme name can not be blank!"), MessageBox.TYPE_ERROR, timeout=5, close_on_any_key=True, windowTitle=self.getTitle())
			self["description"].setText(_("Theme name can not be blank!"))
		elif self.findTheme(themeName):
			valid = False
			self.session.open(MessageBox, _("Theme name '%s' already exists!") % themeName, MessageBox.TYPE_ERROR, timeout=5, close_on_any_key=True, windowTitle=self.getTitle())
			self["description"].setText(_("Theme name '%s' already exists!") % themeName)
		return valid

	def clearDescription(self):
		self["description"].setText("")


def applySkinSettings(fullInit=False):
	def findListItem(item, field, itemList):
		value = "* %s *" % _("Undefined")
		for data in itemList:
			if data[0] == item:
				value = data[field]
				break
		return value

	def findAdditionalChoices(choices, type):
		data = {}
		for scope, dir in ((SCOPE_SKINS, "OverlayHD"), (SCOPE_MEDIA, "hdd"), (SCOPE_MEDIA, "usb")):
			path = pathjoin(resolveFilename(scope), dir, type, "")
			if isdir(path):
				for file in listdir(path):
					# data[splitext(file)[0].replace("_", " ")] = pathjoin(path, file)
					name = splitext(file)[0].replace("_", " ")
					if name in data:
						print("[OverlayHD] Note: Image name '%s' (%s) is duplicated." % (name, file))
					else:
						data[name] = pathjoin(path, file)
		for key in sorted(list(data.keys())):
			choices.append((data.get(key), key))

	initMsg = "C"
	if fullInit:
		initMsg = "Initialization and c"
		print("[OverlayHD] Initializing default skin settings.")
		if debugSkin:
			print("[OverlayHD] Initialize color choices:")
			for value, option in colorChoices:
				print("[OverlayHD]    '0x%08X' = '%s'   (%s)" % (colors.get(value, "Black").argb(), option, value))
			print("[OverlayHD] Initialize transparency choices:")
			for value, option in transparencyChoices:
				print("[OverlayHD]    '%s' = '%s'" % (value, option))
		for (label, color, transparency) in colorElements:
			if color and transparency:
				if label == "ScreenBackground":
					cChoices = colorChoices
					tChoices = transparencyChoices
				else:
					cChoices = backgroundChoice + colorChoices
					tChoices = backgroundChoice + transparencyChoices
				setattr(config.plugins.skin.OverlayHD, "%sColor" % label, ConfigSelection(default=color, choices=cChoices))
				setattr(config.plugins.skin.OverlayHD, "%sTransparency" % label, ConfigSelection(default=transparency, choices=tChoices))
				if debugSkin:
					if color == "Background":
						color = getattr(config.plugins.skin.OverlayHD, "ScreenBackgroundColor").value
					if transparency == "Background":
						transparency = getattr(config.plugins.skin.OverlayHD, "ScreenBackgroundTransparency").value
					print("[OverlayHD] Setting skin color+transp '%s' = '%s' + '%s'   (0x%08X)." % (label, findListItem(color, 1, cChoices), findListItem(transparency, 1, tChoices), colors[color].argb() + int(transparency, 16)))
			else:
				if color:
					setattr(config.plugins.skin.OverlayHD, label, ConfigSelection(default=color, choices=colorChoices))
					if debugSkin:
						print("[OverlayHD] Setting skin color        '%s' = '%s'   (0x%08X)." % (label, findListItem(color, 1, colorChoices), colors.get(color, "Black").argb()))
				if transparency:
					setattr(config.plugins.skin.OverlayHD, label, ConfigSelection(default=transparency, choices=transparencyChoices))
					if debugSkin:
						if transparency == "Background":
							continue
						print("[OverlayHD] Setting skin transparency '%s' = '%s'   (0x%08X)." % (label, findListItem(transparency, 1, transparencyChoices), int(transparency, 16)))
		if debugSkin:
			for table, fontTable in (("Banner", bannerFontChoices), ("Text", textFontChoices), ("Fixed", fixedFontChoices)):
				print("[OverlayHD] Initializing %s font choices:" % table)
				for value, option in fontTable:
					print("[OverlayHD]    '%s'  (%s)" % (option, value))
		for (label, font, fontTable) in fontElements:
			setattr(config.plugins.skin.OverlayHD, label, ConfigSelection(default=font, choices=fontTable))
			if debugSkin:
				print("[OverlayHD] Setting font '%s' = '%s'." % (label, findListItem(font, 1, fontTable)))
		findAdditionalChoices(imageChoices, "backgrounds")
		findAdditionalChoices(spinnerChoices, "spinners")
		if debugSkin:
			for table, optionTable in (("Background", imageChoices), ("Button", buttonChoices), ("Spinner", spinnerChoices)):
				print("[OverlayHD] Initializing %s choices:" % table)
				for value, option in optionTable:
					print("[OverlayHD]    '%s' -> '%s'" % (option, value))
		for (label, default, configType, optionTable) in optionElements:
			if optionTable:
				setattr(config.plugins.skin.OverlayHD, label, configType(default=default, choices=optionTable))
			else:
				setattr(config.plugins.skin.OverlayHD, label, configType(default=default))
			if debugSkin:
				print("[OverlayHD] Setting ption '%s' to '%s'." % (label, default))
		modes = distroModes.get(distro, (None, "Enigma2"))[DISTRO_SCREENLIST]
		for screen in domScreens:
			element, path = domScreens.get(screen, (None, None))
			if element is not None:
				panels = element.findall("panel")
				if panels is not None:
					for panel in panels:
						base = panel.get("base")
						if base is not None:
							for mode in modes:
								newScreen = "%s%s" % (base, mode)
								data, path = domScreens.get(newScreen, (None, None))
								if data is not None:
									panel.set("name", newScreen)
									print("[OverlayHD] Configuring screen '%s', panel '%s', for '%s'." % (screen, base, mode))
									break
	print("[OverlayHD] Configuring skin settings.")
	for (label, color, transparency) in colorElements:
		if color and transparency:
			colorObject = getattr(config.plugins.skin.OverlayHD, "%sColor" % label)
			colorValue = colorObject.value
			if colorValue == "Background":
				colorValue = config.plugins.skin.OverlayHD.ScreenBackgroundColor.value
			transObject = getattr(config.plugins.skin.OverlayHD, "%sTransparency" % label)
			transValue = transObject.value
			if transValue == "Background":
				transValue = config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value
			colors[label] = gRGB(colors[colorValue].argb() | int(transValue, 16))
			if (fullInit and color != colorObject.value or transparency != transObject.value) or colorObject.isChanged() or transObject.isChanged():
				print("[OverlayHD] Configuring skin color '%s' to '%s' + '%s'   (0x%08X)." % (label, findListItem(colorValue, 1, colorChoices), findListItem(transValue, 1, transparencyChoices), colors[label].argb()))
		elif color:
			labelPIG = "%s%s%s" % (label[0:3], "PIG", label[3:])
			colorObject = getattr(config.plugins.skin.OverlayHD, label)
			colorValue = colorObject.value
			if colorValue == "Background":
				colorValue = config.plugins.skin.OverlayHD.ScreenBackgroundColor.value
			if label in derivedForegroundElements:
				colors[label] = colors[colorValue]
				colors[labelPIG] = colors[colorValue]
			elif label in derivedBackgroundElements:
				transValue = config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value if config.plugins.skin.OverlayHD.EPGTransparency.value == "Background" else config.plugins.skin.OverlayHD.EPGTransparency.value
				colors[label] = gRGB(colors[colorValue].argb() | int(transValue, 16))
				colors[labelPIG] = colors[colorValue]
			else:
				colors[label] = colors[colorValue]
			if (fullInit and color != colorObject.value) or colorObject.isChanged():
				print("[OverlayHD] Configuring skin color '%s' to '%s'   (0x%08X)." % (label, findListItem(colorValue, 1, colorChoices), colors[colorValue].argb()))
	for (label, font, fontTable) in fontElements:
		fontObject = getattr(config.plugins.skin.OverlayHD, label)
		fontValue = fontObject.value
		data = list(fonts[label])
		data[0] = fontValue
		fonts[label] = tuple(data)
		if (fullInit and font != fontValue) or fontObject.isChanged():
			print("[OverlayHD] Configuring skin font '%s' to '%s'." % (label, findListItem(fontValue, 1, fontTable)))
	for (label, default, configType, optionsTable) in optionElements:
		optionObject = getattr(config.plugins.skin.OverlayHD, label)
		optionValue = optionObject.value
		if label in imageNames.keys():
			result = applyLogoImage(label, optionValue)
			optionValue = "'%s'" % optionValue if optionValue else "default"
			msg = "'%s' image to %s" % (label, optionValue)
		elif label == "AlwaysShowButtons":
			result = applyShowButtons(optionValue)
			msg = "color button always on display to '%s'" % optionValue
		elif label == "ButtonStyle":
			result = applyButtonStyle(optionValue)
			msg = "color button style to '%s'" % optionValue
		elif label == "EPGShowTicks":
			result = applyShowTicks(optionValue)
			msg = "EPG tick marks to '%s'" % optionValue
		elif label == "RecordBlink":
			result = applyBlink(["session.RecordState"], optionValue)
			msg = "recording indicator blink to '%s'" % optionValue
		elif label == "Spinner":
			result = applySpinner(optionValue)
			optionValue = "'%s'" % optionValue if optionValue else "default"
			msg = "spinner to %s" % optionValue
		elif label == "UpdateBlink":
			result = applyBlink(["global.OnlineStableUpdateState", "global.OnlineUnstableUpdateState"], optionValue)
			msg = "update indicator blink to '%s'" % optionValue
		if result == 0 and ((fullInit and optionValue != optionObject.default) or optionObject.isChanged()):
			print("[OverlayHD] Configuring skin %s." % msg)
	reloadWindowStyles()
	print("[OverlayHD] %sonfiguration completed." % initMsg)


def applyBlink(indicatorList, flag):
	status = -1
	element, path = domScreens.get("ChannelFormatPanel", (None, None))
	if element is not None:
		widgets = element.findall("widget")
		if widgets is not None:
			for widget in widgets:
				if widget.get("source") in indicatorList:
					converts = widget.findall("convert")
					if converts is None:
						break
					for convert in converts:
						if convert.get("type") == "ConditionalShowHide":
							convert.text = "Blink" if flag else ""
							status = 0
							break
	return status


def applyButtonStyle(style):
	status = -4
	for color in buttonColors:
		button = buttonBase % color
		element, path = domScreens.get(button, (None, None))
		if element is None:
			break
		panel = element.find("panel")
		if panel is None:
			break
		panel = panel.find("panel")
		if panel is None:
			break
		name = panel.get("name")
		if name is None:
			break
		panel.set("name", "%s%s" % (button, style))
		status += 1
	return status


def applyLogoImage(logo, image):
	status = 0
	if image == "Random":
		image = imageChoices[randrange(len(imageChoices) - 2) + 2][0]
	target = pathjoin(resolveFilename(SCOPE_GUISKIN), imageNames.get(logo))  # Change image in /usr/share/enigma2/<skin>/.
	try:
		if islink(target):
			unlink(target)
		else:
			remove(target)
	except (IOError, OSError) as err:
		if err.errno != ENOENT:
			print("[OverlayHD] Error %d: Unable to delete the old %s image '%s'!  (%s)" % (err.errno, logo, target, err.strerror))
			status = err.errno
	if image:
		try:
			# shutil.copy2(image, target)
			symlink(image, target)
		except (IOError, OSError) as err:
			print("[OverlayHD] Error %d: Unable to link the %s image to '%s'!  (%s)" % (err.errno, logo, target, err.strerror))
			status = err.errno
	return status


def applyShowButtons(flag):
	def editElement(element, color, flag, attribute):
		if flag:
			if element.get(attribute) is not None:
				del element.attrib[attribute]
		else:
			value = "key_%s" if attribute == "conditional" else "key_%s,Button,Label"
			element.set(attribute, value % color.lower())

	status = -4
	template, path = domScreens.get("ScreenTemplate", (None, None))
	for color in buttonColors:
		button = buttonBase % color
		panels = template.findall("panel")
		if panels is None:
			break
		for panel in panels:
			if panel.get("name") == button:
				editElement(panel, color, flag, "conditional")
		element, path = domScreens.get(button, (None, None))
		if element is None:
			break
		panel = element.find("panel")
		if panel is None:
			break
		panel = panel.find("panel")
		if panel is None:
			break
		editElement(panel, color, flag, "conditional")
		name = panel.get("name")
		if name is None:
			break
		element, path = domScreens.get(name, (None, None))
		if element is None:
			break
		labels = element.findall("eLabel")
		if labels is None:
			break
		for label in labels:
			editElement(label, color, flag, "objectTypes")
		pixmaps = element.findall("ePixmap")
		if pixmaps is None:
			break
		for pixmap in pixmaps:
			editElement(pixmap, color, flag, "objectTypes")
		status += 1
	return status


def applyShowTicks(flag):
	flag = "yes" if flag else "no"
	for screen in ("EPGTimeLinePanel", "GraphicalEPG", "GraphicalEPGPIG", "GraphicalInfoBarEPG"):
		element, path = domScreens.get(screen, (None, None))
		if element is None:
			break
		widgets = element.findall("widget")
		if widgets is None:
			break
		for widget in widgets:
			if widget.get("TimelineTicksOn") is not None:
				widget.set("TimelineTicksOn", flag)
				break
	return 0


def applySpinner(spinner):
	status = 0
	currentSpinner = pathjoin(resolveFilename(SCOPE_GUISKIN), "spinner")
	msg = "[OverlayHD] NOTE: Unexpected spinner %s found within OverlayHD and deleted!"
	if islink(currentSpinner):
		unlink(currentSpinner)
		if debugSkin:
			print("[OverlayHD] Note: Old spinner directory found and deleted!")
	elif isdir(currentSpinner):
		rmtree(currentSpinner)
		print(msg % "directory")
	elif exists(currentSpinner):
		remove(currentSpinner)
		print(msg % "file")
	if spinner:
		try:
			symlink(spinner, currentSpinner)
		except (IOError, OSError) as err:
			print("[OverlayHD] Error %d: Unable to link '%s' spinner directory as '%s'!  (%s)" % (err.errno, spinner, currentSpinner, err.strerror))
			status = err.errno
	return status


def clearSkinSettings():
	pass


def updateOverlayHD():
	# This code is used to ensure that older environments are brought up to current requirements...
	# Remove the old settings conversion program...
	src = resolveFilename(SCOPE_PLUGIN, "Extensions/OverlayHD/OverlayHD_Update")
	if isfile(src):
		remove(src)
		print("[OverlayHD] Defunct settings converter deleted.")
	# Relocate and remove the original themes.xml template...
	src = resolveFilename(SCOPE_PLUGIN, "Extensions/OverlayHD/themes.xml")
	dst = resolveFilename(SCOPE_CONFIG, "OverlayHD_themes.xml")
	if isfile(src):
		if not isfile(dst):
			move(src, dst)
			print("[OverlayHD] Themes file moved to new location.")
		else:
			remove(src)
			print("[OverlayHD] Original OverlayHD themes file deleted.")
	# Set defunct attributes to the default so they will be removed from the settings file...
	for attr in ("ClockStyle", "EPGChannel", "EPGChannelSelected", "EPGDetails", "EPGDuration", "EPGLCN", "EPGProgram", "EPGProgramSelected", "EPGProvider", "EPGRating", "EPGTimes", "EPGTimesSelected", "InfoFileSize"):
		setattr(config.plugins.skin.OverlayHD, attr, ConfigSelection(default="Default", choices=[("Default"), ("None")]))
		getattr(config.plugins.skin.OverlayHD, attr).value = getattr(config.plugins.skin.OverlayHD, attr).default
		getattr(config.plugins.skin.OverlayHD, attr).save()
	config.plugins.skin.OverlayHD.save()


def main(session, **kwargs):
	session.open(OverlayHDSkinManager)


def setup(menuid, **kwargs):
	if menuid == distroModes.get(distro, (None, None))[DISTRO_MENU_IDVAL]:
		return [(_("OverlayHD Skin Setup"), main, "OverlayHD_setup", 1000)]
	return []


def autostart(reason, **kwargs):
	if reason == 0:
		print("[OverlayHD] OverlayHD Skin Manager version %s." % PLUGIN_VERSION_NUMBER)
		print("[OverlayHD] Configuring to run on '%s' in '%s' mode." % (displayDistro, "' then '".join(distroModes.get(distro, (None, "Unknown"))[DISTRO_SCREENLIST])))
		updateOverlayHD()
		applySkinSettings(fullInit=True)
	elif reason == 1:
		print("[OverlayHD] OverlayHD Skin Manager version %s, preparing to unload from '%s'." % (PLUGIN_VERSION_NUMBER, displayDistro))
		clearSkinSettings()


def Plugins(**kwargs):
	pluginList = []
	if config.skin.primary_skin.value == "OverlayHD/skin.xml":
		pluginList.append(PluginDescriptor(where=[PluginDescriptor.WHERE_MENU], needsRestart=False, fnc=setup))
		pluginList.append(PluginDescriptor(where=[PluginDescriptor.WHERE_AUTOSTART], fnc=autostart))
		pluginList.append(PluginDescriptor(name=_("OverlayHD"), where=[PluginDescriptor.WHERE_PLUGINMENU], description="OverlayHD Skin Manager version %s" % PLUGIN_VERSION_NUMBER, icon="OverlayHD.png", fnc=main))
		if config.plugins.skin.OverlayHD.ShowInExtensions.value:
			pluginList.append(PluginDescriptor(name=_("OverlayHD Skin Manager"), where=[PluginDescriptor.WHERE_EXTENSIONSMENU], description="OverlayHD Skin Manager version %s" % PLUGIN_VERSION_NUMBER, icon="OverlayHD.png", fnc=main))
	return pluginList
