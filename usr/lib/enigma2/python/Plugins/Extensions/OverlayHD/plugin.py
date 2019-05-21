# ====================================================
# OverlayHD Skin Manager
# Version Date - 22-May-2019
# Remember to change version number variable below!!!
#
# Repository - https://bitbucket.org/IanSav/overlayhd
# Coding by IanSav (c) 2015-2018
#
# This plugin was originally developed for the
# Beyonwiz Australia distribution of Enigma2.  It
# may be distributed and executed on Beyonwiz and
# OpenViX firmware.
#
# This plugin is NOT free software. It is open source,
# you are allowed to modify it (if you keep the license
# and original author details), but it may not be
# commercially distributed.

PLUGIN_VERSION_NUMBER = "1.71"

import errno
import shutil
import xml.etree.cElementTree

from boxbranding import getImageDistro
from enigma import eEnv, gRGB
from os import listdir, remove, symlink, unlink
from os.path import exists, isdir, isfile, islink
from skin import dom_screens, colorNames, fonts  # , reloadWindowstyles

from Components.ActionMap import HelpableActionMap
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigEnableDisable, ConfigSelection
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.HelpMenu import HelpableScreen
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Setup import Setup
from Screens.Standby import TryQuitMainloop, QUIT_RESTART
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import resolveFilename, SCOPE_CONFIG, SCOPE_CURRENT_SKIN, SCOPE_CURRENT_PLUGIN

distro_configs = {
	"beyonwiz": ("Beyonwiz", "Beyonwiz"),
	"openpli": ("OpenPLi", "Enigma2"),
	"openvix": ("OpenViX", "Enigma2")
}

# Items with a colour and transparency require two lines in the setup XML file.
# (One for ItemColour and one for ItemTransparency.)
#
colour_elements = [
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
	("EPGOverlayColour", "WarmYellow", None),
	("EPGProgressBackground", "DeepGrey", None),
	("EPGProgressBorder", "WarmYellow", None),
	("EPGProgressColour", "WarmYellow", None),
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
	("InfoProgressColour", "Green", None),
	("InfoRatingNext", "Grey", None),
	("InfoRatingNow", "Grey", None),
	("InfoRecordingBackground", "DeepGrey", None),
	("InfoRecordingBorder", "Grey", None),
	("InfoRecordingColour", "OrangeRed", None),
	("InfoServiceData", "LightBlue", None),
	("InfoTimesNext", "Grey", None),
	("InfoTimesNow", "Grey", None),
	("InfoTimesSelected", "Silver", None),
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
	("ProgressColour", "White", None),
	("Resolution", "Silver", None),
	("ResolutionBackground", "Background", "Background"),
	("ScreenBackground", "Black", "0x3f000000"),
	("ScreenSaver", "Black", "0x19000000"),
	("Scrollbar", "Gainsboro", None),
	("SMSHelperBackground", "Background", "Background"),
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
	("TimeShiftColour", "Green", None),
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
	("VolumeColour", "LightBlue", None),
	("WeatherData", "White", None),
	("WeatherLabel", "Grey", None),
	("WeatherProvider", "Orange", None)
]

