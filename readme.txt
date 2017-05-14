COMPILES DAVIS
15-112 Term Project by Jordan Reichgut
Spring 2017

Compiles Davis is a tool for jazz musicians that simulates improvisation. It randomly generates, prints out, and plays back a melody over a set of chord changes. The user can either choose from a list of 20 popular jazz standards whose changes are pre-programmed, or manually input the chord symbols.

The music opens in MuseScore, and open source music composition tool. Within MuseScore, the user can play back, edit, and save the music as a PDF.

Compiles Davis makes use of Music21, an open source Python module developed by MIT for musician programmers. Download links and installation instructions can be found here: http://web.mit.edu/music21/.

Compiles Davis requires MuseScore and music21 to be installed in order to run properly. The music21 master folder must be in the same directory as the Python file using it.

To run the program, open tp.py.

DESIGN

Compiles Davis is targeted toward jazz musicians. It helps them expand their vocabulary by generating catchy “licks” (musical phrases). Plagiarism is commonplace in jazz, and musicians quote each other in their solos all the time. Anyone who uses this tool is encouraged to memorize music it generates and incorporate it in their playing. 

I included a help screen to show the user the correct notation for each type of chord. Additionally, there are buttons below the grid labeled with chord symbols, and pressing one will add the correct suffix to a letter that has already been typed.

This was an original idea. There are similar tools that exist, but I didn’t model this project off anything. Compiles Davis combines my passions of jazz and coding into a practical tool that can be improved in the future.


