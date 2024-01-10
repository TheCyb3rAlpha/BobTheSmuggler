from core.operations.handlers import *
from core.logging.debug import SetLogging
from core.argsparser import SetupArgumentParse, ValidateArgs
from core.utilities.utils import CompressThenEncode64, DisplayBanner, cleanup

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
    PathToZIPFile = CompressThenEncode64(args.i, args.p, args.c)
    print(PathToZIPFile)

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
