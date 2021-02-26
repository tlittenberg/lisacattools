from google_drive_downloader import GoogleDriveDownloader as gdd
from tarfile import open as opentar
import os
import os.path

# download MBHB
if not os.path.exists("tutorial/data/mbh"):
    gdd.download_file_from_google_drive(
        file_id="1iL071Fi5MxHle0CLOqg3JkZIgjQF8EwF",
        dest_path="tutorial/data/MBHDemo.tar",
        showsize=True,
    )
    with opentar("tutorial/data/MBHDemo.tar", "r") as tar:
        tar.extractall("tutorial/data/mbh")  # specify which folder to extract to
    os.remove("tutorial/data/MBHDemo.tar")


# download
if not os.path.exists("tutorial/data/ucb"):
    gdd.download_file_from_google_drive(
        file_id="14ZgAU_67ZzxTJyaScUH_i22nSkpNOp36",
        dest_path="tutorial/data/UCBDemo.tar",
        showsize=True,
    )
    with opentar("tutorial/data/UCBDemo.tar", "r") as tar:
        tar.extractall("tutorial/data/ucb")  # specify which folder to extract to
    os.remove("tutorial/data/UCBDemo.tar")
