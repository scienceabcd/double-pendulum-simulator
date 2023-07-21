import pygame
import numpy as np
from scipy.integrate import odeint

# Physics parameters
g = 9.81
L1, L2 = 1.0, 1.0
m1, m2 = 1.0, 1.0
drag = 0.1  # drag coefficient for air resistance

# Pygame parameters
scale = 200
size = (800, 800)
origin = np.array([size[0]//2, size[1]//2 - 150])  # move the pendulum higher
bg_color = (173, 216, 230)  # light blue background
circle_color = (255, 255, 0)  # yellow circles

def equations(Y, t):
    theta1, z1, theta2, z2 = Y
    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)
    
    theta1_dot = z1
    z1_dot = (m2*g*np.sin(theta2) - m2*s*(L1*z1**2*c + L2*z2**2) - (m1+m2)*g*np.sin(theta1)) / L1 / (m1 + m2*s**2) - drag*z1
    theta2_dot = z2
    z2_dot = ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2) - drag*z2
    
    return theta1_dot, z1_dot, theta2_dot, z2_dot

def run_simulation(Y0, t):
    return odeint(equations, Y0, t)

def main():
    pygame.init()

    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    # Font setup
    pygame.font.init()
    title_font = pygame.font.Font(None, 50)  # 50 is the font size
    description_font = pygame.font.Font(None, 30)  # 30 is the font size
    title = title_font.render('Pendulum Simulator', True, (0, 0, 0))  # Black color
    description = description_font.render('Drag and drop the pendulum to the location you want.', True, (0, 0, 0))  # Black color

    # initial conditions
    Y0 = np.array([np.pi / 7, 0, np.pi / 4, 0])  # smaller initial angles and zero velocities
    t = np.linspace(0, 0.01, 2)  # smaller time interval
    mouse_down = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                pos = pygame.mouse.get_pos()
                pos_vector = np.array(pos) - origin
                Y0[0] = np.arctan2(-pos_vector[1], pos_vector[0]) + np.pi / 2  # calculate the angle from the mouse position (invert y-coordinate)
                Y0[2] = Y0[0]  # make the second pendulum follow the first

        screen.fill(bg_color)  # light blue background

        # Draw title and description
        screen.blit(title, (10, 10))  # 10, 10 is the position of the top left corner of the text
        screen.blit(description, (10, 70))  # 10, 70 is the position of the top left corner of the text

        if mouse_down:  # if the mouse button is down, update the pendulum position continuously
            pos = pygame.mouse.get_pos()
            pos_vector = np.array(pos) - origin
            Y0[0] = np.arctan2(-pos_vector[1], pos_vector[0]) + np.pi / 2  # calculate the angle from the mouse position (invert y-coordinate)
            Y0[2] = Y0[0]  # make the second pendulum follow the first

        Y = run_simulation(Y0, t)

        x1 = int(origin[0] + scale * L1 * np.sin(Y[0, 0]))
        y1 = int(origin[1] + scale * L1 * np.cos(Y[0, 0]))
        x2 = int(x1 + scale * L2 * np.sin(Y[0, 2]))
        y2 = int(y1 + scale * L2 * np.cos(Y[0, 2]))

        pygame.draw.line(screen, (0, 0, 0), origin, (x1, y1), 5)
        pygame.draw.circle(screen, circle_color, (x1, y1), 10)  # yellow circle
        pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 5)
        pygame.draw.circle(screen, circle_color, (x2, y2), 10)  # yellow circle

        pygame.display.flip()

        Y0 = Y[-1, :]

        clock.tick(100)  # increase the frame rate for smoother motion

    pygame.quit()

if __name__ == "__main__":
    main()
