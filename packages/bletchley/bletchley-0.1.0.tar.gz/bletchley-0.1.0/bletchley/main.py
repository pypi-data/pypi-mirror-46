from cryptanalysis.frequency_analysis import frequency_analysis
from ciphers.caesar_cipher import CaesarCipher
import random
import sys

print(sys.argv[0])

with open('text_sample.txt', 'r') as text_file:
    text = text_file.read()

c_cipher = CaesarCipher()

sample_size = 10
correct = 0
iterations = 1
for sample in range(0, sample_size):
    shift = random.randint(1, 26)
    trial_shifts = []
    for iteration in range(0, iterations):
        cipher = c_cipher.encrypt(text, shift)
        trial_shift = frequency_analysis(cipher)
        print(shift, trial_shift)
