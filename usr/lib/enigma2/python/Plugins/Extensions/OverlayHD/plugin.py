#====================================================
# OverlayHD Skin Manager
# Version Date - 11-May-2016
# Version Number - 1.52
# Coding by IanSav
#====================================================
# Remember to change the version number below!!!
#====================================================

from Components.ActionMap import HelpableActionMap
from Components.Label import Label
from Components.Sources.List import List
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigEnableDisable, ConfigSelection
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.HelpMenu import HelpableScreen
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Setup import Setup
from Screens.Standby import TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import resolveFilename, SCOPE_CONFIG, SCOPE_CURRENT_SKIN, SCOPE_CURRENT_PLUGIN
from enigma import eEnv, gRGB
from os import listdir, remove, symlink, unlink
from os.path import exists, isdir, isfile, islink
from skin import dom_screens, colorNames, reloadWindowstyles, fonts
import errno, shutil
import xml.etree.cElementTree

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
	("EPGChannel", "LightBlue", None),
	("EPGChannelSelected", "Blue", None),
	("EPGDetails", "White", None),
	("EPGDuration", "Grey", None),
	("EPGGridBackground", "Orange", None),
	("EPGGridBorder", "Black", None),
	("EPGLCN", "LightBlue", None),
	("EPGOverlayBorder", "Black", None),
	("EPGOverlayColour", "WarmYellow", None),
	("EPGProgram", "White", None),
	("EPGProgramSelected", "White", None),
	("EPGProgressBackground", "DeepGrey", None),
	("EPGProgressBorder", "WarmYellow", None),
	("EPGProgressColour", "WarmYellow", None),
	("EPGProvider", "LightBlue", None),
	("EPGRating", "Grey", None),
	("EPGTimeLine", "Yellow", None),
	("EPGTimes", "Grey", None),
	("EPGTimesSelected", "Silver", None),
	("EPGTransparency", None, "Background"),
	("EPGEntryBackgroundColor", "MidBlack", None),
	("EPGEntryBackgroundColorSelected", "Grey", None),
	("EPGEntryForegroundColor", "White", None),
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
	("FootnoteText", "DimGrey", None),
	("HelpPress", "Yellow", None),
	("InfoBackground", "Background", "Background"),
	("InfobarMediaBackground", "Background", "Background"),
	("InfobarTVBackground", "Background", "Background"),
	("InfoBouquet", "LightBlue", None),
	("InfoBroadcaster", "LightBlue", None),
	("InfoChannel", "LightBlue", None),
	("InfoDetailsNext", "White", None),
	("InfoDetailsNow", "White", None),
	("InfoDiskStats", "DullYellow", None),
	("InfoDurationNext", "LightBlue", None),
	("InfoDurationNow", "LightBlue", None),
	("InfoFileSizeNext", "LightBlue", None),
	("InfoFileSizeNow", "LightBlue", None),
	("InfoLCN", "LightBlue", None),
	("InfoMediaLength", "LightBlue", None),
	("InfoMediaName", "LightBlue", None),
	("InfoMediaPosition", "White", None),
	("InfoMediaRemaining", "White", None),
	("InfoProgramNext", "White", None),
	("InfoProgramNow", "White", None),
	("InfoProgressBackground", "DeepGrey", None),
	("InfoProgressBorder", "Grey", None),
	("InfoProgressColour", "Green", None),
	("InfoRatingNext", "Grey", None),
	("InfoRatingNow", "Grey", None),
	("InfoRecordingBackground", "DeepGrey", None),
	("InfoRecordingBorder", "Grey", None),
	("InfoRecordingColour", "OrangeRed", None),
	("InfoTimesNext", "Grey", None),
	("InfoTimesNow", "Grey", None),
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
	("Resolution", "Silver", None),
	("ResolutionBackground", "Background", "Background"),
	("ScreenBackground", "Black", "0x3f000000"),
	("Scrollbar", "Gainsboro", None),
	("SMSHelperBackground", "Background", "Background"),
	("SMSHelperText", "White", None),
	("Text", "White", None),
	("TextBackground", "Background", "Background"),
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
	("GoodTimes", _("Good Times")),
	("KhammuRabi", _("Khammu Rabi")),
	("NemesisFlatline", _("Nemesis Flatline")),
	("RobotoBlack", _("Roboto Black")),
	("ValisEnigma", _("Valis Enigma"))
]

