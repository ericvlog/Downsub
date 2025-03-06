import os
import sys
import logging
import json
from babelfish import Language
from subliminal import download_best_subtitles, scan_video
from subliminal.cache import region

# Configure global in-memory cache for subliminal
region.configure("dogpile.cache.memory")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("subtitle_downloader.log"),
        logging.StreamHandler()
    ]
)

# OpenSubtitles Account (insert your credentials here if needed)
OPENSUBTITLES_USERNAME = ""
OPENSUBTITLES_PASSWORD = ""

# Cache filenames
FILE_CACHE_FILENAME = "scan_cache.json"
DIR_CACHE_FILENAME = "dir_cache.json"

def load_cache(filename):
    """Load cache from a JSON file."""
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load cache from {filename}: {e}")
    return {}

def save_cache(cache, filename):
    """Save cache to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    except Exception as e:
        logging.error(f"Failed to save cache to {filename}: {e}")

def scan_directory(dir_path, dir_cache, file_cache, ignore_dir_cache=False):
    """
    Recursively scan the directory while following symlinks for movie files.
    Uses a simple directory modification time to decide if the folder changed.
    """
    files_found = []
    current_dir_sig = os.path.getmtime(dir_path)
    cached_dir_sig = dir_cache.get(dir_path)
    
    if not ignore_dir_cache and cached_dir_sig and cached_dir_sig == current_dir_sig:
        logging.info(f"📂 Skipping unchanged directory: {dir_path}")
        return files_found
    
    dir_cache[dir_path] = current_dir_sig

    try:
        with os.scandir(dir_path) as it:
            for entry in it:
                full_path = entry.path

                if entry.is_symlink():
                    real_path = os.path.realpath(entry.path)
                    logging.info(f"🔗 Detected symlink: {entry.path} -> {real_path}")

                if entry.is_dir(follow_symlinks=True):
                    files_found.extend(scan_directory(entry.path, dir_cache, file_cache, ignore_dir_cache))
                elif entry.is_file(follow_symlinks=True) and entry.name.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                    try:
                        stat_info = os.stat(full_path, follow_symlinks=False)
                        file_cache[full_path] = {"mod_time": stat_info.st_mtime, "size": stat_info.st_size}
                        files_found.append(full_path)
                        logging.info(f"🎥 Found file: {full_path}")
                    except FileNotFoundError:
                        logging.warning(f"⚠️ Broken symlink, file not found: {entry.path}")
    except Exception as e:
        logging.error(f"🚨 Error scanning directory {dir_path}: {e}")

    return files_found

def download_subtitles(files):
    """Download subtitles for a list of files."""
    if not files:
        logging.info("✅ No files to process.")
        return

    languages = {Language('eng'), Language('zho')}
    os.environ['SUBLIMINAL_USER_AGENT'] = 'SubDownloader/1.0 (example@example.com)'

    providers = ['opensubtitles', 'opensubtitlescom', 'podnapisi', 'tvsubtitles']
    videos = []
    
    for f in files:
        try:
            video = scan_video(f)
            videos.append((video, f))
        except ValueError as e:
            logging.error(f"⚠️ Could not parse file: {f} - {e}")

    if not videos:
        logging.warning("❌ No valid video files for subtitle download.")
        return

    try:
        subtitles = download_best_subtitles([v[0] for v in videos], languages=languages, providers=providers)
        for video, original_path in videos:
            subs = subtitles.get(video, [])
            for sub in subs:
                sub_path = os.path.splitext(original_path)[0] + f'.{sub.language}.srt'
                with open(sub_path, 'wb') as f:
                    f.write(sub.content)
                logging.info(f"📥 Downloaded subtitle: {sub_path}")
    except Exception as e:
        logging.error(f"🚨 Subtitle download failed: {e}")

def main():
    folder_path = input("Enter movie folder path: ").strip()
    folder_path = os.path.expanduser(folder_path)
    if not os.path.isdir(folder_path):
        logging.error("❌ Invalid folder path.")
        return

    # Initialize cache handling
    init_cache_input = input("Initialize cache? (y/n): ").strip().lower()
    if init_cache_input == "y":
        logging.info("🔄 Initializing cache: Recording all current files and folders...")
        dir_cache = load_cache(DIR_CACHE_FILENAME)
        file_cache = load_cache(FILE_CACHE_FILENAME)
        scan_directory(folder_path, dir_cache, file_cache, ignore_dir_cache=True)
        save_cache(dir_cache, DIR_CACHE_FILENAME)
        save_cache(file_cache, FILE_CACHE_FILENAME)
        logging.info("✅ Cache initialization complete.")
        return

    ignore_cache = input("Ignore cache? (y/n): ").strip().lower() == 'y'
    file_cache = {} if ignore_cache else load_cache(FILE_CACHE_FILENAME)
    dir_cache = {} if ignore_cache else load_cache(DIR_CACHE_FILENAME)
    
    files_to_process = scan_directory(folder_path, dir_cache, file_cache, ignore_dir_cache=ignore_cache)
    logging.info(f"🔎 Found {len(files_to_process)} files to process.")
    
    download_subtitles(files_to_process)

    if not ignore_cache:
        save_cache(file_cache, FILE_CACHE_FILENAME)
        save_cache(dir_cache, DIR_CACHE_FILENAME)

if __name__ == "__main__":
    main()
