from flask import Flask, request, jsonify
import librosa
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/compare', methods=['POST'])
def compare_audio():
    try:
        print("Request files:", request.files)

        file1 = request.files.get('file1')
        file2 = request.files.get('file2')

        if not file1 or not file2:
            return jsonify({'error': 'Files not received'}), 400

        y1, sr1 = librosa.load(file1, sr=16000)
        y2, sr2 = librosa.load(file2, sr=16000)

        print(f"File 1 length: {len(y1)}, File 2 length: {len(y2)}")

        mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1, n_mfcc=13).T
        mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2, n_mfcc=13).T

        min_length = min(len(mfcc1), len(mfcc2))
        mfcc1 = mfcc1[:min_length]
        mfcc2 = mfcc2[:min_length]

        flat_mfcc1 = mfcc1.flatten()
        flat_mfcc2 = mfcc2.flatten()
        similarity = cosine_similarity([flat_mfcc1], [flat_mfcc2])[0][0]


        print("Similarity:", similarity)

        # Decision threshold
        threshold = 0.8
        result = "Yes" if similarity >= threshold else "No"

        return jsonify({'similar': result})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
