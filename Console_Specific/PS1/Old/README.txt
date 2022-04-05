===== Old Method, Use the STR Subtitler Applier instead!! =====
==== Setup ====
  - Use "jPSXdec" to find the video files. Look for "STR" files.
    - You can hit "Select..." with the dropdown next to it set to "all Videos."
  - Select "avi" video format (this is just for subbing, compression doesn't matter) then hit "Save All Selected." Hit "Start" and wait for them all to export.
  - Change the selection to "Image sequence: png," change the output folder, then hit "Apply to all Videos." Hit "Save All Selected" then "Start" again.
  - When closing the tool, save the index file somewhere with your videos.
    - If you open an iso, it'll reinsert automatically later into that iso. To avoid this, extract the files first.

==== Subtitling ====
  - Add the subtitles in Movie Studio. Try to avoid the edges too much since CRTs might cut off.
  - When finished, hide the video track then render the video as a series of PNGs.
  - Check the output and verify they're transparent PNGs with only the subtitles.
  - Optional, delete the empty frames

==== Applying Subtitles ====
  - Run the "SrtSubtitleApplierFromMovieStudio.py" script.
    - Arguments are <raw frames> <subtitle png folder> <output dir>
    - Ex: <code>"C:\Users\yagen\Desktop\Translation Working\Tokyo Dungeon\Videos\PNG\STR" "C:\Users\yagen\Desktop\Translation Working\Tokyo Dungeon\Videos\Subtitles" "C:\Users\yagen\Desktop\Translation Working\Tokyo Dungeon\Videos\Rendered_Frames"</code>
  - Run the "SrtXmlGenerator.py" script
    - Arguments are <rendered frames folder> <output folder>
    - <code>"C:\Users\yagen\Desktop\Translation Working\Tokyo Dungeon\Videos\Rendered_Frames" "C:\Users\yagen\Desktop\Translation Working\Tokyo Dungeon\Videos"</code>

==== Inserting Subtitles ====
  - Open a command prompt and go to your jPSXdec folder
  - Arguments to the inserter are <code>java -jar jpsxdec.jar -x <index_file> -i <video number> -replaceframes <xml_file></code>
  - Ex: <code>java -jar jpsxdec.jar -x "C:\Users\yagen\Desktop\Translation Working\Tokyo Dungeon\Videos\index.idx" -i 2219 -replaceframes "C:\Users\yagen\Desktop\Translation Working\Tokyo Dungeon\Videos\SCENE01.STR.xml"</code>