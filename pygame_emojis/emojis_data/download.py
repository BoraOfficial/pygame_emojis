from io import BytesIO
import pathlib
from zipfile import ZipFile
from urllib.request import urlopen

try:
    import cairosvg
    cairoInstalled = True
except OSError: # OSError: no library called "cairo-2" was found
    cairoInstalled = False


_EMOJIS_DIR: pathlib.Path = pathlib.Path(__file__).parent / "emojis"


def download():
    if not cairoInstalled:
        # Download .png versions if Cairo isn't installed
        zip_url="https://github.com/hfg-gmuend/openmoji/releases/download/16.0.0/openmoji-618x618-color.zip"
    else:
        # Download .svg versions if Cairo is installed
        zip_url="https://github.com/hfg-gmuend/openmoji/releases/latest/download/openmoji-svg-color.zip"

    """Download the emojis from openmoji."""
    print("[pygame_emojis] Download the zip file from ", zip_url)
    resp = urlopen(zip_url)
    zipfile = ZipFile(BytesIO(resp.read()))

    print("[pygame_emojis] Extract the zip file to ", _EMOJIS_DIR)
    zipfile.extractall(_EMOJIS_DIR)


if __name__ == "__main__":
    # Dowload the raw data
    download()
