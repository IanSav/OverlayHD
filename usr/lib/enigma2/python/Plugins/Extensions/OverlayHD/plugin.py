#====================================================
# OverlayHD Skin Manager
# Version Date - 8-Jan-2016
# Version Number - 1.23
# Coding by IanSav
#====================================================
# Remember to change the version number below!!!
#====================================================

from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigEnableDisable, ConfigSelection
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Setup import Setup
from Screens.Standby import TryQuitMainloop
from Tools.Directories import resolveFilename, SCOPE_CURRENT_PLUGIN
from enigma import gRGB
from skin import dom_screens, colorNames, reloadWindowstyles
import xml.etree.cElementTree

screen_elements = (
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
	("DarkerGrey", _("Darker Grey")),
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

config.plugins.skin = ConfigSubsection()
config.plugins.skin.OverlayHD = ConfigSubsection()
config.plugins.skin.OverlayHD.always_active = ConfigYesNo(default=False)
config.plugins.skin.OverlayHD.record_icon_blink = ConfigYesNo(default=True)
config.plugins.skin.OverlayHD.show_debugscreens = ConfigEnableDisable(default=False)
config.plugins.skin.OverlayHD.update_icon_blink = ConfigYesNo(default=True)
config.plugins.skin.OverlayHD.use_enhanced_menu = ConfigEnableDisable(default=False)

for (label, colour, transparency) in screen_elements:
	if colour is None or transparency is None:
		if colour is not None:
			setattr(config.plugins.skin.OverlayHD, label, ConfigSelection(default=colour, choices=colour_choices))
			# print "[OverlayHD] DEBUG (definition): '%s' = '%s'" % (label, colour)
		if transparency is not None:
			setattr(config.plugins.skin.OverlayHD, label, ConfigSelection(default=transparency, choices=transparency_choices))
			# print "[OverlayHD] DEBUG (definition): '%s' = '%s'" % (label, transparency)
	else:
		if label == "ScreenBackground":
			c_choices = colour_choices
			t_choices = transparency_choices
		else:
			c_choices = background_choice + colour_choices
			t_choices = background_choice + transparency_choices
		setattr(config.plugins.skin.OverlayHD, "%s%s" % (label, "Colour"), ConfigSelection(default=colour, choices=c_choices))
		setattr(config.plugins.skin.OverlayHD, "%s%s" % (label, "Transparency"), ConfigSelection(default=transparency, choices=t_choices))
		# print "[OverlayHD] DEBUG (definition): '%sColour' = '%s'" % (label, colour)
		# print "[OverlayHD] DEBUG (definition): '%sTransparency' = '%s'" % (label, transparency)


class OverlayHDSkinManager(Setup):
	ALLOW_SUSPEND = True

	skin = """
	<screen name="OverlayHDSkinManager" title="OverlayHD Skin Manager" position="0,0" size="1280,720" backgroundColor="ScreenBackground" flags="wfNoBorder">
		<panel name="ScreenTemplate" />
		<panel name="ScreenTemplateButtonColours" />
		<panel name="ScreenTemplateButtonTextVKey" />
		<ePixmap pixmap="menus/setup_default.png" position="50,100" size="300,500" alphatest="on" transparent="1" />
		<widget name="menuimage" position="50,100" size="300,500" alphatest="on" transparent="1" zPosition="+1" />
		<panel name="ScreenTemplateConfig4" />
		<panel name="ScreenTemplateFootnote4" />
		<panel name="ScreenTemplateDescription4" />
	</screen>"""

	def __init__(self, session, args = None):
		Setup.__init__(self, session=session, setup="OverlayHDSkinManager", plugin="Extensions/OverlayHD")
 		self.skin = OverlayHDSkinManager.skin
		self.setup_title = _("OverlayHD Skin Manager")
		self.process = False

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		self["key_yellow"] = StaticText(_("Themes"))
		self["key_blue"] = StaticText(_("Default"))

		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'],
		{
			"red" : self.cancel,
			"green": self.save,
			"yellow": self.theme,
			"blue": self.default,
			"cancel": self.cancel
		}, -1)

		self.onExecBegin.append(self.myExecBegin)
		self.onExecEnd.append(self.myExecEnd)

	def changeSettings(self, configElement):
		if self.process:
			self.applySettings()

	def myExecBegin(self):
		for x in self['config'].list:
			x[1].addNotifier(self.changeSettings)
		self.process = True

	def myExecEnd(self):
		self.process = False
		for x in self['config'].list:
			x[1].removeNotifier(self.changeSettings)

	def cancel(self):
		self.process = False
		for x in self['config'].list:
		    x[1].cancel()
		self.applySettings()
		self.close()
		
	def save(self):
		self.process = False
		if self.changedSettings():
			for x in self['config'].list:
				x[1].save()
			config.plugins.skin.OverlayHD.save()
			self.applySettings()
			restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _("GUI needs a restart to apply any new settings.\n\n"
				"Do you want to restart the GUI now?"), MessageBox.TYPE_YESNO)
			restartbox.setTitle(self.setup_title)
		else:
			self.close()

	def restartGUI(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, retvalue=3)
		self.close()

	def theme(self):
		themebox = self.session.open(MessageBox, _("Themes are not yet available."), MessageBox.TYPE_INFO, 5)
		themebox.setTitle(self.setup_title)
		try:
			file = open(resolveFilename(SCOPE_CURRENT_PLUGIN, "OverlayHD/themes.xml"), "r")
			themes = xml.etree.cElementTree.parse(file)
			file.close()
		except:
			pass
		# Not yet implemented!

	def default(self):
		if config.skin.primary_skin.value == "OverlayHD/skin.xml":
			print "[OverlayHD] Setting skin to default settings."
			self.process = False
			for (label, colour, transparency) in screen_elements:
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
			self.applySettings()
			self.process = True
		else:
			print "[OverlayHD] OverlayHD is not the active skin!"

	def changedSettings(self):
		changed = 0
		for x in self['config'].list:
			if x[1].isChanged():
				# print "[OverlayHD] Entries changed!"
				return True
		# print "[OverlayHD] Entries NOT changed!"
		return False

	def applySettings(self):
		index = self["config"].getCurrentIndex()
		applySkinSettings()
		self.applySkin()
		self.instance.invalidate()  # Remove this when the underlying bug is fixed!
		self["config"].setCurrentIndex(index)

