import os
import glob
import re

def fix_car_filenames():
    print("🔧 FIXING CAR FILENAMES")
    print("=" * 50)
    
    original_cars_dir = "original_cars"
    
    if not os.path.exists(original_cars_dir):
        print("❌ original_cars folder not found!")
        return
    
    # Find all image files
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
        image_files.extend(glob.glob(os.path.join(original_cars_dir, ext)))
    
    if not image_files:
        print("❌ No car images found!")
        return
    
    print(f"📁 Found {len(image_files)} image(s) to fix:")
    
    fixed_count = 0
    for old_path in image_files:
        # Get filename without path
        old_name = os.path.basename(old_path)
        
        # Create new clean filename
        new_name = re.sub(r'[^a-zA-Z0-9\.]', '_', old_name)  # Replace special chars with _
        new_name = new_name.replace('__', '_').replace('__', '_')  # Remove double underscores
        new_name = new_name.lower()  # Make lowercase
        
        # If name didn't change, skip
        if new_name == old_name.lower():
            print(f"   ✅ {old_name} (already good)")
            continue
        
        new_path = os.path.join(original_cars_dir, new_name)
        
        # Rename file
        os.rename(old_path, new_path)
        print(f"   🔄 {old_name} → {new_name}")
        fixed_count += 1
    
    print(f"\n✨ Fixed {fixed_count} filename(s)")
    print("🎯 Now run the 3D generator again!")

if __name__ == "__main__":
    fix_car_filenames()