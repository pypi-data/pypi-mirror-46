import os


class Renamer:
    '''
    Renamer object able to rename each file in the given path.
    Directories are untouched.
    A saving file is created and contains the former filename linked to the new ones.
    Renamer object is able to restore filenames as it was before thanks to the saving file.
    '''

    def __init__(self, path='.'):
        self.save_folder = 'save_filenames'     # Name of the folder that contains the saving file
        self.save_file = 'old.txt'              # Filename of the saving file
        self.path = path                        # Path for the location of the target files
        self.di_names = self.read_all_files()   # Dictionary that contains former linked to their new filenames

    def read_all_files(self):
        '''
        Reads the name of each file and returns a dictionary with
        the future replacing filename for each current filename
        '''
        all_files = self.list_files_only()
        fakenames_gen = self.generate_fakenames(all_files)
        dictionary = {}
        for f in all_files:
            name = next(fakenames_gen)      # Get future filename
            ext = os.path.splitext(f)[1]    # Get current file's extension
            dictionary[f] = name + ext      # Add current and future filename
        return dictionary

    def generate_fakenames(self, all_files):
        '''
        Generator that create artificial filenames according to
        number of files in the current path
        '''
        # Calculte the length of the future filenames
        length = len(str(len(all_files)))   # 200 files -> '200' -> length = 3
        # Generator : 000, 001, 002...
        for i in range(0, len(all_files)):
            name = str(i).zfill(length)
            yield name

    def list_files_only(self):
        '''
        Returns all files (not directories) that are in the given path
        '''
        return [f for f in os.listdir(self.path)
                if os.path.isfile(self.path + "/" + f)]

    def save_former_names(self):
        '''
        Create a file to save the former filenames
        '''
        # Create a directory to contain the saving file
        dirname = self.path + '/' + self.save_folder
        if not os.path.exists(dirname): # Create the saving file if not exists
            os.makedirs(dirname)

        # Fill the saving file
        with open(f"{dirname}/{self.save_file}", 'w') as f:
            for name in self.di_names:
                f.write(f'{name}:{self.di_names[name]}\n')

    def rename(self):
        '''
        Rename each file and create save file for back up :
        former filename as value,
        new filename as key
        '''
        location = self.path + "/"  # Location the target files
        # Renaming action is forbidden if folder contains a .dont file
        if '.dont' in os.listdir(location):
            print("Renaming not allowed.")
            return
        # Renaming files is allowed
        # Renaming each file (names are in the Renamer's dictionary)
        for f in self.di_names:
            print(f'Renaming {f} as {self.di_names[f]}')
            os.rename(location + f, location + self.di_names[f])
        # End of the renaming process
        print("Renaming done.")
        # Save the former filenames in a saving file for
        # future a back up
        self.save_former_names()
        print(f"Restore file ready in location {self.save_folder}/{self.save_file}")

    def restore_di_names(self):
        '''
        Returns a dictionary with the former filename as key
        and the most recent filename as value
        '''
        location = self.path + '/' + self.save_folder + '/' # Location of the save file
        di = {}
        # Open the save file
        with open(location + self.save_file, 'r') as f:
            all_lines = f.readlines()
            # Each line of the file contains the former and new name of a file
            for line in all_lines:
                parts = line.split(':')         # Separate former/current name
                parts[1] = parts[1].strip()     # Remove '\n'
                di[parts[1]] = parts[0]         # Put in dictionary
        return di

    def restore(self):
        '''
        Read the saving file to restore the original filenames
        '''
        self.di_names = self.restore_di_names() # Get former names from the save file
        self.rename()       # Rename each file with the curent dictionary


if __name__ == '__main__':
    path = './randomdir'
    r = Renamer(path)
    r.rename()
    input("Enter anything t continue... ")
    r.restore()
