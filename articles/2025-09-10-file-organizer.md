# Organizing Files Automatically with Python

Categories: Automation, Productivity
Tags: files, organization, os, automation

Are you tired of your "Downloads" folder being a complete mess?
With just a few lines of Python, you can automatically sort files into folders based on their type.
This is a perfect small project for everyday productivity.

## Step 1: Import Required Modules

    import os
    import shutil
    from pathlib import Path

## Step 2: Define File Categories

We can map file extensions to their respective folders. Update or extend this mapping as needed.

    FILE_TYPES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt"],
        "Audio": [".mp3", ".wav"],
        "Videos": [".mp4", ".mov", ".avi"]
    }

## Step 3: Create a Sorting Function

The function below moves files into folders based on their extension. Files with no matching category are skipped.

    def organize_files(folder):
        for file in Path(folder).iterdir():
            if file.is_file():
                moved = False
                for category, extensions in FILE_TYPES.items():
                    if file.suffix.lower() in extensions:
                        target_folder = Path(folder) / category
                        target_folder.mkdir(exist_ok=True)
                        shutil.move(str(file), target_folder / file.name)
                        print(f"Moved {file.name} → {category}")
                        moved = True
                        break
                if not moved:
                    print(f"Skipped {file.name} (no matching category)")

## Step 4: Run the Script

Set the `downloads` variable to the folder you want to organize and call the function.

    downloads = str(Path.home() / "Downloads")
    organize_files(downloads)

## Result

Now, instead of a messy folder full of random files, your `Downloads` directory will be neatly organized into **Images**, **Documents**, **Audio**, and **Videos**.

This script can be expanded further:
- Add more categories (e.g., Spreadsheets, Archives)  
- Run it on a schedule with `cron` or Task Scheduler  
- Combine with cloud storage (Google Drive, Dropbox)

A little automation can make your daily computer life much smoother. Try running this script once, and you’ll never want to go back to manual file sorting!

