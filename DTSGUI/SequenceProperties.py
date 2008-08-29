'''
SequenceProperties.py

Copyright (c) 2003 - 2008 James Urquhart(j_urquhart@btinternet.com)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from UserAnimBase import *

# ***************************************************************************************************
## @brief Class that creates and owns the GUI controls on the "Common/All" sub-panel of the Sequences panel. 
#
#  This class contains event handler and resize callbacks for it's associated GUI controls, along
#  with implementations of refreshSequenceOptions and clearSequenceOptions specific to its
#  controls.
#
class SeqCommonControlsClass(SeqControlsClassBase):


	#######################################
	#  init and cleanup methods
	#######################################


	## @brief Initialize the controls and values that are specific to this panel
	#  @note Calls parent init method
	#  @param tabContainer The GUI tab container control into which everything should be placed.
	def __init__(self, tabContainer):
		SeqControlsClassBase.__init__(self, tabContainer)
		
		## Need to set this in all classes derived from SeqControlsClassBase
		#  @note valid values are: "All", "Action", "IFL", "Vis" and eventually "TexUV" and "Morph"
		self.seqFilter = "All"
		
		# initialize GUI controls
		self.guiToggle = Common_Gui.ToggleButton("guiToggle", "Toggle All", "Toggle export of all sequences", self.getNextEvent(), self.handleGuiToggleEvent, self.guiToggleResize)
		self.guiRefresh = Common_Gui.BasicButton("guiRefresh", "Refresh", "Refresh list of sequences", self.getNextEvent(), self.handleGuiRefreshEvent, self.guiRefreshResize)
		self.guiSeqFramesLabel =  Common_Gui.TextDisplayBox("guiSeqFramesLabel", "Frames:  ", None, self.guiSeqFramesLabelResize)
		self.guiSeqDuration = Common_Gui.NumberPicker("guiSeqDuration", "Seconds: ", "The animation plays for this number of seconds", self.getNextEvent(), self.handleGuiSeqDurationEvent, self.guiSeqDurationResize)
		self.guiSeqDurationLock = Common_Gui.ToggleButton("guiSeqDurationLock", "Lock", "Lock Sequence Duration (changes in frame count don't affect playback time)", self.getNextEvent(), self.handleGuiSeqDurationLockEvent, self.guiSeqDurationLockResize)
		self.guiSeqFPS = Common_Gui.NumberPicker("guiSeqFPS", "FPS: ", "The animation plays back at a rate of this number of keyframes per second", self.getNextEvent(), self.handleGuiSeqFPSEvent, self.guiSeqFPSResize)
		self.guiSeqFPSLock = Common_Gui.ToggleButton("guiSeqFPSLock", "Lock", "Lock Sequence FPS (changes in frame count affect playback time, but not Frames Per Second)", self.getNextEvent(), self.handleGuiSeqFPSLockEvent, self.guiSeqFPSLockResize)
		self.guiPriority = Common_Gui.NumberPicker("guiPriority", "Priority", "Sequence playback priority", self.getNextEvent(), self.handleGuiPriorityEvent, self.guiPriorityResize)

		self.guiGroundFrameSamples = Common_Gui.NumberPicker("guiGroundFrameSamples", "Ground Frames", "Amount of ground frames to export", self.getNextEvent(), self.handleGuiGroundFrameSamplesEvent, self.guiGroundFrameSamplesResize)
		self.guiBlendControlsBox = Common_Gui.BasicFrame("guiBlendControlsBox", None, None, None, None, self.guiBlendControlsBoxResize)
		self.guiBlendSequence = Common_Gui.ToggleButton("guiBlendSequence", "Blend animation", "Export action as a Torque blend sequence", self.getNextEvent(), self.handleGuiBlendSequenceEvent, self.guiBlendSequenceResize)
		self.guiRefPoseTitle = Common_Gui.SimpleText("guiRefPoseTitle", "Ref Pose for ", None, self.guiRefPoseTitleResize)
		self.guiRefPoseFrame = Common_Gui.NumberPicker("guiRefPoseFrame", "Frame", "Frame to use for reference pose", self.getNextEvent(), self.handleGuiRefPoseFrameEvent, self.guiRefPoseFrameResize)

		# sequence toolbox controls
		self.guiAddSeq = Common_Gui.BasicButton("guiAddSeq", "Add...", "Define a new sequence", self.getNextEvent(), self.handleGuiAddSeqEvent, self.guiAddSeqResize)
		

		# set initial states
		self.guiToggle.state = False
		self.guiSeqOptsContainer.enabled = False
		self.guiSeqOptsContainer.fade_mode = 5
		self.guiSeqOptsContainer.borderColor = None
		self.guiSeqList.fade_mode = 0
		self.guiSeqDuration.min = 0.00392  # minimum duration = 1/255 of a second
		self.guiSeqDuration.max = 3600.0
		self.guiSeqDuration.value = 0.00392
		self.guiSeqFPS.min = 0.00027777778
		self.guiSeqFPS.max = 255.0
		self.guiSeqFPS.value = 25.0
		self.guiPriority.min = 0
		self.guiPriority.max = 64 # this seems resonable

		self.guiRefPoseTitle.visible = False
		self.guiRefPoseFrame.visible = False
		self.guiRefPoseFrame.min = 1
		

		# add controls to containers
		tabContainer.addControl(self.guiToggle)
		tabContainer.addControl(self.guiRefresh)
		tabContainer.addControl(self.guiAddSeq)
		self.guiSeqOptsContainer.addControl(self.guiSeqFramesLabel)
		self.guiSeqOptsContainer.addControl(self.guiSeqDuration)
		self.guiSeqOptsContainer.addControl(self.guiSeqDurationLock)
		self.guiSeqOptsContainer.addControl(self.guiSeqFPSLock)
		self.guiSeqOptsContainer.addControl(self.guiSeqFPS)
		self.guiSeqOptsContainer.addControl(self.guiPriority) # 15
		
		self.guiSeqOptsContainer.addControl(self.guiGroundFrameSamples) # 2
		self.guiSeqOptsContainer.addControl(self.guiBlendControlsBox)
		self.guiSeqOptsContainer.addControl(self.guiBlendSequence)
		self.guiSeqOptsContainer.addControl(self.guiRefPoseTitle) # 12
		self.guiSeqOptsContainer.addControl(self.guiRefPoseFrame) # 14



	## @brief Cleans up Blender GUI objects before the interpreter exits;
	#     we must destroy any GUI objects that are referenced in a non-global scope
	#     explicitly before interpreter shutdown to avoid the dreaded
	#     "error totblock" message when exiting Blender.
	#  @note The builtin __del__ method is not guaranteed to be called for objects
	#     that still exist when the interpreter exits.
	#  @note Calls base class cleanup method explicitly.
	def cleanup(self):		
		SeqControlsClassBase.cleanup(self)
		del self.guiToggle
		del self.guiRefresh
		del self.guiAddSeq
		del self.guiSeqFramesLabel
		del self.guiSeqDuration
		del self.guiSeqDurationLock
		del self.guiSeqFPS
		del self.guiSeqFPSLock
		del self.guiPriority

		del self.guiGroundFrameSamples
		del self.guiBlendControlsBox
		del self.guiBlendSequence
		del self.guiRefPoseTitle
		del self.guiRefPoseFrame
		

	#########################
	#  Class specific stuff
	#########################
	
	## @brief Overrides base class version to show DSQ button in the sequence list items.
	#  @note Calls base class version with ShowDSQButton set to True.
	def createSequenceListItem(self, seqName, ShowDSQButton=True):
		return SeqControlsClassBase.createSequenceListItem(self, seqName, True)

		
	#######################################
	#  Event handler methods
	#######################################


	## @brief Handle events generated by the "Toggle All" button (guiToggle).
	#  @param control The invoking GUI control (guiToggle)
	def handleGuiToggleEvent(self, control):
		Prefs = DtsGlobals.Prefs
		# no validation needed here.
		for child in self.guiSeqList.controls:
			child.controls[1].state = control.state
			Prefs['Sequences'][child.controls[0].label]['NoExport'] = not control.state

	## @brief Handle events generated by the "Refresh" button (guiRefresh)
	#  @param control The invoking GUI control (guiRefresh)
	def handleGuiRefreshEvent(self, control):
		self.refreshAll()


	def handleGuiAddSeqEvent(self, control):
		# test - create a pupblock
		text = Blender.Draw.Create("NewSequence")
		f = Blender.Draw.Create(1)
		i = Blender.Draw.Create(2)

		block = []

		block.append(("Name: ", text, 0, 30, "The name of the new sequence"))
		block.append(("Start Frame: ", f, 0, 9999))
		block.append(("End Frame: ", i, 0, 9999))

		retval = Blender.Draw.PupBlock("Create Sequence", block)

		print "PupBlock returned", retval

		print "text\t", text
		print "float\t", f
		print "int\t", i
		# must delete temp gui objects explicitly to avoid "error totblock" messages when blender exits.
		del text
		del f
		del i
		del retval


	## @brief Handle events generated by the "Priority" number picker (guiPriority)
	#  @param control The invoking GUI control (guiPriority)
	def handleGuiPriorityEvent(self, control):
		# no validation needed here.
		if self.guiSeqList.itemIndex == -1: return
		seqName, seqPrefs = self.getSelectedSeqNameAndPrefs()
		seqPrefs['Priority'] = control.value

	## @brief Handle events generated by the Duration "Lock" button (guiSeqDurationLock)
	#  @param control The invoking GUI control (guiSeqDurationLock)
	def handleGuiSeqDurationLockEvent(self, control):
		if self.guiSeqList.itemIndex == -1: return
		seqName, seqPrefs = self.getSelectedSeqNameAndPrefs()
		Prefs.lockDuration(seqName)
		self.guiSeqDurationLock.state = True
		self.guiSeqFPSLock.state = False

	## @brief Handle events generated by the FPS "Lock" button (guiSeqFPSLock)
	#  @param control The invoking GUI control (guiSeqFPSLock)
	def handleGuiSeqFPSLockEvent(self, control):
		if self.guiSeqList.itemIndex == -1: return
		seqName, seqPrefs = self.getSelectedSeqNameAndPrefs()
		Prefs.lockFPS(seqName)
		self.guiSeqDurationLock.state = False
		self.guiSeqFPSLock.state = True

	## @brief Handle events generated by the "Duration" number picker (guiSeqDuration)
	#  @param control The invoking GUI control (guiSeqDuration)
	def handleGuiSeqDurationEvent(self, control):
		Prefs = DtsGlobals.Prefs
		if self.guiSeqList.itemIndex == -1: return
		seqName, seqPrefs = self.getSelectedSeqNameAndPrefs()
		duration = Prefs.setSeqDuration(seqName, float(control.value))
		self.guiSeqDuration.value = float(duration)
		self.guiSeqDuration.tooltip = "Playback Time: %f Seconds" % float(duration)
		fps = Prefs.getSeqFPS(seqName)
		self.guiSeqFPS.value = float(fps)
		self.guiSeqFPS.tooltip = "Playback Rate: %f Frames Per Second" % float(fps)

	## @brief Handle events generated by the "FPS" number picker (guiSeqFPS)
	#  @param control The invoking GUI control (guiSeqFPS)
	def handleGuiSeqFPSEvent(self, control):
		Prefs = DtsGlobals.Prefs
		if self.guiSeqList.itemIndex == -1: return
		seqName, seqPrefs = self.getSelectedSeqNameAndPrefs()
		fps = Prefs.setSeqFPS(seqName, float(control.value))
		duration = Prefs.getSeqDuration(seqName)
		self.guiSeqDuration.value = float(duration)
		self.guiSeqDuration.tooltip = "Playback Time: %f Seconds" % float(duration)
		self.guiSeqFPS.value = float(fps)
		self.guiSeqFPS.tooltip = "Playback Rate: %f Frames Per Second" % float(fps)

	## @brief Handle events generated by the "Blend button" (guiBlendSequence)
	#  @param control The invoking GUI control (guiBlendSequence)
	def handleGuiBlendSequenceEvent(self, control):
		Prefs = DtsGlobals.Prefs
		if self.guiSeqList.itemIndex == -1: return
		seqName, seqPrefs = self.getSelectedSeqNameAndPrefs()
		# blend ref pose selection
		seqPrefs['Blend'] = control.state					
		# if blend is true, show the ref pose controls
		if seqPrefs['Blend'] == True:
			self.guiRefPoseTitle.visible = True
			self.guiRefPoseFrame.visible = True
			# todo - should not talk to blender directly, ask SceneInfo instead.
			# reset max to raw number of frames in ref pose action
			try:
				action = Blender.Armature.NLA.GetActions()[seqPrefs['BlendRefPoseAction']]				
				maxNumFrames = DtsShape_Blender.getHighestActFrame(action)
			except: maxNumFrames = 1
			self.guiRefPoseFrame.max = maxNumFrames
		else:
			self.guiRefPoseTitle.visible = False
			self.guiRefPoseFrame.visible = False


	## @brief Handle events generated by the reference pose frames number picker (guiRefPoseFrame)
	#  @param control The invoking GUI control (guiRefPoseMeguiRefPoseFramenu)
	def handleGuiRefPoseFrameEvent(self, control):
		if self.guiSeqList.itemIndex == -1: return
		seqName, seqPrefs = self.getSelectedSeqNameAndPrefs()
		seqPrefs['BlendRefPoseFrame'] = control.value

 	## @brief Handle events generated by the "Frame Samples" number picker (guiGroundFrameSamples)
	#  @param control The invoking GUI control (guiGroundFrameSamples)
	def handleGuiGroundFrameSamplesEvent(self, control):
		if self.guiSeqList.itemIndex == -1: return
		seqName, seqPrefs = self.getSelectedSeqNameAndPrefs()
		seqPrefs['NumGroundFrames'] = control.value


	#######################################
	#  Refresh and Clear methods
	#######################################


	## @brief Refreshes sequence specific option controls on the right side of the sequences panel.
	#  @note This method should be called whenever the sequence list is refreshed, or when sequence
	#     list selection changes.
	#  @param seqName The name of the currently selected sequence.
	#  @param seqPrefs The preferences key of the currently selected sequence.
	def refreshSequenceOptions(self, seqName, seqPrefs):
		Prefs = DtsGlobals.Prefs
		self.clearSequenceOptions()
		self.guiSeqOptsContainerTitle.label = "Selected Sequence:\n '%s'" % seqName

		maxNumFrames = Prefs.getSeqNumFrames(seqName)

		# Update gui control states
		self.guiSeqOptsContainer.enabled = True

		#updateSeqDurationAndFPS(seqName, seqPrefs)

		self.guiSeqFramesLabel.label = "Frames:  " + str(maxNumFrames)

		if maxNumFrames == 0:
			self.guiSeqDuration.value = 0.0
			self.guiSeqDuration.tooltip = "Playback Time: 0.0 Seconds, Sequence has no key frames!"
			self.guiSeqDuration.enabled = False
			# todo - shouldn't talk to blender directly, ask SceneInfo instead...
			try: self.guiSeqFPS.value = float(Blender.Scene.GetCurrent().getRenderingContext().framesPerSec())
			except: self.guiSeqFPS.value = 25.0
			self.guiSeqDuration.tooltip = "Playback Time: %f Seconds, Sequence has no key frames!" % float(seqPrefs['Duration'])
			self.guiSeqFPS.enabled = False
			self.guiPriority.value = 0
		else:			
			self.guiSeqDuration.value = float(seqPrefs['Duration'])
			self.guiSeqDuration.tooltip = "Playback Time: %f Seconds" % float(seqPrefs['Duration'])
			self.guiSeqDuration.enabled = True
			self.guiSeqFPS.value = float(seqPrefs['FPS'])
			self.guiSeqFPS.tooltip = "Playback Rate: %f Frames Per Second" % float(seqPrefs['FPS'])
			self.guiSeqFPS.enabled = True

		self.guiSeqDurationLock.state = seqPrefs['DurationLocked']
		self.guiSeqFPSLock.state = seqPrefs['FPSLocked']
		self.guiPriority.value = seqPrefs['Priority']

		self.guiRefPoseTitle.label = "Ref pose for '%s'" % seqName
		self.guiRefPoseFrame.min = 1

		self.guiRefPoseFrame.max = maxNumFrames
		self.guiRefPoseFrame.value = seqPrefs['BlendRefPoseFrame']
		self.guiGroundFrameSamples.value = seqPrefs['NumGroundFrames']
		self.guiGroundFrameSamples.max = maxNumFrames

		# show/hide ref pose stuff.
		self.guiBlendSequence.state = seqPrefs['Blend']
		if seqPrefs['Blend'] == True:				
			self.guiRefPoseTitle.visible = True
			self.guiRefPoseFrame.visible = True
		else:
			self.guiRefPoseTitle.visible = False
			self.guiRefPoseFrame.visible = False


		# reset static tooltips
		self.guiPriority.tooltip = "Sequence playback priority"
		self.guiSeqFPSLock.tooltip = "Lock Sequence FPS (changes in frame count affect playback time, but not Frames Per Second)"
		self.guiSeqDurationLock.tooltip = "Lock Sequence Duration (changes in frame count don't affect playback time)"

	## @brief Clears sequence specific option controls on the right side of the sequences panel.
	#  @note This method should be called when no sequence list item is currently selected.
	def clearSequenceOptions(self):
		self.guiSeqOptsContainer.enabled = False
		self.guiSeqOptsContainerTitle.label = "Selected Sequence:\n None Selected"
		for control in self.guiSeqOptsContainer.controls:
			control.tooltip = "No sequence is selected"
		self.guiSeqDuration.value = 0.0
		self.guiSeqFPS.value = 0.0
		self.guiPriority.value = 0
		self.guiRefPoseTitle.visible = False
		self.guiRefPoseFrame.visible = False
		self.guiGroundFrameSamples.value = 0
	

	#########################
	#  Resize callback methods
	#########################


	## @brief Resize callback for guiSeqList
	#  @param control The invoking GUI control object
	def guiSeqListResize(self, control, newwidth, newheight):
		control.x = 10
		control.y = 54
		control.height = newheight - 94
		control.width = 299

	## @brief Resize callback for guiSeqListTitle
	#  @param control The invoking GUI control object
	def guiSeqListTitleResize(self, control, newwidth, newheight):
		control.x, control.y, control.height, control.width = 10,310, 20,82

	## @brief Resize callback for guiRefresh
	#  @param control The invoking GUI control object
	def guiRefreshResize(self, control, newwidth, newheight):
		control.x = 112
		control.y = 25
		control.width = 100

	## @brief Resize callback for guiToggle
	#  @param control The invoking GUI control object
	def guiToggleResize(self, control, newwidth, newheight):
		control.x = 10
		control.y = 25
		control.width = 100

	def guiAddSeqResize(self, control, newWidth, newheight):
		control.x = 112
		control.y = 5
		control.width = 100

	## @brief Resize callback for guiSeqOptsContainer
	#  @param control The invoking GUI control object
	def guiSeqOptsContainerResize(self, control, newwidth, newheight):
		control.x, control.y, control.height, control.width = 309,54, newheight-94,newwidth-309

	## @brief Resize callback for guiSeqOptsContainerTitle
	#  @param control The invoking GUI control object
	#def guiSeqOptsContainerTitleResize(self, control, newwidth, newheight):
	#	control.x, control.y, control.height, control.width = 309,newheight-70, 20,82

	## @brief Resize callback for guiSeqFramesLabel
	#  @param control The invoking GUI control object
	def guiSeqFramesLabelResize(self, control, newwidth, newheight):
		control.x = 5
		control.y = newheight - 60
		control.width = newwidth - 10
		control.height = 20

	## @brief Resize callback for guiSeqDuration
	#  @param control The invoking GUI control object
	def guiSeqDurationResize(self, control, newwidth, newheight):
		control.x = 5
		control.y = newheight - 82
		control.width = newwidth - 52

	## @brief Resize callback for guiSeqDurationLock
	#  @param control The invoking GUI control object
	def guiSeqDurationLockResize(self, control, newwidth, newheight):
		control.x = newwidth - 45
		control.y = newheight - 82
		control.width = 40

	## @brief Resize callback for guiSeqFPS
	#  @param control The invoking GUI control object
	def guiSeqFPSResize(self, control, newwidth, newheight):
		control.x = 5
		control.y = newheight - 104
		control.width = newwidth - 52

	## @brief Resize callback for guiSeqFPSLock
	#  @param control The invoking GUI control object
	def guiSeqFPSLockResize(self, control, newwidth, newheight):
		control.x = newwidth - 45
		control.y = newheight - 104
		control.width = 40

	## @brief Resize callback for guiPriority
	#  @param control The invoking GUI control object
	def guiPriorityResize(self, control, newwidth, newheight):
		control.x = 5
		control.y = newheight - 133
		control.width = newwidth - 10

	## @brief Resize callback for guiGroundFrameSamples
	#  @param control The invoking GUI control object
	def guiGroundFrameSamplesResize(self, control, newwidth, newheight):
		control.x = 5
		control.y = newheight - 162
		control.width = newwidth - 10
	
	## @brief Resize callback for guiBlendSequence
	#  @param control The invoking GUI control object
	def guiBlendSequenceResize(self, control, newwidth, newheight):
		control.x = 10
		control.width = newwidth - 20
		control.y = 50

	## @brief Resize callback for guiBlendControlsBox
	#  @param control The invoking GUI control object
	def guiBlendControlsBoxResize(self, control, newwidth, newheight):
		control.x = 5
		control.y = 5
		control.width = newwidth - 10
		control.height = 50

	## @brief Resize callback for guiRefPoseTitle
	#  @param control The invoking GUI control object
	def guiRefPoseTitleResize(self, control, newwidth, newheight):
		control.x = 8
		control.y = 33


	## @brief Resize callback for guiRefPoseFrame
	#  @param control The invoking GUI control object
	def guiRefPoseFrameResize(self, control, newwidth, newheight):
		control.x = 8
		control.y = 8
		control.width = (newwidth) - 16

