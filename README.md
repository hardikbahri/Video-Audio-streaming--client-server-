## Video and Audio Streaming Client and Server

This project involves a Python-based client and server setup for streaming video and audio frames over UDP and TCP protocols. The client receives frames, while the server sends frames. Below are detailed explanations and setup instructions for both the client and server components.

---


#### Description
The client code receives video frames using OpenCV, sockets, and base64 encoding. It also receives audio frames using PyAudio and sockets. It runs concurrently using `ThreadPoolExecutor` to handle both video and audio streams.



#### Description
The server code sends video frames using OpenCV, base64 encoding, and sockets. It also sends audio frames using PyAudio and sockets. It runs concurrently using `ThreadPoolExecutor` to handle video encoding, video transmission, and audio transmission.


### Usage

1. **Client Side**: Run the client code to receive and display video and audio frames. Adjust the `host_ip` variable to match the server's IP address.

2. **Server Side**: Run the server code to send video and audio frames. Adjust the `host_ip` variable to match the server's IP address.

3. **Interaction**: Use the 'q' key to quit the video streaming windows on both client and server sides.

---

### Prerequisites

- Python 3.x
- OpenCV
- NumPy
- PyAudio
- `ffmpeg` (for audio conversion)

Install Python dependencies using pip:

```bash
pip install opencv-python numpy pyaudio
```

---

### Credits

This project utilizes Python libraries and concepts including OpenCV for image processing, PyAudio for audio streaming, and sockets for network communication. Special thanks to the Python community and library developers for their contributions.

