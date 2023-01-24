import os, sys, shutil, time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

"""
    Automates file organization
    It can either be run manually or setup on startup.

    Usage in terminal:
        > python organize.py <directory_to_organize>
"""

TARGET_PATH = sys.argv[1]

# Change directory names or extension types based on your preference
# Omit the . when adding extension types
SUB_DIRS = {
	"images": ["jpg", "jpeg", "jpe", "jif", "jfif", "jfi", "png", "gif", "webp", "dng", "tiff", "tif", "psd", "raw", "arw", "k25", "bmp", "svg", "svgz", "ai", "eps", "ico"],
	"code": ["js", "jsx", "ts", "tsx", "html", "css", "htm", "json", "md", "mdx", "py", "php", "yaml", "sh", "code-workspace"],
	"documents": ["doc", "docx", "odt", "xls", "xlsx", "ppt", "pptx", "pdf", "pdfk", "csv"],
	"archives": ["7z", "apk", "deb", "dmg", "ear", "gca", "genozip", "pak", "partimg", "paq6", "paq7", "paq8", "pkg", "rar", "rpm", "gz", "tgz", "bz2", "tbz2", "tlz", "txz", "iso", "tar", "targz", "xz", "z", "zip", "zipz"],
    "databases": ["db", "dbf", "sql", "xml"],
    "exec": ["exe", "bat", "bin", "apk", "jar", "ini"],
	"text": ["txt" "log"],
	"font": ["fnt", "fon", "otf", "ttf", "woff", "woff2"],
	"audio": ["mp3", "webm"],
    "video": ["mp4","srt","mkv","3gp"],
    "trash": ["part"]
}

def move_file(file_name, dest_dir):
    try:
        dir_location = os.path.join(TARGET_PATH, dest_dir)
        original_filename = file_name
        file_name = os.path.basename(file_name)

        if not os.path.exists(dir_location):
            os.mkdir(dir_location)
        
        if os.path.exists(os.path.join(dir_location, file_name)):
            counter = 1
            name = os.path.basename(file_name).split(".")[0]
            ext = os.path.basename(file_name).split(".")[-1]

            while os.path.exists(os.path.join(dir_location, f"{name}{str(counter)}.{ext}")):
                counter += 1
            file_name = f"{name} ({str(counter)}).{ext}"

        shutil.move(original_filename,os.path.join(dir_location, file_name))

    # To avoid permission errors when downloading larger files and wait for the download to finish
    # Also avoids having scattered .part files while download is in progress
    except:
        time.sleep(5)
        organize_files()

def organize_files(event = None):
    file_types = { file_type: dir_name for dir_name,file_types in SUB_DIRS.items() for file_type in file_types }

    files = [file for file in os.listdir(TARGET_PATH) if os.path.isfile(os.path.join(TARGET_PATH, file))]
    dirs = [di for di in os.listdir(TARGET_PATH) if os.path.isdir(os.path.join(TARGET_PATH, di))]

    # Move files
    for file_name in files:
        ext = file_name.split(".")[-1].lower()
        
        if ext in file_types:
            move_file(os.path.join(TARGET_PATH, file_name), file_types[ext])
        # If file does not have set extensions, move to "misc" folder
        else:
            move_file(os.path.join(TARGET_PATH, file_name), "misc")
    
    # Remove trash directory, recursive
    if os.path.isdir(os.path.join(TARGET_PATH, "trash")):
        shutil.rmtree(os.path.join(TARGET_PATH, "trash"))
                

if __name__ == "__main__":    
    event_handler = PatternMatchingEventHandler(patterns = "*", ignore_patterns = "", ignore_directories = True, case_sensitive = True)                    
    event_handler.on_created = organize_files
    event_handler.on_modified = organize_files
    
    observer = Observer()
    observer.schedule(event_handler, TARGET_PATH, recursive = False)

    observer.start()
    print("Organizer Start")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
