import os 

def new_names(f_list, inp_name):
    """
    Creates new file names in numerical order in form: (input name) (file number)
    Also creates a mapping of new names : old names for undoing process
    """
    mapping = {}

    for counter, old_name in enumerate(f_list, start=1):
        new_name = f"{inp_name} {counter}"
        mapping[new_name] = old_name

    return mapping


def file_retriever():
    """
    Retrieves files within specified folder
    """
    try:
        files = [f for f in os.listdir() if os.path.isfile(f)]
    except PermissionError:
        raise PermissionError("Unable to retrieve files due to lack of permissions")

    print(f"First 10 files within given folder: {files[:10]}")
    return files


def get_path():
    """
    Gets the name of the folder within which the user wishes to rename files
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    while True:
        folder = input("Where would you like to rename files within? Give the name of a folder WITHIN the folder this program is saved: ")
        if os.path.isdir(folder):
            try:
                os.chdir(folder)
                return
            except PermissionError:
                raise PermissionError("Unable to open folder due to lack of permissions")
        print("Folder not found, please try again")


def get_input():
    """
    Asks user for base name for files.
    """
    while True:
        name = input(
            "What do you want to call the files? They will be named like: (name) 1, (name) 2, and so on: ").strip()
        if name:
            return name
        print("Invalid input, please try again")


def apply_mapping(mapping, direction="forward"):
    """
    Renames files using mapping.

    Raises:
        PermissionError: If the program doesn't have the permissions to rename files
        FileNotFoundError: If the program cannot locate a file
    """
    counter = 0
    failures = 0
    succeeded = []

    for new, old in mapping.items():
        ext = os.path.splitext(old)[1]

        if direction == "forward":
            src = old
            dst = new + ext
        elif direction == "undo":
            src = new + ext
            dst = old
            
        try:
            os.rename(src, dst)
            counter += 1
            succeeded.append((src, dst))
        except FileNotFoundError:
            print(f"Missing file: {src}")
            failures += 1
        except PermissionError:
            raise PermissionError("Insufficient permissions to rename files")

        # rollback if 3 failures occured
        if failures == 3 and direction == "forward":
            print("3 rename failures encountered, rolling back...")
            for s, d in succeeded:
                try:
                    os.rename(d, s)
                except:
                    pass 
            return

    if direction == "forward":
        print(f"{counter} files were renamed successfully")
    else:
        print(f"{counter} files were reverted successfully")

def main():
    get_path()
    files = file_retriever()
    base_name = get_input()

    mapping = new_names(files, base_name)

    apply_mapping(mapping, "forward")

    choice = input("Undo this change? (y/n): ").strip().lower()
    if choice == "y":
        apply_mapping(mapping, "undo")


if __name__ == "__main__":
    main()