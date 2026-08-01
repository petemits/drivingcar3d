from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import os
import glob
from datetime import datetime
import math
import random

class ExactCarMotion3D:
    def __init__(self):
        self.output_folder = "exact_car_motion"
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def load_exact_car(self, image_path):
        """Load car image without any changes to the car itself"""
        try:
            car_img = Image.open(image_path).convert('RGBA')
            print(f"✅ Loaded: {os.path.basename(image_path)} - Size: {car_img.size}")
            return car_img
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def create_driving_scene(self, car_image, scene_type="highway"):
        """Create driving scene with exact car and motion effects"""
        # Use larger scene for better quality
        scene_width, scene_height = 1200, 800
        
        # Create scene background
        scene = self.create_scene_background(scene_width, scene_height, scene_type)
        draw = ImageDraw.Draw(scene)
        
        # Draw 3D road
        self.draw_3d_road(draw, scene_width, scene_height)
        
        # Draw environment
        self.draw_environment(draw, scene_width, scene_height, scene_type)
        
        # Prepare exact car (no resizing if possible, or minimal high-quality resize)
        car_processed = self.prepare_exact_car(car_image, scene_width)
        
        # Calculate car position (centered on road)
        car_x = scene_width // 2 - car_processed.width // 2
        car_y = scene_height - car_processed.height - 60
        
        # Add car shadow first
        self.add_realistic_shadow(draw, car_x, car_y, car_processed.width, car_processed.height)
        
        # Add road reflection
        scene = self.add_car_reflection(scene, car_processed, car_x, car_y)
        
        # Paste exact car onto scene
        scene.paste(car_processed, (car_x, car_y), car_processed)
        
        # Add motion effects to background (NOT the car)
        scene = self.add_motion_blur_background(scene, car_x, car_y, car_processed.width, car_processed.height)
        
        # Add speed lines
        scene = self.add_speed_lines(scene, car_x, car_y, car_processed.width, car_processed.height)
        
        return scene
    
    def create_scene_background(self, width, height, scene_type):
        """Create background based on scene type"""
        if scene_type == "highway":
            return self.create_highway_background(width, height)
        elif scene_type == "city":
            return self.create_city_background(width, height)
        elif scene_type == "country":
            return self.create_country_background(width, height)
        else:
            return self.create_highway_background(width, height)
    
    def create_highway_background(self, width, height):
        """Create highway background"""
        bg = Image.new('RGB', (width, height), '#87CEEB')
        draw = ImageDraw.Draw(bg)
        
        # Sky gradient
        for y in range(height // 2):
            blue_val = 135 + (120 * y / (height // 2))
            color = (70, 130, int(blue_val))
            draw.line([(0, y), (width, y)], fill=color)
        
        # Distant mountains
        mountain_points = [
            (0, height // 2), (200, height // 3), (400, height // 2),
            (600, height // 4), (800, height // 2), (1000, height // 3), (width, height // 2)
        ]
        draw.polygon(mountain_points, fill='#78909C')
        
        return bg
    
    def create_city_background(self, width, height):
        """Create city background"""
        bg = Image.new('RGB', (width, height), '#1e88e5')
        draw = ImageDraw.Draw(bg)
        
        # Sky gradient (darker for city)
        for y in range(height // 2):
            blue_val = 100 + (100 * y / (height // 2))
            color = (30, 80, int(blue_val))
            draw.line([(0, y), (width, y)], fill=color)
        
        # City skyline
        buildings = [
            (0, 150), (80, 120), (120, 180), (200, 100), (280, 160),
            (350, 140), (420, 190), (500, 130), (580, 170), (650, 110),
            (720, 150), (800, 180), (880, 140), (960, 160), (width, 150)
        ]
        
        # Fill below skyline
        buildings.append((width, height // 2))
        buildings.append((0, height // 2))
        draw.polygon(buildings, fill='#37474f')
        
        return bg
    
    def create_country_background(self, width, height):
        """Create country road background"""
        bg = Image.new('RGB', (width, height), '#64b5f6')
        draw = ImageDraw.Draw(bg)
        
        # Sky gradient
        for y in range(height // 2):
            blue_val = 150 + (105 * y / (height // 2))
            color = (100, 180, int(blue_val))
            draw.line([(0, y), (width, y)], fill=color)
        
        # Hills
        hill_points = [
            (0, height // 2), (150, height // 2 - 50), (300, height // 2),
            (450, height // 2 - 30), (600, height // 2), (750, height // 2 - 40),
            (900, height // 2), (width, height // 2 - 20)
        ]
        draw.polygon(hill_points, fill='#388e3c')
        
        return bg
    
    def draw_3d_road(self, draw, width, height):
        """Draw 3D perspective road with FIXED boundary checking"""
        # Road surface with strong perspective
        road_top_width = width // 6
        road_bottom_width = width
        
        road_points = [
            (width // 2 - road_bottom_width // 2, height),      # Bottom left
            (width // 2 + road_bottom_width // 2, height),      # Bottom right  
            (width // 2 + road_top_width // 2, height // 2),    # Top right
            (width // 2 - road_top_width // 2, height // 2)     # Top left
        ]
        
        draw.polygon(road_points, fill='#424242')
        
        # Road markings with perspective
        self.draw_perspective_road_markings(draw, width, height)
    
    def draw_perspective_road_markings(self, draw, width, height):
        """Draw road markings that converge in distance - FIXED VERSION"""
        # Center line (gets smaller as it goes back)
        for i in range(8):  # Reduced from 10 to avoid going too high
            y_start = height - (i * 60)
            y_end = y_start - max(10, 25 - i * 2)
            
            # FIX: Ensure y_end is above y_start and within bounds
            if y_end >= y_start or y_end < height // 2:
                continue
                
            line_width = max(2, 8 - i * 0.7)
            
            # Calculate width at this perspective point
            perspective_factor = 1.0 - (i * 0.08)
            current_width = line_width * perspective_factor
            
            # FIX: Ensure coordinates are valid
            x1 = max(0, width // 2 - current_width // 2)
            x2 = min(width, width // 2 + current_width // 2)
            y1 = min(y_start, height - 1)
            y2 = max(y_end, height // 2 + 1)
            
            if x1 < x2 and y1 > y2:  # Ensure valid rectangle
                draw.rectangle([x1, y1, x2, y2], fill='#ffeb3b')
        
        # Lane markings - FIXED VERSION
        for lane in [-1, 1]:
            for i in range(6):  # Reduced from 8
                y_start = height - (i * 70)
                y_end = y_start - 15
                
                # FIX: Check bounds
                if y_end >= y_start or y_end < height // 2:
                    continue
                
                # Calculate lane position with perspective
                base_offset = 180  # Reduced from 200
                perspective_reduction = i * 25
                x_offset = (base_offset - perspective_reduction) * lane
                x_center = width // 2 + x_offset
                
                # FIX: Ensure within bounds
                if 0 <= x_center - 2 < x_center + 2 <= width and y_end < y_start:
                    draw.rectangle([
                        (x_center - 2, y_start),
                        (x_center + 2, y_end)
                    ], fill='#ffeb3b')
    
    def draw_environment(self, draw, width, height, scene_type):
        """Draw environment elements"""
        if scene_type == "highway":
            self.draw_highway_environment(draw, width, height)
        elif scene_type == "city":
            self.draw_city_environment(draw, width, height)
        elif scene_type == "country":
            self.draw_country_environment(draw, width, height)
    
    def draw_highway_environment(self, draw, width, height):
        """Draw highway environment elements"""
        # Road signs
        for i in range(3):  # Reduced from 4
            sign_x = 200 + i * 300  # Adjusted spacing
            sign_y = height // 2 + i * 40
            sign_size = 25 - i * 3
            
            # FIX: Check bounds
            if sign_x >= 0 and sign_x + sign_size <= width and sign_y >= height // 2:
                draw.rectangle([
                    (sign_x, sign_y),
                    (sign_x + sign_size, sign_y + sign_size * 1.5)
                ], fill='#f44336')
    
    def draw_city_environment(self, draw, width, height):
        """Draw city environment elements"""
        # Buildings along road
        for i in range(5):  # Reduced from 6
            building_x = 150 + i * 200  # Adjusted spacing
            building_height = 80 + (i % 3) * 40
            building_width = 60
            
            # FIX: Check bounds
            if (building_x >= 0 and building_x + building_width <= width and 
                height // 2 - building_height >= 0):
                draw.rectangle([
                    (building_x, height // 2 - building_height),
                    (building_x + building_width, height // 2)
                ], fill='#455a64')
    
    def draw_country_environment(self, draw, width, height):
        """Draw country environment elements"""
        # Trees
        for i in range(6):  # Reduced from 8
            tree_x = 150 + i * 150  # Adjusted spacing
            tree_size = 40 + (i % 2) * 20
            
            # FIX: Check bounds
            if (tree_x - tree_size//2 >= 0 and tree_x + tree_size//2 <= width and
                height // 2 - tree_size - 10 >= 0):
                
                # Tree top
                draw.ellipse([
                    (tree_x - tree_size//2, height // 2 - tree_size - 10),
                    (tree_x + tree_size//2, height // 2 - 10)
                ], fill='#2e7d32')
                
                # Tree trunk
                draw.rectangle([
                    (tree_x - 3, height // 2 - 10),
                    (tree_x + 3, height // 2)
                ], fill='#5d4037')
    
    def prepare_exact_car(self, car_image, scene_width):
        """Prepare car image while maintaining exact appearance"""
        # Calculate maximum car size that fits scene
        max_car_width = scene_width // 3
        
        if car_image.width <= max_car_width:
            # Use original size if it fits
            return car_image
        else:
            # Resize but maintain aspect ratio with high quality
            new_width = max_car_width
            new_height = int(car_image.height * (new_width / car_image.width))
            
            # Use LANCZOS for highest quality resampling
            car_resized = car_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"🔧 Resized car: {car_image.size} -> {car_resized.size} (high quality)")
            return car_resized
    
    def add_realistic_shadow(self, draw, car_x, car_y, car_width, car_height):
        """Add realistic car shadow on road"""
        shadow_y = car_y + car_height
        shadow_height = 15  # Reduced height
        
        # FIX: Ensure shadow is within bounds
        if shadow_y + shadow_height <= 800:  # Scene height
            # Shadow points (slightly wider than car)
            shadow_points = [
                (max(0, car_x - 8), shadow_y),
                (min(1200, car_x + car_width + 8), shadow_y),  # Scene width
                (min(1200, car_x + car_width - 3), shadow_y + shadow_height),
                (max(0, car_x + 3), shadow_y + shadow_height)
            ]
            
            # Draw shadow
            draw.polygon(shadow_points, fill=(0, 0, 0, 100))
    
    def add_car_reflection(self, scene, car_image, car_x, car_y):
        """Add car reflection on road surface"""
        # Create flipped version for reflection
        reflection = car_image.transpose(Image.FLIP_TOP_BOTTOM)
        
        # Make reflection transparent and distorted
        reflection = reflection.convert('RGBA')
        reflection_data = np.array(reflection)
        
        # Apply reflection effect (darker, more transparent)
        reflection_data[:,:,3] = reflection_data[:,:,3] // 4  # More transparent
        reflection_data[:,:,:3] = reflection_data[:,:,:3] // 3  # Darker
        
        reflection = Image.fromarray(reflection_data)
        
        # Position reflection - FIXED: Ensure within bounds
        reflection_y = min(car_y + car_image.height, 800 - reflection.height)
        reflection_x = max(0, car_x - 3)
        
        if reflection_y + reflection.height <= 800:  # Scene height
            scene.paste(reflection, (reflection_x, reflection_y), reflection)
        
        return scene
    
    def add_motion_blur_background(self, scene, car_x, car_y, car_width, car_height):
        """Add motion blur to background only (not the car)"""
        try:
            # Convert to numpy for processing
            scene_np = np.array(scene)
            
            # Simple motion blur using PIL instead of scipy
            # Create a temporary blurred version
            blurred_scene = scene.filter(ImageFilter.GaussianBlur(2))
            blurred_np = np.array(blurred_scene)
            
            # Create mask to protect car area
            mask = np.ones(scene_np.shape[:2], dtype=bool)
            
            # Protect car area plus margin
            margin = 15
            y_start = max(0, car_y - margin)
            y_end = min(scene_np.shape[0], car_y + car_height + margin)
            x_start = max(0, car_x - margin)
            x_end = min(scene_np.shape[1], car_x + car_width + margin)
            
            mask[y_start:y_end, x_start:x_end] = False
            
            # Blend based on mask
            result = scene_np.copy()
            for channel in range(3):
                result[:,:,channel] = np.where(
                    mask, 
                    blurred_np[:,:,channel], 
                    scene_np[:,:,channel]
                )
            
            return Image.fromarray(result.astype(np.uint8))
            
        except Exception as e:
            print(f"⚠️  Motion blur failed: {e}. Using original image.")
            return scene
    
    def add_speed_lines(self, scene, car_x, car_y, car_width, car_height):
        """Add speed lines for motion effect"""
        draw = ImageDraw.Draw(scene, 'RGBA')
        
        # Add speed lines coming from behind car - FIXED bounds
        for i in range(10):  # Reduced from 15
            line_x = car_x + car_width + random.randint(0, 80)  # Reduced range
            line_y = car_y + random.randint(10, car_height - 10)  # Stay within car height
            
            # FIX: Ensure lines are within scene bounds
            if line_x < 1200:  # Scene width
                line_length = random.randint(30, 100)  # Reduced length
                end_x = min(1200, line_x + line_length)
                
                draw.line([
                    (line_x, line_y),
                    (end_x, line_y)
                ], fill=(255, 255, 255, 80), width=1)  # Reduced opacity and width
        
        return scene
    
    def generate_all_scenes(self, image_path):
        """Generate multiple driving scenes for one car"""
        car_image = self.load_exact_car(image_path)
        if car_image is None:
            return []
        
        scene_types = ["highway", "city", "country"]
        generated_files = []
        
        for scene_type in scene_types:
            print(f"🎬 Creating {scene_type} driving scene...")
            try:
                scene = self.create_driving_scene(car_image, scene_type)
                
                # Save with descriptive filename
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                timestamp = datetime.now().strftime("%H%M%S")
                filename = f"{self.output_folder}/{base_name}_{scene_type}_driving_{timestamp}.jpg"
                
                scene.save(filename, quality=95)
                generated_files.append((scene_type, filename))
                print(f"✅ Created: {filename}")
                
            except Exception as e:
                print(f"❌ Failed to create {scene_type} scene: {e}")
                continue
        
        return generated_files

def main():
    generator = ExactCarMotion3D()
    
    print("🚗 EXACT CAR MOTION 3D GENERATOR - FIXED VERSION")
    print("🎯 Preserving your car exactly + adding 3D motion effects")
    print("=" * 60)
    
    # Find car images
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
        image_files.extend(glob.glob(ext))
    
    # Remove debug and output files from processing
    image_files = [f for f in image_files if not any(x in f.lower() for x in ['debug', 'road_', 'sample'])]
    
    if not image_files:
        print("❌ No car images found!")
        print("💡 Add your car image to this folder")
        return
    
    print(f"📁 Found {len(image_files)} image(s)")
    for img in image_files:
        print(f"   🖼️  {img}")
    
    all_generated = []
    
    for image_file in image_files:
        print(f"\n🎯 Processing: {image_file}")
        scenes = generator.generate_all_scenes(image_file)
        all_generated.extend(scenes)
    
    print("\n" + "=" * 60)
    if all_generated:
        print(f"✨ SUCCESS! Created {len(all_generated)} driving scenes!")
        print(f"📁 Location: {os.path.abspath(generator.output_folder)}")
        print("\n🎬 Driving scenes created:")
        for scene_type, filepath in all_generated:
            print(f"   • {scene_type}: {os.path.basename(filepath)}")
    else:
        print("❌ No scenes were created due to errors.")

if __name__ == "__main__":
    main()