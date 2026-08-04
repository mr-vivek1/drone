from ursina import color, Vec2

# ==========================
# UI Layout Dimensions
# ==========================
PANEL_WIDTH = 0.25            # Relative to window aspect
PANEL_MARGIN_X = 0.01
PANEL_MARGIN_Y = 0.02

# ==========================
# Component Dimensions
# ==========================
BUTTON_HEIGHT = 0.04
TEXT_SIZE_HEADER = 1.0
TEXT_SIZE_NORMAL = 0.8

SPACING_LARGE = 0.05
SPACING_SMALL = 0.02

# ==========================
# Colors (Professional Light Theme)
# ==========================
COLOR_BG = color.hex('#f0f0f0')       # Light gray background
COLOR_TEXT = color.hex('#222222')     # Almost black text
COLOR_TEXT_DIM = color.hex('#555555') # Dark gray labels

COLOR_BUTTON = color.hex('#e0e0e0')   # Standard button
COLOR_BUTTON_HOVER = color.hex('#d0d0d0') 

COLOR_SELECTED = color.hex('#3498db') # Blue selection
COLOR_SELECTED_TEXT = color.white

COLOR_DELETE = color.hex('#e74c3c')   # Red danger action
COLOR_DELETE_HOVER = color.hex('#c0392b')
COLOR_DELETE_TEXT = color.white

# ==========================
# Styling
# ==========================
BUTTON_RADIUS = 0.1 # Slight rounded corners if supported by Ursina
