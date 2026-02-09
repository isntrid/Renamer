import contextlib
import os
from typing import List, Dict

def new_names(f_list: List[str], inp_name: str) -> Dict[str, str]:
    """
    Creates new file names in numerical order in form: (input name) (file number)
    Also creates a mapping of new names : old names for undoing process
    """
    mapping = {}

    for counter, old_name in enumerate(f_list, start=1):
        new_name = f"{inp_name} {counter}"
        mapping[new_name] = old_name

    return mapping


def file_retriever() -> list[str]:
    """
    Retrieves files within specified folder
    """
    try:
        files = [f for f in os.listdir() if os.path.isfile(f)]
    except PermissionError as e:
        raise PermissionError("Unable to retrieve files due to lack of permissions") from e

    print(f"First 10 files within given folder: {files[:10]}")
    return sorted(files)

def get_path() -> str:
    """
    Gets the absolute path of the folder within which the user wishes to rename files
    
    Raises:
        RunTimeError: Occurs when user fails to input a valid folder name more than 5 times.
    """

    DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

    max_attempts = 5
    for _ in range(max_attempts):
        
        folder = input("Where would you like to rename files within? Give the name of a folder inside your Downloads folder: ").strip()
        target = os.path.join(DOWNLOADS_DIR, folder)
        
        if not folder:
            print("Folder name cannot be empty")
            continue
        if os.path.isdir(target):
            return target
        print("Folder not found, please try again")
    raise RuntimeError("Maximum input attempts exceeded")


def get_input() -> str:
    """
    Asks user for base name for files.

    Raises:
        RuntimeError: Occurs when user fails to input a valid base name more than 5 times.
    """
    max_attempts = 5
    for _ in range(max_attempts):
        
        name = input("What do you want to call the files? They will be named like: (name) 1, (name) 2, and so on: ").strip()

        if not name:
            print("Name cannot be empty")
            continue
        return name

    raise RuntimeError("Maximum input attempts exceeded")


def apply_mapping(mapping: Dict[str, str], direction: str = "forward") -> None:
    """
    Renames files using mapping.

    Raises:
        PermissionError: If the program doesn't have the permissions to rename files
        FileNotFoundError: If the program cannot locate a file
    """
    counter = 0
    failures = 0
    succeeded = []

    for new_name, old_name in mapping.items():
        extension = os.path.splitext(old_name)[1]

        if direction == "forward":
            source = old_name
            destination = new_name + extension
        elif direction == "undo":
            source = new_name + extension
            destination = old_name

        try:
            os.rename(source, destination)
            counter += 1
            succeeded.append((source, destination))
        except FileNotFoundError:
            print(f"Missing file: {source}")
            failures += 1
        except PermissionError as e:
            raise PermissionError("Insufficient permissions to rename files") from e

        # rollback if 3 failures occurred
        if failures == 3 and direction == "forward":
            print("3 rename failures encountered, rolling back...")
            for success_source, success_destination in succeeded:
                with contextlib.suppress(OSError):
                    os.rename(success_destination, success_source)
            return

    if direction == "forward":
        print(f"{counter} files were renamed successfully")
    else:
        print(f"{counter} files were reverted successfully")


def main() -> None:
    
    # main flow
    original_cwd = os.getcwd()
    target_dir = get_path()
    os.chdir(target_dir)
    files = file_retriever()
    base_name = get_input()
    mapping = new_names(files, base_name)
    apply_mapping(mapping, "forward")
    
    max_attempts = 5

    for _ in range(max_attempts):
        choice = input("Undo this change? (y/n): ").strip().lower()

        if choice == "y":
            apply_mapping(mapping, "undo")
            break
        elif choice == "n":
            break
        elif not choice:
            print("Input cannot be empty")
        else:
            print("Please pick between y or n")
    else:
        apply_mapping(mapping, "undo")
        raise RuntimeError("Maximum input attempts exceeded, reverting changes automatically...")
    os.chdir(original_cwd) # changes working directory back to original for safety

if __name__ == "__main__":
    main()