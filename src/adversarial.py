import numpy as np

def add_noise(features):
    print("[info] Applying adversarial noise...")

    noise = np.random.normal(0, 0.05, len(features[0]))

    noisy_features = [features[0] + noise]

    return noisy_features