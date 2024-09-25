import pygame
import numpy as np
import soundcard as sc

# Constants
CHUNK = 1024  # Number of audio samples per frame
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1 kHz)
WIDTH, HEIGHT = 1020, 800 # Window size

# Soundcard setup: Get the loopback microphone (captures audio from speakers)
default_mic = sc.get_microphone(sc.default_speaker().name, include_loopback=True)

# Check if loopback is available
if default_mic is None:
    print("Loopback microphone not available")
    quit()

print(f"Using {default_mic.name} for loopback capture")

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Function to draw waveform
def draw_waveform(audio_data):
    screen.fill((0, 0, 0))  # Clear the screen

    audio_data *= 25

    # Scale audio data to fit in the height of the window
    scaled_data = (audio_data * (HEIGHT / 2)).astype(int) + (HEIGHT // 2)
    # Clamp values to ensure they stay within the window bounds
    scaled_data = np.clip(scaled_data, 0, HEIGHT)

    # Create a list of points to plot (x, y)
    points = [(x, scaled_data[x]) for x in range(len(scaled_data))]

    # Draw lines connecting the points
    pygame.draw.lines(screen, (0, 255, 255), False, points, 2)

    pygame.display.flip()

# Function to draw bars
def draw_bars(audio_data):
    screen.fill((0, 0, 0))  # Clear screen
    num_bars = 100
    bar_width = WIDTH // num_bars

    for i in range(num_bars):
        bar_height = int(freq_magnitude[i] * 1000)  # Scale the magnitude
        color = (0, 255, 0)  # Green bars
        pygame.draw.rect(screen, color, (i * bar_width, HEIGHT - bar_height, bar_width - 2, bar_height))

    pygame.display.flip()

# Start capturing audio from the loopback mic
with default_mic.recorder(samplerate=RATE) as mic:
    while True:
        # Handle closing window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Capture audio data from the loopback microphone
        data = mic.record(numframes=CHUNK)
        mono_data = np.mean(data, axis=1)  # Convert to mono if stereo
        
        # Perform FFT to get frequency data
        fft_data = np.fft.fft(mono_data)
        
        # Get the magnitude of frequencies (for visualization)
        freq_magnitude = np.abs(fft_data[:CHUNK // 2])  # Use only half of FFT (mirrored)

        print(freq_magnitude)  # Output the frequency data (for testing)

        draw_waveform(mono_data)