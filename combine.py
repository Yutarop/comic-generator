from PIL import Image


def combine_images_vertical(image_paths, output_path):
    """
    Combine multiple PNG images vertically and save them as a new file.

    :param image_paths: List of file paths to the images to be combined
    :param output_path: Path where the combined image will be saved
    """
    if not image_paths:
        print("Error: No image files specified for combining.")
        return

    # 1. Open all images
    try:
        images = [Image.open(path).convert("RGBA") for path in image_paths]
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return
    except Exception as e:
        print(f"An error occurred while opening the images: {e}")
        return

    # 2. Calculate the width and height of the combined image
    widths, heights = zip(*(img.size for img in images))
    max_width = max(widths)
    total_height = sum(heights)

    # 3. Create a new blank image
    combined_img = Image.new("RGBA", (max_width, total_height))

    # 4. Paste each image onto the new canvas
    y_offset = 0
    for img in images:
        combined_img.paste(img, (0, y_offset))
        y_offset += img.height

    # 5. Save the combined image
    try:
        combined_img.save(output_path, "PNG")
        print(f"Images successfully combined and saved to '{output_path}'.")
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")
