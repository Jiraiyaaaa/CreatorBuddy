import os
import unidecode
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from pytube import YouTube

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Creator Buddy")

        # YouTube Log0
        logo_path = "youtube_logo.png"
        if os.path.exists(logo_path):
            self.youtube_logo = tk.PhotoImage(file=logo_path)
            self.logo_label = tk.Label(self.root, image=self.youtube_logo)
            self.logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # URL Entry
        self.url_label = tk.Label(self.root, text="Enter YouTube URL:")
        self.url_label.grid(row=1, column=0, padx=10, pady=5)
        self.url_entry = tk.Entry(self.root, width=40)
        self.url_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

        # Project Name Entry
        self.project_name_label = tk.Label(self.root, text="Enter Project Name:")
        self.project_name_label.grid(row=2, column=0, padx=10, pady=5)
        self.project_name_entry = tk.Entry(self.root, width=40)
        self.project_name_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

        # Folder Selection
        self.folder_path_var = tk.StringVar()
        self.folder_label = tk.Label(self.root, text="Select Download Location:")
        self.folder_label.grid(row=3, column=0, padx=10, pady=5)
        self.folder_entry = tk.Entry(self.root, textvariable=self.folder_path_var, width=30)
        self.folder_entry.grid(row=3, column=1, padx=10, pady=0)
        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=3, column=2, padx=0, pady=0)

        # Resolution Selector
        self.resolution_label = tk.Label(self.root, text="Select Resolution:")
        self.resolution_label.grid(row=4, column=0, padx=10, pady=5)
        resolutions = ["720p", "360p", "240p", "144p", "Audio Only"]
        self.resolution_var = tk.StringVar()
        self.resolution_var.set("720p")
        self.resolution_menu = tk.OptionMenu(self.root, self.resolution_var, *resolutions)
        self.resolution_menu.grid(row=4, column=1, padx=10, pady=5)

        # Download Button
        self.download_button = tk.Button(self.root, text="Download", bg="red", fg="yellow", command=self.download_video)
        self.download_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

    def download_video(self):
        url = self.url_entry.get()
        resolution = self.resolution_var.get()
        project_name = self.project_name_entry.get()
        folder_path = self.folder_path_var.get()

        if url == "":
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return
        if project_name == "":
            messagebox.showerror("Error", "Please enter a project name.")
            return
        if folder_path == "":
            messagebox.showerror("Error", "Please select a folder.")
            return

        try:
            yt = YouTube(url)
            if resolution == "Audio Only":
                stream = yt.streams.filter(only_audio=True).first()
            else:
                stream = yt.streams.filter(res=resolution).first()

            project_folder_path = os.path.join(folder_path, project_name)
            if not os.path.exists(project_folder_path):
                os.makedirs(project_folder_path)

            # Remove non-ASCII characters (including emojis) from video title for file path
            video_title = unidecode.unidecode(yt.title)
            video_path = os.path.join(project_folder_path, f"{video_title}.mp4")
            stream.download(output_path=project_folder_path)

            self.save_to_csv(yt, project_folder_path, url)
            messagebox.showinfo("Success", "Video downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def save_to_csv(self, yt, folder_path, video_url):
        csv_file_path = os.path.join(folder_path, "video_info.csv")

        with open(csv_file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if os.stat(csv_file_path).st_size == 0:
                writer.writerow(["Video URL", "Video Title", "Channel Name"])
            writer.writerow([video_url, yt.title, yt.author])

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_var.set(folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    downloader = YouTubeDownloader(root)
    root.mainloop()
