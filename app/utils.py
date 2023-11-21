import os
import shutil

class Utility:
    @staticmethod
    def setup_output_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def empty_output_directory(directory):
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                os.makedirs(directory)
                print(f"Successfully emptied the output directory: {directory}")
            else:
                print(f"The directory does not exist: {directory}")
        except Exception as e:
            print(f"An error occurred while trying to empty the output directory: {e}")