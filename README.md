# EDL-Compare
Compare the EDLs of 2 of your movies to see the difference!

Once a director sat down next to a young editor and decided to remix his whole movie on a whim. The only problem was the entire movie had already been exported and delivered to 3 different vendors across the globe!

Rather than assign this to a production coordinator and an intern, who would surely make mistakes, I solved the problem with python! This solution was faster and more accurate than human labor.


The goal was to create a spreadsheet that would summarize for the different vendors which shots got longer, which shots got shorter, etc. I did not bother to generalize or port into a CLI tool because I would need a director to screw up in the exact same way again for this to be useful. 

I chose to use .edl over .xml due to EDL's use of timecode. XML uses ticks and frame count, which is not ideal for communicating new in's and out's to vendors

So we had 3 data points: 
- EDL1: The original edit timeline (delivered to vendors)
- EDL2: The NEW edit timeline as an .edl (Director's new ideas)
- EDL3: The entire movie exported with handles as a control group

The script essentially creates a list of each shot from each of these EDLs, and it pulls timecode metadata from the .mov's, and compares them. It uses the data from EDL3 to get shot names (since we named them upon delivery to the vendors), and then it compares ins and outs from EDL1 and EDL2 and assigns them one of the following strings, and then delivers all data as a google sheet.

1) "Shot ______ Completely new shot added to timeline"
2) "Shot ______ Completely removed from timeline"
3) "Shot ______ had ___ frames added to head"
4) "Shot ______ had ___ frames removed from head"
5) "Shot ______ had ___ frames added to tail"
6) "Shot ______ had ___ frames removed from tail"


If you would like to use this on your own project, please message me! The variables are hard-coded into the code and can quickly be changed.
