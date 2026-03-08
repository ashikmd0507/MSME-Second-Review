# audio.py
"""
Handles generation of audio assets for the simulation.
"""
import pygame
import numpy

def generate_beep_sound(frequency=1000, duration=0.1, sample_rate=44100):
    """
    Generates a simple beep sound.
    :param frequency: The frequency of the beep in Hz.
    :param duration: The duration of the beep in seconds.
    :param sample_rate: The sample rate for the audio.
    :return: A pygame.mixer.Sound object.
    """
    num_samples = int(sample_rate * duration)
    
    # Create the sound wave (sine wave)
    t = numpy.linspace(0., duration, num_samples, endpoint=False)
    amplitude = 2**15 - 1 # Max amplitude for 16-bit audio
    data = amplitude * numpy.sin(2. * numpy.pi * frequency * t)
    
    # Pygame sounds need 2 channels (stereo), so we stack the data
    data = numpy.repeat(data.reshape(num_samples, 1), 2, axis=1)
    
    # Convert to a pygame Sound object
    sound = pygame.sndarray.make_sound(data.astype(numpy.int16))
    return sound
