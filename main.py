import tkinter
import customtkinter
from pytubefix import YouTube

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

def fetch_and_display_qualities():
    ytLink = link.get()
    if not ytLink:
        return
    
    try:
        ytObject = YouTube(ytLink)
        # Fetch available qualities
        qualities = sorted(set(stream.resolution for stream in ytObject.streams.filter(adaptive=True, file_extension='mp4') if stream.resolution), key=lambda x: (int(x[:-1]), x))
        if not qualities:
            quality_menu.configure(values=["No quality options available"])
        else:
            quality_menu.configure(values=qualities)
            quality_var.set(qualities[0])  # Set default to the highest available quality
    except Exception as e:
        finishLabel.configure(text="Error fetching quality options!", text_color="red")
        print(f"Error: {e}")

def startDownload():
    try:
        ytLink = link.get()
        selected_quality = quality_var.get()
        if not ytLink or not selected_quality:
            finishLabel.configure(text="Please provide URL and select quality!", text_color="red")
            return
        
        print(f"Attempting to download from: {ytLink} at quality {selected_quality}")  # Debug print
        
        # Validate URL
        if "youtube.com" not in ytLink and "youtu.be" not in ytLink:
            finishLabel.configure(text="Invalid URL!", text_color="red")
            return

        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.filter(adaptive=True, file_extension='mp4', resolution=selected_quality).first()
        
        if video is None:
            finishLabel.configure(text="Video stream not available!", text_color="red")
            return
        
        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")
        video.download()
        finishLabel.configure(text="Downloaded!")
    
    except Exception as e:
        finishLabel.configure(text="Download Error!", text_color="red")
        print(f"Error: {e}")  # Print the exception

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()

    # Update progress bar
    progressBar.set(float(percentage_of_completion) / 100)

def on_link_change(*args):
    fetch_and_display_qualities()

# Our app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Copy your YouTube Link!")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
url_var.trace_add("write", on_link_change)  # Call on_link_change when the URL changes
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Quality selection
quality_var = tkinter.StringVar()
quality_menu = customtkinter.CTkOptionMenu(app, variable=quality_var, values=["Select Quality"])
quality_menu.pack(padx=10, pady=10)

# Finished downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progress percentage
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400,progress_color="green")
progressBar.set(0.0)
progressBar.pack(padx=10, pady=10)

# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload ,fg_color="red")
download.pack(padx=10, pady=10)

# Run app
app.mainloop()
