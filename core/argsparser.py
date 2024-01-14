import argparse
import os

def SetupArgumentParse():
    
    # Setup argparse
    parser = argparse.ArgumentParser(description="Embeds EXE/DLL file into an HTML/SVG file.")
    parser.add_argument("-i", required=True, help="Path to the EXE/DLL file or directory (In case multiple files are provided). ", metavar='EXE_FILE')
    parser.add_argument("-p", required=False, help="Password for compression.", metavar='PASSWORD')
    parser.add_argument("-f",required=True, help="HTML Smuggled file (.html)", metavar='OUTPUT_HTML')
    parser.add_argument("-o", required=True, help="Downloaded file name (Your payload is in this file.)", metavar='OUTPUT_FILENAME')
    parser.add_argument("-t", choices=['html', 'svg', 'png', 'gif'], required=True, help="Type of embedded template.")
    parser.add_argument("-c", choices=['7z','zip'], default='zip', help="Compression format: 7z or zip (default: zip)")
    parser.add_argument("-u", required=False, help="URL for the embedded PNG image.", metavar='PNG_URL')
    parser.add_argument("-png", required=False, help="Path to the PNG file for embedding EXE/DLL.", metavar='PNG_FILE')
    parser.add_argument("-gif", required=False, help="Path to the GIF file for embedding EXE/DLL.", metavar='GIF_FILE')
    parser.add_argument("-e", help="HTML file to clone as template.", metavar='CUSTOM_FILE')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging.')
    
    return parser

def ValidateArgs(args):
    # Combine validations for 'png' and 'gif' types
    if args.t in ['png', 'gif']:
        ImageURL = getattr(args, 'u', None)
        LocalFileArg = getattr(args, args.t, None)

        if ImageURL and LocalFileArg:
            raise ValueError(f"You can only specify either -u (URL) or -{args.t} (local file path), not both.")
        elif not ImageURL and not LocalFileArg:
            raise ValueError(f"You must specify either -u (URL) or -{args.t} (local file path) when type is {args.t.upper()}.")