def applySkinSettings():
	if config.skin.primary_skin.value == "OverlayHD/skin.xml":
		print "[OverlayHD] Applying OverlayHD skin settings."
		for (label, colour, transparency) in screen_elements:
			if transparency is None:
				item = eval("config.plugins.skin.OverlayHD.%s" % label)
				piglabel = "%s%s%s" % (label[0:3], "PIG", label[3:])
				if label in derived_foreground_elements:
					colorNames[label] = colorNames[item.value]
					colorNames[piglabel] = colorNames[item.value]
					# print "[OverlayHD] DEBUG (apply) 1: '%s' = '%s'" % (label, item.value)
					# print "[OverlayHD] DEBUG (apply) 2: '%s' = '%s'" % (piglabel, item.value)
				elif label in derived_background_elements:
					if config.plugins.skin.OverlayHD.EPGTransparency.value == "Background":
						tran = long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value, 0x10)
					else:
						tran = long(config.plugins.skin.OverlayHD.EPGTransparency.value, 0x10)
					colorNames[label] = gRGB(colorNames[item.value].argb() | tran)
					colorNames[piglabel] = colorNames[item.value]
					# print "[OverlayHD] DEBUG (apply) 3: '%s' = '%s + 0x%08X'" % (label, item.value, transparency)
					# print "[OverlayHD] DEBUG (apply) 4: '%s' = '%s'" % (piglabel, item.value)
				else:
					colorNames[label] = colorNames[item.value]
					# print "[OverlayHD] DEBUG (apply) 5: '%s' = '%s'" % (label, item.value)
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
				# print "[OverlayHD] DEBUG (apply) 6: '%s' = '%s + 0x%08X'" % (label, col, tran)
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
	if config.plugins.skin.OverlayHD.always_active.value or config.skin.primary_skin.value == "OverlayHD/skin.xml":
		list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_AUTOSTART], fnc=autostart))
		list.append(PluginDescriptor(name=_("OverlayHD"), where=[PluginDescriptor.WHERE_PLUGINMENU],
			description="OverlayHD Skin Manager version 1.23", icon="OverlayHD.png", fnc=main))
	return list
