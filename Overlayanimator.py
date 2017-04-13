from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi
import os
from ij.process import ImageConverter
from ij import IJ, WindowManager, ImagePlus

def Overlayer(ROIs, Title):
	""" Overlays ROIs, saves to .tif and animates aligned images to .gif """
	
	Source_Directory = "D:\\Image_Processing\\Virtualstacks\\Lif_Stack_Split_aligned_all"
	Destination_Directory = "D:\\Image_Processing\\Virtualstacks\\Overlays"
	gif_Directory = "D:\\Image_Processing\\Virtualstacks\\gifs\\"
	
	if not os.path.exists(Destination_Directory):
		os.makedirs(Destination_Directory) 
	if not os.path.exists(gif_Directory):
		os.makedirs(gif_Directory) 	
	
	rm = RoiManager().getInstance()
	total_rois = rm.getIndexes()

	# Removes artefact ROIs from ROI manager.
	for roi in total_rois:
		if roi not in ROIs:
			rm.select(roi)
			rm.runCommand("Delete")


	# Overlays ROI on aligned images, converts to 8-bit (for gif).
	for root, directories, filenames in os.walk(Source_Directory):
		for filename in filenames:
			imp = IJ.openImage(os.path.join(root, filename))	
			converter = ImageConverter(imp)
			converter.setDoScaling(True)
			converter.convertToGray8()
			rm.moveRoisToOverlay(imp)

			# Apply relevant (but enhanced) colors.
			if "C=0" in filename:
				IJ.run(imp, "Cyan Hot", "")
			elif "C=1" or "C=2" in filename:
				IJ.run(imp, "Yellow Hot", "")
								
			IJ.saveAs(imp, "Tiff", os.path.join(Destination_Directory, filename))

	# Opens overlaid images, saves as tiff stack.
	overlay_stack = IJ.run("Image Sequence...", "open="+Destination_Directory+
					" number=100 starting=0 increment=1 scale=100 file=.tif")
	
	IJ.saveAs(overlay_stack, "Tiff", os.path.join(gif_Directory+Title))

	# Animates tiff stack. 
	for root, directories, filenames in os.walk(gif_Directory):
		for filename in filenames:
			if Title in filename:
				# set=xx parameter controls gif speed.
				# for additional parameters run with macro recorder.
				gif = IJ.run("Animated Gif ... ", "set=20 filename="+(os.path.join(root, filename)))
				IJ.saveAs(gif, "Animated Gif...", os.path.join(gif_Directory+Title))

	# Close (because overlay_stack and gif are nonetype objects).
	imp = WindowManager.getCurrentImage()
	imp.close()
	
