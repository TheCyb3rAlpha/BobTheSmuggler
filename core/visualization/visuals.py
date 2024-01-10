from core import logging
import struct

def VisualizePNG(PNGFilePath, InputFilePath=None):
    # Initializes a dictionary that specifies the column widths for a formatted print statement. This helps in pretty-printing the chunk details in a table format.
    ColumnWidth = {'ChunkType': 10, 'PreviewChunkData': 20, 'crc': 10, 'ascii': 10, 'ExtraInfo': 25}
    
    # Sets up a string format template that will be used for displaying chunk information.
    ChunkPrintFormat = "{ChunkType:<{ChunkType_w}} | {PreviewChunkData:<{PreviewChunkData_w}} | {crc:<{crc_w}} | {ascii:<{ascii_w}} | {ExtraInfo:<{ExtraInfo_w}}"

    # Initial header
    headers = {'ChunkType': 'Chunk Type', 'PreviewChunkData': 'Data Preview', 'crc': 'CRC (Hex)', 'ascii': 'ASCII', 'ExtraInfo': 'Extra Info'}

    # Print the headers of the table using the format specified above.
    print(ChunkPrintFormat.format(**{**headers, **{k+'_w': v for k, v in ColumnWidth.items()}}))
    print('-' * (sum(ColumnWidth.values()) + 9))

    # This dictionary contains special chunk types ('exEf' and 'xkEy') and the corresponding visual codes and extra information to display.
    SpecialChunks = {
        'exEf': ("\033[93m", "(!!ZIP got XORED!! File: {EmbeddedInputFile} || Size: {EmbeddedInputFileSize} bytes)\033[0m"),
        'xkEy': ("\033[91m", "(XOR Key: {KeyXOR})\033[0m")
    }

    with open(PNGFilePath, "rb") as f:
        # Read PNG signature (8 bytes)
        if f.read(8) != b'\x89PNG\r\n\x1a\n':
            logging.error("Not a valid PNG file.")
            return

        while True:
            # Reads 4 bytes to get the length of the chunk.
            LengthBytes = f.read(4)
            if len(LengthBytes) < 4:
                break  # EOF
            
            ChunkLength = struct.unpack(">I", LengthBytes)[0]
            ChunkType = f.read(4)
            ChunkData = f.read(ChunkLength)
            CRCbytes = f.read(4)
            ChunkCRC = struct.unpack(">I", CRCbytes)[0]
            
            # Creates a preview of the first 4 bytes of chunk data in hexadecimal form.
            PreviewChunkData = ' '.join(f"{byte:02x}" for byte in ChunkData[:4])
            
            # Creates an ASCII preview of the first 4 bytes of the chunk data.
            PreviewASCII = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in ChunkData[:4])

            ChunkTypeStr = ChunkType.decode('utf-8')

            ExtraInfo = ''
            ColorCode = ''
            # Checks if the chunk is a special one ('exEf' or 'xkEy'), and if so, sets the ExtraInfo and ColorCode accordingly.
            if ChunkTypeStr in SpecialChunks:
                ColorCode, ExtraInfoTemplate = SpecialChunks[ChunkTypeStr]
                if ChunkTypeStr == 'exEf':
                    ExtraInfo = ExtraInfoTemplate.format(EmbeddedInputFile=InputFilePath, EmbeddedInputFileSize=len(ChunkData))
                else:  # xkEy
                    ExtraInfo = ExtraInfoTemplate.format(KeyXOR=ChunkData.hex())

            # Line prints the chunk information using the formatting specified earlier.
            print(ColorCode + ChunkPrintFormat.format(
                ChunkType=ChunkTypeStr,
                PreviewChunkData=PreviewChunkData,
                crc=hex(ChunkCRC),
                ascii=PreviewASCII,
                ExtraInfo=ExtraInfo,
                **{k+'_w': v for k, v in ColumnWidth.items()}
            ))