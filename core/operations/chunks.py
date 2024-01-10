import struct
import zlib

# Create a custom chunk to hold the EXE/DLL data in 7z/Zip Format (Obviously XOR encoded)
# The chunk has the following format:
# Length (4 bytes) + Chunk Type (4 bytes) + Chunk Data + CRC (4 bytes)
def CustomImageChunk(ChunkType, ChunkData, ImageType):
    if ImageType == 'png':
        ChunkLength = len(ChunkData)
        crc = zlib.crc32(ChunkType + ChunkData)
        print(f"\033[93mConstructing a custom Chunk Type: \033[0m\033[91m{ChunkType.decode('utf-8')}\033[0m\033[93m || Chunk Data: \033[0m\033[91m 0x{ChunkData[:8].hex()}\033[0m\033[93m || Checksum value : \033[0m\033[92m{hex(crc)}\033[0m\033[93m for {ImageType.upper()}\033[0m")
        return struct.pack(">I", ChunkLength) + ChunkType + ChunkData + struct.pack(">I", crc)
    elif ImageType == 'gif':
        print(f"\033[93mConstructing a basic Chunk Type: \033[0m\033[91m{ChunkType.decode('utf-8')}\033[0m\033[93m || Chunk Data: \033[0m\033[91m 0x{ChunkData[:8].hex()}\033[0m\033[93m for {ImageType.upper()}\033[0m")
        return ChunkType + ChunkData