import gdown
import argparse

def download_from_drive():
    parser = argparse.ArgumentParser(description="Download a file from Google Drive.")

    # 1. First required argument: The File ID
    parser.add_argument("file_id", help="The Google Drive File ID")
    
    # 2. Second required argument: The Output Path
    # By removing the '--' and 'default', this becomes mandatory
    parser.add_argument("output_path", help="The filename to save the download as")

    args = parser.parse_args()

    file_id = args.file_id
    output_path = args.output_path

    print(f"Downloading File ID: {file_id}")
    print(f"Saving to: {output_path}")

    url = f'https://drive.google.com/uc?id={file_id}'
    
    try:
        gdown.download(url, output_path, quiet=False)
        print(f"File downloaded successfully to: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_from_drive()