COMPILES DAVIS
15-112 Term Project by Jordan Reichgut
Carnegie Mellon University
Spring 2017

Compiles Davis is a tool for jazz musicians that simulates improvisation. It randomly generates, prints out, and plays back melodies over chord changes. The user can either choose from a list of 20 popular jazz standards with pre-programmed changes, or manually input the chord symbols.

The music opens in MuseScore (an open source music composition tool). Within MuseScore, the user can play back, edit, and save the music as a PDF.

Compiles Davis utilizes Music21, an open source Python module developed by MIT for musician programmers. Download links and installation instructions can be found at: http://web.mit.edu/music21/.

Compiles Davis requires MuseScore and Music21 to be installed in order to run properly. The Music21 master folder must be in the same directory as the CompilesDavis.py file.

To use the program, open and run CompilesDavis.py.

DESIGN

Compiles Davis is targeted toward jazz musicians. It can help them expand their vocabulary by generating “licks” (musical phrases). Plagiarism is accepted and encouraged in jazz, and musicians “quote” each other all the time. Anyone who uses this tool is encouraged to use the music it generates in their playing. 

I included a help screen to show the user the correct notation for each type of chord. Additionally, there are buttons below the grid labeled with chord symbols, and pressing one will add the correct suffix to a letter that has already been typed.

This was an original idea. There are similar tools that exist, but I didn’t model this project off any specific program. Compiles Davis combines my passions of jazz and coding into a practical tool that can be developed further in the future.