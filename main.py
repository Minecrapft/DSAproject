import pygame
from colors import Colors
import button 
from ScrollableText import ScrollableTextArea
import random  # For simulating sensor data
import datetime
from loading_screen import LoadingBar
import pygame
import sys
import time
import random
from collections import deque  # <-- Add this for the queue
from linkedList import LinkedList



pygame.init()
clock = pygame.time.Clock()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900
controller_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

def loading_screen(): #loading screen

    openingsound = pygame.mixer.Sound('doneLoading.MP3')


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Loading Screen")

    BACKGROUND = (30, 30, 30)
    TEXT_COLOR = (220, 220, 220)


    small_font = pygame.font.SysFont('Arial', 24)

    loading_bar = LoadingBar(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 40)
    progress = 0
    
    clock = pygame.time.Clock()
    
    # For demonstration, we'll simulate "tasks" loading
    task_text = small_font.render("", True, TEXT_COLOR)
    tasks = ["setting up", "Initializing ", "Preparing the controller", 
            "Setting up audio", "Connecting", "Connected to the device"]
    current_task = 0
    
    while progress < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Clear screen
        controller_window.fill(BACKGROUND)
        
        # Update progress (simulated)
        if progress < (current_task + 1) * (100 / len(tasks)):
            # More natural, non-linear progress
            increment = random.uniform(1, 5)
            progress = min(progress + increment, 100)
            
            # Update task text when reaching new task threshold
            if progress >= (current_task + 1) * (100 / len(tasks)) and current_task < len(tasks) - 1:
                current_task += 1
                
        # Update and draw loading bar
        loading_bar.update(progress)
        loading_bar.draw(screen)
        
        # Draw current task text
        if current_task < len(tasks):
            task_text = small_font.render(tasks[current_task], True, TEXT_COLOR)
        task_rect = task_text.get_rect(midtop=(SCREEN_WIDTH // 2, loading_bar.y + loading_bar.height + 20))
        screen.blit(task_text, task_rect)
        
        if progress == 100:
            openingsound.play()

        # Show tip at bottom of screen
      
        
        pygame.display.flip()
        clock.tick(25)
        
    # When loading is complete, wait a moment before exiting demo
    time.sleep(1)

def main(): #main controller
    pygame.display.set_caption("Controller")

    #background sa controller
    controller_body = pygame.Rect(3, 3, 893, 570)

    #screen and the text area
    info_screen = ScrollableTextArea(20, 20, 360, 300, 20, 0, 0, 0)
    direction_screen = ScrollableTextArea(390, 20, 200, 300, 0, 0, 0, 0)
    status_screen = ScrollableTextArea(600, 20, 280, 300, 0, 20, 0, 0)
    
    # Add a new overlay screen that will show when info button is pressed
    info_overlay = ScrollableTextArea(20, 20, 360, 300, 20, 0, 0, 0)  # Semi-transparent blue
    

    #current date
    current_date = datetime.datetime.now()

    #initial text
    status_screen.add_text("System Status")
    status_screen.add_text("-----------------")
    status_screen.add_text("")
    status_screen.add_text(f"100%")
    status_screen.add_text("")
    status_screen.add_text("Solar Wattage: 0W")
    status_screen.add_text("")
    status_screen.add_text("Container: 0%")
    status_screen.add_text("")
    status_screen.add_text("Charging: No")
    status_screen.add_text("")
    status_screen.add_text("Pump: OFF")
    
    # Add initial text to overlay
    info_overlay.add_text("Robot Information")
    info_overlay.add_text("-----------------")
    info_overlay.add_text("Model: Oilbot 2.0")
    info_overlay.add_text("Serial: WB-2025-0042")
    info_overlay.add_text(f"Date: {current_date.strftime('%Y-%m-%d')}")
    info_overlay.add_text("Pump Type: Peristaltic")
    info_overlay.add_text("Battery: Li-ion 48V")
    info_overlay.add_text("Solar: 20W")
    info_overlay.add_text("Container Cap: 20L")
    info_overlay.add_text("-----------------")
    info_overlay.add_text("Diagnostic Info:")
    info_overlay.add_text(f"Uptime: {0}s")
    info_overlay.add_text(f"Pump Cycles: {0}")
    info_overlay.add_text(f"Power Draw: {0}W")
    info_overlay.add_text(f"Temp: {0}°C")
    info_overlay.add_text(f"Humidity: {0}%")
    info_overlay.add_text(f"signal strength: {0}ms")

    #screen
    controller_screen = pygame.Rect(10, 10, 880, 320)

    #panels
    bottom_panel = pygame.Rect(10, 340, 880, 225)
    dpad_background = pygame.Rect(70, 350, 200, 200)
    dpad_background2 = pygame.Rect(420, 400, 350, 100)

    #mga button shits
    up_button = button.rect_Button(145, 355, 50, 50, '', 20, 0, Colors.LIGHT_BEIGE,'darkred' , 50, 50, 10, 10)
    down_button = button.rect_Button(145, 495, 50, 50, '', 20, 0,Colors.LIGHT_BEIGE,'darkred', 10, 10, 50, 50)
    
    left_button = button.rect_Button(75, 425, 50, 50, '', 20, 0,Colors.LIGHT_BEIGE,'darkred', 50, 10, 50, 10)
    right_button = button.rect_Button(215, 425, 50, 50, '', 20, 0,Colors.LIGHT_BEIGE,'darkred', 10, 50, 10, 50)   
    
    OnOff_button = button.rect_Button(135, 415, 70, 70, 'On/Off', 25,Colors.BLACK, Colors.LIGHT_BEIGE, 'darkred', 50, 50, 50, 50)
    info_button = button.rect_Button(650, 415, 100, 70, 'Info', 25,Colors.BLACK, Colors.LIGHT_BEIGE, 'darkred', 30, 30, 30, 30)
    pump_button = button.rect_Button(440, 415, 100, 70, 'Pump', 25,Colors.BLACK,Colors.LIGHT_BEIGE, 'darkred', 30, 30, 30, 30)
    
    # Button for toggling solar (simulates sunlight)
    solar_button = button.rect_Button(545, 415, 100, 70, 'Solar', 25,Colors.BLACK,Colors.LIGHT_BEIGE, 'darkred', 30, 30, 30, 30)

   

    #font ini sa taas text sa screen
    screen_text_title = pygame.font.SysFont('Roboto', 25, bold=False)

    #screen text
    info_text = 'Info'
    direction_text = 'Direction'
    status_text = 'Status'

    #text rectangle
    info_text_rect = pygame.Rect(30, 30, 20, 20)
    direction_text_rect = pygame.Rect(400, 30, 20, 20)
    status_text_rect = pygame.Rect(610, 30, 20, 20)
        
    #direction tracking
    current_direction = "None"
    

    #Screen text surface
    info_text_surface = screen_text_title.render(info_text, True, Colors.BLACK)
    direction_text_surface = screen_text_title.render(direction_text, True, Colors.BLACK)
    status_text_surface = screen_text_title.render(status_text, True, Colors.BLACK)

    # --- DICTIONARY STATE ---
    robot = {
        "battery_level": 100,
        "charging": False,
        "container_capacity": 0,
        "pump_state": False,
        "robot_state": False,
        "info_state": False,
        "solar_state": False,
        "sunny": True
    }

    #sun
    sunny = True

    # Simulation update timer
    last_update_time = pygame.time.get_ticks()
    update_interval = 100# milliseconds
    
    # Flag to track if container almost full message has been shown
    container_warning_shown = False
    
    # Flag to track if battery low message has been shown
    battery_warning_shown = False
    battery_shutting_down = False

    #for battery drawing
    battery_rect = pygame.Rect(650, 87, 55, 20)
    battery_rect2 = pygame.Rect(705, 92, 6, 10)

    #battery level drawing
    battery_level_drawing10 = pygame.Rect(653, 91, 4, 13)
    battery_level_drawing20 = pygame.Rect(658, 91, 4, 13)
    battery_level_drawing30 = pygame.Rect(663, 91, 4, 13)
    battery_level_drawing40 = pygame.Rect(668, 91, 4, 13)
    battery_level_drawing50 = pygame.Rect(673, 91, 4, 13)
    battery_level_drawing60 = pygame.Rect(678, 91, 4, 13)
    battery_level_drawing70 = pygame.Rect(683, 91, 4, 13)
    battery_level_drawing80 = pygame.Rect(688, 91, 4, 13)
    battery_level_drawing90 = pygame.Rect(693, 91, 4, 13)
    battery_level_drawing100 = pygame.Rect(698, 91, 4, 13)

    #charging image

    

    controller_window.fill(Colors.LIGHT_GRAY)

    #charging image
    charging2 = pygame.image.load('charging_image.png').convert_alpha()
    charging_image = pygame.transform.scale(charging2, (20, 20))

    #Queue for messages
    message_queue = deque()
    message_display_timer = 0
    MESSAGE_DISPLAY_TIME = 5  

    
    # --- Linked List for Direction History ---
    direction_history = LinkedList()

    run = True
    while run:

      

        #background sa controller
        pygame.draw.rect(controller_window, Colors.DARK_BROWN, controller_body, 0, 60, 20, 20)

        # background screen sa controller
        pygame.draw.rect(controller_window, Colors.LIGHT_BEIGE, controller_screen, 0, 0, 20, 20)  
        
        #e draw ang text area sa controller or ang screen mismo sa controller
        info_screen.draw(controller_window)
        direction_screen.draw(controller_window)
        status_screen.draw(controller_window)
        
        # Draw the overlay if info_state is active
        if robot["info_state"]:
            info_overlay.draw(controller_window)

   
        #bottom panel sa controller
        pygame.draw.rect(controller_window, Colors.MEDIUM_BROWN, bottom_panel, 0, 60, 0, 0) 
        pygame.draw.rect(controller_window,Colors.DARK_BROWN, dpad_background, 0, 100, 100, 100)
        pygame.draw.rect(controller_window, Colors.DARK_BROWN, dpad_background2, 0, 40, 40, 40)
        
        
        #buttons sa controller e display sudsab
        up_button.draw(controller_window)
        down_button.draw(controller_window)
        left_button.draw(controller_window)
        right_button.draw(controller_window)
        OnOff_button.draw(controller_window)
        info_button.draw(controller_window)
        pump_button.draw(controller_window)
        solar_button.draw(controller_window)

        #display text sa screen
        controller_window.blit(info_text_surface,(info_text_rect.x+150, info_text_rect.y-5))
        controller_window.blit(direction_text_surface, (direction_text_rect.x+45, direction_text_rect.y-5))
        controller_window.blit(status_text_surface, (status_text_rect.x+100, status_text_rect.y-5))
        

        #battery level drawing
        pygame.draw.rect(controller_window, Colors.BLACK, battery_rect, 2, 0, 0, 0, 0)
        pygame.draw.rect(controller_window, Colors.BLACK, battery_rect2, 0, 1, 0, 1, 0)
        
        

        #battery level drawing
        if robot["battery_level"] >= 90.5:
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing10, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing20, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing30, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing40, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing50, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing60, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing70, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing80, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing90, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing100, 0, 0, 0, 0, 0)

        if robot["battery_level"] >= 80.5:
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing10, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing20, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing30, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing40, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing50, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing60, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing70, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing80, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing90, 0, 0, 0, 0, 0)
            

        if robot["battery_level"] >= 70.5:
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing10, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing20, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing30, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing40, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing50, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing60, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing70, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing80, 0, 0, 0, 0, 0)
        
           

        if robot["battery_level"] >= 60.5:
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing10, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing20, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing30, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing40, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing50, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing60, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing70, 0, 0, 0, 0, 0)
            

        if robot["battery_level"] >= 50.5:
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing10, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing20, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing30, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing40, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing50, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing60, 0, 0, 0, 0, 0)
            
            
        if robot["battery_level"] >= 40.5:
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing10, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing20, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing30, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing40, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing50, 0, 0, 0, 0, 0)
           

        if robot["battery_level"] >= 30.5:
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing10, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing20, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing30, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing40, 0, 0, 0, 0, 0)
            
        if robot["battery_level"] >= 20.5:
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing10, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing20, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing30, 0, 0, 0, 0, 0)
            
        if robot["battery_level"] >= 10.5:
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing10, 0, 0, 0, 0, 0)
            pygame.draw.rect(controller_window, Colors.BLACK, battery_level_drawing20, 0, 0, 0, 0, 0)
            

        if robot["battery_level"] <= 10.5:
            pygame.draw.rect(controller_window, Colors.RED, battery_level_drawing10, 0, 0, 0, 0, 0)
            
            
        if robot["battery_level"] <= 5:
            status_screen.clear()
            status_screen.add_text("System Status")
            status_screen.add_text("-----------------")
            status_screen.add_text("")
            status_screen.add_text(f"{robot['battery_level']:.0f}%")
            status_screen.add_text("")
            status_screen.add_text(f"Solar Wattage: {f'{solar_power:.1F}' if robot['sunny'] else '0'}W")   # Display random wattage
            status_screen.add_text("")
            status_screen.add_text(f"Container: {robot['container_capacity']:.0f}%")
            status_screen.add_text("")
            status_screen.add_text(f"Charging: {'Yes' if robot['charging'] else 'No'}")
            status_screen.add_text("")
            status_screen.add_text(f"Pump: {'ON' if robot['pump_state'] else 'OFF'}")
        
        if info_button.is_clicked_once():
                robot["info_state"] = not robot["info_state"]   



        if OnOff_button.is_clicked_once():
                 
            openingsound = pygame.mixer.Sound('opening.MP3')
            openingsound.play()
            
           
            robot["robot_state"] = not robot["robot_state"]
            status_msg = ">The robot is ON" if robot["robot_state"] else ">The robot is OFF"
            info_screen.add_text(status_msg)
            print(">robot state is ON" if robot["robot_state"] else ">robot state is OFF")

            if not robot["robot_state"]:
                
                
                current_direction = "None"
                
                # Reset warning flags when turning off
                container_warning_shown = False
                battery_warning_shown = False
                
                # Reset stats
               
                robot["charging"] = False
                
                robot["pump_state"] = False
                robot["solar_state"] = False
                robot["info_state"] = False  # Also turn off info overlay
                
                # Update status screen
                status_screen.clear()
                status_screen.add_text("System Status")
                status_screen.add_text("-----------------")
                status_screen.add_text("")
                status_screen.add_text(f"{robot['battery_level']:.0f}%")
                status_screen.add_text("")
                status_screen.add_text(f"Solar Wattage: 0W")  # Display random wattage
                status_screen.add_text("")
                status_screen.add_text(f"Container: {robot['container_capacity']:.0f}%")
                status_screen.add_text("")
                status_screen.add_text(f"Charging: {'Yes' if robot['charging'] else 'No'}")
                status_screen.add_text("")
                status_screen.add_text(f"Pump: {'ON' if robot['pump_state'] else 'OFF'}")
            
        # --- Message Queue Handling ---
        if message_queue and message_display_timer == 0:
            msg, highlight = message_queue.popleft()
            info_screen.add_text(msg, highlight_words=highlight)
            message_display_timer = MESSAGE_DISPLAY_TIME
        if message_display_timer > 0:
            message_display_timer -= 1

        if robot["robot_state"]:
            
            # Update status metrics in real-time
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time >= update_interval:
                last_update_time = current_time
                solar_power = random.uniform(20.001, 22.002)
                
                # Battery decreases while robot is on
                if robot["battery_level"] > 0:
                    robot["battery_level"] = max(0, robot["battery_level"] - .1)
                
                # Solar affects battery when active
                if robot["solar_state"] and robot["sunny"]:
                    if robot["battery_level"] < 100:
                        robot["battery_level"] = min(100, robot["battery_level"] + .15)
                    robot["charging"] = True
                else:
                    robot["charging"] = False
                
                # Container fills when pump is on
                if robot["pump_state"]:
                    robot["container_capacity"] = min(100, robot["container_capacity"] + random.uniform(0.001, 1))

                
                
                # Update the status display
                status_screen.clear()
                status_screen.add_text("System Status")
                status_screen.add_text("-----------------")
                status_screen.add_text(f"")
                status_screen.add_text(f"{robot['battery_level']:.0f}%")
                status_screen.add_text(f"")
                status_screen.add_text(f"Solar Wattage: {f'{solar_power:.1F}' if robot['sunny'] else '0'}W")  # Display random wattage
                status_screen.add_text(f"")
                status_screen.add_text(f"Container: {robot['container_capacity']:.0f}%")
                status_screen.add_text(f"")
                status_screen.add_text(f"Charging: {'Yes' if robot['charging'] else 'No'}")
                status_screen.add_text(f"")
                status_screen.add_text(f"Pump: {'ON' if robot['pump_state'] else 'OFF'}")
                
                # Also update the info overlay with some real-time data
                if robot["info_state"]:

                    
                    # Clear and redraw with updated values
                    info_overlay.clear()
                    info_overlay.add_text("Robot Information")
                    info_overlay.add_text("-----------------")
                    info_overlay.add_text("Model: Oilbot 2.0")
                    info_overlay.add_text("Serial: WB-2025-0042")
                    info_overlay.add_text(f"Date: {current_date.strftime('%Y-%m-%d')}")
                    info_overlay.add_text("Pump Type: Peristaltic")
                    info_overlay.add_text("Battery: Li-ion 48V")
                    info_overlay.add_text("Solar: 20W")
                    info_overlay.add_text("Container Cap: 20L")
                    info_overlay.add_text("-----------------")
                    info_overlay.add_text("Diagnostic Info:")
                    info_overlay.add_text(f"Uptime: {pygame.time.get_ticks()//1000}s")
                    info_overlay.add_text(f"Container in Liters: {int(robot['container_capacity']/5)}L")
                    info_overlay.add_text(f"Power Draw: {f'{random.uniform(10, 10.9):.1f}' if robot['sunny'] else '0'}W")
                    info_overlay.add_text(f"Temp: {random.uniform(35, 42):.1f}°C")
                    info_overlay.add_text(f"Humidity: {random.uniform(40, 70):.1f}%")
                    info_overlay.add_text(f"signal strength: { random.randint(20, 25)}ms")
                    info_overlay.add_text(f"Panels are receiving sunlight: {'True' if robot['sunny'] else 'False'}")
                      
                # Check for battery warning - only show once
                if robot["battery_level"] < 20 and not battery_warning_shown:
                    message_queue.append(("> WARNING : Battery Low!", {"WARNING": Colors.RED}))
                    battery_warning_shown = True

                if robot["battery_level"] <= 3 and not battery_shutting_down:
                    message_queue.append(("> WARNING : robot is shutting down", {"WARNING": Colors.RED}))
                    message_queue.append(("> WARNING : please charge your device", {"WARNING": Colors.RED}))
                    message_queue.append(("or turn on the solar panel", None))
                    battery_shutting_down = True
                    

                    
                # Reset battery warning flag if battery is charged above threshold
                if robot["battery_level"] >= 20:
                    battery_warning_shown = False
                
                # Check for container almost full - only show once
                if robot["container_capacity"] > 90 and not container_warning_shown:
                    message_queue.append((f"> WARNING : Container almost full: {robot['container_capacity']:.1f}%", {"WARNING": Colors.RED}))
                    container_warning_shown = True

                if 99 <= robot["container_capacity"] <= 99.001 and container_warning_shown:
                    message_queue.append(("> WARNING : Container is full!", {"WARNING": Colors.RED}))
                    message_queue.append(("Turning off pump, automatically", None))

                if robot["container_capacity"] == 100:
                    robot["pump_state"] = False
                
                # Reset container warning flag if container is emptied below threshold
                if robot["container_capacity"] <= 90:
                    container_warning_shown = False
                
                
                                        
                # Turn off robot if battery dies
                if robot["battery_level"] <= 5 and not battery_shutting_down and robot["sunny"]:
                    message_queue.append(('> Turning on solar panel, automatically', None))
                    robot["charging"] = True
                    robot["solar_state"] = True

                if robot["battery_level"] == 0:
                    
                    robot["robot_state"] = False
                    robot["battery_level"] = 0
                    info_screen.add_text(">The robot is OFF")
                    direction_screen.clear()
                    direction_screen.add_text("No movement")
                    robot["pump_state"] = False
                    robot["solar_state"] = False
                    robot["info_state"] = False  # Also turn off info overlay
                    status_screen.clear()
                    status_screen.add_text("System Status")
                    status_screen.add_text("-----------------")
                    status_screen.add_text(f"")
                    status_screen.add_text(f"{robot['battery_level']:.0f}%")
                    status_screen.add_text(f"")
                    status_screen.add_text(f"Solar Wattage: 0W")  # Display random wattage
                    status_screen.add_text(f"")
                    status_screen.add_text(f"Container: {robot['container_capacity']:.0f}%")
                    status_screen.add_text(f"")
                    status_screen.add_text(f"Charging: {'Yes' if robot['charging'] else 'No'}")
                    status_screen.add_text(f"")
                    status_screen.add_text(f"Pump: {'ON' if robot['pump_state'] else 'OFF'}")

                
 
            
                # Toggle solar state
                if solar_button.is_clicked_once():
                    
                    
                    robot["solar_state"] = not robot["solar_state"]
                    message_queue.append((">Solar panel is ON" if robot["solar_state"] else ">Solar panel is OFF", None))
                    print("solar state is ON" if robot["solar_state"] else "solar state is OFF")
                
                charging_blink_timer = 0
                show_charging_icon = True

              

            new_direction = None

            if up_button.is_pressed_hold():
                new_direction = "Up"
                print("up")
            elif down_button.is_pressed_hold():
                new_direction = "Down"
                print("down")
            elif left_button.is_pressed_hold():
                new_direction = "Left"
                print("left")
            elif right_button.is_pressed_hold():
                new_direction = "Right"     
                print("right")

            # Moving and pumping drains battery faster
            if new_direction and robot["battery_level"] > 0:
                robot["battery_level"] = max(0, robot["battery_level"] - 0.001)
            
            #handle the text in the direction screen
            if new_direction and new_direction != current_direction:
                current_direction = new_direction
                direction_screen.add_text(f"Moving: {current_direction}")
                direction_history.append(current_direction)  # <-- Store in linked list
    
            if pump_button.is_clicked_once():
                robot["pump_state"] = not robot["pump_state"] 
                message_queue.append((f">Pump is {'On' if robot['pump_state'] else 'Off'}", None))
                # Reset container warning when pump is turned off
                if not robot["pump_state"]:
                    container_warning_shown = False

    
        if robot["charging"]:
            charging_blink_timer += 1
            if charging_blink_timer >= 30:  # Change every half second at 60fps
                charging_blink_timer = 0
                show_charging_icon = not show_charging_icon
            
            if show_charging_icon:
                controller_window.blit(charging_image, (battery_rect.x+65, battery_rect.y))
  

            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEWHEEL:
            # Pass the event to your text area
                info_screen.handle_mouse_wheel(event)
                direction_screen.handle_mouse_wheel(event)
                status_screen.handle_mouse_wheel(event)
                info_overlay.handle_mouse_wheel(event)  # Pass to overlay as well
        #for music purposes

        pygame.display.update()
        clock.tick(60)  
        
    pygame.quit()

