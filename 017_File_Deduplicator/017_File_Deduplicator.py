import os
import hashlib
import tkinter as tk
from tkinter import filedialog
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.progress import track
from rich.table import Table
import time
import math

console = Console()

# Pagination constants
ITEMS_PER_PAGE = 5  # Number of duplicate sets to show per page

def calculate_file_hash(file_path, hash_algorithm="sha256", chunk_size=4096):
    hash_func = getattr(hashlib, hash_algorithm)()
    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(chunk_size):
                hash_func.update(chunk)
    except FileNotFoundError:
        console.print(f"❌ File {file_path} not found.", style="bold red")
        return None
    return hash_func.hexdigest()

def get_file_size(file_path):
    """Get file size in bytes."""
    try:
        return os.path.getsize(file_path)
    except (FileNotFoundError, PermissionError):
        return 0

def format_size(size_bytes):
    """Format bytes to human-readable size."""
    if size_bytes == 0:
        return "0 B"
    size_names = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def find_duplicates(directory):
    file_hashes = {}
    duplicates = {}
    all_files = []
    stats = {
        "total_files": 0,
        "duplicate_sets": 0,
        "total_duplicates": 0,
        "wasted_space": 0,
        "file_sizes": {}  # To store file sizes by hash
    }

    console.print("\n🔍 Scanning directory and calculating file hashes...\n")

    # Collect all files first to track progress
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    
    stats["total_files"] = len(all_files)

    for file_path in track(all_files, description="[cyan]Scanning files..."):
        file_hash = calculate_file_hash(file_path)
        
        if file_hash:
            file_size = get_file_size(file_path)
            
            if file_hash in file_hashes:
                if file_hash not in duplicates:
                    duplicates[file_hash] = [file_hashes[file_hash]]
                    stats["duplicate_sets"] += 1
                    stats["file_sizes"][file_hash] = file_size
                
                duplicates[file_hash].append(file_path)
                stats["total_duplicates"] += 1
                stats["wasted_space"] += file_size
            else:
                file_hashes[file_hash] = file_path
                stats["file_sizes"][file_hash] = file_size
    
    return duplicates, stats

def display_statistics(stats):
    """Display a summary of statistics in a beautiful panel."""
    stats_table = Table(box=box.ROUNDED)
    stats_table.add_column("Statistic", style="bold cyan")
    stats_table.add_column("Value", style="yellow")
    
    stats_table.add_row("Total Files Scanned", str(stats["total_files"]))
    stats_table.add_row("Duplicate Sets Found", str(stats["duplicate_sets"]))
    stats_table.add_row("Total Duplicate Files", str(stats["total_duplicates"]))
    stats_table.add_row("Potential Space Savings", format_size(stats["wasted_space"]))
    
    stats_panel = Panel(
        stats_table,
        title="[bold green]Scan Statistics[/]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2),
        width=50
    )
    
    console.print(stats_panel)

