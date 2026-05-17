# Simple Python Tools

A collection of 23 simple Python tools covering networking, file management, security, multimedia, and more. Each tool lives in its own folder with a dedicated `requirements.txt`.

## Requirements

- Python 3.8+
- Install dependencies per tool: `pip install -r requirements.txt`

---

## Tools

| # | Tool | Description | Dependencies |
|---|------|-------------|--------------|
| 001 | [DNS Lookup](#001-dns-lookup) | Resolve domain names to IP addresses | stdlib only |
| 002 | [Encryption & Decryption](#002-encryption--decryption) | Encrypt and decrypt text files using Fernet | `cryptography` |
| 003 | [File Organizer](#003-file-organizer) | Organize files in a folder by type into subfolders | `rich`, `InquirerPy` |
| 004 | [Ping Tool](#004-ping-tool) | Ping a host and check connectivity | stdlib only |
| 005 | [Port Scanner](#005-port-scanner) | Scan common ports on a target host | stdlib only |
| 006 | [QR Generator](#006-qr-generator) | Generate QR codes from text or URLs | `qrcode`, `Pillow` |
| 007 | [Reminder](#007-reminder) | Set timed desktop notification reminders | `plyer` |
| 008 | [Speedtest](#008-speedtest) | Test internet download/upload speed and ping | `speedtest-cli` |
| 009 | [Steganography](#009-steganography) | Hide and extract secret messages inside images | `Pillow` |
| 010 | [WHOIS](#010-whois) | Query WHOIS information for a domain | `python-whois` |
| 011 | [YouTube Downloader](#011-youtube-downloader) | Download YouTube videos via GUI | `yt-dlp` |
| 012 | [Folder Activity](#012-folder-activity) | Monitor a folder for file changes in real time | `watchdog`, `colorama` |
| 013 | [WiFi Password Viewer](#013-wifi-password-viewer) | View saved WiFi passwords on Windows | stdlib only |
| 014 | [Hash Generator](#014-hash-generator) | Generate MD5, SHA1, SHA256, SHA512 hashes | stdlib only |
| 015 | [Background Remover](#015-background-remover) | Remove image backgrounds automatically | `rembg`, `Pillow` |
| 016 | [XLS to SQLite](#016-xls-to-sqlite) | Convert Excel files to a SQLite database | `pandas`, `openpyxl` |
| 017 | [File Deduplicator](#017-file-deduplicator) | Find and delete duplicate files using SHA-256 | `rich`, `InquirerPy` |
| 018 | [PDF Extractor](#018-pdf-extractor) | Extract text from PDF files | `PyPDF2` |
| 019 | [Currency Converter](#019-currency-converter) | Convert currencies using live exchange rates | `requests`, `streamlit` |
| 020 | [Text to Speech](#020-text-to-speech) | Convert text to speech via GUI | `pyttsx3` |
| 021 | [Image Compressor](#021-image-compressor) | Compress images while preserving quality | `Pillow` |
| 022 | [Mini Chatbot](#022-mini-chatbot) | Simple rule-based chatbot in the terminal | stdlib only |
| 023 | [IP Address Tracker](#023-ip-address-tracker) | Look up geolocation info for an IP address | `requests`, `colorama` |

---

## Usage

### 001 DNS Lookup
Resolves a domain name to its IP address using Python's `socket` module.
```bash
cd 001_DNS_Lookup
python 001_DNS_Lookup.py
```

### 002 Encryption & Decryption
Encrypts a file using Fernet symmetric encryption. Run the encryptor first to generate `secret.key`, then decrypt with the decryptor.
```bash
cd 002_Encryption_and_Decryption
pip install -r requirements.txt
python text_encryption.py   # encrypts → saves secret.key + encrypted_data.txt
python text_decryption.py   # decrypts using secret.key
```

### 003 File Organizer
Scans a folder and moves files into categorized subfolders (Images, Videos, Documents, etc.) with a confirmation prompt before making changes.
```bash
cd 003_File_Organizer
pip install -r requirements.txt
python 003_File_Organizer.py
```

### 004 Ping Tool
Pings a hostname or IP address and reports connectivity.
```bash
cd 004_Ping_tool
python 004_Ping_tool.py
```

### 005 Port Scanner
Scans a set of common ports on a target host and reports which are open.
```bash
cd 005_Port_Scanner
python 005_Port_Scanner.py
```

### 006 QR Generator
Generates a QR code image (`qrcode.png`) from any text or URL you enter.
```bash
cd 006_QR_Generator
pip install -r requirements.txt
python 006_QR_Generator.py
```

### 007 Reminder
Set a reminder with a custom message and delay (in seconds). A desktop notification pops up when the time is up.
```bash
cd 007_Reminder
pip install -r requirements.txt
python 007_Reminder.py
```

### 008 Speedtest
Measures your internet download speed, upload speed, and ping.
```bash
cd 008_Speedtest
pip install -r requirements.txt
python 008_Speedtest.py
```

### 009 Steganography
Hides a secret message inside a PNG image by modifying pixel LSBs, and extracts it back.
```bash
cd 009_Steganography
pip install -r requirements.txt
python steg_encode.py   # encodes message into image.png → encoded_image.png
python steg_decode.py   # decodes message from encoded_image.png
```

### 010 WHOIS
Queries WHOIS registration data for a domain name.
```bash
cd 010_Whois
pip install -r requirements.txt
python 010_Whois.py
```

### 011 YouTube Downloader
GUI tool to download YouTube videos by pasting a URL.
```bash
cd 011_Youtube_Downloader
pip install -r requirements.txt
python 011_Youtube_Downloader.py
```

### 012 Folder Activity
Watches a folder for any file creation, modification, or deletion events and logs them in real time.
```bash
cd 012_Folder_Activity
pip install -r requirements.txt
python 012_Folder_Activity.py
```
> Edit `folder_to_watch` in the script to point to your target folder.

### 013 WiFi Password Viewer
Lists all saved WiFi profiles on Windows and displays their passwords.
```bash
cd 013_Wifi_Password_Viewer
python 013_Wifi_Password_Viewer.py
```
> Windows only. Run as Administrator if passwords are not displayed.

### 014 Hash Generator
Generates a cryptographic hash of any text input. Supports MD5, SHA1, SHA256, and SHA512.
```bash
cd 014_Hash_Generator
python 014_Hash_Generator.py
```

### 015 Background Remover
Automatically removes the background from an image using AI (rembg).
```bash
cd 015_Background_Remover
pip install -r requirements.txt
python 015_Background_Remover.py
```
> Place your image as `avatar.png` in the folder. Output is saved as `avatar-after.png`. The AI model (~170 MB) is downloaded on first run.

### 016 XLS to SQLite
Reads an Excel file and imports it into a SQLite database table.
```bash
cd 016_xls_to_sqlite
pip install -r requirements.txt
python 016_xls_to_sqlite.py
```
> Edit the filename and sheet name variables in the script to match your file.

### 017 File Deduplicator
Scans a folder for duplicate files using SHA-256 hashing, shows them in a paginated list, and lets you select which ones to delete.
```bash
cd 017_File_Deduplicator
pip install -r requirements.txt
python 017_File_Deduplicator.py
```

### 018 PDF Extractor
Extracts all text from a PDF file and optionally saves it to a `.txt` file. Includes a file picker dialog.
```bash
cd 018_Pdf_Extractor
pip install -r requirements.txt
python 018_Pdf_Extractor.py
```

### 019 Currency Converter
Converts between currencies using live rates from the Open Exchange Rates API. Available as both a CLI script and a Streamlit web app.
```bash
cd 019_Currency_Converter
pip install -r requirements.txt

python 019_Currency_Converter.py   # CLI version
streamlit run app_st.py            # web app version
```

### 020 Text to Speech
GUI app that converts typed text to spoken audio using the system's TTS engine.
```bash
cd 020_Text_to_Speech
pip install -r requirements.txt
python 020_Text_to_Speech.py
```

### 021 Image Compressor
Compresses one or more images to reduce file size. Opens a file picker to select images.
```bash
cd 021_Image_Compressor
pip install -r requirements.txt
python 021_Image_Compressor.py
```

### 022 Mini Chatbot
A simple rule-based chatbot in the terminal that responds to basic greetings and questions.
```bash
cd 022_Mini-Chatbot
python app.py
```

### 023 IP Address Tracker
Looks up geolocation information (country, city, ISP, coordinates, etc.) for any public IP address.
```bash
cd 023_IP_Address_Tracker
pip install -r requirements.txt
python main.py
```

---

## License

MIT
