# CEB HubMocap
Blender addon that uses modules to run mocap


## Modules
The modules are files with python embeded that is fully installed with everything needed for the code to run (that is why there are modules for each code, since they need different library)

- [4d humans module](https://carlosedubarreto.gumroad.com/l/py_embed_4dhumans) (Paid)
- [GVHMR](https://carlosedubarreto.gumroad.com/l/py_embed_gvhmr) (Paid)
- [PromptHMR](https://carlosedubarreto.gumroad.com/l/py_embed_prompthmr) (Paid)
- [HaMeR](https://carlosedubarreto.gumroad.com/l/py_embed_hamer) (Paid)


### Free or discount
- **Bought CEB 4d Humans:** If you purchased CEB 4D Humans, contact me and I'll give you the 4d humans module for free.

- **Patreon:** If you are or were a Patreon supporter for **CEB Studios** , let me know and you'll get a full or partial discount (depending on the subscription tier and amount of time, like if you are subscribed to $1 tier for 2 months, you'll get $2 discount)


## Free alternative: Make the module yourself
To make a module you'll need to install the python packages using  python embeded.

It's more complicated than the usual python installation (but not that much), if enough people show interest I can share more information explaining how to do it, so you can be able to use the addon.

Instructions might change depending on the module, since it was needed to make the code to wrap all the dependencies into one folder (some projects like 4d humans uses the windows user folder to store some data, and I had to change the code.)

## What the addon does?
- Make it simple to install the module without touching code.
- Deal with the dependencies like downloading SMPL model that can't be bundled with the module (you'll need a registration from SMPL site to be able to download the file)
- Have a simple way to import the result animation in blender

## Steps to use
- Download the addon from the [Releases](https://github.com/carlosedubarreto/ceb_hubmocap/releases) page
- Install the addon
- download the desired module (or point to the path of the installation you did using python embedded)

### GVHMR
Watch the tutorial on this link https://youtu.be/32qywnynWNA


### 4D Humans 
Video Tutorial: https://www.youtube.com/watch?v=LVBLkBfqpek

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

### PromptHMR and HaMeR:
Watch the tutorial https://youtu.be/Umgay5PUMe0?si=fh6TeUyafi62cFSH its based on CEB HubMocap 0.04

### HaMeR:
More updated information on how to install, based on CEB HubMocap 0.05 https://youtu.be/ruM9yXLBUQY?si=mxJZkXvnzx6ZOFje

## Troubleshooting:
- Its possible that you need Microsoft C++ redistributable to be installed. It will show on the blender console an error with the link  https://aka.ms/vs/16/release/vc_redist.x64.exe If you got this error, you just need to install this file and run again
- On my vistual machine, I was having a problem where it couldnt download the file https://download.pytorch.org/models/resnet50-19c8e357.pth In this case, take a look on the error in the blender console to see where you should save the file. After saving the file there, please run again, now it should work.



## PS.:
Sorry for making the modules a paid product. I'm trying alternatives to make the coding of addons viable.