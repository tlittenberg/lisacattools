# -*- coding: utf-8 -*-
import os.path
from tarfile import open as opentar

from google_drive_downloader import GoogleDriveDownloader as gdd

# download MBH
if not os.path.exists("tutorial/data/mbh"):
    gdd.download_file_from_google_drive(
        file_id="1iL071Fi5MxHle0CLOqg3JkZIgjQF8EwF",
        dest_path="tutorial/data/MBHDemo.tar",
        showsize=True,
    )
    with opentar("tutorial/data/MBHDemo.tar", "r") as tar:
        tar.extractall(
            "tutorial/data/mbh"
        )  # specify which folder to extract to
    os.remove("tutorial/data/MBHDemo.tar")


# download UCB
if not os.path.exists("tutorial/data/ucb"):
    # 06 mo
    gdd.download_file_from_google_drive(
        file_id="14ZgAU_67ZzxTJyaScUH_i22nSkpNOp36",
        dest_path="tutorial/data/UCBDemo_06.tar",
        showsize=True,
    )
    with opentar("tutorial/data/UCBDemo_06.tar", "r") as tar:
        tar.extractall(
            "tutorial/data/ucb"
        )  # specify which folder to extract to
    os.remove("tutorial/data/UCBDemo_06.tar")

    # 03 mo
    gdd.download_file_from_google_drive(
        file_id="1Rbx8PTLHCOHdakGok8DM2pVDzdPXsuUp",
        dest_path="tutorial/data/UCBDemo_03.tar",
        showsize=True,
    )
    with opentar("tutorial/data/UCBDemo_03.tar", "r") as tar:
        tar.extractall(
            "tutorial/data/ucb"
        )  # specify which folder to extract to
    os.remove("tutorial/data/UCBDemo_03.tar")
