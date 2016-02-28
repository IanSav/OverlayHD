#====================================================
# OverlayHD Skin Manager
# Version Date - 27-Feb-2016
# Version Number - 1.32
# Coding by IanSav
#====================================================
# Remember to change the version number below!!!
#====================================================

from Components.ActionMap import HelpableActionMap
from Components.Button import Button
from Components.Sources.List import List
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigEnableDisable, ConfigSelection
from Plugins.Plugin import PluginDescriptor
from Screens.HelpMenu import HelpableScreen
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Setup import Setup
from Screens.Standby import TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_CURRENT_PLUGIN
from enigma import eEnv, gRGB
from os import listdir, symlink, unlink
from os.path import islink
from skin import dom_screens, colorNames, reloadWindowstyles, fonts
import errno, shutil
import xml.etree.cElementTree

colour_elements = (
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
	("EPGEntryBackgroundColor", "DarkerBlue", None),
	("EPGEntryBackgroundColorSelected", "Yellow", None),
	("EPGEntryForegroundColor", "White", None),
	("EPGEntryForegroundColorSelected", "Black", None),
	("EPGRecordBackgroundColor", "DullRed", None),
	("EPGRecordBackgroundColorSelected", "Red", None),
	("EPGRecordForegroundColor", "White", None),
	("EPGRecordForegroundColorSelected", "Black", None),
	("EPGServiceBackgroundColor", "DeepBlue", None),
	("EPGServiceBackgroundColorNow", "Blue", None),
	("EPGServiceForegroundColor", "White", None),
	("EPGServiceForegroundColorNow", "White", None),
	("EPGZapBackgroundColor", "DullGreen", None),
	("EPGZapBackgroundColorSelected", "Green", None),
	("EPGZapForegroundColor", "White", None),
	("EPGZapForegroundColorSelected", "Black", None),
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
)

derived_background_elements = (
	"EPGEntryBackgroundColor",
	"EPGEntryBackgroundColorSelected",
	"EPGRecordBackgroundColor",
	"EPGRecordBackgroundColorSelected",
	"EPGServiceBackgroundColor",
	"EPGServiceBackgroundColorNow",
	"EPGZapBackgroundColor",
	"EPGZapBackgroundColorSelected"
)

derived_foreground_elements = (
	"EPGEntryForegroundColor",
	"EPGEntryForegroundColorSelected",
	"EPGRecordForegroundColor",
	"EPGRecordForegroundColorSelected",
	"EPGServiceForegroundColor",
	"EPGServiceForegroundColorNow",
	"EPGZapForegroundColor",
	"EPGZapForegroundColorSelected"
)

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
	("MidnightBlue", _("Midnight Blue")),
	("Mustard", _("Mustard")),
	("Navy", _("Navy")),
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

font_elements = (
	("ClockFont", "RobotoBlack", banner_font_choices),
	("TitleFont", "RobotoBlack", banner_font_choices),
	("ButtonFont", "NemesisFlatline", text_font_choices),
	("DescriptionFont", "NemesisFlatline", text_font_choices),
	("FixedFont", "MPluss1M", fixed_font_choices),
	("HelpFont", "NemesisFlatline", text_font_choices),
	("MenuFont", "NemesisFlatline", text_font_choices),
	("SMSHelperFont", "MPluss1M", fixed_font_choices),
	("Regular", "NemesisFlatline", text_font_choices),
	("TextFont", "NemesisFlatline", text_font_choices)
)

background_image_choices = [
	(None, "Default")
]

button_choices = [
	("Bar", "Bar"),
	("Block", "Block"),
	("Button", "Button"),
	("Legacy", "Legacy"),
	("Wizard", "Wizard")
]

spinner_choices = [
	(None, "Default")
]

option_elements = (
	("AlwaysActive", False, ConfigYesNo, None),
	("BackgroundImage", "Default.mvi", ConfigSelection, background_image_choices),
	("ButtonStyle", "Block", ConfigSelection, button_choices),
	("EnhancedMenu", False, ConfigEnableDisable, None),
	("RecordBlink", True, ConfigYesNo, None),
	("Spinner", "Balls", ConfigSelection, spinner_choices),
	("UpdateBlink", True, ConfigYesNo, None)
)

