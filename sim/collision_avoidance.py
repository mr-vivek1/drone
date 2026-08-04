from sim.flight_command import FlightCommand
from config import SAFE_DISTANCE

class CollisionAvoidance:
    """Modifies FlightCommands to avoid collisions with neighbors."""
    
    def process(self, command: FlightCommand, drone_state, neighbor_positions) -> FlightCommand:
        """Takes a desired command and returns a safe command."""
        
        safe_command = FlightCommand()
        safe_command.desired_velocity = command.desired_velocity
        safe_command.desired_heading = command.desired_heading
        safe_command.priority = command.priority
        
        avoid = type(command.desired_velocity)(0, 0, 0)
        
        # Generate repel vector from close neighbors
        for pos in neighbor_positions:
            if pos is None:
                continue
            dist = (drone_state.position - pos).length()
            if 0 < dist < SAFE_DISTANCE:
                avoid += (drone_state.position - pos).normalized() * (SAFE_DISTANCE - dist)
                
        # Modify desired velocity with avoidance vector
        safe_command.desired_velocity += avoid * 2
        
        # Cap speed to drone's limits
        if safe_command.desired_velocity.length() > drone_state.maximum_speed:
            safe_command.desired_velocity = safe_command.desired_velocity.normalized() * drone_state.maximum_speed
            
        # Update heading if modifying velocity heavily
        if safe_command.desired_velocity.length() > 0.1:
            safe_command.desired_heading = type(command.desired_velocity)(safe_command.desired_velocity.x, 0, safe_command.desired_velocity.z).normalized()
            
        # Re-calculate thrust vector for the physics engine
        from config import GRAVITY, DRONE_MASS
        Kp = 2.0
        velocity_error = safe_command.desired_velocity - drone_state.velocity
        desired_accel = velocity_error * Kp
        gravity_accel = type(command.desired_velocity)(0, GRAVITY, 0)
        safe_command.thrust_vector = (desired_accel + gravity_accel) * DRONE_MASS
            
        return safe_command
