import os
import shutil
from datetime import datetime

def organize_project():
    print("📁 ORGANIZING PROJECT FILES")
    print("=" * 50)
    
    # Create organized folder structure
    folders = {
        'original_cars': 'Put your REAL car images here',
        '3d_results': '3D driving scenes will be saved here', 
        'debug_files': 'Debug and test files',
        'scripts': 'Python scripts'
    }
    
    for folder, description in folders.items():
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ Created: {folder}/ - {description}")
    
    # Move files to appropriate folders
    files_moved = 0
    
    # Move Python scripts
    for file in os.listdir('.'):
        if file.endswith('.py') and os.path.isfile(file):
            shutil.move(file, f'scripts/{file}')
            print(f"📄 Moved script: {file} → scripts/")
            files_moved += 1
    
    # Move debug files
    debug_files = ['debug_3d_scene.jpg', 'sample_car_debug.jpg', 'test_folder.py']
    for file in debug_files:
        if os.path.exists(file):
            shutil.move(file, f'debug_files/{file}')
            print(f"🐛 Moved debug: {file} → debug_files/")
            files_moved += 1
    
    # Move existing 3D results
    for file in os.listdir('.'):
        if file.startswith('3D_DRIVING_') or file.startswith('ROAD_') or 'driving' in file.lower():
            if os.path.isfile(file):
                shutil.move(file, f'3d_results/{file}')
                print(f"🎯 Moved 3D result: {file} → 3d_results/")
                files_moved += 1
    
    print(f"\n✨ Organized {files_moved} files!")
    print("\n📁 NEW FOLDER STRUCTURE:")
    print("drivingcar3d/")
    print("├── 📁 original_cars/     ← PUT YOUR REAL CAR PHOTOS HERE")
    print("├── 📁 3d_results/        ← 3D driving scenes will appear here") 
    print("├── 📁 scripts/           ← All Python scripts")
    print("├── 📁 debug_files/       ← Test and debug files")
    print("└── 📁 exact_car_motion/  ← Previous outputs")
    
    print("\n🎯 NEXT: Add your real car photos to 'original_cars/' folder!")

if __name__ == "__main__":
    organize_project()