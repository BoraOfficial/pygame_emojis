from io import BytesIO
import pathlib
from zipfile import ZipFile
from urllib.request import urlopen


_PNG_DIR: pathlib.Path = pathlib.Path(__file__).parent / "png"


def download(
    # Why not just use the .png files?
    zip_url="https://github.com/hfg-gmuend/openmoji/releases/download/16.0.0/openmoji-618x618-color.zip",
):
    """Download the emojis from openmoji."""
    print("[pygame_emojis] Download the zip file from ", zip_url)
    resp = urlopen(zip_url)
    zipfile = ZipFile(BytesIO(resp.read()))

    print("[pygame_emojis] Extract the zip file to ", _PNG_DIR)
    zipfile.extractall(_PNG_DIR)


if __name__ == "__main__":
    # Dowload the raw data
    download()
