import pygame
import numpy as np
import pyaudio

# Constants
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format (16-bit integer)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1 kHz)

# PyAudio object
p = pyaudio.PyAudio()

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Open the microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Infinite loop to capture audio data
while True:
    # Handle closing window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            stream.stop_stream()
            stream.close()
            p.terminate()
            quit()

    # Read audio chunk
    data = stream.read(CHUNK)
    
    # Convert data to numpy array (for FFT)
    audio_data = np.frombuffer(data, dtype=np.int16)
    
    # Perform FFT to get frequency data
    fft_data = np.fft.fft(audio_data)
    
    # Get the magnitude of frequencies (for visualization)
    freq_magnitude = np.abs(fft_data[:CHUNK // 2])  # Use only half of FFT (mirrored)

    print(freq_magnitude)  # Output the frequency data (for testing)

    # Clear the screen
    screen.fill((0, 0, 0))