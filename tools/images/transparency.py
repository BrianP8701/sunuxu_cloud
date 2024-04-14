from PIL import Image

def fade_image(image_path, fade_factor):
    """
    Applies a fading effect to an image by blending it with a white background.
    :param image_path: Path to the image file.
    :param fade_factor: Integer between 1 and 100 indicating the fade percentage.
    """
    # Ensure fade_factor is within the expected range
    if not 1 <= fade_factor <= 100:
        raise ValueError("Fade factor must be between 1 and 100.")
    
    # Open the image
    img = Image.open(image_path).convert("RGBA")
    
    # Create a white background image
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    
    # Calculate the alpha for blending
    alpha = fade_factor / 100
    
    # Blend the original image with the white background
    faded_img = Image.blend(white_bg, img, alpha)
    
    # Save the faded image
    faded_img_path = image_path.replace(".jpeg", "_faded.png")  # Ensure saving as PNG to preserve transparency
    faded_img.save(faded_img_path, "PNG")
    
    return faded_img_path

def convert_webp_to_jpeg(image_path):
    """
    Converts a WEBP image to JPEG format.
    :param image_path: Path to the WEBP image file.
    """
    if not image_path.lower().endswith(".webp"):
        raise ValueError("Input file must be a WEBP image.")
    
    # Open the WEBP image
    img = Image.open(image_path)
    
    # Define the output path
    output_path = image_path.replace(".webp", ".jpeg")
    
    # Convert and save the image in JPEG format
    img.convert("RGB").save(output_path, "jpeg")
    
    return output_path


fade_image("ooga.webp", 20)
convert_webp_to_jpeg("ooga.webp")