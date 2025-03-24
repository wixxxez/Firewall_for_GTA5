# Firewall for GTA5 

This program implements a very simple logic. 
It enables or disables a firewall rule that is blocking the Rockstar servers for cloud saves using a hotkey.

You don't need to use the Ethernet glitch anymore for Cayo-Perico, Bogdan, or Clucking Bell. Just press a hotkey when the final cutscene begins. 

It works with every heist in GTA Online (Doomsday, Daimond Casino, Oskar Goodman, etc.)

# How it works: 
1. Start the heist. 
2. When the final cut-scene begins use a hotkey. You should see the following message: 
    - Firewall rule is enabled (green color). Which means that your firewall now blocking IP address of the Rockstar Cloud Server. 
3. Wait until the game load you to online session. If you receive the following message

    ```Save error! Rockastar server is temporary unavailible. Please try again later```
     - It's 
    expected behaviour, which means that everything is going as we planned. 
4. Load to singleplayer game. 
5. Disable rule. (Press hotkey). 
6. Load back to online session.  
7. Wait until game show you "SUCCESSFUL SAVE"


### Run code from source

Run cmd as an administrator 
Navigate to the directory containig this application


    cd C:\Users\vinew\OneDrive\Desktop\soft\GTA5_FirewallRule

    pip install keyboard
    
    python -m src.main


