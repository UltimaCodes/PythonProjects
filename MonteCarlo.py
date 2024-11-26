// A Program that visualizes and calculates an estimate of pi of a 4 Dimensional Hypersphere

import numpy as np
import time
import pygame
from colorama import Fore, Style, init
from multiprocessing import Pool, cpu_count

init(autoreset=True)

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("4D Monte Carlo Pi Estimation")
white = (255, 255, 255)
black = (0, 0, 0)
inside_color = (0, 255, 0)
outside_color = (255, 0, 0)

def estimate_pi_4d(num_samples):
    num_cores = cpu_count()
    batch_size = max(1, num_samples // (10 * num_cores))
    with Pool(processes=num_cores) as pool:
        inside_count = 0
        for i in range(0, num_samples, batch_size):
            random_points = np.random.uniform(-1, 1, (batch_size, 4))
            inside_mask = pool.map(is_inside_hypersphere, random_points)
            inside_count += sum(inside_mask)

            # Visualization
            for point, is_inside in zip(random_points, inside_mask):
                project_and_draw(point, is_inside)

            estimated_volume = inside_count / (i + batch_size)
            estimated_pi = (2 * estimated_volume / 0.5) ** 0.25
            update_loading_bar(i + batch_size, num_samples, estimated_pi)

    return estimated_pi

def is_inside_hypersphere(point):
    return np.sum(point**2) <= 1

def project_and_draw(point, is_inside):
    # Project 4D point to 2D for visualization
    x, y = point[0] * screen_width // 2 + screen_width // 2, point[1] * screen_height // 2 + screen_height // 2

    # Draw the point on the Pygame window
    color = inside_color if is_inside else outside_color
    pygame.draw.circle(screen, color, (int(x), int(y)), 2)

    pygame.display.flip()

def update_loading_bar(current, total, current_pi):
    percentage = (current / total) * 100
    progress_bar_length = 50
    progress = int(percentage * progress_bar_length / 100)
    remaining = total - current
    time_remaining = remaining / (current / (time.time() - start_time)) if current > 0 else 0

    loading_bar = f"Progress: [{'=' * progress}{' ' * (progress_bar_length - progress)}] {percentage:.3f}% | Current Pi: {current_pi:.8f} | ETA: {time_remaining:.2f} seconds"

    print(f"\r{Fore.GREEN}{loading_bar}{Style.RESET_ALL}", end='', flush=True)

if __name__ == "__main__":
    # Input validation loop
    while True:
        try:
            num_samples = int(input(f"{Fore.GREEN}Number of samples: {Style.RESET_ALL}"))
            if num_samples <= 0:
                raise ValueError("Number of samples must be a positive integer.")
            break
        except ValueError as e:
            print(f"{Fore.RED}Invalid input: {e}. Please enter a valid positive integer.{Style.RESET_ALL}")

    start_time = time.time()
    
    # Main Pygame loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(black)
        
        estimated_pi_4d = estimate_pi_4d(num_samples)
        
        pygame.display.flip()

    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"\n{Fore.GREEN}Estimated value of pi in 4D space: {estimated_pi_4d}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Time taken: {elapsed_time:.2f} seconds{Style.RESET_ALL}")

    pygame.quit()
    exit()
