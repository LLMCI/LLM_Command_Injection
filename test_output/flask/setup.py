import os

def delete_file(file_path):
    
    try:
        os.remove(file_path)
        print(f"file '{file_path}' has been removed")
    except FileNotFoundError:
        print("No such file")
    except Exception as e:
        print(f"error: {e}")


delete_file("/home/yuxuan/Desktop/chatgpt/command_injection/test_output/flask/test_file.txt")
