# CEB HubMocap
Blender addon that uses modules to run mocap


## Modules
Currently it works with 4dhumans and planned to have GVHMR

[4d humans module](https://carlosedubarreto.gumroad.com/l/py_embed_4dhumans) (Paid)

### Free or discount
- **Bought CEB 4d Humans:** If you purchased CEB 4D Humans, contact me and I'll give you the 4d humans module for free.

- **Patreon:** If you are or were a Patreon supporter for **CEB Studios** , let me know and you'll get a full or partial discount (depending on the subscription tier and amount of time, like if you are subscribed to $1 tier for 2 months, you'll get $2 discount)


## Free alternative: Make the module yourself
To make a module you'll need to install the python packages using  python embedded.

It's more complicated than the usual python installation (but not that much), if enough people show interest I can instructions explaining how to do it, so you can be able to use the addon.

Instructions might change depending on the module, since it was needed to make the code to wrap all the dependencies into one folder (some projects like 4d humans uses the windows user folder to store some data, and I had to change the code.)

## What the addon does?
- Make it simple to install the module without touching code.
- Deal with the dependencies like downloading SMPL model that can't be bundled with the module (you'll need a registration from SMPL site to be able to download the file)
- Have a simple way to import the result animation in blender

## Steps to use
- Download the addon from the [Releases](https://github.com/carlosedubarreto/ceb_hubmocap/releases) page
- Install the addon
- download the desired module (or point to the path of the installation you did using python embedded)

### In the addon (for 4D Humans):
- Choose the module, that will show only the options of module installation and execution just for that module
- Select a folder to install the module (it will be remembered when you open blender again)
- Select the module zip file and press the "Start Unzip" button
- if you dont have a registration at the site SMPLify, choose the **Register** button to open the link of the site to register
- if you already have a registration, choose the button **Download** and inser your email and password (this is not stored, its only used to authenticate to SMPLify site to be able to download the zip file with the model needed)
- Press the **Download SMPL PKL** button and wait for it to finish
- Press **Setup SMPL** for the addon to place the model on the corret path

## Running a video
At the top of the addon you have a string box with a button that you can use to select the desired video (prefer to use mp4 videos) and press **Run**.

After finishing the process press the button **Update** to see how many character was detected on the video, and on the **Character** option you can select which one to load (if it has more than one) it is has only one, leave **Character** at = 1

Press the **Import Mocap** to load the result in blender.

Done.

## PS.:
Sorry for making the modules a paid product. I'm trying alternatives to make the coding of addons viable.