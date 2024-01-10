from core.logging.debug import logging

def SaveAsTemplate(ObfuscatedCodeJS, TemplateType, OutputFileName):
    logging.debug(f"Saving to {OutputFileName} with template type {TemplateType.upper()}.")

    # Common HTML template for 'html', 'png', 'gif'
    CommonHTMLTemplate = """
        <html>
        <body>
            <script type="application/javascript">{}</script>
        </body>
        </html>
    """

    # SVG template
    SVGTemplate = """
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <svg height="100%" version="1.1" viewBox="0 0 1700 863" width="100%" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <script type="text/javascript"><![CDATA[
                document.addEventListener("DOMContentLoaded", function() {{
                    {}
                }})]]></script>
        </svg>
    """

    # Template selection
    if TemplateType in ["html", "png", "gif"]:
        template = CommonHTMLTemplate.format(ObfuscatedCodeJS)
        with open(OutputFileName, "w") as file:
            file.write(template)
        logging.debug(f"HTML template written to {OutputFileName}.")
    elif TemplateType == "svg":
        template = SVGTemplate.format(ObfuscatedCodeJS)
        with open(OutputFileName, "w") as file:
            file.write(template)
        logging.debug(f"SVG template written to {OutputFileName}.")
    else:
        raise ValueError("Unsupported template type!")
    
