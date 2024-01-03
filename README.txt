Tool to help cleaning the project.

It won't regenerate the visual studio project files yet due to unkown issues. Might fix in the future.

For this script to work:
1. Place the .py file in the root of your project;
2. Open a terminal;
3. If you don't have pyinstaller, install it: pip install pyinstaller
4. Run pyinstaller --onefile <NameOfThePythonScript.py>;
5. Delete the .spec file;
6. Move the .exe file from your dist folder into the root folder.

Now you can use the tool.

The tool was broken into 2 sub-tools: CR & Nuke.

CR stands for "Clean and Regenerate", which is all that it does. It's usuable, but you have to open the .uproject to rebuild the project and plugins.

Nuke.py does the same thing as CR, but after regenerating, does a clean build with UBT to reset all the build artifacts and then builds the project and plugins with UBT. The problem is that it still requires to build the "missing" modules, even though I've seen that UBT built them.

Will work on this feature in the future.

To generate the .exe file, make sure you have python installed and added in the env path variables + pyinstaller installed aswell.

Run the following command "pyinstaller --onefile <NameOfThePythonScript.py>" to generate the executable which would be in the root of the project in a folder called "dist". Cut & paste into the root of the project, delete the "dist" folder and also the .spec file as well, since we don't need that.