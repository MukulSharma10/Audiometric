let mediaRecorder;
let audioChunks = [];

// Select DOM elements
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const audioPlayback = document.getElementById('audioPlayback');
const downloadLink = document.getElementById('downloadLink');

// Event listeners
recordButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);

async function startRecording() {
  // Request access to microphone
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  
  // Create a MediaRecorder instance
  mediaRecorder = new MediaRecorder(stream);

  // Start recording
  mediaRecorder.start();
  recordButton.disabled = true;
  stopButton.disabled = false;

  // Capture audio chunks
  mediaRecorder.ondataavailable = event => {
    audioChunks.push(event.data);
  };

  // Reset audio chunks when recording stops
  mediaRecorder.onstop = () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    audioChunks = []; // Clear the buffer

    // Create an audio URL and set it to the audio element
    const audioURL = URL.createObjectURL(audioBlob);
    audioPlayback.src = audioURL;

    // Set up the download link
    downloadLink.href = audioURL;
    downloadLink.style.display = 'block';
  };

  console.log("Recording started...");
}

function stopRecording() {
  mediaRecorder.stop();
  recordButton.disabled = false;
  stopButton.disabled = true;
  console.log("Recording stopped.");
}
