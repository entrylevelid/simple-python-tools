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

## License

MIT
