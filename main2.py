import librosa
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt

y1, sr1 = librosa.load("file1.wav", sr=None) 
y2, sr2 = librosa.load("file2.wav", sr=None)

target_sr = 16000
if sr1 != target_sr:
    y1 = librosa.resample(y1, orig_sr=sr1, target_sr=target_sr)
if sr2 != target_sr:
    y2 = librosa.resample(y2, orig_sr=sr2, target_sr=target_sr)

mfcc1 = librosa.feature.mfcc(y=y1, sr=target_sr, n_mfcc=13) 
mfcc2 = librosa.feature.mfcc(y=y2, sr=target_sr, n_mfcc=13)

mfcc1 = mfcc1.T
mfcc2 = mfcc2.T

flat_mfcc1 = mfcc1.flatten()
flat_mfcc2 = mfcc2.flatten()

cos_sim = cosine_similarity([flat_mfcc1], [flat_mfcc2])[0][0]
print("Cosine Similarity:", cos_sim)

dist, _ = librosa.sequence.dtw(mfcc1.T, mfcc2.T, metric='euclidean')
print("DTW Distance:", dist)

min_length = min(len(mfcc1), len(mfcc2))
mfcc1 = mfcc1[:min_length]
mfcc2 = mfcc2[:min_length]

mse = np.mean((mfcc1 - mfcc2) ** 2)
print("Mean Squared Error:", mse)

plt.figure(figsize=(10, 4))
librosa.display.specshow(mfcc1.T, sr=target_sr, x_axis='time')
plt.colorbar()
plt.title('MFCC (Speech 1)')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
librosa.display.specshow(mfcc2.T, sr=target_sr, x_axis='time')
plt.colorbar()
plt.title('MFCC (Speech 2)')
plt.tight_layout()
plt.show()