def password_input(): #password input para makadto sa main controller
    
    Enter_button = button.rect_Button(480, 300, 130, 30, 'Enter', 23,Colors.WHITE, "#185D72", "#0E98BA", 5, 5, 5, 5)
    Base_font = pygame.font.Font(None, 25)
    input_text = ''
    display_text = ''
    password = '123'
    box_name = 'Password'
    pygame.display.set_caption("Password")

    input_rect = pygame.Rect(310, 250, 140, 32)
    password_container = pygame.Rect(310, 250, 300, 32)
    password_BG = pygame.Rect(300, 180, 320, 180)
    color_active = Colors.BLACK
    color_passive = pygame.Color('gray60')
    color = color_passive
    active = False
    grant_access = False
    run = True
    while run:

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        display_text = display_text[:-1]
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                        display_text += "*"
        

        if active:
            color = color_active
        else:
            color = color_passive
        
        
        controller_window.fill('#FFFAFA')

        pygame.draw.rect(controller_window,"#d6cab8", password_BG, 0 , 0, 5, 5, 5, 5)
        Enter_button.draw(controller_window)
        pygame.draw.rect(controller_window, "#f0ece4", password_container, 0 , 0, 5, 5, 5, 5)
        pygame.draw.rect(controller_window, color, input_rect, 2 , 0, 5, 5, 5, 5)
        
        

        
        Box_name = Base_font.render(box_name, True, Colors.BLACK)
        controller_window.blit(Box_name, (input_rect.x+0, input_rect.y-20))   

        text_surface = Base_font.render(display_text, True, Colors.BLACK)
        controller_window.blit(text_surface, (input_rect.x+15, input_rect.y+11))  

        input_rect.w = max(300, text_surface.get_width()+10)  

        if input_text == password:
            if Enter_button.is_clicked_once():
                print("clicked")
                grant_access = True
                run = False 
                loading_screen()              
                main() # main controller
        else:   
            print("incorrect")

        pygame.display.update()    
        clock.tick(60)

    pygame.quit()

#password_input() #e run ang password_input function para makadto sa main controller   
if __name__ == "__main__":
    main()#e run ang loading screen