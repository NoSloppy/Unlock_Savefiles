# Unlock_Savefiles
Make ProffieOS save files user-friendly for editing.

ProffieOS saves .ini files to the SD card in a format that can be tricky to edit afterwards.  
This application is built on on python script that creates a user-friendly version of the .ini that can be edited in any text editor.  
This works for any .ini ProffieOS saves (presets, global, curstate, gestures).  


Go to the Releases on the right side of the repo page, choose the latest, then click the .zip file to download.  
The .zip file contains:
 - MacOS .app
- Windows .exe
- Linux executable

Choose your flavor.

Run Unlock_Savefiles and you get prompted to choose the .ini file you are looking to make edits to.  
It creates a version without all of the hex “in the way”.  

The resulting .ini file is the one you want.  
The previous version is renamed .bak, and there’s a .old version of the tmp file.  

Please let me know if there’s any issues.  
*Note** MacOS first run only - Right-click and choose Open, then confirm you want to open it.  
It'll complain that I'm an "Unknown Developer" if you try to open normally by double clicking the .app.  
