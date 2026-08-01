import os
import glob
from PIL import Image, ImageDraw
import numpy as np
from datetime import datetime

def debug_folder_contents():
    """Show exactly what's in the folder"""
    print("🔍 DEBUG: Checking folder contents...")
    print(f"📁 Current folder: {os.path.abspath('.')}")
    print("\n📋 ALL FILES IN FOLDER:")
    
    all_files = os.listdir('.')
    if not all_files:
        print("   ❌ Folder is EMPTY!")
        return []
    
    for i, file in enumerate(all_files):
        file_path = os.path.join('.', file)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            print(f"   {i+1}. 📄 {file} ({file_size} bytes)")
        else:
            print(f"   {i+1}. 📁 {file}/")
    
    return all_files

def find_images():
    """Find all image files with detailed debugging"""
    print("\n🎯 Looking for image files...")
    
    image_extensions = [
        '*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp',
        '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.TIFF', '*.WEBP'
    ]
    
    found_images = []
    
    for extension in image_extensions:
        matches = glob.glob(extension)
        if matches:
            print(f"   ✅ Found {extension}: {matches}")
            found_images.extend(matches)
        else:
            print(f"   ❌ No {extension} files found")
    
    return found_images

def create_sample_car_image():
    """Create a sample car image if none exists"""
    print("\n🔄 Creating sample car image for testing...")
    
    # Create a simple car image
    img = Image.new('RGB', (400, 200), color='red')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple car
    draw.rectangle([50, 80, 350, 150], fill='blue')  # Car body
    draw.rectangle([70, 60, 150, 80], fill='blue')   # Car top
    draw.rectangle([200, 60, 280, 80], fill='blue')  # Car top
    draw.ellipse([80, 140, 140, 180], fill='black')  # Wheel
    draw.ellipse([260, 140, 320, 180], fill='black') # Wheel
    
    # Save sample image
    sample_path = "sample_car_debug.jpg"
    img.save(sample_path, quality=95)
    print(f"✅ Created sample image: {sample_path}")
    return sample_path

def quick_3d_scene(image_path):
    """Create a quick 3D scene to test"""
    print(f"\n🎨 Creating 3D scene with: {image_path}")
    
    try:
        # Load the image
        car_img = Image.open(image_path)
        print(f"   ✅ Image loaded: {car_img.size}")
        
        # Create simple scene
        scene = Image.new('RGB', (800, 600), '#87CEEB')
        draw = ImageDraw.Draw(scene)
        
        # Draw simple road
        draw.rectangle([200, 300, 600, 600], fill='#333333')
        
        # Add road lines
        for i in range(5):
            y = 400 + i * 40
            draw.rectangle([390, y, 410, y+20], fill='yellow')
        
        # Resize and place car
        car_resized = car_img.resize((200, 100))
        scene.paste(car_resized, (300, 450))
        
        # Save result
        output_path = "debug_3d_scene.jpg"
        scene.save(output_path, quality=95)
        print(f"✅ Created 3D scene: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error creating scene: {e}")
        return None

def main():
    print("🚗 CAR ON ROAD 3D - DEBUG VERSION")
    print("=" * 60)
    
    # Step 1: Check folder contents
    all_files = debug_folder_contents()
    
    # Step 2: Find images
    images = find_images()
    
    if not images:
        print("\n❌ PROBLEM: No car images found!")
        print("\n💡 SOLUTION: You need to:")
        print("   1. Add your car image to this folder")
        print("   2. OR Use the sample image I'll create")
        
        # Create sample image for testing
        sample_path = create_sample_car_image()
        images = [sample_path]
    
    print(f"\n🎯 IMAGES TO PROCESS: {images}")
    
    # Step 3: Test with first image
    if images:
        first_image = images[0]
        result = quick_3d_scene(first_image)
        
        if result:
            print(f"\n✨ SUCCESS! Test completed.")
            print(f"📁 Your 3D scene: {os.path.abspath(result)}")
            print(f"📁 Your original image: {os.path.abspath(first_image)}")
        else:
            print("\n❌ Failed to create 3D scene")
    
    print("\n" + "=" * 60)
    print("📝 NEXT STEPS:")
    print("1. If this worked, run the main script: python car_on_road_3d.py")
    print("2. Make sure your car image is in this folder")
    print("3. Supported formats: JPG, PNG, BMP, etc.")
    print("4. File names should be simple (no special characters)")

if __name__ == "__main__":
    main()