button_screens = (
	"ScreenTemplateButtonRed",
	"ScreenTemplateButtonGreen",
	"ScreenTemplateButtonYellow",
	"ScreenTemplateButtonBlue",
	"ScreenTemplateButtonColourBacks"
)

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
		setattr(config.plugins.skin.OverlayHD, "%s%s" % (label, "Colour"), ConfigSelection(default=colour, choices=c_choices))
		setattr(config.plugins.skin.OverlayHD, "%s%s" % (label, "Transparency"), ConfigSelection(default=transparency, choices=t_choices))
		# print "[OverlayHD] DEBUG (definition): Colour '%sColour' = '%s'" % (label, colour)
		# print "[OverlayHD] DEBUG (definition): Colour '%sTransparency' = '%s'" % (label, transparency)

for (label, font, font_table) in font_elements:
	setattr(config.plugins.skin.OverlayHD, label, ConfigSelection(default=font, choices=font_table))
	# print "[OverlayHD] DEBUG (definition): Font '%s' = '%s' (%s)" % (label, font, font_table)

for fname in sorted(listdir(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/backgrounds"))):
	background_image_choices.append((fname, fname[0:-4]))
for fname in sorted(listdir(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/spinners"))):
	spinner_choices.append((fname, fname))

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
		self.process = False

		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("OK"))
		self["key_yellow"] = Button(_("Themes"))  # "Save Theme" - Only enable if changed.
		self["key_blue"] = Button(_("Default"))

		self["actions"] = HelpableActionMap(self, ["OkCancelActions", "ColorActions"], {
			"ok": (self.save, _("Save and apply any changes")),
			"cancel": (self.cancel, _("Cancel and discard any changes")),
			"red" : (self.cancel, _("Cancel and discard any changes")),
			"green": (self.save, _("Save and apply any changes")),
			"yellow": (self.theme, _("Manage themes")),
			"blue": (self.default, _("Apply and save the default skin"))
		}, description=_("Basic Functions"))

		self.onExecBegin.append(self.myExecBegin)
		self.onExecEnd.append(self.myExecEnd)

	def changeSettings(self, configElement):
		if self.process:
			# for (label, colour, transparency) in colour_elements:
			# 	if colour is None or transparency is None:
			# 		if configElement == eval("config.plugins.skin.OverlayHD.%s" % label):
			# 			print "[OverlayHD] DEBUG (changeSettings): '%s' = '%s'" % (label, configElement.value)
			# 	else:
			# 		if colour is not None and configElement == eval("config.plugins.skin.OverlayHD.%sColour" % label):
			# 			print "[OverlayHD] DEBUG (changeSettings): '%sColour' = '%s'" % (label, configElement.value)
			# 		if transparency is not None and configElement == eval("config.plugins.skin.OverlayHD.%sTransparency" % label):
			# 			print "[OverlayHD] DEBUG (changeSettings): '%sTransparency' = '%s'" % (label, configElement.value)
			self.applySettings()

	def myExecBegin(self):
		for x in self["config"].list:
			x[1].addNotifier(self.changeSettings)
		self.process = True

	def myExecEnd(self):
		self.process = False
		for x in self["config"].list:
			x[1].removeNotifier(self.changeSettings)

	def cancel(self):
		self.process = False
		for x in self["config"].list:
		    x[1].cancel()
		self.applySettings()
		self.close()
		
	def save(self):
		self.process = False
		if self.changedSettings():
			for x in self["config"].list:
				x[1].save()
			config.plugins.skin.OverlayHD.save()
			self.applySettings()
			restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _("The GUI needs to be restarted to apply the changes.\n\n"
				"Do you want to restart the GUI now?"), MessageBox.TYPE_YESNO)
			restartbox.setTitle(self.setup_title)
		else:
			self.close()

	def restartGUI(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, retvalue=3)
		self.close()

	def theme(self):
		self.session.open(OverlayHDThemeManager)

	def default(self):
		if config.skin.primary_skin.value == "OverlayHD/skin.xml":
			print "[OverlayHD] Setting skin to default settings."
			self.process = False
			config.plugins.skin.OverlayHD.ButtonStyle.value = config.plugins.skin.OverlayHD.ButtonStyle.default
			for (label, colour, transparency) in colour_elements:
				if colour is None or transparency is None:
					item = eval("config.plugins.skin.OverlayHD.%s" % label)
					item.value = item.default
					# print "[OverlayHD] DEBUG (default): '%s' = '%s'" % (label, item.default)
				else:
					item = eval("config.plugins.skin.OverlayHD.%sColour" % label)
					item.value = item.default
					# print "[OverlayHD] DEBUG (default): '%sColour' = '%s'" % (label, item.default)
					item = eval("config.plugins.skin.OverlayHD.%sTransparency" % label)
					item.value = item.default
					# print "[OverlayHD] DEBUG (default): '%sTransparency' = '%s'" % (label, item.default)
			for (label, font, font_table) in font_elements:
				item = eval("config.plugins.skin.OverlayHD.%s" % label)
				item.value = item.default
				# print "[OverlayHD] DEBUG (default): '%s' = '%s'" % (label, item.default)
			for (label, default, config_type, option_table) in option_elements:
				item = eval("config.plugins.skin.OverlayHD.%s" % label)
				item.value = item.default
				# print "[OverlayHD] DEBUG (default): '%s' = '%s'" % (label, item.default)
			self.applySettings()
			self.process = True
		else:
			print "[OverlayHD] OverlayHD is not the active skin!"

	def changedSettings(self):
		changed = 0
		for x in self["config"].list:
			if x[1].isChanged():
				# print "[OverlayHD] Entries changed."
				return True
		# print "[OverlayHD] Entries NOT changed."
		return False

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
		<panel name="ScreenTemplateButtonColours" />
		<panel name="ScreenTemplateButtonText" />
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

		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Apply"))
		self["key_yellow"] = Button(_("Delete"))
		self["key_blue"] = Button(_("Save"))

		self["actions"] = HelpableActionMap(self, ["OkCancelActions", "ColorActions", "VirtualKeyboardActions"], {
			"ok": (self.applyTheme, _("Apply theme, return to Skin Manager")),
			"cancel": (self.cancelTheme, _("Cancel theme selection, return to Skin Manager")),
			"red": (self.cancelTheme, _("Cancel theme selection, return to Skin Manager")),
			"green": (self.applyTheme, _("Apply theme, return to Skin Manager")),
			"yellow": (self.deleteTheme, _("Delete theme")),
			"yellowlong": (self.exportTheme, _("Export theme")),
			"blue": (self.saveTheme, _("Save current skin settings as a theme")),
			"bluelong": (self.importTheme, _("Import theme")),
			"showVirtualKeyboard": (self.renameTheme, _("Rename theme"))
		}, description=_("Theme Functions"))

		self["themes"] = List()
		self.filename = resolveFilename(SCOPE_CURRENT_PLUGIN, "Extensions/OverlayHD/themes.xml")
		try:
			chan = open(self.filename, "r")
			self.dom_themes = xml.etree.cElementTree.parse(chan)
			chan.close()
			self["themes"].updateList(self.buildMenu())
		except (IOError, OSError), (err, errmsg):
			if err == errno.ENOENT:
				self.dom_themes = xml.etree.cElementTree.ElementTree(self.createTheme("Default"))
				self.saveThemes()
				print "[OverlayHD] Created 'Default' theme."
			else:
				self.dom_themes = None
				errtext = "Error %d: %s - '%s'" % (err, errmsg, self.filename)
				print "[OverlayHD] Error opening themes file! (%s)" % errtext
				# themebox = self.session.open(MessageBox, _("Unable to open/access themes!\n\n%s") % errtext, MessageBox.TYPE_ERROR, 10)
				# themebox.setTitle(self.setup_title)

	def findTheme(self, name):
		if self.dom_themes:
			themes = self.dom_themes.findall("theme")
			for theme in themes:
				n = theme.get("name", None)
				if n == name:
					return theme
		return None

	def createTheme(self, name):
		if name == "Default":
			root = xml.etree.cElementTree.Element("themes")
			mode = "default"
		else:
			root = self.dom_themes.getroot()
			mode = "value"
		root.text = "\n\t"
		root.tail = "\n"
		theme = xml.etree.cElementTree.SubElement(root, "theme", {"name": name})
		theme.text = "\n\t\t"
		theme.tail = "\n"
		for (label, colour, transparency) in colour_elements:
			if colour is None or transparency is None:
				item = eval("config.plugins.skin.OverlayHD.%s.%s" % (label, mode))
				element = xml.etree.cElementTree.SubElement(theme, "colour", {"name": label, "value": item})
				element.tail = "\n\t\t"
				# print "[OverlayHD] DEBUG: '%s' = '%s'" % (label, item)
			else:
				item = eval("config.plugins.skin.OverlayHD.%sColour.%s" % (label, mode))
				element = xml.etree.cElementTree.SubElement(theme, "colour", {"name": "%sColour" % label, "value": item})
				element.tail = "\n\t\t"
				# print "[OverlayHD] DEBUG: '%sColour' = '%s " % (label, item)
				item = eval("config.plugins.skin.OverlayHD.%sTransparency.%s" % (label, mode))
				element = xml.etree.cElementTree.SubElement(theme, "colour", {"name": "%sTransparency" % label, "value": item})
				element.tail = "\n\t\t"
				# print "[OverlayHD] DEBUG: '%sTransparency' = '%s'" % (label, item)
		for (label, font, font_table) in font_elements:
			item = eval("config.plugins.skin.OverlayHD.%s.%s" % (label, mode))
			element = xml.etree.cElementTree.SubElement(theme, "font", {"name": label, "value": item})
			element.tail = "\n\t\t"
			# print "[OverlayHD] DEBUG: '%s' = '%s'" % (label, item)
		for (label, default, config_type, option_table) in option_elements:
			item = str(eval("config.plugins.skin.OverlayHD.%s.%s" % (label, mode)))
			if option_table is None:
				element = xml.etree.cElementTree.SubElement(theme, "option", {"name": label, "type": "boolean", "value": item})
			else:
				element = xml.etree.cElementTree.SubElement(theme, "option", {"name": label, "value": item})
			element.tail = "\n\t\t"
			# print "[OverlayHD] DEBUG: '%s' = '%s'" % (label, item)
		element.tail = "\n\t"
		return root

	def saveThemes(self):
		self["themes"].updateList(self.buildMenu())
		self.dom_themes.write(self.filename)

	def buildMenu(self):
		menu = []
		if self.dom_themes:
			themes = self.dom_themes.findall("theme")
			# print "[OverlayHD] Theme count = %d" % len(themes)
			for theme in themes:
				name = theme.get("name", None)
				menu.append((name, name))
				# print "[OverlayHD] Theme = '%s'" % name
		return menu

	def cancelTheme(self):
		self.close()

	def applyTheme(self):
		name = self["themes"].getCurrent()[0]
		theme = self.findTheme(name)
		if theme:
			print "[OverlayHD] Loading theme '%s'" % name
			colours = theme.findall("colour")
			for colour in colours:
				name = colour.get("name", None)
				value = colour.get("value", None)
				if name and value:
					try:
						eval("config.plugins.skin.OverlayHD.%s" % name).value = value
						# print "[OverlayHD] Theme colour = '%s', value = '%s'" % (name, value)
					except:
						print "[OverlayHD] Theme colour = '%s', value = '%s' is invalid!" % (name, value)
			fonts = theme.findall("font")
			for font in fonts:
				name = font.get("name", None)
				value = font.get("value", None)
				if name and value:
					try:
						eval("config.plugins.skin.OverlayHD.%s" % name).value = value
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
						eval("config.plugins.skin.OverlayHD.%s" % name).vale = value
						# print "[OverlayHD] Theme option = '%s', value = '%s'" % (name, value)
					except:
						print "[OverlayHD] Theme option = '%s', value = '%s' is invalid!" % (name, value)
			applySkinSettings()
			self.applySkin()
			self.instance.invalidate()  # Remove this when the underlying bug is fixed!
		self.close()

	def deleteTheme(self):
		name = self["themes"].getCurrent()[0]
		popup = self.session.openWithCallback(self.deleteThemeAction, MessageBox, _("Do you really want to delete the '%s' theme?") % name, MessageBox.TYPE_YESNO)
		popup.setTitle(self.setup_title)

	def deleteThemeAction(self, answer):
		if answer is True:
			name = self["themes"].getCurrent()[0]
			theme = self.findTheme(name)
			if theme:
				print "[OverlayHD] Deleting theme '%s'" % name
				self.dom_themes.getroot().remove(theme)
			self.saveThemes()

	def saveTheme(self):
		popup = self.session.openWithCallback(self.saveThemeAction, VirtualKeyBoard, title=_("Enter a name for this theme:"), text="")
		popup.setTitle(self.setup_title)

	def saveThemeAction(self, name):
		if name:
			if self.findTheme(name):
				themebox = self.session.open(MessageBox, _("Theme name already exists!"), MessageBox.TYPE_ERROR, 5)
				themebox.setTitle(self.setup_title)
			else:
				print "[OverlayHD] Saving theme as '%s'." % name
				self.createTheme(name)
				self.saveThemes()
		else:
			themebox = self.session.open(MessageBox, _("Theme name can not be blank!"), MessageBox.TYPE_ERROR, 5)
			themebox.setTitle(self.setup_title)

	def renameTheme(self):
		name = self["themes"].getCurrent()[0]
		popup = self.session.openWithCallback(self.renameThemeAction, VirtualKeyBoard, title=_("Enter the new name for this theme:"), text=name)
		popup.setTitle(self.setup_title)

	def renameThemeAction(self, name):
		oldname = self["themes"].getCurrent()[0]
		print "[OverlayHD] Rename theme '%s' to '%s'." % (oldname, name)
		self.saveThemes()

	def exportTheme(self):
		print "[OverlayHD] Export theme."
		themebox = self.session.open(MessageBox, _("Theme export not yet available!"), MessageBox.TYPE_ERROR, 5)
		themebox.setTitle(self.setup_title)
		# self.saveThemes()

	def importTheme(self):
		print "[OverlayHD] Import theme."
		themebox = self.session.open(MessageBox, _("Theme import not yet available!"), MessageBox.TYPE_ERROR, 5)
		themebox.setTitle(self.setup_title)
		# self.saveThemes()

def applySkinSettings():
	if config.skin.primary_skin.value == "OverlayHD/skin.xml":
		print "[OverlayHD] Applying OverlayHD skin settings."
		for (label, colour, transparency) in colour_elements:
			if transparency is None:
				item = eval("config.plugins.skin.OverlayHD.%s" % label).value
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
				col = eval("config.plugins.skin.OverlayHD.%sColour" % label).value
				if col == "Background":
					col = config.plugins.skin.OverlayHD.ScreenBackgroundColour.value
				tran = eval("config.plugins.skin.OverlayHD.%sTransparency" % label).value
				if tran == "Background":
					tran = long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value, 0x10)
				else:
					tran = long(tran, 0x10)
				colorNames[label] = gRGB(colorNames[col].argb() | tran)
		for (label, font, font_table) in font_elements:
			data = list(fonts[label])
			data[0] = eval("config.plugins.skin.OverlayHD.%s" % label).value
			fonts[label] = tuple(data)
		for (label, default, config_type, options_table) in option_elements:
			if label == "BackgroundImage":
				dst = eEnv.resolve("${datadir}/backdrop.mvi")
				try:
					unlink(dst)
				except:
					pass
				src = eval("config.plugins.skin.OverlayHD.%s" % label).value
				try:
					if src is None:
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
			elif label == "Spinner":
				linkname = resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/spinner")
				if islink(linkname):
					unlink(linkname)
				item = eval("config.plugins.skin.OverlayHD.%s" % label).value
				if item is not None:
					try:
						symlink(resolveFilename(SCOPE_CURRENT_SKIN, "OverlayHD/spinners/%s" % item), linkname)
					except (IOError, OSError), (err, errmsg):
						errtext = "Error %d: %s - '%s'" % (err, errmsg, linkname)
						print "[OverlayHD] Error linking spinner directory! (%s)" % errtext
		reloadWindowstyles()
	else:
		print "[OverlayHD] OverlayHD is not the active skin!"


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
		applySkinSettings()
	elif reason == 1:
		# print "[OverlayHD] OverlayHD Skin Manager unloaded."
		pass

def Plugins(**kwargs):
	list = []
	if config.plugins.skin.OverlayHD.AlwaysActive.value or config.skin.primary_skin.value == "OverlayHD/skin.xml":
		list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_AUTOSTART], fnc=autostart))
		list.append(PluginDescriptor(name=_("OverlayHD"), where=[PluginDescriptor.WHERE_PLUGINMENU],
			description="OverlayHD Skin Manager version 1.32", icon="OverlayHD.png", fnc=main))
	return list
