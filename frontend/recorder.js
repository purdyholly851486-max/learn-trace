class WavRecorder {
  constructor() {
    this.stream = null;
    this.context = null;
    this.source = null;
    this.processor = null;
    this.sink = null;
    this.buffers = [];
    this.sampleRate = 44100;
    this.startedAt = null;
  }

  async start() {
    this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    this.context = new (window.AudioContext || window.webkitAudioContext)();
    this.sampleRate = this.context.sampleRate;
    this.source = this.context.createMediaStreamSource(this.stream);
    this.processor = this.context.createScriptProcessor(4096, 1, 1);
    this.sink = this.context.createGain();
    this.sink.gain.value = 0;
    this.buffers = [];
    this.startedAt = Date.now();

    this.processor.onaudioprocess = (event) => {
      const input = event.inputBuffer.getChannelData(0);
      this.buffers.push(new Float32Array(input));
    };

    this.source.connect(this.processor);
    this.processor.connect(this.sink);
    this.sink.connect(this.context.destination);
  }

  async stop() {
    if (!this.context) return null;
    const duration = (Date.now() - this.startedAt) / 1000;
    this.processor.disconnect();
    this.source.disconnect();
    this.sink.disconnect();
    this.stream.getTracks().forEach((track) => track.stop());
    await this.context.close();

    const samples = this._merge(this.buffers);
    const blob = this._encodeWav(samples, this.sampleRate);
    this.stream = null;
    this.context = null;
    this.source = null;
    this.processor = null;
    this.sink = null;
    return { blob, duration };
  }

  _merge(buffers) {
    const length = buffers.reduce((sum, b) => sum + b.length, 0);
    const out = new Float32Array(length);
    let offset = 0;
    for (const b of buffers) {
      out.set(b, offset);
      offset += b.length;
    }
    return out;
  }

  _encodeWav(samples, sampleRate) {
    const bytesPerSample = 2;
    const blockAlign = bytesPerSample;
    const buffer = new ArrayBuffer(44 + samples.length * bytesPerSample);
    const view = new DataView(buffer);

    const writeString = (offset, text) => {
      for (let i = 0; i < text.length; i += 1) view.setUint8(offset + i, text.charCodeAt(i));
    };

    writeString(0, 'RIFF');
    view.setUint32(4, 36 + samples.length * bytesPerSample, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * blockAlign, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, 16, true);
    writeString(36, 'data');
    view.setUint32(40, samples.length * bytesPerSample, true);

    let offset = 44;
    for (let i = 0; i < samples.length; i += 1) {
      const s = Math.max(-1, Math.min(1, samples[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
      offset += 2;
    }
    return new Blob([view], { type: 'audio/wav' });
  }
}

window.WavRecorder = WavRecorder;