def show_duplicates_paginated(duplicates, stats):
    """Display duplicates with pagination"""
    all_duplicate_items = list(duplicates.items())
    total_items = len(all_duplicate_items)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    current_page = 1
    choices = []
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(f"\n[bold cyan]Duplicate Files (Page {current_page}/{total_pages}):[/bold cyan]")
        
        # Calculate start and end indices for the current page
        start_idx = (current_page - 1) * ITEMS_PER_PAGE
        end_idx = min(start_idx + ITEMS_PER_PAGE, total_items)
        
        # Display pagination info
        pagination_text = f"[bold cyan]Showing items {start_idx + 1}-{end_idx} of {total_items} duplicate sets[/bold cyan]"
        console.print(pagination_text)
        
        # Show current page's duplicates
        page_choices = []
        for idx, (hash_val, files) in enumerate(all_duplicate_items[start_idx:end_idx], start=start_idx + 1):
            file_size = format_size(stats["file_sizes"].get(hash_val, 0))
            display = f"{idx}. {len(files)} files - Size: {file_size} - Hash: {hash_val[:12]}..."
            
            # Create choice text with filenames included
            choice_text = display
            for file in files:
                filename = os.path.basename(file)
                file_size = format_size(get_file_size(file))  # Show individual file size
                choice_text += f"\n   - {filename} ({file}) [{file_size}]"
            
            # Add formatted choice with full file information
            page_choices.append({"name": choice_text, "value": hash_val})
            choices.append({"name": choice_text, "value": hash_val})
            
            # Display duplicate set in a table
            table = Table(box=box.ROUNDED, title=f"[bold cyan]Set #{idx}: {len(files)} files - Hash: {hash_val[:12]}...[/bold cyan]")
            table.add_column("File", style="bold yellow")
            table.add_column("Path", style="green")
            table.add_column("Size", style="cyan")
            
            for file in files:
                filename = os.path.basename(file)
                directory = os.path.dirname(file)
                file_size = format_size(get_file_size(file))
                table.add_row(filename, directory, file_size)
            
            console.print(table)
        
        # Display pagination controls if there's more than one page
        if total_pages > 1:
            # Display statistics only on the first page
            if current_page == 1:
                display_statistics(stats)
                
            navigation_choices = []
            
            if current_page > 1:
                navigation_choices.append({"name": "⬅️ Previous Page", "value": "prev"})
                
            if current_page < total_pages:
                navigation_choices.append({"name": "➡️ Next Page", "value": "next"})
                
            navigation_choices.append({"name": "🔢 Go to specific page", "value": "goto"})
            navigation_choices.append({"name": "✅ Continue to actions", "value": "continue"})
            
            nav_question = [
                {
                    "type": "list",
                    "name": "navigation",
                    "message": f"📄 Page {current_page} of {total_pages}. Navigate:",
                    "choices": navigation_choices
                }
            ]
            
            nav_choice = prompt(nav_question)
            
            if nav_choice["navigation"] == "prev":
                current_page -= 1
            elif nav_choice["navigation"] == "next":
                current_page += 1
            elif nav_choice["navigation"] == "goto":
                goto_question = [
                    {
                        "type": "input",
                        "name": "page_number",
                        "message": f"Enter page number (1-{total_pages}):",
                        "default": str(current_page),
                        "validate": lambda val: (
                            True if val.isdigit() and 1 <= int(val) <= total_pages
                            else f"Please enter a valid number between 1 and {total_pages}"
                        )
                    }
                ]
                goto_answer = prompt(goto_question)
                current_page = int(goto_answer["page_number"])
            else:  # continue
                break
        else:
            console.print("\nPress Enter to continue...", style="bold cyan")
            input()
            # Display statistics if this is the first page and only one page exists
            if current_page == 1:
                display_statistics(stats)
            break
    
    return choices

def delete_duplicates(duplicates, selected_hashes):
    for selected_hash in selected_hashes:
        files = duplicates[selected_hash]
        # Create list of tuples with (file_path, file_size)
        files_with_sizes = [(file, get_file_size(file)) for file in files]
        # Sort by file size in descending order
        files_with_sizes.sort(key=lambda x: x[1], reverse=True)
        
        # Keep the largest file (first in sorted list)
        largest_file = files_with_sizes[0][0]
        console.print(f"📌 Keeping largest file: {largest_file} ({format_size(files_with_sizes[0][1])})", style="bold blue")
        
        # Delete all other files
        files_to_delete = [file for file, _ in files_with_sizes[1:]]
        for file in files_to_delete:
            try:
                os.remove(file)
                console.print(f"✅ Deleted: {file}", style="bold green")
            except Exception as e:
                console.print(f"❌ Failed to delete {file}: {e}", style="bold red")

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide main window
    folder_selected = filedialog.askdirectory(title="📂 Select directory to scan for duplicates")
    
    # Force focus back to terminal/console after dialog closes
    root.destroy()  # Properly destroy the Tkinter instance
    
    # For Windows systems, attempt to refocus the console window
    if os.name == 'nt':
        try:
            import win32gui
            import win32con
            # Try to bring console window to front
            console_hwnd = win32gui.GetForegroundWindow()
            win32gui.SetForegroundWindow(console_hwnd)
        except ImportError:
            # If pywin32 is not available, inform but continue
            console.print("Note: Install pywin32 for better window focus handling", style="dim")
    
    return folder_selected

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    title_text = Text("FILE DEDUPLICATOR", style="bold cyan", justify="center")
    subtitle = Text("A CLI tool to find and clean duplicate files", style="green", justify="center")
    author = Text("By: Kenkyo Adrian", style="dim", justify="center")
    help_hint = Text("Select 'Show help information' from the menu for assistance", style="italic yellow", justify="center")
    
    header_panel = Panel.fit(
        Text.assemble(title_text, "\n", subtitle, "\n", author, "\n", help_hint),
        border_style="blue",
        box=box.ROUNDED,
        padding=(1, 4)
    )
    
    console.print(header_panel)

