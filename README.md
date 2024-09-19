# Audio Encryption and Decryption with ElGamal Algorithm
This repository provides a Python implementation for encrypting and decrypting audio files (WAV format) using the ElGamal encryption algorithm. 

## Overview
The program splits the audio data into blocks, encrypts each block, and stores the encrypted data. Decryption reconstructs the original audio file, which is then compared with the original to verify the integrity of the encryption and decryption processes.

## Files
`encrypt.py:`
* Reads a WAV audio file.  
* Splits the audio data into blocks.  
* Encrypts each block using the ElGamal encryption algorithm.  
* Saves the encrypted data and the private key.

`decrypt.py:`
* Loads the encrypted audio data and private key.
* Decrypts the encrypted blocks.
* Reconstructs the original audio file.
* Validates the decrypted file by comparing it to the original audio file.

`validate.py:`
* Reads audio file parameters.
* Validates whether the decrypted audio file matches the original audio file (ignoring the number of frames).

## Required Python libraries:
`numpy`
`wave`
`pickle`
`secrets`
`random`
`sympy`

### You can install the necessary libraries by running:

    pip install numpy sympy

## Usage
To encrypt an audio file (input.wav), run the encrypt.py script.  
To decrypt the encrypted audio file, run the decrypt.py script.