derived_background_elements = [
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

derived_foreground_elements = [
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

colour_choices = [
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
	("Yellow", _("Yellow"))
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

background_choice = [("Background", _("Background"))]

transparency_choices = [
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

banner_font_choices = [
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

text_font_choices = [
	("ArialNarrow", _("Arial Narrow")),
	("DejaVuSansCondensed", _("DejaVu Sans Condensed")),
	("DejaVuSansCondensedBold", _("DejaVu Sans Condensed Bold")),
	("DejaVuSerifCondensed", _("DejaVu Serif Condensed")),
	("DejaVuSerifCondensedBold", _("DejaVu Serif Condensed Bold")),
	("KhammuRabi", _("Khammu Rabi")),
	("NemesisFlatline", _("Nemesis Flatline")),
	("ValisEnigma", _("Valis Enigma"))
]

fixed_font_choices = [
	("AndaleMono", _("Andale Mono")),
	("DejaVuSansMono", _("DejaVu Sans Mono")),
	("DejaVuSansMonoBold", _("DejaVu Sans Mono Bold")),
	("MPluss1M", _("M+ 1M")),
	("VeraSansMono", _("Vera Sans Mono"))
]

font_elements = [
	("Body", "NemesisFlatline", text_font_choices),
	("ButtonFont", "NemesisFlatline", text_font_choices),
	("ChoiceList", "NemesisFlatline", text_font_choices),
	("ClockFont", "RobotoBlack", banner_font_choices),
	("DescriptionFont", "NemesisFlatline", text_font_choices),
	("EPGEventFont", "NemesisFlatline", text_font_choices),
	("EPGServiceFont", "NemesisFlatline", text_font_choices),
	("EPGTimeLineFont", "NemesisFlatline", text_font_choices),
	("FAVEventFont", "NemesisFlatline", text_font_choices),
	("FAVLCNFont", "NemesisFlatline", text_font_choices),
	("FAVServiceFont", "NemesisFlatline", text_font_choices),
	("FixedFont", "MPluss1M", fixed_font_choices),
	("HelpFont", "NemesisFlatline", text_font_choices),
	("InfoDescriptionFont", "NemesisFlatline", text_font_choices),
	("InfoEventFont", "NemesisFlatline", text_font_choices),
	("InfoOtherFont", "NemesisFlatline", text_font_choices),
	("InfoTimeFont", "NemesisFlatline", text_font_choices),
	("MenuFont", "NemesisFlatline", text_font_choices),
	("MovieSelectionFont", "NemesisFlatline", text_font_choices),
	("SMSHelperFont", "DejaVuSansCondensed", text_font_choices),
	("Regular", "NemesisFlatline", text_font_choices),
	("TextFont", "NemesisFlatline", text_font_choices),
	("TitleFont", "RobotoBlack", banner_font_choices)
]

background_image_choices = [
	("", _("Default"))
]

button_base = "ScreenTemplateButton"

button_colours = [
	"Red",
	"Green",
	"Yellow",
	"Blue",
]

button_choices = [
	("Bar", _("Bar")),
	("Block", _("Block")),
	("Button", _("Button")),
	("Circle", _("Circle")),
	("Legacy", _("Legacy")),
	("Wizard", _("Wizard"))
]

spinner_choices = [
	("", _("Default"))
]

option_elements = [
	("AlwaysActive", False, ConfigYesNo, None),
	("AlwaysShowButtons", True, ConfigYesNo, None),
	("BackgroundImage", "", ConfigSelection, background_image_choices),
	("ButtonStyle", "Block", ConfigSelection, button_choices),
	("EnhancedMenu", False, ConfigEnableDisable, None),
	("EPGSettings", False, ConfigYesNo, None),
	("EPGShowTicks", True, ConfigYesNo, None),
	("FAVSettings", False, ConfigYesNo, None),
	("FontSettings", False, ConfigYesNo, None),
	("GeneralSettings", False, ConfigYesNo, None),
	("InfoSettings", False, ConfigYesNo, None),
	("MenuSettings", False, ConfigYesNo, None),
	("PanelSettings", False, ConfigYesNo, None),
	("RecordBlink", True, ConfigYesNo, None),
	("ShowInExtensions", False, ConfigYesNo, None),
	("SortThemes", False, ConfigYesNo, None),
	("Spinner", "", ConfigSelection, spinner_choices),
	("TextSettings", False, ConfigYesNo, None),
	("UpdateBlink", True, ConfigYesNo, None),
	("UseGroups", True, ConfigYesNo, None)
]

display_groups = [
	"EPGSettings",
	"FAVSettings",
	"FontSettings",
	"GeneralSettings",
	"InfoSettings",
	"MenuSettings",
	"PanelSettings",
	"TextSettings"
]

repaint_list = [
	"BannerBorder",
	"BannerClock",
	"BannerClockBackgroundColour",
	"BannerClockBackgroundTransparency",
	"BannerTitle",
	"ButtonStyle",
	"FootnoteBackgroundColour",
	"FootnoteBackgroundTransparency",
	"FootnoteText",
	"MenuBackgroundColour",
	"MenuBackgroundTransparency",
	"MenuDisabled",
	"MenuSelectedColour",
	"MenuSelectedTransparency",
	"MenuText",
	"MenuTextSelected",
	"Pinstripe",
	"ScreenBackgroundColour",
	"ScreenBackgroundTransparency",
	"Scrollbar",
	"Text",
	"TextBackgroundColour",
	"TextBackgroundTransparency",
	"VolumeBackground",
	"VolumeColour"
]

dont_restart = [
	"BackgroundImage",
	"EPGSettings",
	"GeneralSettings",
	"FontSettings",
	"InfoSettings",
	"MenuSettings",
	"PanelSettings",
	"RecordBlink",
	"SortThemes",
	"Spinner",
	"TextSettings",
	"UpdateBlink",
	"UseGroups"
]

config.plugins.skin = ConfigSubsection()
config.plugins.skin.OverlayHD = ConfigSubsection()

for (label, colour, transparency) in colour_elements:
	if colour is None or transparency is None:
		if colour is not None:
			setattr(config.plugins.skin.OverlayHD, label, ConfigSelection(default=colour, choices=colour_choices))
			# print "[OverlayHD] DEBUG (definition): Colour '%s' = '%s'" % (label, colour)
		if transparency is not None:
			setattr(config.plugins.skin.OverlayHD, label, ConfigSelection(default=transparency, choices=transparency_choices))
			# print "[OverlayHD] DEBUG (definition): Colour '%s' = '%s'" % (label, transparency)
	else:
		if label == "ScreenBackground":
			c_choices = colour_choices
			t_choices = transparency_choices
		else:
			c_choices = background_choice + colour_choices
			t_choices = background_choice + transparency_choices
		setattr(config.plugins.skin.OverlayHD, "%sColour" % label, ConfigSelection(default=colour, choices=c_choices))
		setattr(config.plugins.skin.OverlayHD, "%sTransparency" % label, ConfigSelection(default=transparency, choices=t_choices))
		# print "[OverlayHD] DEBUG (definition): Colour '%sColour' = '%s'" % (label, colour)
		# print "[OverlayHD] DEBUG (definition): Colour '%sTransparency' = '%s'" % (label, transparency)

for (label, font, font_table) in font_elements:
	setattr(config.plugins.skin.OverlayHD, label, ConfigSelection(default=font, choices=font_table))
	# print "[OverlayHD] DEBUG (definition): Font '%s' = '%s' (%s)" % (label, font, font_table)

for fname in sorted(listdir(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/backgrounds"))):
	background_image_choices.append((fname, _(fname[0:-4])))
for fname in sorted(listdir(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/spinners"))):
	spinner_choices.append((fname, _(fname)))

for (label, default, config_type, option_table) in option_elements:
	if option_table:
		setattr(config.plugins.skin.OverlayHD, label, config_type(default=default, choices=option_table))
	else:
		setattr(config.plugins.skin.OverlayHD, label, config_type(default=default))
	# print "[OverlayHD] DEBUG (definition): Option '%s' = '%s' (%s)" % (label, default, option_table)


class OverlayHDSkinManager(Setup, HelpableScreen):
	ALLOW_SUSPEND = True

	def __init__(self, session):
		Setup.__init__(self, session=session, setup="OverlayHDSkinManager", plugin="Extensions/OverlayHD")
		HelpableScreen.__init__(self)  # TEMP

		self["key_yellow"] = StaticText(_("Themes"))
		self["key_blue"] = StaticText(_("Default"))
		self["key_help"] = StaticText(_("HELP"))  # TEMP

		self["OverlayHDActions"] = HelpableActionMap(self, "ColorActions", {
			"yellow": (self.theme, _("Manage themes")),
			"blue": (self.default, _("Apply the default skin settings"))
		}, prio=0, description=_("OverlayHD Functions"))

		background_image_choices = [("", _("Default"))]
		for fname in sorted(listdir(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/backgrounds"))):
			background_image_choices.append((fname, _(fname[0:-4])))
		config.plugins.skin.OverlayHD.BackgroundImage.setChoices(default=config.plugins.skin.OverlayHD.BackgroundImage.value, choices=background_image_choices)
		spinner_choices = [("", _("Default"))]
		for fname in sorted(listdir(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/spinners"))):
			spinner_choices.append((fname, _(fname)))
		config.plugins.skin.OverlayHD.Spinner.setChoices(default=config.plugins.skin.OverlayHD.Spinner.value, choices=spinner_choices)
		self.addNotifiers()

	def addNotifiers(self):
		config.plugins.skin.OverlayHD.UseGroups.addNotifier(self.changeGrouping, initial_call=False, immediate_feedback=True)
		for x in repaint_list:
			getattr(config.plugins.skin.OverlayHD, x).addNotifier(self.changeSettings, initial_call=False, immediate_feedback=True)

	def removeNotifiers(self):
		config.plugins.skin.OverlayHD.UseGroups.removeNotifier(self.changeGrouping)
		for x in repaint_list:
			getattr(config.plugins.skin.OverlayHD, x).removeNotifier(self.changeSettings)

# 	def selectionChanged(self):
# 		entry = self["config"].getCurrent()[1]
# 		for x in config.plugins.skin.OverlayHD.dict():
# 			if entry is getattr(config.plugins.skin.OverlayHD, x):
# 				print "[OverlayHD] DEBUG: 'config.plugins.skin.OverlayHD.%s'" % x
# 				break

	def changeGrouping(self, configElement):
		if config.plugins.skin.OverlayHD.UseGroups.value:
			for x in display_groups:
				getattr(config.plugins.skin.OverlayHD, x).value = False
		else:
			for x in display_groups:
				getattr(config.plugins.skin.OverlayHD, x).value = True

	def changeSettings(self, configElement):
		self.applySettings()

	def keyCancel(self):  # TEMP
		self.confirmCancel(False)

	def closeRecursive(self):  # TEMP
		self.confirmCancel(True)

	def confirmCancel(self, recursiveClose):  # TEMP
		if self.changedSettings(checkNoRestartList=False) or self["config"].isChanged():
			self.recursiveClose = recursiveClose
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("Really close without saving settings?"), default=False)
		else:
			self.close(recursiveClose)

	def cancelConfirm(self, result):  # TEMP
		if not result:
			return
		self.removeNotifiers()
		for x in config.plugins.skin.OverlayHD.dict():
			getattr(config.plugins.skin.OverlayHD, x).cancel()
		# This may not be needed...
		for x in self["config"].list:
			x[1].cancel()
		self.applySettings()
		self.close(self.recursiveClose)

	def keySave(self):  # TEMP
		self.removeNotifiers()
		changed = self.changedSettings(checkNoRestartList=True)
		for x in config.plugins.skin.OverlayHD.dict():
			getattr(config.plugins.skin.OverlayHD, x).save()
		# This may not be needed...
		for x in self["config"].list:
			x[1].save()
		config.plugins.skin.OverlayHD.save()
		self.applySettings()
		if changed:
			popup = self.session.openWithCallback(self.restartGUI, MessageBox, _("The GUI needs to be restarted to apply the changes.\n\nDo you want to restart the GUI now?"), MessageBox.TYPE_YESNO)
			popup.setTitle(self.setup_title)
		else:
			self.close()

	def restartGUI(self, answer):  # TEMP
		if answer:
			self.session.open(TryQuitMainloop, retvalue=QUIT_RESTART)
		self.close()

	def changedSettings(self, checkNoRestartList=True):
		# print "[OverlayHD] DEBUG: Looking for changes. checkNoRestartList = ", checkNoRestartList
		for x in config.plugins.skin.OverlayHD.dict():
			if checkNoRestartList and x in dont_restart:
				continue
			if getattr(config.plugins.skin.OverlayHD, x).isChanged():
				# print "[OverlayHD] DEBUG: Entries changed."
				return True
		# print "[OverlayHD] DEBUG: Entries NOT changed."
		return False

	def theme(self):
		self.removeNotifiers()
		self.session.openWithCallback(self.themeClosed, OverlayHDThemeManager)

	def themeClosed(self):
		self.applySettings()
		self.addNotifiers()

	def default(self):
		self.removeNotifiers()
		print "[OverlayHD] Setting OverlayHD skin to default settings."
		for (label, colour, transparency) in colour_elements:
			if colour is None or transparency is None:
				item = getattr(config.plugins.skin.OverlayHD, label)
				item.value = item.default
				# print "[OverlayHD] DEBUG (default): '%s' = '%s'" % (label, item.default)
			else:
				item = getattr(config.plugins.skin.OverlayHD, "%sColour" % label)
				item.value = item.default
				# print "[OverlayHD] DEBUG (default): '%sColour' = '%s'" % (label, item.default)
				item = getattr(config.plugins.skin.OverlayHD, "%sTransparency" % label)
				item.value = item.default
				# print "[OverlayHD] DEBUG (default): '%sTransparency' = '%s'" % (label, item.default)
		for (label, font, font_table) in font_elements:
			item = getattr(config.plugins.skin.OverlayHD, label)
			item.value = item.default
			# print "[OverlayHD] DEBUG (default): '%s' = '%s'" % (label, item.default)
		for (label, default, config_type, option_table) in option_elements:
			item = getattr(config.plugins.skin.OverlayHD, label)
			item.value = item.default
			# print "[OverlayHD] DEBUG (default): '%s' = '%s'" % (label, item.default)
		if config.skin.primary_skin.value == "OverlayHD/skin.xml":
			self.applySettings()
			msg = ""
		else:
			msg = "\n\nNOTE: OverlayHD is not the active skin."
		popup = self.session.open(MessageBox, _("Default OverlayHD skin settings applied.%s") % msg, MessageBox.TYPE_INFO, 5)
		popup.setTitle(self.setup_title)
		self.addNotifiers()

	def applySettings(self):
		index = self["config"].getCurrentIndex()
		applySkinSettings(False)
		self.applySkin()
		self.instance.invalidate()  # Remove this when the underlying bug is fixed!
		self["config"].setCurrentIndex(index)


class OverlayHDThemeManager(Screen, HelpableScreen):
	skin = """
	<screen name="OverlayHDThemeManager" title="OverlayHD Theme Manager" position="0,0" size="1280,720" backgroundColor="ScreenBackground" flags="wfNoBorder">
		<panel name="ScreenTemplate" />
		<ePixmap pixmap="menus/setup_default.png" position="50,100" size="300,500" alphatest="on" transparent="1" />
		<widget source="themes" render="Listbox" position="400,80" size="830,550" backgroundColor="MenuBackground" backgroundColorSelected="MenuSelected" enableWrapAround="1" foregroundColor="MenuText" foregroundColorSelected="MenuTextSelected" scrollbarMode="showOnDemand" transparent="0">
			<convert type="TemplatedMultiContent">
				{
				"template":
					[
					MultiContentEntryText(pos = (20, 0), size = (790, 35), font = 0, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0),
					],
				"fonts": [gFont("Regular", 25)],
				"itemHeight": 35
				}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = OverlayHDThemeManager.skin
		# self.skinName = ["OverlayHDThemeManager"]
		HelpableScreen.__init__(self)
		self.setup_title = _("OverlayHD Theme Manager")
		Screen.setTitle(self, self.setup_title)

		self["key_menu"] = StaticText(_("MENU"))
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Apply"))
		self["key_yellow"] = StaticText(_("Save"))
		self["key_blue"] = StaticText(_("Create"))
		self["key_help"] = StaticText(_("HELP"))

		self["actions"] = HelpableActionMap(self, ["OkCancelActions", "ColorActions", "MenuActions"], {
			"ok": (self.applyTheme, _("Apply the currently highlighted theme, return to OverlayHD Skin Manager")),
			"cancel": (self.cancelTheme, _("Cancel theme selection, return to OverlayHD Skin Manager")),
			"menu": (self.themeMenu, _("Menu of actions applicable to the currently highlighted theme")),
			"red": (self.cancelTheme, _("Cancel theme selection, return to OverlayHD Skin Manager")),
			"green": (self.applyTheme, _("Apply the currently highlighted theme, return to OverlayHD Skin Manager")),
			"yellow": (self.saveTheme, _("Save current skin settings as the currently highlighted theme")),
			"blue": (self.newTheme, _("Create a new theme using the current skin settings"))
		}, prio=0, description=_("Theme Functions"))
		self["themes"] = List()
		self.filename = resolveFilename(SCOPE_CONFIG, "OverlayHD_themes.xml")
		self.dom_themes = None
		try:
			self.dom_themes = xml.etree.cElementTree.parse(self.filename)
		except (IOError, OSError), (err, errmsg):
			if err == errno.ENOENT:
				self.dom_themes = xml.etree.cElementTree.ElementTree(xml.etree.cElementTree.Element("themes"))
				self.updateTheme("Default", mode="default")
				self.updateTheme("Current", mode="value")
				self.saveThemes()
				print "[OverlayHD] Themes 'Default' and 'Current' created."
			else:
				self.errtext = "Error %d: %s - '%s'" % (err, errmsg, self.filename)
				print "[OverlayHD] Error opening themes file! (%s)" % self.errtext
		self["themes"].updateList(self.listThemes())
		self.onShown.append(self.screenShown)

	def screenShown(self):
		if self.dom_themes is None:
			popup = self.session.open(MessageBox, _("Unable to open/access themes file!\n\n%s") % self.errtext, MessageBox.TYPE_ERROR, 10)
			popup.setTitle(self.setup_title)
			self.close()

	def findTheme(self, name):
		if self.dom_themes:
			themes = self.dom_themes.findall("theme")
			for theme in themes:
				n = theme.get("name", None)
				if n == name:
					return theme
		return None

	def updateTheme(self, name=None, mode="value"):
		if name is None:
			name = self["themes"].getCurrent()[0]
		theme = self.findTheme(name)
		if theme is None:
			theme = xml.etree.cElementTree.SubElement(self.dom_themes.getroot(), "theme", {"name": name})
		else:
			theme.clear()
			theme.set("name", name)
		for (label, colour, transparency) in colour_elements:
			if colour is None or transparency is None:
				item = eval("config.plugins.skin.OverlayHD.%s.%s" % (label, mode))
				element = xml.etree.cElementTree.SubElement(theme, "colour", {"name": label, "value": item})
				# print "[OverlayHD] DEBUG: '%s' = '%s'" % (label, item)
			else:
				item = eval("config.plugins.skin.OverlayHD.%sColour.%s" % (label, mode))
				element = xml.etree.cElementTree.SubElement(theme, "colour", {"name": "%sColour" % label, "value": item})
				# print "[OverlayHD] DEBUG: '%sColour' = '%s'" % (label, item)
				item = eval("config.plugins.skin.OverlayHD.%sTransparency.%s" % (label, mode))
				element = xml.etree.cElementTree.SubElement(theme, "colour", {"name": "%sTransparency" % label, "value": item})
				# print "[OverlayHD] DEBUG: '%sTransparency' = '%s'" % (label, item)
		for (label, font, font_table) in font_elements:
			item = eval("config.plugins.skin.OverlayHD.%s.%s" % (label, mode))
			element = xml.etree.cElementTree.SubElement(theme, "font", {"name": label, "value": item})
			# print "[OverlayHD] DEBUG: '%s' = '%s'" % (label, item)
		for (label, default, config_type, option_table) in option_elements:
			item = str(eval("config.plugins.skin.OverlayHD.%s.%s" % (label, mode)))
			if option_table is None:
				element = xml.etree.cElementTree.SubElement(theme, "option", {"name": label, "type": "boolean", "value": item})
			else:
				element = xml.etree.cElementTree.SubElement(theme, "option", {"name": label, "value": item})
			# print "[OverlayHD] DEBUG: '%s' = '%s'" % (label, item)

	def listThemes(self):
		list = []
		if self.dom_themes:
			themes = self.dom_themes.findall("theme")
			# print "[OverlayHD] Theme count = %d" % len(themes)
			for theme in themes:
				name = theme.get("name", None)
				list.append((name, name))
				# print "[OverlayHD] Theme = '%s'" % name
			if config.plugins.skin.OverlayHD.SortThemes.value:
				list.sort(key=lambda item: item[0])
		return list

	def saveThemes(self):
		self["themes"].updateList(self.listThemes())
		self.xmlIndent(self.dom_themes.getroot())
		self.dom_themes.write(self.filename)

	def xmlIndent(self, element, level=0):
		indent = "\n" + level * "\t"
		if len(element):
			if not element.text or not element.text.strip():
				element.text = indent + "\t"
			if not element.tail or not element.tail.strip():
				element.tail = indent
			for element in element:
				self.xmlIndent(element, level + 1)
			if not element.tail or not element.tail.strip():
				element.tail = indent
		else:
			if level and (not element.tail or not element.tail.strip()):
				element.tail = indent

	def checkThemeName(self, name):
		validflag = True
		if name is None:
			validflag = False
		if name == "":
			validflag = False
			popup = self.session.open(MessageBox, _("Theme name can not be blank!"), MessageBox.TYPE_ERROR, 5)
			popup.setTitle(self.setup_title)
		if self.findTheme(name):
			validflag = False
			popup = self.session.open(MessageBox, _("Theme name '%s' already exists!") % name, MessageBox.TYPE_ERROR, 5)
			popup.setTitle(self.setup_title)
		return validflag

	def themeMenu(self):
		theme_actions = [
			(_("Save theme"), self.saveTheme),
			(_("Rename theme"), self.renameTheme),
			(_("Delete theme"), self.deleteTheme),
			(_("Export theme"), self.exportTheme),
			(_("Import theme"), self.importTheme),
			(_("Create new theme"), self.newTheme)
		]
		name = self["themes"].getCurrent()[0]
		menu = []
		for action in theme_actions:
			menu.append(action)
		self.session.openWithCallback(self.themeMenuAction, ChoiceBox, title=_("OverlayHD Theme: '%s'") % name, list=menu, skin_name="OverlayHDThemeMenu")

	def themeMenuAction(self, choice):
		if choice is None:
			return
		# print "[OverlayHD] Theme menu choice =", choice
		choice[1](self["themes"].getCurrent()[0])

	def cancelTheme(self):
		self.close()

	def applyTheme(self, name=None):
		if name is None:
			try:
				name = self["themes"].getCurrent()[0]
			except:
				popup = self.session.open(MessageBox, _("There are no themes to apply!"), MessageBox.TYPE_ERROR, 5)
				popup.setTitle(self.setup_title)
				return
		theme = self.findTheme(name)
		if theme is not None:
			print "[OverlayHD] Loading theme '%s'." % name
			colours = theme.findall("colour")
			for colour in colours:
				name = colour.get("name", None)
				value = colour.get("value", None)
				if name and value:
					try:
						getattr(config.plugins.skin.OverlayHD, name).value = value
						# print "[OverlayHD] Theme colour = '%s', value = '%s'" % (name, value)
					except:
						print "[OverlayHD] Theme colour = '%s', value = '%s' is invalid!" % (name, value)
			fonts = theme.findall("font")
			for font in fonts:
				name = font.get("name", None)
				value = font.get("value", None)
				if name and value:
					try:
						getattr(config.plugins.skin.OverlayHD, name).value = value
						# print "[OverlayHD] Theme font = '%s', value = '%s'" % (name, value)
					except:
						print "[OverlayHD] Theme font = '%s', value = '%s' is invalid!" % (name, value)
			options = theme.findall("option")
			for option in options:
				name = option.get("name", None)
				type = option.get("type", None)
				value = option.get("value", None)
				if name and value:
					try:
						if type == "boolean":
							if value in ("True", "Yes", "On", "Enable", "Enabled"):
								value = True
							if value in ("False", "No", "Off", "Disable", "Disabled"):
								value = False
						getattr(config.plugins.skin.OverlayHD, name).value = value
						# print "[OverlayHD] Theme option = '%s', value = '%s'" % (name, value)
					except:
						print "[OverlayHD] Theme option = '%s', value = '%s' is invalid!" % (name, value)
		self.close()

	def newTheme(self, name=None):
		popup = self.session.openWithCallback(self.newThemeAction, VirtualKeyBoard, title=_("Enter a name for this new theme:"), text="")
		popup.setTitle(self.setup_title)

	def newThemeAction(self, name):
		if self.checkThemeName(name):
			print "[OverlayHD] Creating theme '%s'." % name
			self.updateTheme(name)
			self.saveThemes()
			# popup = self.session.open(MessageBox, _("Theme '%s' created.") % name, MessageBox.TYPE_INFO, 3)
			# popup.setTitle(self.setup_title)

	def saveTheme(self, name=None):
		if name is None:
			try:
				name = self["themes"].getCurrent()[0]
			except:
				self.newTheme()
				return
		print "[OverlayHD] Saving theme '%s'." % name
		self.updateTheme(name)
		self.saveThemes()
		popup = self.session.open(MessageBox, _("Theme '%s' saved.") % name, MessageBox.TYPE_INFO, 3)
		popup.setTitle(self.setup_title)

	def renameTheme(self, name):
		popup = self.session.openWithCallback(self.renameThemeAction, VirtualKeyBoard, title=_("Enter new name for the '%s' theme:") % name, text=name)
		popup.setTitle(self.setup_title)

	def renameThemeAction(self, name):
		if self.checkThemeName(name):
			oldname = self["themes"].getCurrent()[0]
			theme = self.findTheme(oldname)
			if theme is not None:
				print "[OverlayHD] Renaming theme '%s' to '%s'." % (oldname, name)
				theme.set("name", name)
				self.saveThemes()
				# popup = self.session.open(MessageBox, _("Theme '%s' renamed to '%s'.") % (oldname, name), MessageBox.TYPE_INFO, 3)
				# popup.setTitle(self.setup_title)

	def deleteTheme(self, name):
		popup = self.session.openWithCallback(self.deleteThemeAction, MessageBox, _("Do you really want to delete the '%s' theme?") % name, MessageBox.TYPE_YESNO)
		popup.setTitle(self.setup_title)

	def deleteThemeAction(self, answer):
		if answer:
			name = self["themes"].getCurrent()[0]
			theme = self.findTheme(name)
			if theme is not None:
				print "[OverlayHD] Deleting theme '%s'." % name
				self.dom_themes.getroot().remove(theme)
				self.saveThemes()
				# popup = self.session.open(MessageBox, _("Theme '%s' deleted.") % name, MessageBox.TYPE_INFO, 3)
				# popup.setTitle(self.setup_title)

	def exportTheme(self, name):
		print "[OverlayHD] Export theme."
		popup = self.session.open(MessageBox, _("Theme export not yet available!"), MessageBox.TYPE_ERROR, 5)
		popup.setTitle(self.setup_title)
		# self.saveThemes()

	def importTheme(self, name):
		print "[OverlayHD] Import theme."
		popup = self.session.open(MessageBox, _("Theme import not yet available!"), MessageBox.TYPE_ERROR, 5)
		popup.setTitle(self.setup_title)
		# self.saveThemes()

def applySkinSettings(fullinit):
	if config.skin.primary_skin.value == "OverlayHD/skin.xml":
		(distro, code) = distro_configs.get(getImageDistro(), ("Unknown", "Enigma2"))
		if fullinit:
			print "[OverlayHD] OverlayHD Skin Manager version %s: Configuring to run in '%s' mode." % (PLUGIN_VERSION_NUMBER, distro)
			for screen in dom_screens:
				element, path = dom_screens.get(screen, (None, None))
				if element is not None:
					panels = element.findall("panel")
					if panels is not None:
						for panel in panels:
							name = panel.get("name", None)
							base = panel.get("base", None)
							if name and base:
								panel.set("name", base + code)
								# print "[OverlayHD] DEBUG: Screen '%s', Base '%s', OldName '%s' -> NewName '%s'" % (screen, base, name, base + code)
								print "[OverlayHD] Adjusting screen '%s'." % screen
								break
		#
		print "[OverlayHD] Applying OverlayHD skin settings."
		for (label, colour, transparency) in colour_elements:
			if transparency is None:
				item = getattr(config.plugins.skin.OverlayHD, label).value
				piglabel = "%s%s%s" % (label[0:3], "PIG", label[3:])
				if label in derived_foreground_elements:
					colorNames[label] = colorNames[item]
					colorNames[piglabel] = colorNames[item]
				elif label in derived_background_elements:
					if config.plugins.skin.OverlayHD.EPGTransparency.value == "Background":
						tran = long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value, 0x10)
					else:
						tran = long(config.plugins.skin.OverlayHD.EPGTransparency.value, 0x10)
					colorNames[label] = gRGB(colorNames[item].argb() | tran)
					colorNames[piglabel] = colorNames[item]
				else:
					colorNames[label] = colorNames[item]
			elif colour is not None:
				col = getattr(config.plugins.skin.OverlayHD, "%sColour" % label).value
				if col == "Background":
					col = config.plugins.skin.OverlayHD.ScreenBackgroundColour.value
				tran = getattr(config.plugins.skin.OverlayHD, "%sTransparency" % label).value
				if tran == "Background":
					tran = long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value, 0x10)
				else:
					tran = long(tran, 0x10)
				colorNames[label] = gRGB(colorNames[col].argb() | tran)
		for (label, font, font_table) in font_elements:
			data = list(fonts[label])
			data[0] = getattr(config.plugins.skin.OverlayHD, label).value
			fonts[label] = tuple(data)
		for (label, default, config_type, options_table) in option_elements:
			if label == "AlwaysShowButtons":
				for colour in button_colours:
					element, path = dom_screens.get(button_base + colour, (None, None))
					if element is not None:
						panels = element.findall("panel")
						if panels is not None:
							# print "[OverlayHD] %s panel (%d instances):" % (button_base + colour, len(panels))
							for panel in panels:
								if config.plugins.skin.OverlayHD.AlwaysShowButtons.value:
									if panel.get("conditional", None) is not None:
										del panel.attrib["conditional"]
										# print "[OverlayHD]       panel - Removing conditional attribute."
								else:
									if panel.get("conditional", None) is None:
										panel.set("conditional", "key_%s" % colour.lower())
										# print "[OverlayHD]       panel - Adding conditional attribute."
								# print "[OverlayHD] DEBUG: XML dump:\n\t%s\n" % xml.etree.cElementTree.tostring(element)
					for (style, label) in button_choices:
						element, path = dom_screens.get(button_base + colour + style, (None, None))
						if element is not None:
							pixmaps = element.findall("ePixmap")
							if pixmaps is not None:
								# print "[OverlayHD] %s ePixmap (%d instances):" % (button_base + colour + style, len(pixmaps))
								for pixmap in pixmaps:
									if config.plugins.skin.OverlayHD.AlwaysShowButtons.value:
										if pixmap.get("objectTypes", None) is not None:
											del pixmap.attrib["objectTypes"]
											# print "[OverlayHD]       ePixmap - Removing objectTypes attribute."
									else:
										if pixmap.get("objectTypes", None) is None:
											pixmap.set("objectTypes", "key_%s,Button,Label" % colour.lower())
											# print "[OverlayHD]       ePixmap - Adding objectTypes attribute."
							widgets = element.findall("widget")
							if widgets is not None:
								# print "[OverlayHD] %s widget (%d instances):" % (button_base + colour + style, len(widgets))
								for widget in widgets:
									if widget.get("render", None) == "Pixmap":
										if config.plugins.skin.OverlayHD.AlwaysShowButtons.value:
											if widget.get("objectTypes", None) is not None:
												del widget.attrib["objectTypes"]
												# print "[OverlayHD]       Pixmap - Removing objectTypes attribute."
												converts = widget.findall("convert")
												if converts is not None:
													for convert in converts:
														if convert.get("type", None) == "ConditionalShowHide":
															widget.remove(convert)
															# print "[OverlayHD]       Pixmap - Removing 'ConditionalShowHide' converter."
															break
										else:
											if widget.get("objectTypes", None) is None:
												widget.set("objectTypes", "key_%s,StaticText" % colour.lower())
												# print "[OverlayHD]       Pixmap - Adding 'source' objectTypes attribute."
												found = False
												converts = widget.findall("convert")
												if converts is not None:
													for convert in converts:
														if convert.get("type", None) == "ConditionalShowHide":
															found = True
															# print "[OverlayHD]       Pixmap - 'ConditionalShowHide' converter exists."
												if not found:
													convert = xml.etree.cElementTree.Element("convert", type="ConditionalShowHide")
													widget.append(convert)
													# print "[OverlayHD]       Pixmap - Adding 'ConditionalShowHide' converter."
							# print "[OverlayHD] DEBUG: XML widget dump:\n\t%s\n" % xml.etree.cElementTree.tostring(element)
			elif label == "BackgroundImage":
				dst = eEnv.resolve("${datadir}") + "/backdrop.mvi"
				try:
					unlink(dst)
				except:
					pass
				src = getattr(config.plugins.skin.OverlayHD, label).value
				try:
					if src == "":
						src = eEnv.resolve("${datadir}/bootlogo.mvi")
						shutil.copy(src, dst)
					else:
						shutil.copy(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/backgrounds/%s" % src), dst)
				except (IOError, OSError), (err, errmsg):
					errtext = "Error %d: %s - '%s'" % (err, errmsg, dst)
					print "[OverlayHD] Error copying boot logo image! (%s)" % errtext
			elif label == "ButtonStyle":
				for colour in button_colours:
					element, path = dom_screens.get(button_base + colour, (None, None))
					if element is not None:
						panel = element.find("panel")
						name = panel.get("name", None)
						if name is not None:
							panel.set("name", button_base + colour + config.plugins.skin.OverlayHD.ButtonStyle.value)
			elif label == "EPGShowTicks":
				if config.plugins.skin.OverlayHD.EPGShowTicks.value:
					setting = "yes"
				else:
					setting = "no"
				for screen in ("EPGTimeLinePanel", "GraphicalEPG", "GraphicalEPGPIG", "GraphicalInfoBarEPG"):
					element, path = dom_screens.get(screen, (None, None))
					if element is not None:
						widgets = element.findall("widget")
						if widgets is not None:
							for widget in widgets:
								if widget.get("TimelineTicksOn", None) is not None:
									widget.set("TimelineTicksOn", setting)
									break
			elif label == "RecordBlink":
				element, path = dom_screens.get("ChannelFormatPanel", (None, None))
				if element is not None:
					widgets = element.findall("widget")
					if widgets is not None:
						for widget in widgets:
							if widget.get("source", None) == "session.RecordState":
								converts = widget.findall("convert")
								if converts is not None:
									for convert in converts:
										if convert.get("type", None) == "ConditionalShowHide":
											if config.plugins.skin.OverlayHD.RecordBlink.value:
												convert.text = "Blink"
											else:
												convert.text = ""
											break
			elif label == "Spinner":
				linkname = resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/spinner")
				if islink(linkname):
					unlink(linkname)
				elif isdir(linkname):
					shutil.rmtree(linkname)
					print "[OverlayHD] NOTE: Unexpected spinner directory found and deleted!"
				elif exists(linkname):
					remove(linkname)
					print "[OverlayHD] NOTE: Unexpected spinner file found and deleted!"
				item = getattr(config.plugins.skin.OverlayHD, label).value
				if item != "":
					try:
						symlink(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/spinners/%s" % item), linkname)
					except (IOError, OSError), (err, errmsg):
						errtext = "Error %d: %s - '%s'" % (err, errmsg, linkname)
						print "[OverlayHD] Error linking spinner directory! (%s)" % errtext
			elif label == "UpdateBlink":
				element, path = dom_screens.get("ChannelFormatPanel", (None, None))
				if element is not None:
					widgets = element.findall("widget")
					if widgets is not None:
						for widget in widgets:
							if widget.get("source", None) in ("global.OnlineStableUpdateState", "global.OnlineUnstableUpdateState"):
								converts = widget.findall("convert")
								if converts is not None:
									for convert in converts:
										if convert.get("type", None) == "ConditionalShowHide":
											if config.plugins.skin.OverlayHD.UpdateBlink.value:
												convert.text = "Blink"
											else:
												convert.text = ""
											break
		if code == "Beyonwiz":
			from skin import reloadWindowstyles
			reloadWindowstyles()
	else:
		print "[OverlayHD] OverlayHD is not the active skin."

def updateOverlayHD():
	# This code is used to ensure that older environments are brought up to current requirements...
	# Remove the old settings conversion program...
	src = resolveFilename(SCOPE_CURRENT_PLUGIN, "Extensions/OverlayHD/OverlayHD_Update")
	if isfile(src):
		remove(src)
		print "[OverlayHD] Defunct settings converter deleted."
	# Relocate and remove the original themes.xml template...
	src = resolveFilename(SCOPE_CURRENT_PLUGIN, "Extensions/OverlayHD/themes.xml")
	dst = resolveFilename(SCOPE_CONFIG, "OverlayHD_themes.xml")
	if isfile(src):
		if not isfile(dst):
			shutil.move(src, dst)
			print "[OverlayHD] Themes file moved to new location."
		else:
			remove(src)
			print "[OverlayHD] Default themes file deleted."
	# Set defunct attributes to the default so they will be removed from the settings file...
	for attr in ("BootImage", "ClockStyle", "EPGChannel", "EPGChannelSelected", "EPGDetails", "EPGDuration", "EPGLCN", "EPGProgram", "EPGProgramSelected", "EPGProvider", "EPGRating", "EPGTimes", "EPGTimesSelected", "InfoFileSize"):
		setattr(config.plugins.skin.OverlayHD, attr, ConfigSelection(default="Default", choices=[("Default"), ("None")]))
		getattr(config.plugins.skin.OverlayHD, attr).value = getattr(config.plugins.skin.OverlayHD, attr).default
		getattr(config.plugins.skin.OverlayHD, attr).save()
	config.plugins.skin.OverlayHD.save()

def start_menu_main(menuid, **kwargs):
	if menuid == "system":
		return [(_("OverlayHD Skin Manager"), main, "OverlayHD", None)]
	else:
		return []

def main(session, **kwargs):
	session.open(OverlayHDSkinManager)

def autostart(reason, **kwargs):
	# (distro, code) = distro_configs.get(getImageDistro(), ("Unknown", "Enigma2"))
	if reason == 0:
		# print "[OverlayHD] OverlayHD Skin Manager for '%s' loaded." % distro
		updateOverlayHD()
		applySkinSettings(True)
	elif reason == 1:
		# print "[OverlayHD] OverlayHD Skin Manager for '%s' unloaded." % distro
		pass

def Plugins(**kwargs):
	list = []
	if config.plugins.skin.OverlayHD.AlwaysActive.value or config.skin.primary_skin.value == "OverlayHD/skin.xml":
		list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_AUTOSTART], fnc=autostart))
		list.append(PluginDescriptor(name=_("OverlayHD"), where=[PluginDescriptor.WHERE_PLUGINMENU], description="OverlayHD Skin Manager version %s" % PLUGIN_VERSION_NUMBER, icon="OverlayHD.png", fnc=main))
		if config.plugins.skin.OverlayHD.ShowInExtensions.value:
			list.append(PluginDescriptor(name=_("OverlayHD Skin Manager"), where=[PluginDescriptor.WHERE_EXTENSIONSMENU], description="OverlayHD Skin Manager version %s" % PLUGIN_VERSION_NUMBER, icon="OverlayHD.png", fnc=main))
	return list
