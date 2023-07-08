import zipfile

def compress_files_to_zip(file_map, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder_path, files in file_map.items():
            for file in files:
                file_path = folder_path + '/' + file
                zipf.write(file_path, arcname=file)

# Example usage
file_map = {
    '/path/to/folder1': ['file1.txt', 'file2.txt', 'file3.txt'],
    '/path/to/folder2': ['fileA.txt'],
    '/path/to/folder3': ['fileB.txt'],
}
zip_file_path = '/path/to/output.zip'
compress_files_to_zip(file_map, zip_file_path)