text_font_choices = [
	("ArialNarrow", _("Arial Narrow")),
	("KhammuRabi", _("Khammu Rabi")),
	("NemesisFlatline", _("Nemesis Flatline")),
	("ValisEnigma", _("Valis Enigma"))
]

fixed_font_choices = [
	("AndaleMono", _("Andale Mono")),
	("MPluss1M", _("M+ 1M")),
	("VeraSansMono", _("Vera Sans Mono"))
]

font_elements = [
	("ClockFont", "RobotoBlack", banner_font_choices),
	("TitleFont", "RobotoBlack", banner_font_choices),
	("ButtonFont", "NemesisFlatline", text_font_choices),
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
	("SMSHelperFont", "MPluss1M", fixed_font_choices),
	("Regular", "NemesisFlatline", text_font_choices),
	("TextFont", "NemesisFlatline", text_font_choices)
]

background_image_choices = [
	("", _("Default"))
]

button_choices = [
	("Bar", _("Bar")),
	("Block", _("Block")),
	("Button", _("Button")),
	("Legacy", _("Legacy")),
	("Wizard", _("Wizard"))
]

clock_choices = [
	("24Hour", _("Digital (24 Hour)")),
	("12Hour", _("Digital (12 Hour)")),
	("Analogue", _("Analogue (12 Hour)"))
]

epg_choices = [
	("left", _("Left aligned")),
	("center", _("Centred"))
]

spinner_choices = [
	("", _("Default"))
]

option_elements = [
	("AlwaysActive", False, ConfigYesNo, None),
	("BackgroundImage", "", ConfigSelection, background_image_choices),
	("ButtonStyle", "Block", ConfigSelection, button_choices),
	("ClockStyle", "24Hour", ConfigSelection, clock_choices),
	("EnhancedMenu", False, ConfigEnableDisable, None),
	("EPGAlignment", "left", ConfigSelection, epg_choices),
	("EPGSettings", False, ConfigYesNo, None),
	("EPGShowTicks", True, ConfigYesNo, None),
	("FAVSettings", False, ConfigYesNo, None),
	("FontSettings", False, ConfigYesNo, None),
	("GeneralSettings", False, ConfigYesNo, None),
	("InfoSettings", False, ConfigYesNo, None),
	("MenuSettings", False, ConfigYesNo, None),
	("PanelSettings", False, ConfigYesNo, None),
	("RecordBlink", True, ConfigYesNo, None),
	("SortThemes", False, ConfigYesNo, None),
	("Spinner", "", ConfigSelection, spinner_choices),
	("TextSettings", False, ConfigYesNo, None),
	("UpdateBlink", True, ConfigYesNo, None),
	("UseGroups", True, ConfigYesNo, None)
]

button_screens = [
	"ScreenTemplateButtonRed",
	"ScreenTemplateButtonGreen",
	"ScreenTemplateButtonYellow",
	"ScreenTemplateButtonBlue",
	"ScreenTemplateButtonColourBacks"
]

clock_screens = [
	"ClockBannerPanel",
	"ScreenTemplateClock"
]

display_groups = [
	"EPGSettings",
	"FontSettings",
	"GeneralSettings",
	"InfoSettings",
	"MenuSettings",
	"PanelSettings",
	"TextSettings"
]

