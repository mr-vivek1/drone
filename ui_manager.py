from ursina import *
from ui_config import *

class UIManager:
    def __init__(self, swarm, camera_controller):
        self.swarm = swarm
        self.camera_controller = camera_controller
        self.swarm.selection_callback = self.on_drone_selected
        self.selected_drone = None
        
        # -------------------------------------------------
        # UI HELPERS
        # -------------------------------------------------
        def create_header(parent, text, y_pos):
            return Text(text=text, parent=parent, y=y_pos, x=0, origin=(0, 0), 
                        scale=TEXT_SIZE_HEADER, color=COLOR_TEXT)
                        
        def create_button(parent, text, y_pos, click_func, bg_color=COLOR_BUTTON, txt_color=COLOR_TEXT):
            return Button(parent=parent, text=text, y=y_pos, scale=(0.9, BUTTON_HEIGHT), 
                          color=bg_color, text_color=txt_color, on_click=click_func)
                          
        def create_label_value(parent, label_text, y_pos):
            # Left aligned label
            Text(text=label_text, parent=parent, y=y_pos, x=-0.45, origin=(-0.5, 0), scale=TEXT_SIZE_NORMAL, color=COLOR_TEXT_DIM)
            # Right aligned value
            val_text = Text(text="-", parent=parent, y=y_pos, x=0.45, origin=(0.5, 0), scale=TEXT_SIZE_NORMAL, color=COLOR_TEXT)
            return val_text
        
        # -------------------------------------------------
        # LEFT PANEL (Navigation, Spawn, List)
        # -------------------------------------------------
        self.left_bg = Entity(
            parent=camera.ui, 
            model='quad', 
            color=COLOR_BG, 
            scale=(PANEL_WIDTH, 1.0), # full height
            x=0, # set dynamically in update()
            y=0
        )
        
        # Current Y tracking for layout
        cur_y = 0.45
        
        create_header(self.left_bg, "View Controls", cur_y)
        cur_y -= SPACING_LARGE
        create_button(self.left_bg, 'Top View', cur_y, self.camera_controller.top_view)
        cur_y -= BUTTON_HEIGHT + SPACING_SMALL
        create_button(self.left_bg, 'Side View', cur_y, self.camera_controller.side_view)
        cur_y -= BUTTON_HEIGHT + SPACING_SMALL
        create_button(self.left_bg, 'Front View', cur_y, self.camera_controller.front_view)
        cur_y -= BUTTON_HEIGHT + SPACING_SMALL
        create_button(self.left_bg, 'Free Camera', cur_y, self.camera_controller.reset)
        
        cur_y -= SPACING_LARGE * 1.5
        create_header(self.left_bg, "Spawn Drones", cur_y)
        cur_y -= SPACING_LARGE
        self.spawn_input = InputField(parent=self.left_bg, default_value='3', y=cur_y, scale=(0.9, BUTTON_HEIGHT), text_color=COLOR_TEXT, color=color.white)
        cur_y -= BUTTON_HEIGHT + SPACING_SMALL
        create_button(self.left_bg, 'Spawn', cur_y, self.spawn_drones, bg_color=color.white)
        
        cur_y -= SPACING_LARGE * 1.5
        create_header(self.left_bg, "Drone List", cur_y)
        cur_y -= SPACING_LARGE
        
        # Container for scrolling list
        self.list_content = Entity(parent=self.left_bg, y=cur_y)
        self.drone_buttons = []
        
        # Basic scroll tracking
        self.scroll_y = 0
        
        # -------------------------------------------------
        # RIGHT PANEL (Info, Telemetry, Actions)
        # -------------------------------------------------
        self.right_bg = Entity(
            parent=camera.ui, 
            model='quad', 
            color=COLOR_BG, 
            scale=(PANEL_WIDTH, 1.0), 
            x=0, # set dynamically in update()
            y=0
        )
        
        r_y = 0.45
        self.right_info_title = Text(
            parent=camera.ui,
            text="Drone Information",
            y=r_y,
            x=0, # set dynamically in update()
            origin=(0, 0.5),
            scale=TEXT_SIZE_HEADER,
            color=COLOR_TEXT,
            z=-0.1
        )
        
        self.right_info_text = Text(
            parent=camera.ui,
            text="No drone selected.",
            y=r_y - SPACING_LARGE,
            x=0, # set dynamically in update()
            origin=(0, 0.5),
            scale=TEXT_SIZE_NORMAL,
            color=COLOR_TEXT,
            z=-0.1
        )
        
        r_y = 0.01
        create_header(self.right_bg, "Actions", r_y)
        r_y -= SPACING_LARGE
        
        create_button(self.right_bg, 'Hover', r_y, self.assign_hover, bg_color=color.white)
        r_y -= BUTTON_HEIGHT + SPACING_SMALL
        create_button(self.right_bg, 'Waypoint', r_y, self.assign_waypoint, bg_color=color.white)
        r_y -= BUTTON_HEIGHT + SPACING_SMALL
        create_button(self.right_bg, 'Patrol', r_y, self.assign_patrol, bg_color=color.white)
        r_y -= BUTTON_HEIGHT + SPACING_SMALL
        create_button(self.right_bg, 'Return Home', r_y, self.assign_return_home, bg_color=color.white)
        
        r_y -= SPACING_LARGE
        Button(parent=self.right_bg, text='Pause', y=r_y, scale=(0.43, BUTTON_HEIGHT), x=-0.23, color=color.white, text_color=COLOR_TEXT, on_click=self.pause_mission)
        Button(parent=self.right_bg, text='Resume', y=r_y, scale=(0.43, BUTTON_HEIGHT), x=0.23, color=color.white, text_color=COLOR_TEXT, on_click=self.resume_mission)
        
        r_y -= BUTTON_HEIGHT + SPACING_SMALL
        Button(parent=self.right_bg, text='Delete', y=r_y, scale=(0.43, BUTTON_HEIGHT), x=-0.23, color=COLOR_DELETE, text_color=COLOR_DELETE_TEXT, on_click=self.delete_selected)
        Button(parent=self.right_bg, text='Focus', y=r_y, scale=(0.43, BUTTON_HEIGHT), x=0.23, color=color.white, text_color=COLOR_TEXT, on_click=self.focus_selected)
        
        self.update_list()

    def input(self, key):
        if key == 'scroll up':
            self.scroll_y = max(0, self.scroll_y - 1)
            self.update_list()
        elif key == 'scroll down':
            drones = self.swarm.get_drones()
            max_scroll = max(0, len(drones) - 15)
            self.scroll_y = min(max_scroll, self.scroll_y + 1)
            self.update_list()

    def spawn_drones(self):
        try:
            count = int(self.spawn_input.text)
            self.swarm.spawn_drones(count)
            self.update_list()
        except ValueError:
            pass

    def delete_selected(self):
        if self.selected_drone:
            self.swarm.remove_drone(self.selected_drone)
            self.selected_drone = None
            self.update_list()

    def focus_selected(self):
        if self.selected_drone:
            self.camera_controller.focus_on(self.selected_drone)
            
    def pause_mission(self):
        if self.selected_drone:
            drone_id = self.selected_drone.sim_model.id
            manager = self.swarm.simulator.swarm_model.mission_manager
            if drone_id in manager.active_assignments:
                manager.pause_mission(drone_id)

    def resume_mission(self):
        if self.selected_drone:
            drone_id = self.selected_drone.sim_model.id
            manager = self.swarm.simulator.swarm_model.mission_manager
            if drone_id in manager.active_assignments:
                manager.resume_mission(drone_id)
            
    def assign_hover(self):
        if self.selected_drone:
            self.swarm.simulator.swarm_model.assign_hover(self.selected_drone.sim_model.id)

    def assign_waypoint(self):
        if self.selected_drone:
            self.swarm.simulator.swarm_model.assign_waypoint(self.selected_drone.sim_model.id)

    def assign_patrol(self):
        if self.selected_drone:
            self.swarm.simulator.swarm_model.assign_patrol(self.selected_drone.sim_model.id)

    def assign_return_home(self):
        if self.selected_drone:
            self.swarm.simulator.swarm_model.assign_return_home(self.selected_drone.sim_model.id)

    def on_drone_selected(self, drone_entity):
        self.selected_drone = drone_entity
        self.update_list()

    def update_list(self):
        for btn in self.drone_buttons:
            destroy(btn)
        self.drone_buttons.clear()
        
        drones = self.swarm.get_drones()
        
        # Max drones visible in the scroll window
        visible_count = 15
        start_idx = self.scroll_y
        end_idx = min(len(drones), start_idx + visible_count)
        
        for i in range(start_idx, end_idx):
            drone = drones[i]
            y_pos = - ((i - start_idx) * (BUTTON_HEIGHT + 0.01))
            
            is_selected = (drone == self.selected_drone)
            bg_color = COLOR_SELECTED if is_selected else color.white
            txt_color = COLOR_SELECTED_TEXT if is_selected else COLOR_TEXT
            
            btn = Button(
                parent=self.list_content,
                text=drone.sim_model.readable_id,
                y=y_pos,
                scale=(0.9, BUTTON_HEIGHT),
                color=bg_color,
                text_color=txt_color,
                on_click=Func(self.swarm.select_drone, drone)
            )
            self.drone_buttons.append(btn)

    def update(self):
        # Dynamically update UI layout to prevent ZeroDivisionError during resize/minimize
        if window.size[0] > 0 and window.size[1] > 0:
            self.left_bg.x = window.left.x + PANEL_WIDTH / 2
            self.right_bg.x = window.right.x - PANEL_WIDTH / 2
            self.right_info_title.x = window.right.x - PANEL_WIDTH / 2
            self.right_info_text.x = window.right.x - PANEL_WIDTH / 2
            
        if not self.selected_drone:
            self.right_info_title.text = "Drone Information"
            self.right_info_text.text = "No drone selected."
            return
            
        model = self.selected_drone.sim_model
        state = model.state
        manager = self.swarm.simulator.swarm_model.mission_manager
        
        mission_name = "Idle"
        mission_status = "Standby"
        target_wp = "None"
        distance_rem = "N/A"
        
        if model.id in manager.active_assignments:
            assignment = manager.active_assignments[model.id]
            mission_name = type(assignment.mission).__name__
            mission_status = assignment.mission.status.value
            
            if assignment.mission.active_waypoint:
                wp = assignment.mission.active_waypoint
                target_wp = wp.id
                distance_rem = f"{(wp.position - state.position).length():.1f}"
            
        import math
        heading_deg = math.degrees(math.atan2(state.heading.z, state.heading.x))
        if heading_deg < 0: heading_deg += 360
        
        vel_mag = state.velocity.length()
        
        info = []
        info.append(f"Drone ID: {model.readable_id}")
        info.append(f"Mission: {mission_name}")
        info.append(f"Status: {mission_status}")
        info.append("-" * 48)
        info.append(f"Position (X, Y, Z): ({state.position.x:.1f}, {state.position.y:.1f}, {state.position.z:.1f})")
        info.append(f"Altitude (meters): {state.position.y:.1f}")
        info.append(f"Speed (m/s): {vel_mag:.1f}")
        info.append(f"Velocity (X, Y, Z): ({state.velocity.x:.1f}, {state.velocity.y:.1f}, {state.velocity.z:.1f})")
        info.append(f"Heading (degrees): {heading_deg:.0f}°")
        info.append("-" * 48)
        info.append(f"Target Waypoint: {target_wp}")
        if distance_rem != "N/A":
            info.append(f"Distance Remaining (meters): {distance_rem}")
        else:
            info.append(f"Distance Remaining (meters): N/A")
            
        self.right_info_text.text = "\n".join(info)
