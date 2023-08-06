import random

import librosa
import numpy as np

from audiomentations.core.transforms_interface import BasicTransform


class AddGaussianNoise(BasicTransform):
    """Add gaussian noise to the samples"""

    def __init__(self, min_amplitude=0.001, max_amplitude=0.015, p=0.5):
        super().__init__(p)
        self.min_amplitude = min_amplitude
        self.max_amplitude = max_amplitude

    def apply(self, samples, sample_rate):
        noise = np.random.randn(len(samples)).astype(np.float32)
        amplitude = random.uniform(self.min_amplitude, self.max_amplitude)
        samples = samples + amplitude * noise
        return samples


class TimeStretch(BasicTransform):
    """Time stretch the signal without changing the pitch"""

    def __init__(self, min_rate=0.8, max_rate=1.25, leave_length_unchanged=True, p=0.5):
        super().__init__(p)
        assert min_rate > 0.1
        assert max_rate < 10
        assert min_rate <= max_rate
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.leave_length_unchanged = leave_length_unchanged

    def apply(self, samples, sample_rate):
        """
        If `rate > 1`, then the signal is sped up.
        If `rate < 1`, then the signal is slowed down.
        """
        rate = random.uniform(self.min_rate, self.max_rate)
        time_stretched_samples = librosa.effects.time_stretch(samples, rate)
        if self.leave_length_unchanged:
            # Apply zero padding if the time stretched audio is not long enough to fill the
            # whole space, or crop the time stretched audio if it ended up too long.
            padded_samples = np.zeros(shape=samples.shape, dtype=samples.dtype)
            window = time_stretched_samples[: samples.shape[0]]
            actual_window_length = len(window)  # may be smaller than samples.shape[0]
            padded_samples[:actual_window_length] = window
            time_stretched_samples = padded_samples
        return time_stretched_samples


class PitchShift(BasicTransform):
    """Pitch shift the sound up or down without changing the tempo"""

    def __init__(self, min_semitones=-4, max_semitones=4, p=0.5):
        super().__init__(p)
        assert min_semitones >= -12
        assert max_semitones <= 12
        assert min_semitones <= max_semitones
        self.min_semitones = min_semitones
        self.max_semitones = max_semitones

    def apply(self, samples, sample_rate):
        num_semitones = random.uniform(self.min_semitones, self.max_semitones)
        pitch_shifted_samples = librosa.effects.pitch_shift(
            samples, sample_rate, n_steps=num_semitones
        )
        return pitch_shifted_samples


class Shift(BasicTransform):
    """
    Shift the samples forwards or backwards. Samples that roll beyond the first or last position
    are re-introduced at the last or first.
    """

    def __init__(self, min_fraction=-0.5, max_fraction=0.5, p=0.5):
        """
        :param min_fraction: float, fraction of total sound length
        :param max_fraction: float, fraction of total sound length
        :param p:
        """
        super().__init__(p)
        assert min_fraction >= -1
        assert max_fraction <= 1
        self.min_fraction = min_fraction
        self.max_fraction = max_fraction

    def apply(self, samples, sample_rate):
        num_places_to_shift = int(
            round(random.uniform(self.min_fraction, self.max_fraction) * len(samples))
        )
        shifted_samples = np.roll(samples, num_places_to_shift)
        return shifted_samples


class Normalize(BasicTransform):
    """
    Apply a constant amount of gain, so that highest signal level present in the sound becomes
    0 dBFS, i.e. the loudest level allowed if all samples must be between -1 and 1. Also known
    as peak normalization.
    """

    def __init__(self, p=0.5):
        super().__init__(p)

    def apply(self, samples, sample_rate):
        max_amplitude = np.amax(np.abs(samples))
        normalized_samples = samples / max_amplitude
        return normalized_samples
