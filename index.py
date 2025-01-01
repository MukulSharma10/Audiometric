import librosa
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def compute_mfcc(file_path, target_sr=16000, n_mfcc=13):
    try:
        y, sr = librosa.load(file_path, sr=None)  
        if sr != target_sr:
            y = librosa.resample(y, orig_sr=sr, target_sr=target_sr) 
        mfcc = librosa.feature.mfcc(y=y, sr=target_sr, n_mfcc=n_mfcc)  
        return mfcc.T 
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        exit(1)

def compare_mfcc(mfcc1, mfcc2):
    min_length = min(len(mfcc1), len(mfcc2))
    mfcc1, mfcc2 = mfcc1[:min_length], mfcc2[:min_length]
    flat_mfcc1, flat_mfcc2 = mfcc1.flatten(), mfcc2.flatten()

    cos_sim = cosine_similarity([flat_mfcc1], [flat_mfcc2])[0][0]
    return cos_sim

def main():
    file1 = "file1.wav" 
    file2 = "file2.wav"  
    threshold = 0.9  

    print(f"Processing files:\n  File 1: {file1}\n  File 2: {file2}")

    print("Computing MFCCs...")
    mfcc1 = compute_mfcc(file1)
    mfcc2 = compute_mfcc(file2)

    print("Comparing MFCCs...")
    similarity = compare_mfcc(mfcc1, mfcc2)

    print(f"Similarity Score: {similarity:.4f}")
    if similarity >= threshold:
        print("Access Granted")
        print("Files are similar.")
    else:
        print("Access Denied")
        print("Files are not similar.")

if __name__ == "__main__":
    main()
