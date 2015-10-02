#====================================================
# OverlayHD Skin Manager
# Version Date - 22-Sep-2015
# Version Number - 1.10
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
from enigma import gRGB
from skin import dom_screens, colorNames
import xml.etree.cElementTree

colour_choices = [
	("Black", _("Black")),
	("Blue", _("Blue")),
	("Coral", _("Coral")),
	("Cyan", _("Cyan")),
	("DarkerGrey", _("Darker Grey")),
	("DarkGrey", _("Dark Grey")),
	("DeepGrey", _("Deep Grey")),
	("DeepPink", _("Deep Pink")),
	("DimGrey", _("Dim Grey")),
	("DodgerBlue", _("Dodger Blue")),
	("DullGreen", _("Dull Green")),
	("DullRed", _("Dull Red")),
	("DullYellow", _("Dull Yellow")),
	("Gainsboro", _("Gainsboro")),
	("Gold", _("Gold")),
	("Green", _("Green")),
	("Grey", _("Grey")),
	("GreyBlue", _("Grey Blue")),
	("Indigo", _("Indigo")),
	("LightBlue", _("Light Blue")),
	("LightGrey", _("Light Grey")),
	("LightRed", _("Light Red")),
	("LightSlateBlue", _("Light Slate Blue")),
	("Magenta", _("Magenta")),
	("Maroon", _("Maroon")),
	("MediumBlue", _("Medium Blue")),
	("Navy", _("Navy")),
	("Orange", _("Orange")),
	("OrangeRed", _("Orange Red")),
	("Pink", _("Pink")),
	("Purple", _("Purple")),
	("Red", _("Red")),
	("RoyalBlue", _("Royal Blue")),
	("SaddleBrown", _("Saddle Brown")),
	("Silver", _("Silver")),
	("Tan", _("Tan")),
	("Teal", _("Teal")),
	("WarmYellow", _("Warm Yellow")),
	("White", _("White")),
	("Yellow", _("Yellow"))
]

