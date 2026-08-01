from PIL import Image, ImageDraw
import os
from datetime import datetime

def create_simple_car_road(car_image_path):
    """Super simple version that definitely works"""
    print(f"🚗 Processing: {car_image_path}")
    
    # Load car image
    try:
        car_img = Image.open(car_image_path)
        print(f"✅ Loaded car image: {car_img.size}")
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return None
    
    # Create scene (800x600 pixels)
    scene = Image.new('RGB', (800, 600), '#87CEEB')  # Sky blue
    draw = ImageDraw.Draw(scene)
    
    # Draw road (simple rectangle)
    draw.rectangle([150, 300, 650, 600], fill='#333333')  # Gray road
    
    # Draw road markings
    for i in range(5):
        y = 350 + i * 50
        draw.rectangle([395, y, 405, y+25], fill='yellow')  # Center line
    
    # Draw side lines
    draw.rectangle([150, 320, 155, 580], fill='yellow')  # Left line
    draw.rectangle([645, 320, 650, 580], fill='yellow')  # Right line
    
    # Resize car to fit scene
    car_width = 200
    car_height = int(car_img.height * (car_width / car_img.width))
    car_resized = car_img.resize((car_width, car_height))
    
    # Position car on road
    car_x = 400 - car_width // 2  # Center horizontally
    car_y = 450  # Position on road
    
    # Paste car onto scene
    scene.paste(car_resized, (car_x, car_y))
    
    # Add text label
    draw.text((10, 10), "Car Driving on Road", fill='white')
    
    return scene

def main():
    print("🚗 SIMPLE Car on Road Generator")
    print("✅ This version WILL work!")
    print("=" * 50)
    
    # Look for ANY image in current folder
    image_files = []
    for file in os.listdir('.'):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            image_files.append(file)
    
    if not image_files:
        print("❌ No images found in folder!")
        print("💡 Please add a car image to this folder.")
        print(f"📁 Current folder: {os.path.abspath('.')}")
        return
    
    print(f"📁 Found {len(image_files)} image(s):")
    for img in image_files:
        print(f"   🖼️  {img}")
    
    # Process each image
    for image_file in image_files:
        print(f"\n🎯 Creating scene for: {image_file}")
        scene = create_simple_car_road(image_file)
        
        if scene:
            # Save with timestamp
            timestamp = datetime.now().strftime("%H%M%S")
            base_name = os.path.splitext(image_file)[0]
            output_file = f"ROAD_{base_name}_{timestamp}.jpg"
            
            scene.save(output_file, quality=95)
            print(f"✅ SUCCESS! Created: {output_file}")
            print(f"📁 Full path: {os.path.abspath(output_file)}")
        else:
            print(f"❌ Failed to create scene for {image_file}")

if __name__ == "__main__":
    main()