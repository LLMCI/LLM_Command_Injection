import os
import shutil

def extract_py_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for dirpath, dirnames, filenames in os.walk(source_folder):
        for filename in filenames:
            if filename.endswith('.py'):
               
                subfolder_prefix = os.path.basename(dirpath)
                
                if os.path.abspath(dirpath) == os.path.abspath(source_folder):
                    prefixed_filename = filename
                else:
                    prefixed_filename = f"{subfolder_prefix}_{filename}"
                
                source_path = os.path.join(dirpath, filename)
                destination_path = os.path.join(destination_folder, prefixed_filename)
                
                unique_counter = 1
                while os.path.exists(destination_path):
                    destination_path = os.path.join(
                        destination_folder,
                        f"{subfolder_prefix}_{os.path.splitext(filename)[0]}_{unique_counter}{os.path.splitext(filename)[1]}"
                    )
                    unique_counter += 1

                shutil.copy(source_path, destination_path)


source_folder = "folder_path"
destination_folder = "folder_path"
extract_py_files(source_folder, destination_folder)