def show_help():
    """Display help information in a panel"""
    help_table = Table(box=box.ROUNDED)
    help_table.add_column("Menu Option", style="bold cyan", width=25)
    help_table.add_column("Description", style="yellow", width=45)
    
    # Add command descriptions
    help_table.add_row("Scan for duplicate files", "Browse and scan a directory for duplicate files")
    help_table.add_row("Show help information", "Display this help menu")
    help_table.add_row("Exit", "Close the application")
    
    # Add action descriptions
    action_table = Table(box=box.ROUNDED)
    action_table.add_column("Action", style="bold cyan", width=25)
    action_table.add_column("Description", style="yellow", width=45)
    
    action_table.add_row("Select specific sets", "Choose which duplicate sets to clean up")
    action_table.add_row("Clean ALL duplicate files", "Remove all duplicates (keeping largest file from each set)")
    action_table.add_row("Return to main menu", "Go back to the main menu")
    
    # Navigation instructions
    nav_table = Table(box=box.ROUNDED)
    nav_table.add_column("Navigation", style="bold magenta", width=25)
    nav_table.add_column("Description", style="yellow")
    
    nav_table.add_row("↑/↓ Arrow Keys", "Navigate up and down through menu options")
    nav_table.add_row("Enter", "Select the highlighted option")
    nav_table.add_row("Space", "Toggle selection in checkbox menus (when selecting duplicate sets)")
    
    # Add pagination navigation instructions
    pagination_table = Table(box=box.ROUNDED)
    pagination_table.add_column("Pagination Controls", style="bold blue", width=25)
    pagination_table.add_column("Description", style="yellow", width=45)
    
    pagination_table.add_row("⬅️ Previous Page", "Move to the previous page of duplicate-sets")
    pagination_table.add_row("➡️ Next Page", "Move to the next page of duplicate sets")
    pagination_table.add_row("🔢 Go to specific page", "Jump to a specific page number")
    pagination_table.add_row("✅ Continue to actions", "Finish browsing and proceed to actions")
    
    tips_table = Table(box=box.ROUNDED)
    tips_table.add_column("Tips", style="bold green", width=70)
    
    tips_table.add_row("• Files are compared using SHA-256 hash, ensuring accurate detection")
    tips_table.add_row("• The largest file is kept when deleting duplicates")
    tips_table.add_row("• Use the statistics panel to see potential space savings")
    tips_table.add_row("• Results are paginated for easier browsing with many duplicates")
    tips_table.add_row("• You can access this help anytime from the main menu")
    
    # Create a Group with all the components
    from rich.console import Group
    
    help_content = Group(
        Text("Menu Options:", style="bold magenta"),
        help_table,
        Text("\nAvailable Actions:", style="bold magenta"),
        action_table,
        Text("\nNavigation Controls:", style="bold magenta"),
        nav_table,
        Text("\nPagination Controls:", style="bold magenta"),
        pagination_table,
        Text("\nTips & Tricks:", style="bold magenta"),
        tips_table
    )
    
    help_panel = Panel(
        help_content,
        title="[bold cyan]Help & Information[/]",
        border_style="blue",
        box=box.ROUNDED,
        padding=(1, 1),  # Reduced padding
        width=80  # Set a fixed width to make the panel more compact
    )
    
    console.print(help_panel)
    
    # Wait for user to press enter
    console.print("\nPress Enter to continue...", style="bold cyan")
    input()

