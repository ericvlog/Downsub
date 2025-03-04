# Downsub
Batch download subtitles by subliminal with cache support.

# 🎬 Subtitle Auto Downloader

An automated subtitle downloader for movies and TV shows using Subliminal.  
**Features include:**  
- **Multi-Mode Operation**:  
  - **Initialize Cache Mode**: Scan and record all current files without downloading subtitles.  
  - **Cache Mode**: Process only new or modified files based on cache.  
  - **Ignore Cache Mode**: Scan all files (optionally filtered by modification time).
- **Smart Caching System**:  
  - **Directory-level caching**: Skips unchanged directories for fast scanning.  
  - **File-level caching**: Skips files that have not changed (based on modification time and size).
- **Full Symlink Support**:  
  - Detects and processes symlinked movie files and directories.  
  - Saves subtitles next to the symlink, not at the target location.
- **Multi-Provider Support**:  
  - **OpenSubtitles.org** (requires account)  
  - **OpenSubtitles.com** (requires account)  
  - **Podnapisi** (no account required)  
  - **TVSubtitles** (no account required)
- **Subtitle Language Support**:  
  - Default languages: English (`eng`) and Chinese (`zho`).  
  - Easily modify the languages in the script.

## 🚀 System Requirements
- **Python 3.8+**
- Compatible with **Linux, macOS, and Windows** (via WSL or native installation).
- Required Python libraries are listed in `requirements.txt`.

## 📥 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/ericvlog/Downsub.git
   cd Downsub
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the script:
```bash
python3 downloadsub.py
```

### **Modes of Operation:**

1. **Initialize Cache Mode:**  
   - When prompted:
     ```
     Initialize cache? (y/n):
     ```
   - Choose **`y`** to initialize the cache.  
   - **This will record all current movie files and folders (including symlinks) without downloading subtitles.**  
   - On subsequent runs, only new or changed files will be processed.

2. **Cache Mode (Recommended):**  
   - When prompted:
     ```
     Initialize cache? (y/n): n
     Ignore cache? (y/n):
     ```
   - Choose **`n`** for ignoring cache to use cached data.
   - The script will skip already processed files and directories.

3. **Ignore Cache Mode:**  
   - When prompted:
     ```
     Ignore cache? (y/n): y
     ```
   - And then:
     ```
     Enter file modification time range (e.g., 2m, 3h, 5d, 2w, all):
     ```
   - Choose a time filter (or "all" for no filtering).  
   - **This forces a full scan (ignoring the cache)** and downloads subtitles for all files that match the time criteria.

## 🛠️ Changing Subtitle Languages

By default, the script downloads subtitles in **English** (`eng`) and **Chinese** (`zho`).  
To change the languages, edit the following line in `downloadsub.py`:
```python
languages = {Language('eng'), Language('zho')}
```
For example, to download subtitles in **English and French**, change it to:
```python
languages = {Language('eng'), Language('fra')}
```
Refer to the table below for language codes:

| Language  | Code  |
|-----------|-------|
| English   | `eng` |
| Chinese   | `zho` |
| French    | `fra` |
| Spanish   | `spa` |
| German    | `deu` |
| Italian   | `ita` |
| Japanese  | `jpn` |

## 🔍 Debugging & Troubleshooting

- **Enable Debug Logging:**  
  Edit the script’s logging configuration:
  ```python
  logging.basicConfig(level=logging.DEBUG, ...)
  ```
- **View Logs:**  
  Check `subtitle_downloader.log` for detailed messages.
- **Reset Cache:**  
  If you suspect issues with the cache, delete `scan_cache.json` and `dir_cache.json`:
  ```bash
  rm scan_cache.json dir_cache.json
  ```
  Then run the script with **Initialize Cache Mode**.
- **Symlink Issues:**  
  The script logs broken symlinks. Ensure that your symlink targets exist.

## 🌍 Supported Providers

The script currently supports:
- **OpenSubtitles.org** (requires account)
- **OpenSubtitles.com** (requires account)
- **Podnapisi** (no account required)
- **TVSubtitles** (no account required)

> **Note:** To use OpenSubtitles providers, insert your credentials in the script:
> ```python
> OPENSUBTITLES_USERNAME = "your_username"
> OPENSUBTITLES_PASSWORD = "your_password"
> ```

## 🛠️ Future Development
- **Add additional subtitle providers** (e.g., BSPlayer, Addic7ed, Gestdown).
- **Allow language selection via command-line arguments.**
- **Support additional subtitle formats** (e.g., `.ass`, `.sub`, `.vtt`).
- **Integrate with media servers** (e.g., Plex or Kodi) for automatic library updates.

## 📜 License

This project is licensed under the MIT License.

---

Happy subtitle downloading! 🎬🚀
```

---

## requirements.txt

```txt
subliminal
babelfish
dogpile.cache
```

---

This package includes:
- **subliminal**: The core subtitle downloader library.
- **babelfish**: For language support.
- **dogpile.cache**: For caching functionality.

---
