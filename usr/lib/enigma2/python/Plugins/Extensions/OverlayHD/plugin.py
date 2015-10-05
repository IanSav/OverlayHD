#====================================================
# OverlayHD Skin Manager
# Version Date - 2-Oct-2015
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
	("DarkerBlue", _("Darker Blue")),
	("DarkerGrey", _("Darker Grey")),
	("DarkGrey", _("Dark Grey")),
	("DeepBlue", _("Deep Blue")),
	("DeepGrey", _("Deep Grey")),
	("DeepPink", _("Deep Pink")),
	("DimGrey", _("Dim Grey")),
	("DodgerBlue", _("Dodger Blue")),
	("DullBlue", _("Dull Blue")),
	("DullGreen", _("Dull Green")),
	("DullRed", _("Dull Red")),
	("DullYellow", _("Dull Yellow")),
	("EgyptianBlue", _("Egyptian Blue")),
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
	("MidnightBlue", _("Midnight Blue")),
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
config.plugins.skin.OverlayHD.VolumeBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.VolumeColour = ConfigSelection(default="Blue", choices=colour_choices)
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

config.plugins.skin.OverlayHD.GraphicalEPGTransparency = ConfigSelection(default="0x00000001", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.InfobarEPGTransparency = ConfigSelection(default="0x00000001", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.EPGBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGProgram = ConfigSelection(default="Gold", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTimes = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGDuration = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRating = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGDetails = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTimeLineBorderColour = ConfigSelection(default="ScreenBackground", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTimeLineColour = ConfigSelection(default="DullYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGGridBackground = ConfigSelection(default="Orange", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryBackgroundColor = ConfigSelection(default="DarkerBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryBackgroundColorSelected = ConfigSelection(default="Yellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryForegroundColor = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryForegroundColorNowSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRecordBackgroundColor = ConfigSelection(default="DullRed", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRecordBackgroundColorSelected = ConfigSelection(default="Red", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRecordForegroundColor = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRecordForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGServiceBackgroundColor = ConfigSelection(default="DeepBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGServiceBackgroundColorNow = ConfigSelection(default="Blue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGServiceForegroundColor = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGServiceForegroundColorNow = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGZapBackgroundColor = ConfigSelection(default="DullGreen", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGZapBackgroundColorSelected = ConfigSelection(default="Green", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGZapForegroundColor = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGZapForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGBorder = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGColour = ConfigSelection(default="WarmYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGProgressBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGProgressColour = ConfigSelection(default="WarmYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGProgressBorder = ConfigSelection(default="WarmYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGTimeLineBorderColour = ConfigSelection(default="ScreenBackground", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGTimeLineColour = ConfigSelection(default="DullYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGGridBackground = ConfigSelection(default="Orange", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGEntryBackgroundColor = ConfigSelection(default="DarkerBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGEntryBackgroundColorSelected = ConfigSelection(default="Yellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGEntryForegroundColor = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGEntryForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGRecordBackgroundColor = ConfigSelection(default="DullRed", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGRecordBackgroundColorSelected = ConfigSelection(default="Red", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGRecordForegroundColor = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGRecordForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGServiceBackgroundColor = ConfigSelection(default="DeepBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGServiceBackgroundColorNow = ConfigSelection(default="Blue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGServiceForegroundColor = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGServiceForegroundColorNow = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGZapBackgroundColor = ConfigSelection(default="DullGreen", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGZapBackgroundColorSelected = ConfigSelection(default="Green", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGPIGZapForegroundColor = ConfigSelection(default="White", choices=colour_choices)
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
		if config.skin.primary_skin.value == "OverlayHD/skin.xml":
			print "[OverlayHD] Setting skin to default settings."
			self.process = False
			config.plugins.skin.OverlayHD.ScreenBackgroundColour.value = "Black"
			config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value = "0x3f000000"
			config.plugins.skin.OverlayHD.BannerClock.value = "White"
			config.plugins.skin.OverlayHD.BannerTitle.value = "White"
			config.plugins.skin.OverlayHD.Pinstripe.value = "DarkerGrey"
			config.plugins.skin.OverlayHD.MenuBackgroundColour.value = "Black"
			config.plugins.skin.OverlayHD.MenuBackgroundTransparency.value = "0x00000001"
			config.plugins.skin.OverlayHD.MenuSelectedColour.value = "DodgerBlue"
			config.plugins.skin.OverlayHD.MenuSelectedTransparency.value = "0x26000000"
			config.plugins.skin.OverlayHD.MenuText.value = "White"
			config.plugins.skin.OverlayHD.MenuTextSelected.value = "White"
			config.plugins.skin.OverlayHD.FootnoteBackgroundColour.value = "Black"
			config.plugins.skin.OverlayHD.FootnoteBackgroundTransparency.value = "0x00000001"
			config.plugins.skin.OverlayHD.FootnoteText.value = "DimGrey"
			config.plugins.skin.OverlayHD.TextBackgroundColour.value = "Black"
			config.plugins.skin.OverlayHD.TextBackgroundTransparency.value = "0x00000001"
			config.plugins.skin.OverlayHD.Text.value = "White"
			config.plugins.skin.OverlayHD.SMSHelperBackgroundColour.value = "Black"
			config.plugins.skin.OverlayHD.SMSHelperBackgroundTransparency.value = "0x00000001"
			config.plugins.skin.OverlayHD.SMSHelperText.value = "White"
			config.plugins.skin.OverlayHD.VolumeBackground.value = "Black"
			config.plugins.skin.OverlayHD.VolumeColour.value = "Blue"
			config.plugins.skin.OverlayHD.FindCharacter.value = "Gold"
			config.plugins.skin.OverlayHD.InfoBackgroundColour.value = "Black"
			config.plugins.skin.OverlayHD.InfoBackgroundTransparency.value = "0x00000001"
			config.plugins.skin.OverlayHD.InfoLCN.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoChannel.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoBroadcaster.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoBouquet.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoProgramNow.value = "White"
			config.plugins.skin.OverlayHD.InfoTimesNow.value = "Grey"
			config.plugins.skin.OverlayHD.InfoDurationNow.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoFileSizeNow.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoDetailsNow.value = "White"
			config.plugins.skin.OverlayHD.InfoRatingNow.value = "Grey"
			config.plugins.skin.OverlayHD.InfoProgramNext.value = "White"
			config.plugins.skin.OverlayHD.InfoTimesNext.value = "Grey"
			config.plugins.skin.OverlayHD.InfoDurationNext.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoFileSizeNext.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoDetailsNext.value = "White"
			config.plugins.skin.OverlayHD.InfoRatingNext.value = "Grey"
			config.plugins.skin.OverlayHD.InfoRecording.value = "DullRed"
			config.plugins.skin.OverlayHD.InfoRecordingProgress.value = "DeepGrey"
			config.plugins.skin.OverlayHD.InfoMediaName.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoMediaLength.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoDiskStats.value = "DullYellow"
			config.plugins.skin.OverlayHD.TunerBackgroundColour.value = "Black"
			config.plugins.skin.OverlayHD.TunerBackgroundTransparency.value = "0x00000001"
			config.plugins.skin.OverlayHD.GraphicalEPGTransparency.value = "0x00000001"
			config.plugins.skin.OverlayHD.InfobarEPGTransparency.value = "0x00000001"
			config.plugins.skin.OverlayHD.EPGBackground.value = "Black"
			config.plugins.skin.OverlayHD.EPGProgram.value = "Gold"
			config.plugins.skin.OverlayHD.EPGTimes.value = "Grey"
			config.plugins.skin.OverlayHD.EPGDuration.value = "Grey"
			config.plugins.skin.OverlayHD.EPGRating.value = "Grey"
			config.plugins.skin.OverlayHD.EPGDetails.value = "White"
			config.plugins.skin.OverlayHD.EPGTimeLineBorderColour.value = "ScreenBackground"
			config.plugins.skin.OverlayHD.EPGTimeLineColour.value = "DullYellow"
			config.plugins.skin.OverlayHD.EPGGridBackground.value = "Orange"
			config.plugins.skin.OverlayHD.EPGEntryBackgroundColor.value = "DarkerBlue"
			config.plugins.skin.OverlayHD.EPGEntryBackgroundColorSelected.value = "Yellow"
			config.plugins.skin.OverlayHD.EPGEntryForegroundColor.value = "White"
			config.plugins.skin.OverlayHD.EPGEntryForegroundColorSelected.value = "Black"
			config.plugins.skin.OverlayHD.EPGEntryForegroundColorNowSelected.value = "Black"
			config.plugins.skin.OverlayHD.EPGRecordBackgroundColor.value = "DullRed"
			config.plugins.skin.OverlayHD.EPGRecordBackgroundColorSelected.value = "Red"
			config.plugins.skin.OverlayHD.EPGRecordForegroundColor.value = "White"
			config.plugins.skin.OverlayHD.EPGRecordForegroundColorSelected.value = "Black"
			config.plugins.skin.OverlayHD.EPGServiceBackgroundColor.value = "DeepBlue"
			config.plugins.skin.OverlayHD.EPGServiceBackgroundColorNow.value = "Blue"
			config.plugins.skin.OverlayHD.EPGServiceForegroundColor.value = "White"
			config.plugins.skin.OverlayHD.EPGServiceForegroundColorNow.value = "White"
			config.plugins.skin.OverlayHD.EPGZapBackgroundColor.value = "DullGreen"
			config.plugins.skin.OverlayHD.EPGZapBackgroundColorSelected.value = "Green"
			config.plugins.skin.OverlayHD.EPGZapForegroundColor.value = "White"
			config.plugins.skin.OverlayHD.EPGZapForegroundColorSelected.value = "Black"
			config.plugins.skin.OverlayHD.EPGPIGBackground.value = "Black"
			config.plugins.skin.OverlayHD.EPGPIGBorder.value = "Black"
			config.plugins.skin.OverlayHD.EPGPIGColour.value = "WarmYellow"
			config.plugins.skin.OverlayHD.EPGPIGProgressBackground.value = "DeepGrey"
			config.plugins.skin.OverlayHD.EPGPIGProgressColour.value = "WarmYellow"
			config.plugins.skin.OverlayHD.EPGPIGProgressBorder.value = "WarmYellow"
			config.plugins.skin.OverlayHD.EPGPIGTimeLineBorderColour.value = "ScreenBackground"
			config.plugins.skin.OverlayHD.EPGPIGTimeLineColour.value = "DullYellow"
			config.plugins.skin.OverlayHD.EPGPIGGridBackground.value = "Orange"
			config.plugins.skin.OverlayHD.EPGPIGEntryBackgroundColor.value = "DarkerBlue"
			config.plugins.skin.OverlayHD.EPGPIGEntryBackgroundColorSelected.value = "Yellow"
			config.plugins.skin.OverlayHD.EPGPIGEntryForegroundColor.value = "White"
			config.plugins.skin.OverlayHD.EPGPIGEntryForegroundColorSelected.value = "Black"
			config.plugins.skin.OverlayHD.EPGPIGRecordBackgroundColor.value = "DullRed"
			config.plugins.skin.OverlayHD.EPGPIGRecordBackgroundColorSelected.value = "Red"
			config.plugins.skin.OverlayHD.EPGPIGRecordForegroundColor.value = "White"
			config.plugins.skin.OverlayHD.EPGPIGRecordForegroundColorSelected.value = "Black"
			config.plugins.skin.OverlayHD.EPGPIGServiceBackgroundColor.value = "DeepBlue"
			config.plugins.skin.OverlayHD.EPGPIGServiceBackgroundColorNow.value = "Blue"
			config.plugins.skin.OverlayHD.EPGPIGServiceForegroundColor.value = "White"
			config.plugins.skin.OverlayHD.EPGPIGServiceForegroundColorNow.value = "White"
			config.plugins.skin.OverlayHD.EPGPIGZapBackgroundColor.value = "DullGreen"
			config.plugins.skin.OverlayHD.EPGPIGZapBackgroundColorSelected.value = "Green"
			config.plugins.skin.OverlayHD.EPGPIGZapForegroundColor.value = "White"
			config.plugins.skin.OverlayHD.EPGPIGZapForegroundColorSelected.value = "Black"

			self.process = True
			self.applySettings()
		else:
			print "[OverlayHD] OverlayHD is not the active skin!"

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
	if colour.value != "0x00000001":
		trans = long(transparency.value, 0x10)
	else:
		trans = long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value, 0x10)
	return gRGB(colorNames[colour.value].argb() | trans)

def applySkinSettings():
	if config.skin.primary_skin.value == "OverlayHD/skin.xml":
		print "[OverlayHD] Applying OverlayHD skin settings."
		colorNames["ScreenBackground"] = gRGB(colorNames[config.plugins.skin.OverlayHD.ScreenBackgroundColour.value].argb() |
							long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value, 0x10))
		colorNames["BannerClock"] = colorNames[config.plugins.skin.OverlayHD.BannerClock.value]
		colorNames["BannerTitle"] = colorNames[config.plugins.skin.OverlayHD.BannerTitle.value]
		colorNames["Pinstripe"] = colorNames[config.plugins.skin.OverlayHD.Pinstripe.value]
		# colorNames["MenuBackground"] = buildColour(config.plugins.skin.OverlayHD.MenuBackgroundColour, config.plugins.skin.OverlayHD.MenuBackgroundTransparency)
		colorNames["MenuBackground"] = colorNames["ScreenBackground"]
		colorNames["MenuSelected"] = buildColour(config.plugins.skin.OverlayHD.MenuSelectedColour, config.plugins.skin.OverlayHD.MenuSelectedTransparency)
		colorNames["MenuText"] = colorNames[config.plugins.skin.OverlayHD.MenuText.value]
		colorNames["MenuTextSelected"] = colorNames[config.plugins.skin.OverlayHD.MenuTextSelected.value]
		# colorNames["FootnoteBackground"] = buildColour(config.plugins.skin.OverlayHD.FootnoteBackgroundColour, config.plugins.skin.OverlayHD.FootnoteBackgroundTransparency)
		colorNames["FootnoteBackground"] = colorNames["ScreenBackground"]
		colorNames["FootnoteText"] = colorNames[config.plugins.skin.OverlayHD.FootnoteText.value]
		# colorNames["TextBackground"] = buildColour(config.plugins.skin.OverlayHD.TextBackgroundColour, config.plugins.skin.OverlayHD.TextBackgroundTransparency)
		colorNames["TextBackground"] = colorNames["ScreenBackground"]
		colorNames["Text"] = colorNames[config.plugins.skin.OverlayHD.Text.value]
		# colorNames["SMSHelperBackground"] = buildColour(config.plugins.skin.OverlayHD.SMSHelperBackgroundColour, config.plugins.skin.OverlayHD.SMSHelperBackgroundTransparency)
		colorNames["SMSHelperBackground"] = colorNames["ScreenBackground"]
		colorNames["SMSHelperText"] = colorNames[config.plugins.skin.OverlayHD.SMSHelperText.value]
		colorNames["VolumeBackground"] = colorNames[config.plugins.skin.OverlayHD.VolumeBackground.value]
		colorNames["VolumeColour"] = colorNames[config.plugins.skin.OverlayHD.VolumeColour.value]
		colorNames["FindCharacter"] = colorNames[config.plugins.skin.OverlayHD.FindCharacter.value]
		# colorNames["InfoBackground"] = buildColour(config.plugins.skin.OverlayHD.InfoBackgroundColour, config.plugins.skin.OverlayHD.InfoBackgroundTransparency)
		colorNames["InfoBackground"] = colorNames["ScreenBackground"]
		colorNames["InfoLCN"] = colorNames[config.plugins.skin.OverlayHD.InfoLCN.value]
		colorNames["InfoChannel"] = colorNames[config.plugins.skin.OverlayHD.InfoChannel.value]
		colorNames["InfoBroadcaster"] = colorNames[config.plugins.skin.OverlayHD.InfoBroadcaster.value]
		colorNames["InfoBouquet"] = colorNames[config.plugins.skin.OverlayHD.InfoBouquet.value]
		colorNames["InfoProgramNow"] = colorNames[config.plugins.skin.OverlayHD.InfoProgramNow.value]
		colorNames["InfoTimesNow"] = colorNames[config.plugins.skin.OverlayHD.InfoTimesNow.value]
		colorNames["InfoDurationNow"] = colorNames[config.plugins.skin.OverlayHD.InfoDurationNow.value]
		colorNames["InfoFileSizeNow"] = colorNames[config.plugins.skin.OverlayHD.InfoFileSizeNow.value]
		colorNames["InfoDetailsNow"] = colorNames[config.plugins.skin.OverlayHD.InfoDetailsNow.value]
		colorNames["InfoRatingNow"] = colorNames[config.plugins.skin.OverlayHD.InfoRatingNow.value]
		colorNames["InfoProgramNext"] = colorNames[config.plugins.skin.OverlayHD.InfoProgramNext.value]
		colorNames["InfoTimesNext"] = colorNames[config.plugins.skin.OverlayHD.InfoTimesNext.value]
		colorNames["InfoDurationNext"] = colorNames[config.plugins.skin.OverlayHD.InfoDurationNext.value]
		colorNames["InfoFileSizeNext"] = colorNames[config.plugins.skin.OverlayHD.InfoFileSizeNext.value]
		colorNames["InfoDetailsNext"] = colorNames[config.plugins.skin.OverlayHD.InfoDetailsNext.value]
		colorNames["InfoRatingNext"] = colorNames[config.plugins.skin.OverlayHD.InfoRatingNext.value]
		colorNames["InfoRecording"] = colorNames[config.plugins.skin.OverlayHD.InfoRecording.value]
		colorNames["InfoRecordingProgress"] = colorNames[config.plugins.skin.OverlayHD.InfoRecordingProgress.value]
		colorNames["InfoMediaName"] = colorNames[config.plugins.skin.OverlayHD.InfoMediaName.value]
		colorNames["InfoMediaLength"] = colorNames[config.plugins.skin.OverlayHD.InfoMediaLength.value]
		colorNames["InfoDiskStats"] = colorNames[config.plugins.skin.OverlayHD.InfoDiskStats.value]
		# colorNames["TunerBackground"] = buildColour(config.plugins.skin.OverlayHD.TunerBackgroundColour, config.plugins.skin.OverlayHD.TunerBackgroundTransparency)
		colorNames["TunerBackground"] = colorNames["ScreenBackground"]
		# colorNames["GraphicalEPGTransparency"] = buildColour(config.plugins.skin.OverlayHD.InfoBackgroundColour, config.plugins.skin.OverlayHD.InfoBackgroundTransparency)
		colorNames["GraphicalEPGTransparency"] = colorNames["ScreenBackground"]
		# colorNames["InfobarEPGTransparency"] = buildColour(config.plugins.skin.OverlayHD.InfoBackgroundColour, config.plugins.skin.OverlayHD.InfoBackgroundTransparency)
		colorNames["InfobarEPGTransparency"] = colorNames["ScreenBackground"]
		colorNames["EPGBackground"] = colorNames[config.plugins.skin.OverlayHD.EPGBackground.value]
		colorNames["EPGProgram"] = colorNames[config.plugins.skin.OverlayHD.EPGProgram.value]
		colorNames["EPGTimes"] = colorNames[config.plugins.skin.OverlayHD.EPGTimes.value]
		colorNames["EPGDuration"] = colorNames[config.plugins.skin.OverlayHD.EPGDuration.value]
		colorNames["EPGRating"] = colorNames[config.plugins.skin.OverlayHD.EPGRating.value]
		colorNames["EPGDetails"] = colorNames[config.plugins.skin.OverlayHD.EPGDetails.value]
		colorNames["EPGTimeLineBorderColour"] = colorNames[config.plugins.skin.OverlayHD.EPGTimeLineBorderColour.value]
		colorNames["EPGTimeLineColour"] = colorNames[config.plugins.skin.OverlayHD.EPGTimeLineColour.value]
		colorNames["EPGGridBackground"] = colorNames[config.plugins.skin.OverlayHD.EPGGridBackground.value]
		colorNames["EPGEntryBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryBackgroundColor.value]
		colorNames["EPGEntryBackgroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryBackgroundColorSelected.value]
		colorNames["EPGEntryForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryForegroundColor.value]
		colorNames["EPGEntryForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryForegroundColorSelected.value]
		colorNames["EPGEntryForegroundColorNowSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryForegroundColorNowSelected.value]
		colorNames["EPGRecordBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordBackgroundColor.value]
		colorNames["EPGRecordBackgroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordBackgroundColorSelected.value]
		colorNames["EPGRecordForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordForegroundColor.value]
		colorNames["EPGRecordForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordForegroundColorSelected.value]
		colorNames["EPGServiceBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceBackgroundColor.value]
		colorNames["EPGServiceBackgroundColorNow"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceBackgroundColorNow.value]
		colorNames["EPGServiceForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceForegroundColor.value]
		colorNames["EPGServiceForegroundColorNow"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceForegroundColorNow.value]
		colorNames["EPGZapBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGZapBackgroundColor.value]
		colorNames["EPGZapBackgroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGZapBackgroundColorSelected.value]
		colorNames["EPGZapForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGZapForegroundColor.value]
		colorNames["EPGZapForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGZapForegroundColorSelected.value]
		colorNames["EPGPIGBackground"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGBackground.value]
		colorNames["EPGPIGBorder"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGBorder.value]
		colorNames["EPGPIGColour"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGColour.value]
		colorNames["EPGPIGProgressBackground"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGProgressBackground.value]
		colorNames["EPGPIGProgressColour"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGProgressColour.value]
		colorNames["EPGPIGProgressBorder"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGProgressBorder.value]
		colorNames["EPGPIGTimeLineBorderColour"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGTimeLineBorderColour.value]
		colorNames["EPGPIGTimeLineColour"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGTimeLineColour.value]
		colorNames["EPGPIGGridBackground"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGGridBackground.value]
		colorNames["EPGPIGEntryBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGEntryBackgroundColor.value]
		colorNames["EPGPIGEntryBackgroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGEntryBackgroundColorSelected.value]
		colorNames["EPGPIGEntryForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGEntryForegroundColor.value]
		colorNames["EPGPIGEntryForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGEntryForegroundColorSelected.value]
		colorNames["EPGPIGRecordBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGRecordBackgroundColor.value]
		colorNames["EPGPIGRecordBackgroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGRecordBackgroundColorSelected.value]
		colorNames["EPGPIGRecordForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGRecordForegroundColor.value]
		colorNames["EPGPIGRecordForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGRecordForegroundColorSelected.value]
		colorNames["EPGPIGServiceBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGServiceBackgroundColor.value]
		colorNames["EPGPIGServiceBackgroundColorNow"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGServiceBackgroundColorNow.value]
		colorNames["EPGPIGServiceForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGServiceForegroundColor.value]
		colorNames["EPGPIGServiceForegroundColorNow"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGServiceForegroundColorNow.value]
		colorNames["EPGPIGZapBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGZapBackgroundColor.value]
		colorNames["EPGPIGZapBackgroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGZapBackgroundColorSelected.value]
		colorNames["EPGPIGZapForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGZapForegroundColor.value]
		colorNames["EPGPIGZapForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGPIGZapForegroundColorSelected.value]
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
			description="OverlayHD Skin Manager version 1.10", icon="OverlayHD.png", fnc=main))
	return list
