import os

def find_files_with_methods(directory, methods):
    matched_files = {}

    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            try:
                with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for method in methods:
                        if method + '(' in content:
                            if filename not in matched_files:
                                matched_files[filename] = []
                            matched_files[filename].append(method)
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}. File: {filename} could not be read as UTF-8.")
                # Handle files that cannot be read in UTF-8 here, if necessary
                # For instance, log the error or try a different encoding

    return matched_files

def main():
    directory = 'folder_path'  
    methods_to_search = ['eval', 'exec', 'subprocess.call', 'subprocess.run', 'subprocess.Popen', 'subprocess.check_output', 'os.popen', 'os.system', 
                         'os.spawnl', 'os.spawnle', 'os.spawnlp', 'os.spawnlpe', 'os.spawnv', 'os.spawnve', 'os.spawnvp', 'os.spawnvpe', 'os.posix_spawn()', 
                         'os.posix_spawnp()', 'os.execl', 'os.execle', 'os.execlp', 'os.execlpe', 'os.execv', 'os.execve', 'os.execvp', 'os.execvpe' ]

    matched_files = find_files_with_methods(directory, methods_to_search)

    count=0
    for filename, methods in matched_files.items():
        print(f"File: {filename} has the methods: {', '.join(methods)}")
        count+=1
    print(count)

if __name__ == "__main__":
    main()

