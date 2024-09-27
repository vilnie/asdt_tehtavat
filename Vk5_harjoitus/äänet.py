
import numpy as np
import pyaudio
import time
import sys
 
class Torvi:
    def __init__(self):
        # Alusta Pyaudio
        self.p = pyaudio.PyAudio()
        self.RATE = 44100  # Näytteenottotaajuus
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.RATE,
                                  output=True)
 
    def generate_sine_wave(self, frequency, duration):
        t = np.linspace(0, duration, int(self.RATE * duration), endpoint=False)
        return (0.5 * np.sin(2 * np.pi * frequency * t)).astype(np.float32)
   
    def generate_sine_wave_ikkunoitu(self, frequency, duration):
        t = np.linspace(0, duration, int(self.RATE * duration), endpoint=False)
        sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        blackman_window = np.blackman(len(t))
        return (sine_wave * blackman_window).astype(np.float32)
 
    def soita(self, frequency, duration, voimakkuus):
        audio_signal = voimakkuus/100*self.generate_sine_wave(frequency, duration)
        self.stream.write(audio_signal.tobytes())
 
    def soita_pehmea(self, frequency, duration, voimakkuus):
        audio_signal = voimakkuus/100*self.generate_sine_wave_ikkunoitu(frequency, duration)
        self.stream.write(audio_signal.tobytes())
 
    def soita_c(self):
        self.soita_pehmea(261.63,0.2,20)
 
    def soita_cy(self):
        self.soita_pehmea(1.05946*261.63,0.2,20)
 
    def soita_d(self):
        self.soita_pehmea(1.05946**2*261.63,0.2,20)
 
    def soita_dy(self):
        self.soita_pehmea(1.05946**3*261.63,0.2,20)
 
    def soita_e(self):
        self.soita_pehmea(1.05946**4*261.63,0.2,20)
 
    def soita_f(self):
        self.soita_pehmea(1.05946**5*261.63,0.2,20)
 
    def soita_fy(self):
        self.soita_pehmea(1.05946**6*261.63,0.2,20)
 
    def soita_g(self):
        self.soita_pehmea(1.05946**7*261.63,0.2,20)
 
    def soita_gy(self):
        self.soita_pehmea(1.05946**8*261.63,0.2,20)
 
    def soita_a(self):
        self.soita_pehmea(1.05946**9*261.63,0.2,20)
 
    def soita_ay(self):
        self.soita_pehmea(1.05946**10*261.63,0.2,20)
 
    def soita_b(self):
        self.soita_pehmea(1.05946**11*261.63,0.2,20)
 
    def __del__(self):
        # Sulje stream ja Pyaudio
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
 
# Esimerkki käytöstä
if __name__ == "__main__":
    torvi = Torvi()
    frequencies = [500, 1000, 1500, 2000, 2500]  # Taajuudet Hz
   
    #torvi.soita_pehmea(4*110,0.2,5)
 
    #Muista että kakkosen 12:s neliöjuuri on 1,05946
    #torvi.soita_pehmea(220,0.5,25)
    #torvi.soita_pehmea((1/1.05946)*220,0.2,25)
 
    #torvi.soita_c()
    #torvi.soita_e()
    #torvi.soita_e()
 
    #torvi.soita_c()
    #torvi.soita_fy()
    #torvi.soita_ay()
   
    torvi.soita_pehmea(250,1.5,20)
 
    sys.exit()
 
    lahtotaajuus=220
    for i in range(12):
        torvi.soita_pehmea(440*1.05946**(i),0.3,30)
   
 
    sys.exit()
 
    for taajuus in [1000,900,800,700]:
        torvi.soita_pehmea(taajuus,0.1,10)
 
    torvi.soita_pehmea(900,0.5,20)
    sys.exit()
 
    torvi.soita_pehmea(1000,0.2,10)
   
    #time.sleep(1)
 
    for freq in frequencies:    
        torvi.soita(freq, 0.1,10)
   
    for freq in frequencies:
        torvi.soita_pehmea(freq,0.1,10)