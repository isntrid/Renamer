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
    os.chdir(os.path.dirname(os.path.abspath(__file__))) # sets working directory to main folder within which file is within

    max_attempts = 5
    for attempts in range(max_attempts):
        folder = input("Where would youlike to rename files within? Give the name of a folder WITHIN the folder this program is saved: ")
        if os.path.isdir(folder):
            try:
                os.chdir(folder)
                return
            except PermissionError:
                raise PermissionError("Unable to open folder due to lack of permissions")
        print("Folder not found, please try again")
    raise RuntimeError("Maximum input attempts exceeded")


def get_input():
    """
    Asks user for base name for files.
    """
    
    max_attempts = 5
    for attempts in range(max_attempts):
        name = input(
            "What do you want to call the files? They will be named like: (name) 1, (name) 2, and so on: ").strip()
        if name:
            return name
        print("Invalid input, please try again")
    raise RuntimeError("Maximum input attempts exceeded")


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
        except PermissionError:
            raise PermissionError("Insufficient permissions to rename files")

        # rollback if 3 failures occured
        if failures == 3 and direction == "forward":
            print("3 rename failures encountered, rolling back...")
            for success_source, success_destination in succeeded:
                try:
                    os.rename(success_destination, success_source)
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
