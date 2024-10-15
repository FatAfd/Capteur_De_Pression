# Python script to generate Eagle .scr file for creating a component with pins

component_name = "MyComponent"
num_pins = 4

# Create .scr content
scr_content = f"""
GRID MM;
LAYER 1;

# Create component
ADD {component_name} U 0 0 0;

# Add pins to the component
"""
for pin_number in range(1, num_pins + 1):
    scr_content += f"ADD {component_name} {pin_number} {pin_number * 2} 90;\n"

# Save to .scr file
with open("create_component.scr", "w") as scr_file:
    scr_file.write(scr_content)

