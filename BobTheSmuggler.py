from core.operations.handlers import *
from core.logging.debug import SetLogging
from core.argsparser import SetupArgumentParse, ValidateArgs
from core.utilities.utils import CompressFileDir, DisplayBanner, cleanup

BANNER_PATH = "./resources/config/banner/banner.txt"

def main():
    DisplayBanner(os.path.abspath(BANNER_PATH))
    # Set up and parse arguments
    parser = SetupArgumentParse()
    args = parser.parse_args()

    # Set up logging
    if args.verbose:
        print(f"Verbose Mode: ON")
        SetLogging(args.verbose)
    else:
        print(f"Verbose Mode : OFF")

    # Validate arguments
    ValidateArgs(args)
    print(f"Starting Compression and Encryption stage...")
    PathToZIPFile = CompressFileDir(args.i, args.p, args.c)
    print(f"\033[93mCompression and Encryption stage completed. \033[0m\033[91mArchive file created : \033[0m\033[92m{PathToZIPFile}\033[0m | \033[91mSize : \033[0m\033[92m{round(os.path.getsize(PathToZIPFile)/1024)} bytes\033[0m\n")

    # Handling based on the type
    if args.t == 'html':
        HandleHTML(args, PathToZIPFile)
    elif args.t == 'png':
        HandlePNG(args, PathToZIPFile)
    elif args.t == 'gif':
        HandleGIF(args, PathToZIPFile)
    elif args.t == 'svg':
        HandleSVG(args, PathToZIPFile)
    else:
        SetLogging.error(f"Unsupported type: {args.t}")
        raise ValueError(f"Unsupported type: {args.t}")
    
    cleanup()

if __name__ == "__main__":
    main()
