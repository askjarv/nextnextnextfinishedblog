---
title: "Missing folder in Outlook"
date: 2011-03-03
categories: 
  - "microsoft-office"
tags: 
  - "mailbox"
  - "office-2003"
  - "office-2007"
  - "office-2010"
  - "ost"
---

Missing Folder in Outlook (item may show in other Outlook sessions, or Outlook Web Access, but doesn't show in Outlook).

This normally happens when your local cache has become corrupt- you can “repair” it by deleting it and recreating it:

1. Quit Outlook, if it is running. Quit Lync/OCS client if running/any apps which access Outlook.
2. From the **Start** menu, choose **Run**.
3. In the Run window, type this path in the **Open** box and click OK: "%APPDATA%\\Microsoft\\Outlook\\" To find the exact path, follow the steps above to get to **Offline Folder File Settings** (steps 1-4 for Outlook 2002/2003/2007/2010, or steps 1-3 for Outlook 2000). You can see the .ost file location in the **File** box. You may want to copy and paste that information in the Run window for accuracy and ease.
4. In the Explorer window, locate the .ost file to be deleted. Select it and press DELETE on your keyboard or click the Delete icon on the toolbar.
5. Open up Outlook again
6. In Outlook 2007: Open the **Tools** menu. In Outlook 2010: Open the **File** tab on the Ribbon, click **Info**, and choose **Account Settings.**
7. Click **Account Settings**, then double-click **Microsoft Exchange**.
8. Click **More Settings**.
9. Click the **Advanced** tab, then click **Offline Folder File Settings**.
10. In the **File** box, type the path to the file that you want to use as the .ost file and click **OK**. The default name is **Outlook.ost**. If this file already exists, you will be prompted for a new name.If you see this message, click **OK**: _"<path> <filename>.ost could not be found. Would you like to create it?"_ (_<path>_ represents the path to the .ost file and _<filename>_ represents the name of the .ost file.)
     
     \[caption id="attachment\_23" align="alignnone" width="300" caption="Screenshot- Offline Folder File Settings"\]![Screenshot- Offline Folder File Settings](images/1.jpg "Screenshot - OST")\[/caption\]
11. Click **OK**, **Next**, and then click **Finish**. **Note**: Outlook must be connected to the Exchange server for the initial creation and synchronization of the Offline Folder file.
