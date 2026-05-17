import os
import shutil
import logging
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from InquirerPy import prompt

console = Console()

# Setup logging
logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuration with expanded extension map
extension_map = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".ico", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv", ".rtf", ".odt"],
    "Software": [".exe", ".msi", ".dmg", ".apk", ".bat", ".sh"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb", ".go", ".ts"],
    "Text": [".md", ".log", ".ini", ".json", ".xml", ".yaml", ".yml"]
}
others_folder = "Others"

# Function to handle file naming conflicts
def get_unique_filename(dest_path):
    dest_path = Path(dest_path)
    base, ext = dest_path.stem, dest_path.suffix
    counter = 1
    while dest_path.exists():
        dest_path = dest_path.with_name(f"{base}_{counter}{ext}")
        counter += 1
    return str(dest_path)

# Function to display header
def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    title_text = Text("FILE ORGANIZER", style="bold cyan", justify="center")
    subtitle = Text("A tool to organize files by extension", style="green", justify="center")
    header_panel = Panel(
        Text.assemble(title_text, "\n", subtitle),
        border_style="blue",
        box=box.ROUNDED,
        padding=(1, 4)
    )
    console.print(header_panel)

# Function to organize files
def organize_files(source_folder):
    source_folder = Path(source_folder)
    stats = {folder: 0 for folder in list(extension_map.keys()) + [others_folder]}
    stats["errors"] = 0
    
    # Validate source folder
    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Source folder {source_folder} does not exist or is not a directory")
        console.print(f"❌ Source folder {source_folder} does not exist or is not a directory", style="bold red")
        return stats

    # Create folders
    for folder in list(extension_map.keys()) + [others_folder]:
        (source_folder / folder).mkdir(exist_ok=True)

    # Process files
    table = Table(box=box.ROUNDED, title="[bold cyan]Files Organized[/bold cyan]")
    table.add_column("File", style="bold yellow")
    table.add_column("Destination", style="green")
    table.add_column("Status", style="white")

    for file_path in source_folder.iterdir():
        if file_path.is_file():
            moved = False
            for folder, extensions in extension_map.items():
                if file_path.suffix.lower() in extensions:
                    dest_folder = source_folder / folder
                    dest_path = get_unique_filename(dest_folder / file_path.name)
                    try:
                        shutil.move(str(file_path), dest_path)
                        logging.info(f"Moved {file_path.name} to {folder}")
                        table.add_row(file_path.name, folder, "✅ Success")
                        stats[folder] += 1
                    except (PermissionError, OSError) as e:
                        logging.error(f"Error moving {file_path.name}: {e}")
                        table.add_row(file_path.name, folder, f"❌ Error: {e}")
                        stats["errors"] += 1
                    moved = True
                    break
            if not moved:
                dest_folder = source_folder / others_folder
                dest_path = get_unique_filename(dest_folder / file_path.name)
                try:
                    shutil.move(str(file_path), dest_path)
                    logging.info(f"Moved {file_path.name} to {others_folder}")
                    table.add_row(file_path.name, others_folder, "✅ Success")
                    stats[others_folder] += 1
                except (PermissionError, OSError) as e:
                    logging.error(f"Error moving {file_path.name}: {e}")
                    table.add_row(file_path.name, others_folder, f"❌ Error: {e}")
                    stats["errors"] += 1

    console.print(table)
    return stats

# Function to display statistics
def display_statistics(stats):
    stats_table = Table(box=box.ROUNDED)
    stats_table.add_column("Category", style="bold cyan")
    stats_table.add_column("Files Moved", style="yellow")
    
    for folder, count in stats.items():
        if folder != "errors":
            stats_table.add_row(folder, str(count))
    stats_table.add_row("Errors", str(stats["errors"]))
    
    stats_panel = Panel(
        stats_table,
        title="[bold green]Organization Statistics[/]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2),
        width=50
    )
    
    console.print(stats_panel)

# Function to select folder and run organizer
def select_folder():
    print_header()
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    source_folder = filedialog.askdirectory(title="📂 Select Source Folder")
    root.destroy()

    if not source_folder:
        console.print("❎ No folder selected.", style="bold yellow")
        return None

    console.print(f"📂 Selected folder: {source_folder}", style="bold green")
    confirm_question = [
        {
            "type": "confirm",
            "name": "confirm",
            "message": "Proceed with organizing files in this folder?",
            "default": True
        }
    ]
    confirm = prompt(confirm_question)
    
    if confirm["confirm"]:
        return source_folder
    else:
        console.print("❎ Organization cancelled.", style="bold yellow")
        return None

# Main execution
if __name__ == "__main__":
    source_folder = select_folder()
    if source_folder:
        stats = organize_files(source_folder)
        display_statistics(stats)
        console.print("\n✅ File organization completed!", style="bold green")
    console.print("\nPress Enter to exit...", style="bold cyan")
    input()