repaint_notifications = [
	"BannerBorder",
	"BannerClock",
	"BannerClockBackgroundColour",
	"BannerClockBackgroundTransparency",
	"BannerTitle",
	"ButtonStyle",
	"ClockStyle",
	"FootnoteBackgroundColour",
	"FootnoteBackgroundTransparency",
	"FootnoteText",
	"HelpPress",
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
	"UseGroups",
	"VolumeBackground",
	"VolumeColour"
]

restart_safe = [
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

	skin = """
	<screen name="OverlayHDSkinManager" title="OverlayHD Skin Manager" position="0,0" size="1280,720" backgroundColor="ScreenBackground" flags="wfNoBorder">
		<panel name="ScreenTemplate" />
		<panel name="ScreenTemplateButtonColours" />
		<panel name="ScreenTemplateButtonTextVKey" />
		<panel name="ScreenTemplateButtonHelp" />
		<ePixmap pixmap="menus/setup_default.png" position="50,100" size="300,500" alphatest="on" transparent="1" />
		<widget name="menuimage" position="50,100" size="300,500" alphatest="on" transparent="1" zPosition="+1" />
		<panel name="ScreenTemplateConfig4" />
		<panel name="ScreenTemplateFootnote4" />
		<panel name="ScreenTemplateDescription4" />
	</screen>"""

	def __init__(self, session):
		Setup.__init__(self, session=session, setup="OverlayHDSkinManager", plugin="Extensions/OverlayHD")
 		self.skin = OverlayHDSkinManager.skin
		self.skinName = ["OverlayHDSkinManager", "Setup"]
		HelpableScreen.__init__(self)
		self.setup_title = _("OverlayHD Skin Manager")

		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Save"))
		self["key_yellow"] = Label(_("Themes"))
		self["key_blue"] = Label(_("Default"))

		self["actions"] = HelpableActionMap(self, ["OkCancelActions", "ColorActions"], {
			"ok": (self.save, _("Save and apply changes")),
			"OK": (self.save, _("Save and apply changes")),
			"cancel": (self.cancel, _("Cancel and discard changes")),
			"red" : (self.cancel, _("Cancel and discard changes")),
			"green": (self.save, _("Save and apply changes")),
			"yellow": (self.theme, _("Manage themes")),
			"blue": (self.default, _("Apply the default skin settings"))
		}, description=_("Basic Functions"))

		self.process = False
		background_image_choices = [("", _("Default"))]
		for fname in sorted(listdir(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/backgrounds"))):
			background_image_choices.append((fname, _(fname[0:-4])))
		config.plugins.skin.OverlayHD.BackgroundImage.setChoices(default=config.plugins.skin.OverlayHD.BackgroundImage.default, choices=background_image_choices)
		spinner_choices = [("", _("Default"))]
		for fname in sorted(listdir(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/spinners"))):
			spinner_choices.append((fname, _(fname)))
		config.plugins.skin.OverlayHD.Spinner.setChoices(default=config.plugins.skin.OverlayHD.Spinner.default, choices=spinner_choices)
		for x in repaint_notifications:
			getattr(config.plugins.skin.OverlayHD, x).addNotifier(self.changeSettings)
		self.process = True

	def removeNotifications(self):
		self.process = False
		for x in repaint_notifications:
			getattr(config.plugins.skin.OverlayHD, x).removeNotifier(self.changeSettings)

	def changeSettings(self, configElement):
		if self.process:
			if configElement == config.plugins.skin.OverlayHD.UseGroups:
				self.updateGroups()
			else:
				self.applySettings()

	def cancel(self):
		self.removeNotifications()
		for x in config.plugins.skin.OverlayHD.dict():
			getattr(config.plugins.skin.OverlayHD, x).cancel()
		self.applySettings()
		self.close()

	def save(self):
		self.removeNotifications()
		if self.changedSettings():
			for x in config.plugins.skin.OverlayHD.dict():
				getattr(config.plugins.skin.OverlayHD, x).save()
			config.plugins.skin.OverlayHD.save()
			self.applySettings()
			popup = self.session.openWithCallback(self.restartGUI, MessageBox, _("The GUI needs to be restarted to apply the changes.\n\n"
				"Do you want to restart the GUI now?"), MessageBox.TYPE_YESNO)
			popup.setTitle(self.setup_title)
		else:
			self.close()

	def restartGUI(self, answer):
		if answer:
			self.session.open(TryQuitMainloop, retvalue=3)
		self.close()

	def theme(self):
		self.process = False
		self.session.openWithCallback(self.themeClosed, OverlayHDThemeManager)

	def themeClosed(self):
		self.applySettings()
		self.process = True

	def default(self):
		if config.skin.primary_skin.value == "OverlayHD/skin.xml":
			print "[OverlayHD] Setting skin to default settings."
			self.process = False
			config.plugins.skin.OverlayHD.ButtonStyle.value = config.plugins.skin.OverlayHD.ButtonStyle.default
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
			self.applySettings()
			self.process = True
		else:
			print "[OverlayHD] OverlayHD is not the active skin."

	def changedSettings(self):
		changed = 0
		for x in config.plugins.skin.OverlayHD.dict():
			if getattr(config.plugins.skin.OverlayHD, x).isChanged():
				# print "[OverlayHD] Entries changed."
				return True
		# print "[OverlayHD] Entries NOT changed."
		return False

	def updateGroups(self):
		if config.plugins.skin.OverlayHD.UseGroups.value:
			for x in display_groups:
				getattr(config.plugins.skin.OverlayHD, x).value = False
		else:
			for x in display_groups:
				getattr(config.plugins.skin.OverlayHD, x).value = True

	def applySettings(self):
		index = self["config"].getCurrentIndex()
		applySkinSettings()
		self.applySkin()
		self.instance.invalidate()  # Remove this when the underlying bug is fixed!
		self["config"].setCurrentIndex(index)


class OverlayHDThemeManager(Screen, HelpableScreen):
	skin = """
	<screen name="OverlayHDThemeManager" title="OverlayHD Theme Manager" position="0,0" size="1280,720" backgroundColor="ScreenBackground" flags="wfNoBorder">
		<panel name="ScreenTemplate" />
		<panel name="ScreenTemplateButtonMenu" />
		<panel name="ScreenTemplateButtonColours" />
		<panel name="ScreenTemplateButtonHelp" />
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

		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Apply"))
		self["key_yellow"] = Label(_("Save"))
		self["key_blue"] = Label(_("Create"))

		self["actions"] = HelpableActionMap(self, ["OkCancelActions", "ColorActions", "MenuActions"], {
			"ok": (self.applyTheme, _("Apply the currently highlighted theme, return to Skin Manager")),
			"cancel": (self.cancelTheme, _("Cancel theme selection, return to Skin Manager")),
			"menu": (self.themeMenu, _("Menu of actions applicable to the currently highlighted theme")),
			"red": (self.cancelTheme, _("Cancel theme selection, return to Skin Manager")),
			"green": (self.applyTheme, _("Apply the currently highlighted theme, return to Skin Manager")),
			"yellow": (self.saveTheme, _("Save current skin settings as the currently highlighted theme")),
			"blue": (self.newTheme, _("Create a new theme using the current skin settings"))
		}, description=_("Theme Functions"))

		self["themes"] = List()
		self.filename = resolveFilename(SCOPE_CONFIG, "OverlayHD_themes.xml")
		self.dom_themes = None
		try:
			chan = open(self.filename, "r")
			self.dom_themes = xml.etree.cElementTree.parse(chan)
			chan.close()
			self["themes"].updateList(self.listThemes())
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
		self.onShown.append(self.screenShown)

	def screenShown(self):
		if self.dom_themes == None:
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
		indent = "\n" + level*"\t"
		if len(element):
			if not element.text or not element.text.strip():
				element.text = indent + "\t"
			if not element.tail or not element.tail.strip():
				element.tail = indent
			for element in element:
				self.xmlIndent(element, level+1)
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


def applySkinSettings():
	if config.skin.primary_skin.value == "OverlayHD/skin.xml":
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
			if label == "BackgroundImage":
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
				for screen in button_screens:
					elements, path = dom_screens.get(screen, (None, None))
					if elements:
						element = elements.find("panel")
						name = element.get("name", None)
						if name:
							element.set("name", "%s%s" % (screen, config.plugins.skin.OverlayHD.ButtonStyle.value))
			elif label == "ClockStyle":
				for screen in clock_screens:
					elements, path = dom_screens.get(screen, (None, None))
					if elements:
						element = elements.find("panel")
						name = element.get("name", None)
						if name:
							element.set("name", "%s%s" % (screen, config.plugins.skin.OverlayHD.ClockStyle.value))
			elif label == "EPGShowTicks":
				if config.plugins.skin.OverlayHD.EPGShowTicks.value:
					setting = "yes"
				else:
					setting = "no"
				for screen in ("GraphicalEPG", "GraphicalEPGPIG", "GraphicalInfoBarEPG"):
					elements, path = dom_screens.get(screen, (None, None))
					if elements:
						widgets = elements.findall("widget")
						for widget in widgets:
							if widget.get("TimelineTicksOn", "") != "":
								widget.set("TimelineTicksOn", setting)
								break
			elif label == "EPGAlignment":
				for screen in ("GraphicalEPG", "GraphicalEPGPIG", "GraphicalInfoBarEPG"):
					elements, path = dom_screens.get(screen, (None, None))
					if elements:
						widgets = elements.findall("widget")
						for widget in widgets:
							if widget.get("EntryFontAlignment", "") != "":
								widget.set("EntryFontAlignment", config.plugins.skin.OverlayHD.EPGAlignment.value)
								break
			elif label == "RecordBlink":
				elements, path = dom_screens.get("ChannelFormatPanel", (None, None))
				if elements:
					widgets = elements.findall("widget")
					for widget in widgets:
						if widget.get("source", "") == "session.RecordState":
							converts = widget.findall("convert")
							for convert in converts:
								if convert.get("type", "") == "ConditionalShowHide":
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
				elements, path = dom_screens.get("ChannelFormatPanel", (None, None))
				if elements:
					widgets = elements.findall("widget")
					for widget in widgets:
						if widget.get("source", "") in ("global.OnlineStableUpdateState", "global.OnlineUnstableUpdateState"):
							converts = widget.findall("convert")
							for convert in converts:
								if convert.get("type", "") == "ConditionalShowHide":
									if config.plugins.skin.OverlayHD.UpdateBlink.value:
										convert.text = "Blink"
									else:
										convert.text = ""
									break
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

def start_menu_main(menuid, **kwargs):
	if menuid == "system":
		return [(_("OverlayHD Skin Manager"), main, "OverlayHD", None)]
	else:
		return []

def main(session, **kwargs):
	session.open(OverlayHDSkinManager)

def autostart(reason, **kwargs):
	if reason == 0:
		# print "[OverlayHD] OverlayHD Skin Manager loaded."
		updateOverlayHD()
		applySkinSettings()
	elif reason == 1:
		# print "[OverlayHD] OverlayHD Skin Manager unloaded."
		pass

def Plugins(**kwargs):
	list = []
	if config.plugins.skin.OverlayHD.AlwaysActive.value or config.skin.primary_skin.value == "OverlayHD/skin.xml":
		list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_AUTOSTART], fnc=autostart))
		list.append(PluginDescriptor(name=_("OverlayHD"), where=[PluginDescriptor.WHERE_PLUGINMENU],
			description="OverlayHD Skin Manager version 1.52", icon="OverlayHD.png", fnc=main))
	return list
