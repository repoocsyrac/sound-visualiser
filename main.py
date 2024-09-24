import pygame
import numpy as np
import soundcard as sc

# Constants
CHUNK = 1024  # Number of audio samples per frame
#FORMAT = pyaudio.paInt16  # Audio format (16-bit integer)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1 kHz)
WIDTH, HEIGHT = 800, 400 # Window size

# PyAudio object
#p = pyaudio.PyAudio()

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

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw bars for each frequency bin
        num_bars = 100  # Number of frequency bins to visualize
        bar_width = WIDTH // num_bars

        '''
        for i in range(num_bars):
            bar_height = int(freq_magnitude[i] / 500)  # Scale the magnitude
            color = (0, 255, 0)  # Green bars
            # Draw the bar
            pygame.draw.rect(screen, color, (i * bar_width, HEIGHT - bar_height, bar_width - 2, bar_height))
        '''

        '''
        # draw circles
        for i in range(num_bars):
            radius = int(freq_magnitude[i] / 300)  # Scale radius
            pygame.draw.circle(screen, (0, 255 - i * 2, i * 2), (WIDTH // 2, HEIGHT // 2), radius, 1)
        '''

        # Draw waveforms
        for i in range(len(mono_data) - 1):
            pygame.draw.line(screen, (0, 255, 255), (i, HEIGHT // 2 + mono_data[i] // 50), (i + 1, HEIGHT // 2 + mono_data[i + 1] // 50))

        # Update the display
        pygame.display.flip()