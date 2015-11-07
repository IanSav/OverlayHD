#====================================================
# OverlayHD Skin Manager
# Version Date - 4-Nov-2015
# Version Number - 1.17
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
	("Mustard", _("Mustard")),
	("Navy", _("Navy")),
	("Orange", _("Orange")),
	("OrangeRed", _("Orange Red")),
	("OxfordBlue", _("Oxford Blue")),
	("Pink", _("Pink")),
	("PowderBlue", _("Powder Blue")),
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

config.plugins.skin.OverlayHD.ScreenBackgroundColour = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.ScreenBackgroundTransparency = ConfigSelection(default="0x3f000000", choices=transparency_choices)

config.plugins.skin.OverlayHD.BannerBorder = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.BannerClock = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.BannerClockDate = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.BannerClockTime = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.BannerTitle = ConfigSelection(default="White", choices=colour_choices)

config.plugins.skin.OverlayHD.EPGBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGChannel = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGChannelSelected = ConfigSelection(default="Blue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGDetails = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGDuration = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGGridBackground = ConfigSelection(default="Orange", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGLCN = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGOverlayBorder = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGOverlayColour = ConfigSelection(default="WarmYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGProgram = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGProgramSelected = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGProgressBackground = ConfigSelection(default="DeepGrey", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGProgressBorder = ConfigSelection(default="WarmYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGProgressColour = ConfigSelection(default="WarmYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGProvider = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGRating = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTimeLine = ConfigSelection(default="Yellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTimes = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTimesSelected = ConfigSelection(default="Silver", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGTransparency = ConfigSelection(default="Background", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.EPGEntryBackgroundColor = ConfigSelection(default="DarkerBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryBackgroundColorSelected = ConfigSelection(default="Yellow", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryForegroundColor = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.EPGEntryForegroundColorSelected = ConfigSelection(default="Black", choices=colour_choices)
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

config.plugins.skin.OverlayHD.FindCharacter = ConfigSelection(default="Gold", choices=colour_choices)
config.plugins.skin.OverlayHD.FootnoteBackgroundColour = ConfigSelection(default="Background", choices=background_choice + colour_choices)
config.plugins.skin.OverlayHD.FootnoteBackgroundTransparency = ConfigSelection(default="Background", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.FootnoteText = ConfigSelection(default="DimGrey", choices=colour_choices)

config.plugins.skin.OverlayHD.HelpPress = ConfigSelection(default="Yellow", choices=colour_choices)

config.plugins.skin.OverlayHD.InfoBackgroundColour = ConfigSelection(default="Background", choices=background_choice + colour_choices)
config.plugins.skin.OverlayHD.InfoBackgroundTransparency = ConfigSelection(default="Background", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.InfoBouquet = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoBroadcaster = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoChannel = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDetailsNext = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDetailsNow = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDiskStats = ConfigSelection(default="DullYellow", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDurationNext = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoDurationNow = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoFileSizeNext = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoFileSizeNow = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoLCN = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoMediaLength = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoMediaName = ConfigSelection(default="LightBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoMediaPosition = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoMediaRemaining = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoProgramNext = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoProgramNow = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoProgressBorder = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoRatingNext = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoRatingNow = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoRecording = ConfigSelection(default="DullRed", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoRecordingProgress = ConfigSelection(default="DeepGrey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoTimesNext = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.InfoTimesNow = ConfigSelection(default="Grey", choices=colour_choices)

config.plugins.skin.OverlayHD.MenuBackgroundColour = ConfigSelection(default="Background", choices=background_choice + colour_choices)
config.plugins.skin.OverlayHD.MenuBackgroundTransparency = ConfigSelection(default="Background", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.MenuDisabled = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.MenuSelectedColour = ConfigSelection(default="DodgerBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.MenuSelectedTransparency = ConfigSelection(default="0x26000000", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.MenuText = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.MenuTextSelected = ConfigSelection(default="White", choices=colour_choices)

config.plugins.skin.OverlayHD.PictureBackgroundColour = ConfigSelection(default="Background", choices=background_choice + colour_choices)
config.plugins.skin.OverlayHD.PictureBackgroundTransparency = ConfigSelection(default="Background", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.PictureLabel = ConfigSelection(default="DullGreen", choices=colour_choices)
config.plugins.skin.OverlayHD.PictureLabelBorder = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.Pinstripe = ConfigSelection(default="DarkerGrey", choices=colour_choices)

config.plugins.skin.OverlayHD.Resolution = ConfigSelection(default="Silver", choices=colour_choices)
config.plugins.skin.OverlayHD.ResolutionBackgroundColour = ConfigSelection(default="Background", choices=background_choice + colour_choices)
config.plugins.skin.OverlayHD.ResolutionBackgroundTransparency = ConfigSelection(default="Background", choices=background_choice + transparency_choices)

config.plugins.skin.OverlayHD.SMSHelperBackgroundColour = ConfigSelection(default="Background", choices=background_choice + colour_choices)
config.plugins.skin.OverlayHD.SMSHelperBackgroundTransparency = ConfigSelection(default="Background", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.SMSHelperText = ConfigSelection(default="White", choices=colour_choices)

config.plugins.skin.OverlayHD.TextBackgroundColour = ConfigSelection(default="Background", choices=background_choice + colour_choices)
config.plugins.skin.OverlayHD.TextBackgroundTransparency = ConfigSelection(default="Background", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.Text = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.TextSelected = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.TextIndented = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.TextIndentedSelected = ConfigSelection(default="Silver", choices=colour_choices)
config.plugins.skin.OverlayHD.TextLabel = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.TextWaiting = ConfigSelection(default="Gold", choices=colour_choices)
config.plugins.skin.OverlayHD.TimeShiftBorder = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.TimeShiftData = ConfigSelection(default="Silver", choices=colour_choices)
config.plugins.skin.OverlayHD.TunerBackgroundColour = ConfigSelection(default="Background", choices=background_choice + colour_choices)
config.plugins.skin.OverlayHD.TunerBackgroundTransparency = ConfigSelection(default="Background", choices=background_choice + transparency_choices)
config.plugins.skin.OverlayHD.TunerBER = ConfigSelection(default="OrangeRed", choices=colour_choices)
config.plugins.skin.OverlayHD.TunerBorder = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.TunerCurrent = ConfigSelection(default="DullGreen", choices=colour_choices)
config.plugins.skin.OverlayHD.TunerData = ConfigSelection(default="Silver", choices=colour_choices)
config.plugins.skin.OverlayHD.TunerIdle = ConfigSelection(default="DimGrey", choices=colour_choices)
config.plugins.skin.OverlayHD.TunerLabel = ConfigSelection(default="PowderBlue", choices=colour_choices)
config.plugins.skin.OverlayHD.TunerRecording = ConfigSelection(default="Orange", choices=colour_choices)

config.plugins.skin.OverlayHD.VolumeBackground = ConfigSelection(default="Black", choices=colour_choices)
config.plugins.skin.OverlayHD.VolumeColour = ConfigSelection(default="LightBlue", choices=colour_choices)

config.plugins.skin.OverlayHD.WeatherData = ConfigSelection(default="White", choices=colour_choices)
config.plugins.skin.OverlayHD.WeatherLabel = ConfigSelection(default="Grey", choices=colour_choices)
config.plugins.skin.OverlayHD.WeatherProvider = ConfigSelection(default="Orange", choices=colour_choices)


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
			config.plugins.skin.OverlayHD.BannerBorder.value = "Black"
			config.plugins.skin.OverlayHD.BannerClock.value = "White"
			config.plugins.skin.OverlayHD.BannerClockDate.value = "LightBlue"
			config.plugins.skin.OverlayHD.BannerClockTime.value = "White"
			config.plugins.skin.OverlayHD.BannerTitle.value = "White"
			config.plugins.skin.OverlayHD.EPGBackground.value = "Black"
			config.plugins.skin.OverlayHD.EPGChannel.value = "LightBlue"
			config.plugins.skin.OverlayHD.EPGChannelSelected.value = "Blue"
			config.plugins.skin.OverlayHD.EPGDetails.value = "White"
			config.plugins.skin.OverlayHD.EPGDuration.value = "Grey"
			config.plugins.skin.OverlayHD.EPGGridBackground.value = "Orange"
			config.plugins.skin.OverlayHD.EPGLCN.value = "LightBlue"
			config.plugins.skin.OverlayHD.EPGOverlayBorder.value = "Black"
			config.plugins.skin.OverlayHD.EPGOverlayColour.value = "WarmYellow"
			config.plugins.skin.OverlayHD.EPGProgram.value = "White"
			config.plugins.skin.OverlayHD.EPGProgramSelected.value = "White"
			config.plugins.skin.OverlayHD.EPGProgressBackground.value = "DeepGrey"
			config.plugins.skin.OverlayHD.EPGProgressBorder.value = "WarmYellow"
			config.plugins.skin.OverlayHD.EPGProgressColour.value = "WarmYellow"
			config.plugins.skin.OverlayHD.EPGProvider.value = "LightBlue"
			config.plugins.skin.OverlayHD.EPGRating.value = "Grey"
			config.plugins.skin.OverlayHD.EPGTimeLine.value = "Yellow"
			config.plugins.skin.OverlayHD.EPGTimes.value = "Grey"
			config.plugins.skin.OverlayHD.EPGTimesSelected.value = "Silver"
			config.plugins.skin.OverlayHD.EPGTransparency.value = "Background"
			config.plugins.skin.OverlayHD.EPGEntryBackgroundColor.value = "DarkerBlue"
			config.plugins.skin.OverlayHD.EPGEntryBackgroundColorSelected.value = "Yellow"
			config.plugins.skin.OverlayHD.EPGEntryForegroundColor.value = "White"
			config.plugins.skin.OverlayHD.EPGEntryForegroundColorSelected.value = "Black"
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
			config.plugins.skin.OverlayHD.FindCharacter.value = "Gold"
			config.plugins.skin.OverlayHD.FootnoteBackgroundColour.value = "Background"
			config.plugins.skin.OverlayHD.FootnoteBackgroundTransparency.value = "Background"
			config.plugins.skin.OverlayHD.FootnoteText.value = "DimGrey"
			config.plugins.skin.OverlayHD.HelpPress.value = "Yellow"
			config.plugins.skin.OverlayHD.InfoBackgroundColour.value = "Background"
			config.plugins.skin.OverlayHD.InfoBackgroundTransparency.value = "Background"
			config.plugins.skin.OverlayHD.InfoBouquet.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoBroadcaster.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoChannel.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoDetailsNext.value = "White"
			config.plugins.skin.OverlayHD.InfoDetailsNow.value = "White"
			config.plugins.skin.OverlayHD.InfoDiskStats.value = "DullYellow"
			config.plugins.skin.OverlayHD.InfoDurationNext.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoDurationNow.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoFileSizeNext.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoFileSizeNow.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoLCN.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoMediaLength.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoMediaName.value = "LightBlue"
			config.plugins.skin.OverlayHD.InfoMediaPosition.value = "White"
			config.plugins.skin.OverlayHD.InfoMediaRemaining.value = "White"
			config.plugins.skin.OverlayHD.InfoProgramNext.value = "White"
			config.plugins.skin.OverlayHD.InfoProgramNow.value = "White"
			config.plugins.skin.OverlayHD.InfoProgressBorder.value = "Grey"
			config.plugins.skin.OverlayHD.InfoRatingNext.value = "Grey"
			config.plugins.skin.OverlayHD.InfoRatingNow.value = "Grey"
			config.plugins.skin.OverlayHD.InfoRecording.value = "DullRed"
			config.plugins.skin.OverlayHD.InfoRecordingProgress.value = "DeepGrey"
			config.plugins.skin.OverlayHD.InfoTimesNext.value = "Grey"
			config.plugins.skin.OverlayHD.InfoTimesNow.value = "Grey"
			config.plugins.skin.OverlayHD.MenuBackgroundColour.value = "Background"
			config.plugins.skin.OverlayHD.MenuBackgroundTransparency.value = "Background"
			config.plugins.skin.OverlayHD.MenuDisabled.value = "Grey"
			config.plugins.skin.OverlayHD.MenuSelectedColour.value = "DodgerBlue"
			config.plugins.skin.OverlayHD.MenuSelectedTransparency.value = "0x26000000"
			config.plugins.skin.OverlayHD.MenuText.value = "White"
			config.plugins.skin.OverlayHD.MenuTextSelected.value = "White"
			config.plugins.skin.OverlayHD.PictureBackgroundColour.value = "Background"
			config.plugins.skin.OverlayHD.PictureBackgroundTransparency.value = "Background"
			config.plugins.skin.OverlayHD.PictureLabel.value = "DullGreen"
			config.plugins.skin.OverlayHD.PictureLabelBorder.value = "Black"
			config.plugins.skin.OverlayHD.Pinstripe.value = "DarkerGrey"
			config.plugins.skin.OverlayHD.Resolution.value = "Silver"
			config.plugins.skin.OverlayHD.ResolutionBackgroundColour.value = "Background"
			config.plugins.skin.OverlayHD.ResolutionBackgroundTransparency.value = "Background"
			config.plugins.skin.OverlayHD.SMSHelperBackgroundColour.value = "Background"
			config.plugins.skin.OverlayHD.SMSHelperBackgroundTransparency.value = "Background"
			config.plugins.skin.OverlayHD.SMSHelperText.value = "White"
			config.plugins.skin.OverlayHD.TextBackgroundColour.value = "Background"
			config.plugins.skin.OverlayHD.TextBackgroundTransparency.value = "Background"
			config.plugins.skin.OverlayHD.Text.value = "White"
			config.plugins.skin.OverlayHD.TextSelected.value = "White"
			config.plugins.skin.OverlayHD.TextIndented.value = "Grey"
			config.plugins.skin.OverlayHD.TextIndentedSelected.value = "Silver"
			config.plugins.skin.OverlayHD.TextLabel.value = "Grey"
			config.plugins.skin.OverlayHD.TextWaiting.value = "Gold"
			config.plugins.skin.OverlayHD.TimeShiftBorder.value = "Grey"
			config.plugins.skin.OverlayHD.TimeShiftData.value = "Silver"
			config.plugins.skin.OverlayHD.TunerBackgroundColour.value = "Background"
			config.plugins.skin.OverlayHD.TunerBackgroundTransparency.value = "Background"
			config.plugins.skin.OverlayHD.TunerBER.value = "OrangeRed"
			config.plugins.skin.OverlayHD.TunerBorder.value = "Grey"
			config.plugins.skin.OverlayHD.TunerCurrent.value = "DullGreen"
			config.plugins.skin.OverlayHD.TunerData.value = "Silver"
			config.plugins.skin.OverlayHD.TunerIdle.value = "DimGrey"
			config.plugins.skin.OverlayHD.TunerLabel.value = "PowderBlue"
			config.plugins.skin.OverlayHD.TunerRecording.value = "Orange"
			config.plugins.skin.OverlayHD.VolumeBackground.value = "Black"
			config.plugins.skin.OverlayHD.VolumeColour.value = "LightBlue"
			config.plugins.skin.OverlayHD.WeatherData.value = "White"
			config.plugins.skin.OverlayHD.WeatherLabel.value = "Grey"
			config.plugins.skin.OverlayHD.WeatherProvider.value = "Orange"
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
	if colour.value == "Background":
		col = config.plugins.skin.OverlayHD.ScreenBackgroundColour.value
	else:
		col = colour.value
	if transparency.value == "Background":
		trans = long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value, 0x10)
	else:
		trans = long(transparency.value, 0x10)
	return gRGB(colorNames[col].argb() | trans)

def applySkinSettings():
	if config.skin.primary_skin.value == "OverlayHD/skin.xml":
		print "[OverlayHD] Applying OverlayHD skin settings."
		colorNames["ScreenBackground"] = gRGB(colorNames[config.plugins.skin.OverlayHD.ScreenBackgroundColour.value].argb() |
							long(config.plugins.skin.OverlayHD.ScreenBackgroundTransparency.value, 0x10))
		colorNames["BannerBorder"] = colorNames[config.plugins.skin.OverlayHD.BannerBorder.value]
		colorNames["BannerClock"] = colorNames[config.plugins.skin.OverlayHD.BannerClock.value]
		colorNames["BannerClockDate"] = colorNames[config.plugins.skin.OverlayHD.BannerClockDate.value]
		colorNames["BannerClockTime"] = colorNames[config.plugins.skin.OverlayHD.BannerClockTime.value]
		colorNames["BannerTitle"] = colorNames[config.plugins.skin.OverlayHD.BannerTitle.value]
		colorNames["EPGBackground"] = colorNames[config.plugins.skin.OverlayHD.EPGBackground.value]
		colorNames["EPGChannel"] = colorNames[config.plugins.skin.OverlayHD.EPGChannel.value]
		colorNames["EPGChannelSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGChannelSelected.value]
		colorNames["EPGDetails"] = colorNames[config.plugins.skin.OverlayHD.EPGDetails.value]
		colorNames["EPGDuration"] = colorNames[config.plugins.skin.OverlayHD.EPGDuration.value]
		colorNames["EPGGridBackground"] = colorNames[config.plugins.skin.OverlayHD.EPGGridBackground.value]
		colorNames["EPGLCN"] = colorNames[config.plugins.skin.OverlayHD.EPGLCN.value]
		colorNames["EPGOverlayBorder"] = colorNames[config.plugins.skin.OverlayHD.EPGOverlayBorder.value]
		colorNames["EPGOverlayColour"] = colorNames[config.plugins.skin.OverlayHD.EPGOverlayColour.value]
		colorNames["EPGProgram"] = colorNames[config.plugins.skin.OverlayHD.EPGProgram.value]
		colorNames["EPGProgramSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGProgramSelected.value]
		colorNames["EPGProgressBackground"] = colorNames[config.plugins.skin.OverlayHD.EPGProgressBackground.value]
		colorNames["EPGProgressBorder"] = colorNames[config.plugins.skin.OverlayHD.EPGProgressBorder.value]
		colorNames["EPGProgressColour"] = colorNames[config.plugins.skin.OverlayHD.EPGProgressColour.value]
		colorNames["EPGRating"] = colorNames[config.plugins.skin.OverlayHD.EPGRating.value]
		colorNames["EPGTimeLine"] = colorNames[config.plugins.skin.OverlayHD.EPGTimeLine.value]
		colorNames["EPGTimes"] = colorNames[config.plugins.skin.OverlayHD.EPGTimes.value]
		colorNames["EPGTimesSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGTimesSelected.value]
		colorNames["EPGEntryBackgroundColor"] = buildColour(config.plugins.skin.OverlayHD.EPGEntryBackgroundColor, config.plugins.skin.OverlayHD.EPGTransparency)
		colorNames["EPGEntryBackgroundColorSelected"] = buildColour(config.plugins.skin.OverlayHD.EPGEntryBackgroundColorSelected, config.plugins.skin.OverlayHD.EPGTransparency)
		colorNames["EPGEntryForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryForegroundColor.value]
		colorNames["EPGEntryForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryForegroundColorSelected.value]
		colorNames["EPGRecordBackgroundColor"] = buildColour(config.plugins.skin.OverlayHD.EPGRecordBackgroundColor, config.plugins.skin.OverlayHD.EPGTransparency)
		colorNames["EPGRecordBackgroundColorSelected"] = buildColour(config.plugins.skin.OverlayHD.EPGRecordBackgroundColorSelected, config.plugins.skin.OverlayHD.EPGTransparency)
		colorNames["EPGRecordForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordForegroundColor.value]
		colorNames["EPGRecordForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordForegroundColorSelected.value]
		colorNames["EPGServiceBackgroundColor"] = buildColour(config.plugins.skin.OverlayHD.EPGServiceBackgroundColor, config.plugins.skin.OverlayHD.EPGTransparency)
		colorNames["EPGServiceBackgroundColorNow"] = buildColour(config.plugins.skin.OverlayHD.EPGServiceBackgroundColorNow, config.plugins.skin.OverlayHD.EPGTransparency)
		colorNames["EPGServiceForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceForegroundColor.value]
		colorNames["EPGServiceForegroundColorNow"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceForegroundColorNow.value]
		colorNames["EPGZapBackgroundColor"] = buildColour(config.plugins.skin.OverlayHD.EPGZapBackgroundColor, config.plugins.skin.OverlayHD.EPGTransparency)
		colorNames["EPGZapBackgroundColorSelected"] = buildColour(config.plugins.skin.OverlayHD.EPGZapBackgroundColorSelected, config.plugins.skin.OverlayHD.EPGTransparency)
		colorNames["EPGZapForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGZapForegroundColor.value]
		colorNames["EPGZapForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGZapForegroundColorSelected.value]
		colorNames["EPGPIGEntryBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryBackgroundColor.value]
		colorNames["EPGPIGEntryBackgroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryBackgroundColorSelected.value]
		colorNames["EPGPIGEntryForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryForegroundColor.value]
		colorNames["EPGPIGEntryForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGEntryForegroundColorSelected.value]
		colorNames["EPGPIGRecordBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordBackgroundColor.value]
		colorNames["EPGPIGRecordBackgroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordBackgroundColorSelected.value]
		colorNames["EPGPIGRecordForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordForegroundColor.value]
		colorNames["EPGPIGRecordForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGRecordForegroundColorSelected.value]
		colorNames["EPGPIGServiceBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceBackgroundColor.value]
		colorNames["EPGPIGServiceBackgroundColorNow"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceBackgroundColorNow.value]
		colorNames["EPGPIGServiceForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceForegroundColor.value]
		colorNames["EPGPIGServiceForegroundColorNow"] = colorNames[config.plugins.skin.OverlayHD.EPGServiceForegroundColorNow.value]
		colorNames["EPGPIGZapBackgroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGZapBackgroundColor.value]
		colorNames["EPGPIGZapBackgroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGZapBackgroundColorSelected.value]
		colorNames["EPGPIGZapForegroundColor"] = colorNames[config.plugins.skin.OverlayHD.EPGZapForegroundColor.value]
		colorNames["EPGPIGZapForegroundColorSelected"] = colorNames[config.plugins.skin.OverlayHD.EPGZapForegroundColorSelected.value]
		colorNames["FindCharacter"] = colorNames[config.plugins.skin.OverlayHD.FindCharacter.value]
		colorNames["FootnoteBackground"] = buildColour(config.plugins.skin.OverlayHD.FootnoteBackgroundColour, config.plugins.skin.OverlayHD.FootnoteBackgroundTransparency)
		colorNames["FootnoteText"] = colorNames[config.plugins.skin.OverlayHD.FootnoteText.value]
		colorNames["HelpPress"] = colorNames[config.plugins.skin.OverlayHD.HelpPress.value]
		colorNames["InfoBackground"] = buildColour(config.plugins.skin.OverlayHD.InfoBackgroundColour, config.plugins.skin.OverlayHD.InfoBackgroundTransparency)
		colorNames["InfoBouquet"] = colorNames[config.plugins.skin.OverlayHD.InfoBouquet.value]
		colorNames["InfoBroadcaster"] = colorNames[config.plugins.skin.OverlayHD.InfoBroadcaster.value]
		colorNames["InfoChannel"] = colorNames[config.plugins.skin.OverlayHD.InfoChannel.value]
		colorNames["InfoDetailsNext"] = colorNames[config.plugins.skin.OverlayHD.InfoDetailsNext.value]
		colorNames["InfoDetailsNow"] = colorNames[config.plugins.skin.OverlayHD.InfoDetailsNow.value]
		colorNames["InfoDiskStats"] = colorNames[config.plugins.skin.OverlayHD.InfoDiskStats.value]
		colorNames["InfoDurationNext"] = colorNames[config.plugins.skin.OverlayHD.InfoDurationNext.value]
		colorNames["InfoDurationNow"] = colorNames[config.plugins.skin.OverlayHD.InfoDurationNow.value]
		colorNames["InfoFileSizeNext"] = colorNames[config.plugins.skin.OverlayHD.InfoFileSizeNext.value]
		colorNames["InfoFileSizeNow"] = colorNames[config.plugins.skin.OverlayHD.InfoFileSizeNow.value]
		colorNames["InfoLCN"] = colorNames[config.plugins.skin.OverlayHD.InfoLCN.value]
		colorNames["InfoMediaLength"] = colorNames[config.plugins.skin.OverlayHD.InfoMediaLength.value]
		colorNames["InfoMediaName"] = colorNames[config.plugins.skin.OverlayHD.InfoMediaName.value]
		colorNames["InfoMediaPosition"] = colorNames[config.plugins.skin.OverlayHD.InfoMediaPosition.value]
		colorNames["InfoMediaRemaining"] = colorNames[config.plugins.skin.OverlayHD.InfoMediaRemaining.value]
		colorNames["InfoProgramNext"] = colorNames[config.plugins.skin.OverlayHD.InfoProgramNext.value]
		colorNames["InfoProgramNow"] = colorNames[config.plugins.skin.OverlayHD.InfoProgramNow.value]
		colorNames["InfoProgressBorder"] = colorNames[config.plugins.skin.OverlayHD.InfoProgressBorder.value]
		colorNames["InfoRatingNext"] = colorNames[config.plugins.skin.OverlayHD.InfoRatingNext.value]
		colorNames["InfoRatingNow"] = colorNames[config.plugins.skin.OverlayHD.InfoRatingNow.value]
		colorNames["InfoRecording"] = colorNames[config.plugins.skin.OverlayHD.InfoRecording.value]
		colorNames["InfoRecordingProgress"] = colorNames[config.plugins.skin.OverlayHD.InfoRecordingProgress.value]
		colorNames["InfoTimesNext"] = colorNames[config.plugins.skin.OverlayHD.InfoTimesNext.value]
		colorNames["InfoTimesNow"] = colorNames[config.plugins.skin.OverlayHD.InfoTimesNow.value]
		colorNames["MenuBackground"] = buildColour(config.plugins.skin.OverlayHD.MenuBackgroundColour, config.plugins.skin.OverlayHD.MenuBackgroundTransparency)
		colorNames["MenuDisabled"] = colorNames[config.plugins.skin.OverlayHD.MenuDisabled.value]
		colorNames["MenuSelected"] = buildColour(config.plugins.skin.OverlayHD.MenuSelectedColour, config.plugins.skin.OverlayHD.MenuSelectedTransparency)
		colorNames["MenuText"] = colorNames[config.plugins.skin.OverlayHD.MenuText.value]
		colorNames["MenuTextSelected"] = colorNames[config.plugins.skin.OverlayHD.MenuTextSelected.value]
		colorNames["PictureBackground"] = buildColour(config.plugins.skin.OverlayHD.PictureBackgroundColour, config.plugins.skin.OverlayHD.PictureBackgroundTransparency)
		colorNames["PictureLabel"] = colorNames[config.plugins.skin.OverlayHD.PictureLabel.value]
		colorNames["PictureLabelBorder"] = colorNames[config.plugins.skin.OverlayHD.PictureLabelBorder.value]
		colorNames["Pinstripe"] = colorNames[config.plugins.skin.OverlayHD.Pinstripe.value]
		colorNames["Resolution"] = colorNames[config.plugins.skin.OverlayHD.Resolution.value]
		colorNames["ResolutionBackground"] = buildColour(config.plugins.skin.OverlayHD.ResolutionBackgroundColour, config.plugins.skin.OverlayHD.ResolutionBackgroundTransparency)
		colorNames["SMSHelperBackground"] = buildColour(config.plugins.skin.OverlayHD.SMSHelperBackgroundColour, config.plugins.skin.OverlayHD.SMSHelperBackgroundTransparency)
		colorNames["SMSHelperText"] = colorNames[config.plugins.skin.OverlayHD.SMSHelperText.value]
		colorNames["TextBackground"] = buildColour(config.plugins.skin.OverlayHD.TextBackgroundColour, config.plugins.skin.OverlayHD.TextBackgroundTransparency)
		colorNames["Text"] = colorNames[config.plugins.skin.OverlayHD.Text.value]
		colorNames["TextSelected"] = colorNames[config.plugins.skin.OverlayHD.TextSelected.value]
		colorNames["TextIndented"] = colorNames[config.plugins.skin.OverlayHD.TextIndented.value]
		colorNames["TextIndentedSelected"] = colorNames[config.plugins.skin.OverlayHD.TextIndentedSelected.value]
		colorNames["TimeShiftBorder"] = colorNames[config.plugins.skin.OverlayHD.TimeShiftBorder.value]
		colorNames["TimeShiftData"] = colorNames[config.plugins.skin.OverlayHD.TimeShiftData.value]
		colorNames["TunerBackground"] = buildColour(config.plugins.skin.OverlayHD.TunerBackgroundColour, config.plugins.skin.OverlayHD.TunerBackgroundTransparency)
		colorNames["TunerBER"] = colorNames[config.plugins.skin.OverlayHD.TunerBER.value]
		colorNames["TunerBorder"] = colorNames[config.plugins.skin.OverlayHD.TunerBorder.value]
		colorNames["TunerCurrent"] = colorNames[config.plugins.skin.OverlayHD.TunerCurrent.value]
		colorNames["TunerData"] = colorNames[config.plugins.skin.OverlayHD.TunerData.value]
		colorNames["TunerIdle"] = colorNames[config.plugins.skin.OverlayHD.TunerIdle.value]
		colorNames["TunerLabel"] = colorNames[config.plugins.skin.OverlayHD.TunerLabel.value]
		colorNames["TunerRecording"] = colorNames[config.plugins.skin.OverlayHD.TunerRecording.value]
		colorNames["VolumeBackground"] = colorNames[config.plugins.skin.OverlayHD.VolumeBackground.value]
		colorNames["VolumeColour"] = colorNames[config.plugins.skin.OverlayHD.VolumeColour.value]
		colorNames["WeatherData"] = colorNames[config.plugins.skin.OverlayHD.WeatherData.value]
		colorNames["WeatherLabel"] = colorNames[config.plugins.skin.OverlayHD.WeatherLabel.value]
		colorNames["WeatherProvider"] = colorNames[config.plugins.skin.OverlayHD.WeatherProvider.value]
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
			description="OverlayHD Skin Manager version 1.17", icon="OverlayHD.png", fnc=main))
	return list
