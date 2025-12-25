import requests
import argparse

parser = argparse.ArgumentParser(description="Download a file from Google Drive.")

parser.add_argument("--url", help="Link of the file to downlad")
parser.add_argument("--output_path", help="The filename to save the download as")
args = parser.parse_args()

# This is a multi-line script, not a one-liner
url = args.url
filename = args.output_path
with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)