def main():
    print_header()
    while True:
        menu_question = [
            {
                "type": "list",
                "name": "menu_choice",
                "message": "📋 What would you like to do?",
                "choices": [
                    {"name": "🔍 Scan for duplicate files", "value": "scan"},
                    {"name": "❓ Show help information", "value": "help"},
                    {"name": "❌ Exit", "value": "exit"}
                ]
            }
        ]
        menu = prompt(menu_question)

        if menu["menu_choice"] == "exit":
            console.print("👋 Exiting program. Goodbye!", style="bold red")
            break
            
        if menu["menu_choice"] == "help":
            show_help()
            continue

        directory = select_directory()
        if not directory:
            console.print("❎ No directory selected. Returning to main menu...", style="bold yellow")
            continue

        duplicates, stats = find_duplicates(directory)
        
        if not duplicates:
            console.print("\n🎉 No duplicate files found.", style="bold green")
            # Display statistics for scanned files even when no duplicates found
            display_statistics(stats)
            # Pause briefly to ensure message is seen before showing the next prompt
            time.sleep(1)
            continue

        # Show duplicates with pagination (stats will be displayed on the first page)
        duplicate_choices = show_duplicates_paginated(duplicates, stats)
        
        # Add option after scanning
        action_question = [
            {
                "type": "list",
                "name": "action_choice",
                "message": "🔧 Choose an action:",
                "choices": [
                    {"name": "🔍 Select specific duplicate sets to clean", "value": "select"},
                    {"name": "🗑️ Clean ALL duplicate files (keep largest file from each set)", "value": "clean_all"},
                    {"name": "❓ Show help information", "value": "help"},
                    {"name": "↩️ Return to main menu", "value": "return"}
                ]
            }
        ]
        action = prompt(action_question)
        
        # Check for help command
        if action["action_choice"] == "help":
            show_help()
            continue
            
        if action["action_choice"] == "return":
            continue
            
        elif action["action_choice"] == "clean_all":
            # Clean all duplicates at once
            console.print("\n⚠️ This will delete ALL duplicate files (keeping largest from each set)", style="bold yellow")
            confirm_question = [
                {
                    "type": "confirm",
                    "name": "confirm_delete",
                    "message": f"⚠️ Are you sure you want to delete ALL duplicates? This cannot be undone!",
                    "default": False,
                }
            ]
            confirm = prompt(confirm_question)
            if confirm["confirm_delete"]:
                # Get all hash values
                all_hashes = list(duplicates.keys())
                delete_duplicates(duplicates, all_hashes)
                console.print("✅ Bulk deletion completed!", style="bold green")
            else:
                console.print("❎ Bulk deletion cancelled.", style="bold yellow")
                
        elif action["action_choice"] == "select":
            # Implement paginated selection for duplicate sets
            select_question = [
                {
                    "type": "checkbox",
                    "name": "hashes_to_delete",
                    "message": "🧹 Select duplicate sets to clean (largest file will be kept):",
                    "choices": duplicate_choices,
                }
            ]
            selected = prompt(select_question)

            if selected["hashes_to_delete"]:
                confirm_question = [
                    {
                        "type": "confirm",
                        "name": "confirm_delete",
                        "message": f"⚠️ Are you sure you want to delete selected duplicates?",
                        "default": False,
                    }
                ]
                confirm = prompt(confirm_question)
                if confirm["confirm_delete"]:
                    delete_duplicates(duplicates, selected["hashes_to_delete"])
                else:
                    console.print("❎ Deletion cancelled.", style="bold yellow")
            else:
                console.print("No duplicate sets selected.", style="bold yellow")

        console.print("\n✅ Process completed. Returning to main menu...", style="bold green")

if __name__ == "__main__":
    main()