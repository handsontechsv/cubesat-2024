import os

def get_file_name_without_extension(file_path):
    base_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(base_name)
    return file_name_without_extension

# Example usage:
file_path = '/path/to/your/file/example.txt'
result = get_file_name_without_extension(file_path)
print(result)
