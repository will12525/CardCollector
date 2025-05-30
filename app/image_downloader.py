import pathlib
import requests
import time

def download_image(card_tcgp_id, destination_path):
    url = f"https://tcgplayer-cdn.tcgplayer.com/product/{card_tcgp_id}_200w.jpg"
    file_name = f"{card_tcgp_id}.jpg"
    print(url, file_name)
    try:
        # Check if the image file already exists
        image_path = pathlib.Path(destination_path, file_name).resolve()
        if not image_path.exists():
            print(image_path)
            # Download the image data only if the file doesn't exist
            image_response = requests.get(url, stream=True)
            image_response.raise_for_status()

            # Save the image to the specified file
            with open(image_path, "wb") as f:
                for chunk in image_response.iter_content(1024):
                    f.write(chunk)

            print(f"Image downloaded: {file_name}")
            time.sleep(0.5)
        else:
            print(f"Image already exists: {file_name}")
    except Exception as e:
        print(f"Error downloading image: {e}")
