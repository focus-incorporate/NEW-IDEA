class AudioProcessor extends AudioWorkletProcessor {
  process(inputs, outputs, parameters) {
    const input = inputs[0];
    const channel = input[0];
    
    if (channel && channel.length > 0) {
      this.port.postMessage({
        audioData: channel.buffer
      });
    }
    
    return true;
  }
}

registerProcessor('audio-processor', AudioProcessor);
