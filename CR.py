import os
import shutil
import subprocess
import datetime

# Function to write to a log file
def log_message(message):
    with open("script_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")
        print(message)

def find_uproject_file():
    """Find a .uproject file in the current directory."""
    for file in os.listdir(os.getcwd()):
        if file.endswith(".uproject"):
            return file
    return None

def folder_exists(folder_path):
    """Check if a folder exists."""
    return os.path.exists(folder_path)

def delete_folder(folder_path):
    """Delete a folder if it exists."""
    if folder_exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted folder: {folder_path}")

def check_folders_exist(folder_list):
    """Check if any folders in the given list exist."""
    return any(folder_exists(folder) for folder in folder_list)

def delete_plugin_folders(plugin_folder):
    """Delete specific folders in each plugin subfolder."""
    for plugin in os.listdir(plugin_folder):
        plugin_path = os.path.join(plugin_folder, plugin)
        if os.path.isdir(plugin_path):
            # Folders to delete in each plugin
            for folder_name in ["Binaries", "Intermediate"]:
                delete_folder(os.path.join(plugin_path, folder_name))

    """Generate Visual Studio project files for an Unreal Engine project."""
def generate_vs_project(uproject_path):
    cmd = 'UnrealVersionSelector.exe /projectfiles "' + uproject_path + '"'
    print("Running command: " + cmd)
    try:
        subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Generated Visual Studio project files.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate Visual Studio project files: {e}")
        print("Error output: " + e.stderr.decode())

def clean_and_build_unreal_project(full_uproject_path, project_name, build_configuration="Development", platform="Win64"):
    """
    Rebuild the Unreal Engine project using UnrealBuildTool.
    :param full_uproject_path: Full path to the .uproject file.
    :param project_name: Name of the Unreal project (without .uproject extension).
    :param build_configuration: Build configuration (e.g., Development, Shipping).
    :param platform: Target platform (e.g., Win64, Win32).
    """
    # Command to clean and rebuild the project
    cmd_clean = f'UnrealBuildTool.exe -clean {project_name} {platform} {build_configuration} -project="{full_uproject_path}" -waitmutex'
    cmd_build = f'UnrealBuildTool.exe {project_name} {platform} {build_configuration} -project="{full_uproject_path}" -waitmutex'

    # Status 
    cmd_clean_status = False
    cmd_build_status = False
    
    # Run the clean command
    print("Running clean command: " + cmd_clean)
    try:
        subprocess.run(cmd_clean, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Successfully cleaned the Unreal Engine project.")
        cmd_clean_status = True
    except subprocess.CalledProcessError as e:
        print(f"Failed to clean Unreal Engine project: {e}")
        print("Error output: " + e.stderr.decode())

    # Run the build command
    print("Running build command: " + cmd_build)
    try:
        subprocess.run(cmd_build, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Successfully rebuilt the Unreal Engine project.")
        cmd_build_status = True
    except subprocess.CalledProcessError as e:
        print(f"Failed to rebuild Unreal Engine project: {e}")
        print("Error output: " + e.stderr.decode())

    return cmd_clean_status and cmd_build_status


def main():
    root_folders = [os.path.join(os.getcwd(), folder) for folder in ["Binaries", "Intermediate", "Saved"]]
    plugins_folder = os.path.join(os.getcwd(), "Plugins")

    # Check if root or plugin folders exist before deleting
    root_folders_exist = check_folders_exist(root_folders)
    plugins_folder_exist = os.path.exists(plugins_folder)

    # Delete root folders
    for folder in root_folders:
        delete_folder(folder)

    # Delete plugin folders
    if plugins_folder_exist:
        delete_plugin_folders(plugins_folder)

    # Generate VS project files
    # getting the full path of the .uproject file, if exists
    project_root_path = os.getcwd()
    uproject_file = find_uproject_file()

    if uproject_file:
        full_uproject_path = os.path.join(project_root_path, uproject_file)
        project_name = os.path.splitext(uproject_file)[0]
        print("Found .uproject file:" + uproject_file)
        print("Full path to .uproject file:" + full_uproject_path)
        print("Project name: " + project_name)
    else:
        print("No .uproject file found.")

    #build_status = False

    if root_folders_exist or plugins_folder_exist:
        if os.path.exists(uproject_file):
            generate_vs_project(full_uproject_path)
            #build_status = clean_and_build_unreal_project(full_uproject_path, project_name)
        else:
            print(f"{uproject_file} not found, skipping project generation.")

    #print("Project cleaned and built with status: " + str(build_status))
    print("Script ended.")

if __name__ == "__main__":
    main()