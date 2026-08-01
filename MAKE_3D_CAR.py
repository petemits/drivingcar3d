import os
import sys
from PIL import Image, ImageDraw, ImageFilter
import glob
from datetime import datetime

# Add scripts folder to path so we can import from it
sys.path.append('scripts')

def main():
    print("🚗 CAR 3D DRIVING SCENE GENERATOR")
    print("=" * 50)
    
    # Check if original_cars folder exists and has images
    original_cars_dir = "original_cars"
    output_dir = "3d_results"
    
    if not os.path.exists(original_cars_dir):
        print(f"❌ Folder '{original_cars_dir}' not found!")
        print("💡 Please run the organizer script first")
        return
    
    # Find car images
    car_images = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
        car_images.extend(glob.glob(os.path.join(original_cars_dir, ext)))
    
    if not car_images:
        print("❌ No car photos found in 'original_cars' folder!")
        print(f"\n💡 WHAT TO DO:")
        print(f"1. Open the '{original_cars_dir}' folder")
        print(f"2. Copy your real car photos into it")
        print(f"3. Run this script again")
        print(f"\n📁 Folder location: {os.path.abspath(original_cars_dir)}")
        return
    
    print(f"✅ Found {len(car_images)} car photo(s):")
    for img in car_images:
        print(f"   🖼️  {os.path.basename(img)}")
    
    # Create output folder
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"\n🎬 Creating 3D driving scenes...")
    
    # Process each car image
    successful_creations = 0
    
    for car_path in car_images:
        try:
            print(f"\n🚗 Processing: {os.path.basename(car_path)}")
            
            # Load car image
            car_img = Image.open(car_path).convert('RGBA')
            car_name = os.path.splitext(os.path.basename(car_path))[0]
            
            # Create different scene types
            scene_types = ["highway", "city_road", "countryside", "mountain_pass"]
            
            for scene_type in scene_types:
                # Create scene
                scene = create_3d_scene(car_img, scene_type)
                
                # Save scene
                timestamp = datetime.now().strftime("%H%M%S")
                output_filename = f"{car_name}_{scene_type}_{timestamp}.jpg"
                output_path = os.path.join(output_dir, output_filename)
                
                scene.save(output_path, quality=95)
                print(f"   ✅ {scene_type}: {output_filename}")
                successful_creations += 1
        
        except Exception as e:
            print(f"   ❌ Error with {os.path.basename(car_path)}: {e}")
            continue
    
    print(f"\n✨ SUCCESSFULLY CREATED {successful_creations} 3D DRIVING SCENES!")
    print(f"📁 View your results in: {os.path.abspath(output_dir)}")
    print(f"\n🎯 You can now:")
    print(f"   • Share your 3D car scenes")
    print(f"   • Add more car photos to '{original_cars_dir}' and run again")
    print(f"   • Use the images for social media, presentations, etc.")

def create_3d_scene(car_img, scene_type):
    """Create a 3D driving scene with the car"""
    width, height = 1200, 800
    
    # Create background based on scene type
    if scene_type == "highway":
        scene = create_highway_scene(width, height)
    elif scene_type == "city_road":
        scene = create_city_scene(width, height)
    elif scene_type == "countryside":
        scene = create_countryside_scene(width, height)
    else:  # mountain_pass
        scene = create_mountain_scene(width, height)
    
    draw = ImageDraw.Draw(scene)
    
    # Draw 3D road
    draw_3d_road(draw, width, height)
    
    # Prepare car
    car_width = 400
    car_height = int(car_img.height * (car_width / car_img.width))
    car_resized = car_img.resize((car_width, car_height), Image.Resampling.LANCZOS)
    
    # Position car on road
    car_x = width // 2 - car_width // 2
    car_y = height - car_height - 80
    
    # Add shadow
    draw.rectangle([
        car_x - 15, car_y + car_height,
        car_x + car_width + 15, car_y + car_height + 20
    ], fill=(0, 0, 0, 100))
    
    # Paste car
    scene.paste(car_resized, (car_x, car_y), car_resized)
    
    return scene

def create_highway_scene(width, height):
    """Create highway background"""
    scene = Image.new('RGB', (width, height), '#87CEEB')
    draw = ImageDraw.Draw(scene)
    
    # Sky gradient
    for y in range(height // 2):
        blue_val = 135 + (120 * y / (height // 2))
        draw.line([(0, y), (width, y)], fill=(70, 130, int(blue_val)))
    
    # Distant mountains
    draw.polygon([
        (0, height//2), (300, height//3), (600, height//2),
        (900, height//4), (width, height//2)
    ], fill='#78909C')
    
    return scene

def create_city_scene(width, height):
    """Create city background"""
    scene = Image.new('RGB', (width, height), '#1e88e5')
    draw = ImageDraw.Draw(scene)
    
    # Darker sky
    for y in range(height // 2):
        blue_val = 100 + (100 * y / (height // 2))
        draw.line([(0, y), (width, y)], fill=(30, 80, int(blue_val)))
    
    # Buildings
    for i in range(8):
        b_x = i * 150
        b_height = 100 + (i % 3) * 50
        draw.rectangle([b_x, height//2 - b_height, b_x + 120, height//2], fill='#37474f')
    
    return scene

def create_countryside_scene(width, height):
    """Create countryside background"""
    scene = Image.new('RGB', (width, height), '#64b5f6')
    draw = ImageDraw.Draw(scene)
    
    # Light sky
    for y in range(height // 2):
        blue_val = 150 + (105 * y / (height // 2))
        draw.line([(0, y), (width, y)], fill=(100, 180, int(blue_val)))
    
    # Hills
    draw.polygon([
        (0, height//2), (200, height//2-60), (400, height//2),
        (600, height//2-40), (800, height//2), (width, height//2-30)
    ], fill='#388e3c')
    
    return scene

def create_mountain_scene(width, height):
    """Create mountain background"""
    scene = Image.new('RGB', (width, height), '#42a5f5')
    draw = ImageDraw.Draw(scene)
    
    # Sky
    for y in range(height // 2):
        blue_val = 120 + (135 * y / (height // 2))
        draw.line([(0, y), (width, y)], fill=(50, 150, int(blue_val)))
    
    # Mountains
    draw.polygon([
        (0, height//2), (150, height//3), (300, height//2),
        (450, height//4), (600, height//2), (750, height//3),
        (900, height//2), (width, height//2)
    ], fill='#546e7a')
    
    return scene

def draw_3d_road(draw, width, height):
    """Draw 3D perspective road"""
    # Road surface
    road_points = [
        (0, height), (width, height),           # Bottom
        (width//2 + 250, height//2),           # Top right
        (width//2 - 250, height//2)            # Top left
    ]
    draw.polygon(road_points, fill='#424242')
    
    # Road markings
    for i in range(12):
        y = height - (i * 50)
        if y > height//2 + 50:
            line_width = max(3, 10 - i * 0.6)
            draw.rectangle([
                width//2 - line_width//2, y,
                width//2 + line_width//2, y - 25
            ], fill='yellow')

if __name__ == "__main__":
    main()