background_choice = [("0x00000001", _("Background"))]

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
config.plugins.skin.OverlayHD.ScreenBackgroundColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.ScreenBackgroundTransparency = ConfigSelection(default="0x3f000000", choices=transparency_choices)
config.plugins.skin.OverlayHD.BannerClock = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.BannerTitle = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.Pinstripe = ConfigSelection(default="DarkerGrey", choices=colour_choices)
config.plugins.skin.OverlayHD.MenuBackgroundColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.MenuBackgroundTransparency = ConfigSelection(default="0x00000001", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.MenuSelectedColour = ConfigSelection(default="DodgerBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.MenuSelectedTransparency = ConfigSelection(default="0x26000000", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.MenuText = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.MenuTextSelected = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.FootnoteBackgroundColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.FootnoteBackgroundTransparency = ConfigSelection(default="0x00000001", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.FootnoteText = ConfigSelection(default="DimGrey", choices=colour_choices)
config.plugins.skin.OverlayHD.TextBackgroundColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.TextBackgroundTransparency = ConfigSelection(default="0x00000001", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.Text = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.SMSHelperBackgroundColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.SMSHelperBackgroundTransparency = ConfigSelection(default="0x00000001", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.SMSHelperText = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.FindCharacter = ConfigSelection(default="Gold", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoBackgroundColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoBackgroundTransparency = ConfigSelection(default="0x00000001", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.InfoLCN = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoChannel = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoBroadcaster = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoBouquet = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoProgramNow = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoTimesNow = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDurationNow = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoFileSizeNow = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDetailsNow = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoRatingNow = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoProgramNext = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoTimesNext = ConfigSelection(default="LightGrey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDurationNext = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoFileSizeNext = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDetailsNext = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoRatingNext = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoRecording = ConfigSelection(default="DullRed", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoRecordingProgress = ConfigSelection(default="DeepGrey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoMediaName = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoMediaLength = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDiskStats = ConfigSelection(default="DullYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.TunerBackgroundColour = ConfigSelection(default="Black", choices=colour_choices)

config.plugins.skin.OverlayHD.EPGBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGProgram = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTimes = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGDuration = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRating = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGDetails = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTimeLineBorderColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTimeLineColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGGridBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryBackgroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryBackgroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryForegroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRecordBackgroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRecordBackgroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRecordForegroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRecordForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGServiceBackgroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGServiceBackgroundColorNow = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGServiceForegroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGServiceForegroundColorNow = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGZapBackgroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGZapBackgroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGZapForegroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGZapForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGBorder = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGProgressBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGProgressColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGProgressBorder = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGTimeLineBorderColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGTimeLineColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGGridBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGEntryBackgroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGEntryBackgroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGEntryForegroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGEntryForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGRecordBackgroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGRecordBackgroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGRecordForegroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGRecordForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGServiceBackgroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGServiceBackgroundColorNow = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGServiceForegroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGServiceForegroundColorNow = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGZapBackgroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGZapBackgroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGZapForegroundColor = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGZapForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)

config.plugins.skin.OverlayHD.TunerBackgroundTransparency = ConfigSelection(default="0x00000001", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.show_debugscreens = ConfigEnableDisable(default=False)
config.plugins.skin.OverlayHD.use_enhanced_menu = ConfigEnableDisable(default=False)
config.plugins.skin.OverlayHD.record_icon_blink = ConfigYesNo(default=True)
config.plugins.skin.OverlayHD.update_icon_blink = ConfigYesNo(default=True)


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
		self["key_yellow"] = StaticText()
		self["key_blue"] = StaticText(_("Default"))

		self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'],
		{
			"red" : self.cancel,
			"green": self.save,
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

	def default(self):
		if config.skin.primary_skin.getValue() == "OverlayHD/skin.xml":
			print "[OverlayHD] OverlayHD Skin Manager - Setting OverlayHD skin to default settings."
			self.process = False
			config.plugins.skin.OverlayHD.ScreenBackgroundColour.setValue("Black")
			config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.setValue("0x3f000000")
			config.plugins.skin.OverlayHD.BannerClock.setValue("White")
			config.plugins.skin.OverlayHD.BannerTitle.setValue("White")
			config.plugins.skin.OverlayHD.Pinstripe.setValue("DarkerGrey")
			config.plugins.skin.OverlayHD.MenuBackgroundColour.setValue("Black")
			config.plugins.skin.OverlayHD.MenuBackgroundTransparency.setValue("0x00000001")
			config.plugins.skin.OverlayHD.MenuSelectedColour.setValue("DodgerBlue")
			config.plugins.skin.OverlayHD.MenuSelectedTransparency.setValue("0x26000000")
			config.plugins.skin.OverlayHD.MenuText.setValue("White")
			config.plugins.skin.OverlayHD.MenuTextSelected.setValue("White")
			config.plugins.skin.OverlayHD.FootnoteBackgroundColour.setValue("Black")
			config.plugins.skin.OverlayHD.FootnoteBackgroundTransparency.setValue("0x00000001")
			config.plugins.skin.OverlayHD.FootnoteText.setValue("DimGrey")
			config.plugins.skin.OverlayHD.TextBackgroundColour.setValue("Black")
			config.plugins.skin.OverlayHD.TextBackgroundTransparency.setValue("0x00000001")
			config.plugins.skin.OverlayHD.Text.setValue("White")
			config.plugins.skin.OverlayHD.SMSHelperBackgroundColour.setValue("Black")
			config.plugins.skin.OverlayHD.SMSHelperBackgroundTransparency.setValue("0x00000001")
			config.plugins.skin.OverlayHD.SMSHelperText.setValue("White")
			config.plugins.skin.OverlayHD.FindCharacter.setValue("Gold")
			config.plugins.skin.OverlayHD.InfoBackgroundColour.setValue("Black")
			config.plugins.skin.OverlayHD.InfoBackgroundTransparency.setValue("0x00000001")
			config.plugins.skin.OverlayHD.InfoLCN.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoChannel.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoBroadcaster.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoBouquet.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoProgramNow.setValue("White")
			config.plugins.skin.OverlayHD.InfoTimesNow.setValue("Grey")
			config.plugins.skin.OverlayHD.InfoDurationNow.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoFileSizeNow.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoDetailsNow.setValue("White")
			config.plugins.skin.OverlayHD.InfoRatingNow.setValue("Grey")
			config.plugins.skin.OverlayHD.InfoProgramNext.setValue("White")
			config.plugins.skin.OverlayHD.InfoTimesNext.setValue("Grey")
			config.plugins.skin.OverlayHD.InfoDurationNext.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoFileSizeNext.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoDetailsNext.setValue("White")
			config.plugins.skin.OverlayHD.InfoRatingNext.setValue("Grey")
			config.plugins.skin.OverlayHD.InfoRecording.setValue("DullRed")
			config.plugins.skin.OverlayHD.InfoRecordingProgress.setValue("DeepGrey")
			config.plugins.skin.OverlayHD.InfoMediaName.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoMediaLength.setValue("LightBlue")
			config.plugins.skin.OverlayHD.InfoDiskStats.setValue("DullYellow")
			config.plugins.skin.OverlayHD.TunerBackgroundColour.setValue("Black")
			config.plugins.skin.OverlayHD.TunerBackgroundTransparency.setValue("0x00000001")
			self.process = True
			self.applySettings()
		else:
			print "[OverlayHD] OverlayHD Skin Manager - OverlayHD is not the active skin!"

	def changedSettings(self):
		changed = 0
		for x in self['config'].list:
			if x[1].isChanged():
				changed += 1
		if changed:
			# print "[OverlayHD] Entries changed!"
			return True
		else:
			# print "[OverlayHD] Entries NOT changed!"
			return False

	def applySettings(self):
		index = self["config"].getCurrentIndex()
		applySkinSettings()
		self.applySkin()
		self.instance.invalidate()  # Remove this when the underlying bug is fixed!
		self["config"].setCurrentIndex(index)

def buildColour(colour, transparency):
	if colour.getValue() != "0x00000001":
		trans = long(transparency.getValue(), 0x10)
	else:
		trans = long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.getValue(), 0x10)
	return gRGB(colorNames[colour.getValue()].argb() | trans)

def applySkinSettings():
	if config.skin.primary_skin.getValue() == "OverlayHD/skin.xml":
		print "[OverlayHD] OverlayHD Skin Manager - Applying OverlayHD skin settings."
		colorNames["ScreenBackground"] = gRGB(colorNames[config.plugins.skin.OverlayHD.ScreenBackgroundColour.getValue()].argb() |
							long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.getValue(), 0x10))
		colorNames["BannerClock"] = colorNames[config.plugins.skin.OverlayHD.BannerClock.getValue()]
		colorNames["BannerTitle"] = colorNames[config.plugins.skin.OverlayHD.BannerTitle.getValue()]
		colorNames["Pinstripe"] = colorNames[config.plugins.skin.OverlayHD.Pinstripe.getValue()]
		# colorNames["MenuBackground"] = buildColour(config.plugins.skin.OverlayHD.MenuBackgroundColour, config.plugins.skin.OverlayHD.MenuBackgroundTransparency)
		colorNames["MenuBackground"] = colorNames["ScreenBackground"]
		colorNames["MenuSelected"] = buildColour(config.plugins.skin.OverlayHD.MenuSelectedColour, config.plugins.skin.OverlayHD.MenuSelectedTransparency)
		colorNames["MenuText"] = colorNames[config.plugins.skin.OverlayHD.MenuText.getValue()]
		colorNames["MenuTextSelected"] = colorNames[config.plugins.skin.OverlayHD.MenuTextSelected.getValue()]
		# colorNames["FootnoteBackground"] = buildColour(config.plugins.skin.OverlayHD.FootnoteBackgroundColour, config.plugins.skin.OverlayHD.FootnoteBackgroundTransparency)
		colorNames["FootnoteBackground"] = colorNames["ScreenBackground"]
		colorNames["FootnoteText"] = colorNames[config.plugins.skin.OverlayHD.FootnoteText.getValue()]
		# colorNames["TextBackground"] = buildColour(config.plugins.skin.OverlayHD.TextBackgroundColour, config.plugins.skin.OverlayHD.TextBackgroundTransparency)
		colorNames["TextBackground"] = colorNames["ScreenBackground"]
		colorNames["Text"] = colorNames[config.plugins.skin.OverlayHD.Text.getValue()]
		# colorNames["SMSHelperBackground"] = buildColour(config.plugins.skin.OverlayHD.SMSHelperBackgroundColour, config.plugins.skin.OverlayHD.SMSHelperBackgroundTransparency)
		colorNames["SMSHelperBackground"] = colorNames["ScreenBackground"]
		colorNames["SMSHelperText"] = colorNames[config.plugins.skin.OverlayHD.SMSHelperText.getValue()]
		colorNames["FindCharacter"] = colorNames[config.plugins.skin.OverlayHD.FindCharacter.getValue()]
		# colorNames["InfoBackground"] = buildColour(config.plugins.skin.OverlayHD.InfoBackgroundColour, config.plugins.skin.OverlayHD.InfoBackgroundTransparency)
		colorNames["InfoBackground"] = colorNames["ScreenBackground"]
		colorNames["InfoLCN"] = colorNames[config.plugins.skin.OverlayHD.InfoLCN.getValue()]
		colorNames["InfoChannel"] = colorNames[config.plugins.skin.OverlayHD.InfoChannel.getValue()]
		colorNames["InfoBroadcaster"] = colorNames[config.plugins.skin.OverlayHD.InfoBroadcaster.getValue()]
		colorNames["InfoBouquet"] = colorNames[config.plugins.skin.OverlayHD.InfoBouquet.getValue()]
		colorNames["InfoProgramNow"] = colorNames[config.plugins.skin.OverlayHD.InfoProgramNow.getValue()]
		colorNames["InfoTimesNow"] = colorNames[config.plugins.skin.OverlayHD.InfoTimesNow.getValue()]
		colorNames["InfoDurationNow"] = colorNames[config.plugins.skin.OverlayHD.InfoDurationNow.getValue()]
		colorNames["InfoFileSizeNow"] = colorNames[config.plugins.skin.OverlayHD.InfoFileSizeNow.getValue()]
		colorNames["InfoDetailsNow"] = colorNames[config.plugins.skin.OverlayHD.InfoDetailsNow.getValue()]
		colorNames["InfoRatingNow"] = colorNames[config.plugins.skin.OverlayHD.InfoRatingNow.getValue()]
		colorNames["InfoProgramNext"] = colorNames[config.plugins.skin.OverlayHD.InfoProgramNext.getValue()]
		colorNames["InfoTimesNext"] = colorNames[config.plugins.skin.OverlayHD.InfoTimesNext.getValue()]
		colorNames["InfoDurationNext"] = colorNames[config.plugins.skin.OverlayHD.InfoDurationNext.getValue()]
		colorNames["InfoFileSizeNext"] = colorNames[config.plugins.skin.OverlayHD.InfoFileSizeNext.getValue()]
		colorNames["InfoDetailsNext"] = colorNames[config.plugins.skin.OverlayHD.InfoDetailsNext.getValue()]
		colorNames["InfoRatingNext"] = colorNames[config.plugins.skin.OverlayHD.InfoRatingNext.getValue()]
		colorNames["InfoRecording"] = colorNames[config.plugins.skin.OverlayHD.InfoRecording.getValue()]
		colorNames["InfoRecordingProgress"] = colorNames[config.plugins.skin.OverlayHD.InfoRecordingProgress.getValue()]
		colorNames["InfoMediaName"] = colorNames[config.plugins.skin.OverlayHD.InfoMediaName.getValue()]
		colorNames["InfoMediaLength"] = colorNames[config.plugins.skin.OverlayHD.InfoMediaLength.getValue()]
		colorNames["InfoDiskStats"] = colorNames[config.plugins.skin.OverlayHD.InfoDiskStats.getValue()]
		# colorNames["TunerBackground"] = buildColour(config.plugins.skin.OverlayHD.TunerBackgroundColour, config.plugins.skin.OverlayHD.TunerBackgroundTransparency)
		colorNames["TunerBackground"] = colorNames["ScreenBackground"]
	else:
		print "[OverlayHD] OverlayHD Skin Manager - OverlayHD is not the active skin!"


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
	if config.plugins.skin.OverlayHD.always_active.getValue() or config.skin.primary_skin.getValue() == "OverlayHD/skin.xml":
		list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_AUTOSTART], fnc=autostart))
		list.append(PluginDescriptor(name=_("OverlayHD"), where=[PluginDescriptor.WHERE_PLUGINMENU],
			description="OverlayHD Skin Manager version 1.10", icon="OverlayHD.png", fnc=main))
	return list
