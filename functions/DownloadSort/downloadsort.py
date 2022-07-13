from tkinter.messagebox import askyesno

import yaml
import os
import shutil
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd

logging.basicConfig(format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)


def action_window():
    # commands
    def get_values() -> dict:
        """
        Retrieves the values from the text field to configure the config.
        :return:
        """
        params = {
            "DownloadFolder": ent_download_folder.get(),
            "VideoFolder": ent_video_folder.get(),
            "ImageFolder": ent_image_folder.get(),
            "ExecutableFolder": ent_exec_folder.get(),
            "DocumentFolder": ent_documents_folder.get(),
            "MusicFolder": ent_music_folder.get(),
            "ArchiveFolder": ent_archives_folder.get(),
        }
        # TODO: Does not work yet
        for param in params:
            current_param = params.get(param)
            if current_param in ("", " ", None):
                messagebox.showerror("One of more parameter is empty or invalid.")
            return {}
        return params

    def confirm_exit():
        if askyesno("Verify", "Quit ? ?"):
            exit()
        else:
            return None

    def confirm_start():
        if askyesno(
                "Verify",
                f"""
            Proceed with following settings ?
            Download Folder: {ent_download_folder.get()}
            Video Folder: {ent_video_folder.get()}
            Image Folder: {ent_image_folder.get()}
            Music Folder: {ent_music_folder.get()}
            Executable Folder: {ent_exec_folder.get()}
            Documents Folder: {ent_documents_folder.get()}
            Archive Folder: {ent_archives_folder.get()}
                    """,
        ):
            run()
        else:
            return None

    # Function for opening the
    # file explorer window

    # def load_config():
    # TODO: Implement load
    #  pass

    # def save_config():
    # TODO: Implement save
    # pass

    def run():
        settings = get_values()
        # TODO: Fix error dialog
        if settings == {}:
            return None
        move_handler = DownloadSort(settings)
        move_handler.move_handler()
        lbl_selections["text"] = "Started..."

    def select_dir(folder: str) -> int:
        folder_dir = fd.askdirectory()
        if folder == "download":
            ent_download_folder.insert(0, folder_dir)
        elif folder == "video":
            ent_video_folder.insert(0, folder_dir)
        elif folder == "image":
            ent_image_folder.insert(0, folder_dir)
        elif folder == "documents":
            ent_documents_folder.insert(0, folder_dir)
        elif folder == "exec":
            ent_exec_folder.insert(0, folder_dir)
        elif folder == "archives":
            ent_archives_folder.insert(0, folder_dir)
        elif folder == "music":
            ent_music_folder.insert(0, folder_dir)
        else:
            return -1
        return 1

    window = tk.Tk()
    window.title("DownloadSort Application")
    window.rowconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=500, weight=1)
    frm_menu = tk.Frame(window, relief=tk.RAISED, bd=2)
    frm_selection = tk.Frame(window)

    # Define components
    lbl_download_label = tk.Label(frm_selection, text="Download Folder:", anchor="w")
    lbl_download_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    ent_download_folder = tk.Entry(frm_selection)
    ent_download_folder.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    bt_download_folder = tk.Button(
        frm_selection, text="Browse...", command=lambda: select_dir("download")
    )
    bt_download_folder.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

    sep = ttk.Separator(frm_selection, orient="horizontal")
    sep.grid(row=1, columnspan=3, ipadx=200, pady=10)

    lbl_video_label = tk.Label(frm_selection, text="Video Folder:", anchor="w")
    lbl_video_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    ent_video_folder = tk.Entry(frm_selection)
    ent_video_folder.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
    bt_video_folder = tk.Button(
        frm_selection, text="Browse...", command=lambda: select_dir("video")
    )
    bt_video_folder.grid(row=2, column=2, sticky="ew", padx=5, pady=5)

    lbl_image_label = tk.Label(frm_selection, text="Image Folder:", anchor="w")
    lbl_image_label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    ent_image_folder = tk.Entry(frm_selection)
    ent_image_folder.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
    bt_image_folder = tk.Button(
        frm_selection, text="Browse...", command=lambda: select_dir("image")
    )
    bt_image_folder.grid(row=3, column=2, sticky="ew", padx=5, pady=5)

    lbl_documents_label = tk.Label(frm_selection, text="Documents Folder:", anchor="w")
    lbl_documents_label.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
    ent_documents_folder = tk.Entry(frm_selection)
    ent_documents_folder.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
    bt_documents_folder = tk.Button(
        frm_selection, text="Browse...", command=lambda: select_dir("documents")
    )
    bt_documents_folder.grid(row=4, column=2, sticky="ew", padx=5, pady=5)

    lbl_archives_label = tk.Label(frm_selection, text="Archive Folder:", anchor="w")
    lbl_archives_label.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
    ent_archives_folder = tk.Entry(frm_selection)
    ent_archives_folder.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
    bt_archives_folder = tk.Button(
        frm_selection, text="Browse...", command=lambda: select_dir("archives")
    )
    bt_archives_folder.grid(row=5, column=2, sticky="ew", padx=5, pady=5)

    lbl_exec_label = tk.Label(frm_selection, text="Executable Folder:", anchor="w")
    lbl_exec_label.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
    ent_exec_folder = tk.Entry(frm_selection)
    ent_exec_folder.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
    bt_exec_folder = tk.Button(
        frm_selection, text="Browse...", command=lambda: select_dir("exec")
    )
    bt_exec_folder.grid(row=6, column=2, sticky="ew", padx=5, pady=5)

    lbl_music_label = tk.Label(frm_selection, text="Music Folder:", anchor="w")
    lbl_music_label.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
    ent_music_folder = tk.Entry(frm_selection)
    ent_music_folder.grid(row=7, column=1, sticky="ew", padx=5, pady=5)
    bt_music_folder = tk.Button(
        frm_selection, text="Browse...", command=lambda: select_dir("music")
    )
    bt_music_folder.grid(row=7, column=2, sticky="ew", padx=5, pady=5)

    lbl_wip = tk.Label(frm_menu, text="^^^ WIP ^^^")
    lbl_wip.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    btn_confirm = tk.Button(frm_menu, text="Save Config", command=get_values)
    btn_confirm.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_load = tk.Button(frm_menu, text="Load Config")
    btn_load.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    btn_start = tk.Button(frm_menu, text="Start!", command=confirm_start)
    btn_start.grid(row=9, column=0, sticky="ew", padx=5, pady=5)

    btn_exit = tk.Button(frm_menu, text="Exit", command=confirm_exit)
    btn_exit.grid(row=10, column=0, sticky="ew", padx=5, pady=5)

    frm_menu.grid(row=0, column=0, sticky="ns")
    frm_selection.grid(row=0, column=1, sticky="nsew")

    lbl_selections = tk.Label(frm_selection, text="Waiting for input...")

    # Pack components

    window.mainloop()


class DownloadSort:
    def __init__(self, settings: dict):
        print(f"Loading configuration...")
        self.settings = settings
        self.types = self.__settings_loader("types")

    def __settings_loader(
            self, settings: str, config_path: str = "../../settings/config.yml"
    ) -> dict:
        """
        Loads all needed settings.

        :param settings: What to load
        :param config_path: The path to the config file, has a set default.
        :return: dict
        """
        full_path = os.path.join(os.path.dirname(__file__), config_path)
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
    action_window()
