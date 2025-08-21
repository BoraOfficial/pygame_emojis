from io import BytesIO
import pathlib
from zipfile import ZipFile
from urllib.request import urlopen

try:
    import cairosvg
    cairo_installed = True
except OSError: # OSError: no library called "cairo-2" was found
    cairo_installed = False


_EMOJIS_DIR: pathlib.Path = pathlib.Path(__file__).parent / "emojis"


def download():
    base_url = "https://github.com/hfg-gmuend/openmoji/releases/latest/download/"

    zip_url = f"{base_url}{'openmoji-svg-color.zip' if cairo_installed else 'openmoji-618x618-color.zip'}"

    """Download the emojis from openmoji."""
    print("[pygame_emojis] Download the zip file from ", zip_url)
    resp = urlopen(zip_url)
    zipfile = ZipFile(BytesIO(resp.read()))

    print("[pygame_emojis] Extract the zip file to ", _EMOJIS_DIR)
    zipfile.extractall(_EMOJIS_DIR)


if __name__ == "__main__":
    # Dowload the raw data
    download()
