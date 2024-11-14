import streamlit as st
import requests
import os
from io import BytesIO

# Streamlit frontend
def streamlit_app():
    st.title("Video and Audio Capture")

    st.components.v1.html(
        """
        <video id="video" width="640" height="480" autoplay></video>
        <button id="startButton">Start Recording</button>
        <button id="stopButton">Stop Recording</button>

        <script>
            let mediaRecorder;
            let recordedChunks = [];

            const video = document.getElementById('video');
            const startButton = document.getElementById('startButton');
            const stopButton = document.getElementById('stopButton');

            navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                .then(stream => {
                    video.srcObject = stream;
                    mediaRecorder = new MediaRecorder(stream);

                    mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            recordedChunks.push(event.data);
                        }
                    };

                    mediaRecorder.onstop = () => {
                        const blob = new Blob(recordedChunks, { type: 'video/webm' });
                        const formData = new FormData();
                        formData.append('video', blob, 'recorded_video.webm');

                        fetch('/upload', {
                            method: 'POST',
                            body: formData
                        }).then(response => response.json())
                          .then(data => console.log(data))
                          .catch(error => console.error('Error:', error));

                        recordedChunks = [];
                    };
                });

            startButton.onclick = () => {
                mediaRecorder.start();
            };

            stopButton.onclick = () => {
                mediaRecorder.stop();
            };
        </script>
        """,
        height=600
    )


if __name__ == '__main__':
    # Run Streamlit app
    streamlit_app()
