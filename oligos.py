##imports
import wx
import wx.grid
import wx.lib.scrolledpanel
import os
import os.path
import time
import platform
import multiprocessing
import Bio.PDB
import webbrowser
from threading import Thread
from tools import *

class D2OPanel(wx.lib.scrolledpanel.ScrolledPanel):
	def __init__(self, parent, W, H):
		wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, id=-1, pos=(10, 60), size=(340, H-330), name="ProtFixbb")
		winh = H-330
		Sizer=wx.GridBagSizer
		self.SetSizer(Sizer)
		self.SetBackgroundColour("#333333")
		self.parent = parent

		if (platform.system() == "Windows"):
			self.lblProt = wx.StaticText(self, -1, "DNAworks Oligo Design", (25, 15), (270, 25), wx.ALIGN_CENTRE)
			self.lblProt.SetFont(wx.Font(12, wx.DEFAULT, wx.ITALIC, wx.BOLD))
		elif (platform.system() == "Darwin"):
			self.lblProt = wx.StaticBitmap(self, -1, wx.Image(self.parent.parent.scriptdir + "/images/osx/fixbb/lblFixbb.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(25, 15), size=(270, 25))
		else:
			self.lblProt = wx.StaticText(self, -1, "DNAworks Oligo Design", (70, 15), style=wx.ALIGN_CENTRE)
			self.lblProt.SetFont(wx.Font(12, wx.DEFAULT, wx.ITALIC, wx.BOLD))
			resizeTextControlForUNIX(self.lblProt, 0, self.GetSize()[0])
		self.lblProt.SetForegroundColour("#FFFFFF")

		'''if (platform.system()=="Windows"):
			self.lblTitle=wx.StaticText(self, label="Job Title", pos= (10,120))
		elif (platform.system() == "Darwin"):
			self.lblTitle = wx.StaticBitmap(self, -1, wx.Image(self.parent.parent.scriptdir + "/images/osx/fixbb/lblFixbb.png",
				wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(25, 15), size=(270, 25))
		self.lblTitle.SetFont(wx.Font(5, wx.DEFAULT))
		self.lblTitle.SetForegroundColour("#FFFFFF")'''

		self.jbTitle=wx.TextCtrl(self, value="Job title",pos=(7,50), size=(119,25))
		#self.jbTitle.Bind

		self.emailBox=wx.TextCtrl(self, value="Your email(optional)",pos=(150,50), size=(119,25))
		#self.jbTitle.Bind

		self.minTemp=wx.TextCtrl(self, value="55",pos=(7,90), size=(119,25))
		#self.jbTitle.Bind

		self.maxTemp=wx.TextCtrl(self, value="75",pos=(150,90), size=(119,25))
		#self.jbTitle.Bind


		self.minLen=wx.TextCtrl(self, value="60",pos=(7,120), size=(119,25))
		#self.jbTitle.Bind

		self.maxLen=wx.TextCtrl(self, value="",pos=(150,120), size=(119,25))
		#self.jbTitle.Bind


		self.AAlist = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS", "LEU", "MET", "ASN", "PRO", "GLN", "ARG", "SER", "THR", "VAL", "TRP", "TYR"]
		self.AAlist.sort()

		self.tagMenu = wx.ComboBox(self, pos=(7, 190), size=(119, 25), choices=self.AAlist, style=wx.CB_READONLY)
		self.tagMenu.Bind(wx.EVT_COMBOBOX, self.desMenuSelect)
		self.tagMenu.SetToolTipString("Select Restriction Site")
		self.tagView = ""
		self.selectedModel = ""

		self.tagBox=wx.TextCtrl(self, value="Whatever you want",pos=(150,190), size=(119,25))
		#self.jbTitle.Bind

		self.Sizer.Add(self, self.lblProt, (3,0), (6,1))
		self.Sizer.Add(self, self.jbTitle, (1,2), (3,1))
		self.Sizer.Add(self, self.emailBox, (5,2), (3,1))
		self.Sizer.Add(self, self.minTemp, (1,4), (3,1))
		self.Sizer.Add(self, self.maxTemp, (5,4), (3,1))
		self.Sizer.Add(self, self.minLen, (1,6), (3,1))
		self.Sizer.Add(self, self.maxLen, (5,6), (3,1))
		self.Sizer.Add(self, self.tagMenu, (1,8), (3,1))
		self.Sizer.Add(self, self.tagBox, (5,8), (3,1))
		self.Layout()


		'''button format
		if (platform.system() == "Darwin"):
			self.btnApply = wx.BitmapButton(self, id=-1, bitmap=wx.Image(self.parent.parent.scriptdir + "/images/osx/fixbb/btnApply.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap(), pos=(131, 190), size=(181, 25))
		else:
			self.btnApply = wx.Button(self, id=-1, label="Apply Selection", pos=(131, 190), size=(181, 25))
			self.btnApply.SetForegroundColour("#000000")
			self.btnApply.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
		self.btnApply.Bind(wx.EVT_BUTTON, self.applySelection)
		self.btnApply.SetToolTipString("Apply the default add type selection to the current resfile selection")
		'''

	##create input file
	##def  input_Design(self):



		#grab output from deamon set time limit: Make liberal for DNAworks #sigh
		##wx interface for outpur, popup=
		##pdbparser- identify 'X' chromophore
			##pop up

		## p=open('oligosinput', 'w')
