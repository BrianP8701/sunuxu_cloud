from PIL import Image
import os

def make_image_square(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        if width == height:
            print("Image is already square.")
            return
        new_size = max(width, height)
        new_img = Image.new("RGB", (new_size, new_size), (0, 0, 0))
        paste_position = ((new_size - width) // 2, (new_size - height) // 2)
        new_img.paste(img, paste_position)
        # Extract directory and filename to construct new path correctly
        dir_name, file_name = os.path.split(image_path)
        new_image_path = os.path.join(dir_name, f"square_{file_name}")
        new_img.save(new_image_path)
        print(f"Square image saved to {new_image_path}")

# Example usage
make_image_square("/Users/brianprzezdziecki/Downloads/ww.jpeg")
make_image_square("/Users/brianprzezdziecki/Downloads/qq.jpeg")
