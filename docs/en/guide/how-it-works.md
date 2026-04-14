# How It Works

Open Avatar Chat uses a modular Handler architecture, combining different ASR, LLM, TTS, and Avatar modules through configuration files.

## Architecture Overview

The system consists of these core modules:

- **Client Handler**: Manages WebRTC audio/video stream connections
- **VAD Handler**: Voice Activity Detection, identifying speech start/end
- **ASR Handler**: Automatic Speech Recognition, converting speech to text
- **LLM Handler**: Language model inference, generating dialogue responses
- **Agent Handler**: Multi-turn tool-calling Agent, replacing traditional LLM Handler (Beta)
- **TTS Handler**: Text-to-Speech, synthesizing response text into speech
- **Avatar Handler**: Digital human driver, generating facial animations from speech

## Performance

Using a PC with an i9-13900KF processor and Nvidia RTX 4090, the average response delay is about 2.2 seconds after ten tests.

The delay is measured from the end of user speech to the start of the digital human's speech, including RTC round-trip time, VAD stop delay, and computation time.

## Data Flow

1. User sends audio/video stream via browser (WebRTC)
2. VAD detects whether the user is speaking
3. ASR converts speech to text
4. LLM/Agent generates response text
5. TTS converts text to speech
6. Avatar generates facial animation from speech
7. Synthesized audio/video stream returns to user via WebRTC
