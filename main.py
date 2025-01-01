import librosa
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

y1, sr1 = librosa.load("file1.wav", sr=None) 
y2, sr2 = librosa.load("file2.wav", sr=None)

target_sr = 16000
if sr1 != target_sr:
    y1 = librosa.resample(y1, orig_sr=sr1, target_sr=target_sr)
if sr2 != target_sr:
    y2 = librosa.resample(y2, orig_sr=sr2, target_sr=target_sr)

S1 = librosa.feature.melspectrogram(y=y1, sr=target_sr, n_mels=128, fmax=8000)
S2 = librosa.feature.melspectrogram(y=y2, sr=target_sr, n_mels=128, fmax=8000)

log_S1 = librosa.power_to_db(S1, ref=np.max)
log_S2 = librosa.power_to_db(S2, ref=np.max)

flat_S1 = log_S1.flatten()
flat_S2 = log_S2.flatten()

cos_sim = cosine_similarity([flat_S1], [flat_S2])[0][0]
print("Cosine Similarity:", cos_sim)

mse = np.mean((flat_S1 - flat_S2) ** 2)
print("Mean Squared Error:", mse)

plt.figure(figsize=(10, 4))
librosa.display.specshow(log_S1, sr=target_sr, x_axis='time', y_axis='mel', fmax=8000)
plt.colorbar(format='%+2.0f dB')
plt.title('Mel Spectrogram (Speech 1)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
librosa.display.specshow(log_S2, sr=target_sr, x_axis='time', y_axis='mel', fmax=8000)
plt.colorbar(format='%+2.0f dB')
plt.title('Mel Spectrogram (Speech 2)')
plt.tight_layout()
plt.show()