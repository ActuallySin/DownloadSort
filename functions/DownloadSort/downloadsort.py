import yaml
import os
import shutil
import logging

logging.basicConfig(format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)


class DownloadSort:
    def __init__(self):
        print(f"Loading configuration...")
        self.settings = self.__settings_loader("settings")
        self.types = self.__settings_loader("types")

    def __settings_loader(self, settings: str, config_path: str = "./config.yml") -> dict:
        """
        Loads all needed settings.

        :param settings: What to load
        :param config_path: The path to the config file, has a set default.
        :return: None
        """
        full_path = os.path.join(os.getcwd(), config_path)
        with open(full_path, mode="r", encoding="utf-8") as configs:
            if settings == "settings":
                settings = yaml.safe_load(configs)["Directory_Settings"]
            elif settings == "types":
                settings = yaml.safe_load(configs)["FileTypes"]
            else:
                logger.error(f"Failed to load the config")
        return settings

    def __mover(self, folder: str, name: str):
        """
        Moves the file from one location to another

        :param folder: The destination folder
        :param name: The name of the file
        :return: None
        """
        try:
            source = os.path.join(self.settings.get("DownloadFolder"), name)
            dest = os.path.join(self.settings.get(folder), name)
            shutil.move(source, dest)
        except Exception as exp:
            logger.error(f"Error moving file {name} to Image Folder with error: {exp}")

    def move_handler(self):
        """
        The actual handler for all methods

        :return: None
        """
        print(f"Starting to move files for you.............")
        for file in os.listdir(self.settings.get("DownloadFolder")):
            filename = os.fsdecode(file)
            if filename.endswith(tuple(self.types["Images"])):
                self.__mover("ImageFolder", filename)
            elif filename.endswith(tuple(self.types["Documents"])):
                self.__mover("DocumentFolder", filename)
            elif filename.endswith(tuple(self.types["Executables"])):
                self.__mover("ExecutableFolder", filename)
            elif filename.endswith(tuple(self.types["Videos"])):
                self.__mover("VideoFolder", filename)
            elif filename.endswith(tuple(self.types["Music"])):
                self.__mover("MusicFolder", filename)
            elif filename.endswith(tuple(self.types["Archives"])):
                self.__mover("ArchiveFolder", filename)
        print(f"Done.")


if __name__ == "__main__":
    move_handler = DownloadSort()
    move_handler.move_handler()
