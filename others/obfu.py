# Modified from @irsdl's script
# Enhancements include improved encoding validation, error handling, and safer parameter parsing, 
# with contributions from Wild West CyberSecurity and Tequila_Ninja.
import urllib.parse
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

lackoFart = '''
    ,o888888o.     8 888888888o   8 8888888888   8 8888      88    d888888o.       ,o888888o.           .8.    8888888 8888888888 ,o888888o.     8 888888888o.   
 . 8888     `88.   8 8888    `88. 8 8888         8 8888      88  .`8888:' `88.    8888     `88.        .888.         8 8888    . 8888     `88.   8 8888    `88.  
,8 8888       `8b  8 8888     `88 8 8888         8 8888      88  8.`8888.   Y8 ,8 8888       `8.      :88888.        8 8888   ,8 8888       `8b  8 8888     `88  
88 8888        `8b 8 8888     ,88 8 8888         8 8888      88  `8.`8888.     88 8888               . `88888.       8 8888   88 8888        `8b 8 8888     ,88  
88 8888         88 8 8888.   ,88' 8 888888888888 8 8888      88   `8.`8888.    88 8888              .8. `88888.      8 8888   88 8888         88 8 8888.   ,88'  
88 8888         88 8 8888888888   8 8888         8 8888      88    `8.`8888.   88 8888             .8`8. `88888.     8 8888   88 8888         88 8 888888888P'   
88 8888        ,8P 8 8888    `88. 8 8888         8 8888      88     `8.`8888.  88 8888            .8' `8. `88888.    8 8888   88 8888        ,8P 8 8888`8b       
`8 8888       ,8P  8 8888      88 8 8888         ` 8888     ,8P 8b   `8.`8888. `8 8888       .8' .8'   `8. `88888.   8 8888   `8 8888       ,8P  8 8888 `8b.     
 ` 8888     ,88'   8 8888    ,88' 8 8888           8888   ,d8P  `8b.  ;8.`8888    8888     ,88' .888888888. `88888.  8 8888    ` 8888     ,88'   8 8888   `8b.   
    `8888888P'     8 888888888P   8 8888            `Y88888P'    `Y8888P ,88P'     `8888888P'  .8'       `8. `88888. 8 8888       `8888888P'     8 8888     `88. 

'''

IBM_ENCODING_MAP = {
    "ibm037": "cp037",
    "ibm500": "cp500",
    "cp875": "cp875",
    "ibm1026": "cp1026",
    "ibm273": "cp273",
    "ibm424": "cp424",
    "ibm870": "cp870",
    "ibm01140": "cp1140",
    "ibm01141": "cp1140",
    "ibm01142": "cp1140",
    "ibm01143": "cp1140",
    "ibm01144": "cp1140",
    "ibm01145": "cp1140",
    "ibm01146": "cp1140",
    "ibm01147": "cp1140",
    "ibm01148": "cp1140",
    "ibm01149": "cp1140",
    "ibm277": "cp500",
    "ibm278": "cp500",
    "ibm280": "cp500",
    "ibm284": "cp500",
    "ibm285": "cp500",
    "ibm290": "cp500",
    "ibm297": "cp500",
    "ibm420": "cp500",
    "ibm423": "cp500",
    "ibm-thai": "cp1160",
    "ibm871": "cp871",
    "ibm880": "cp500",
    "ibm905": "cp500",
    "ibm00924": "utf-16",
    "x-ebcdic-koreanextended": "cp933",
    "ibm01047": "cp1047",
    "unicodefffe": "utf-16",
    "utf-32be": "utf-32-be",
}


additional_info = """
Target Systems and Encoding Guidelines:

Nginx, uWSGI-Django-Python3
-----------------------------------
Supported Encodings: IBM037, IBM500, cp875, IBM1026, IBM273
- Query string and body need to be encoded.
- URL-decoded parameters in query string and body.
- Equal sign and ampersand must be encoded (no URL encoding).

Nginx, uWSGI-Django-Python2
-----------------------------------
Supported Encodings: IBM037, IBM500, cp875, IBM1026, utf-16, utf-32, utf-32BE, IBM424
- Query string and body need to be encoded.
- URL-decoded parameters in query string and body afterwards.
- Equal sign and ampersand should NOT be encoded.

Apache-TOMCAT8-JVM1.8-JSP
-----------------------------------
Supported Encodings: IBM037, IBM500, IBM870, cp875, IBM1026, IBM01140-IBM01149, utf-16, utf-32, utf-32BE, IBM273-IBM285, IBM290, IBM297, IBM420, IBM424, IBM-Thai, IBM871, cp1025
- Query string remains in original format (URL encoding allowed).
- Body can be sent with/without URL encoding.
- Equal sign and ampersand should NOT be encoded.

Apache-TOMCAT7-JVM1.6-JSP
-----------------------------------
Supported Encodings: IBM037, IBM500, IBM870, cp875, IBM1026, IBM01140-IBM01149, utf-16, utf-32, utf-32BE, IBM273, IBM277, IBM278, IBM280, IBM284, IBM285, IBM297, IBM420, IBM424, IBM-Thai, IBM871, cp1025
- Query string remains in original format (URL encoding allowed).
- Body can be sent with/without URL encoding.
- Equal sign and ampersand should NOT be encoded.

IIS6, 7.5, 8, 10 - ASPX (v4.x)
-----------------------------------
Supported Encodings: IBM037, IBM500, IBM870, cp875, IBM1026, IBM01047, IBM01140-IBM01149, utf-16, unicodeFFFE, utf-32, utf-32BE, IBM273-IBM285, IBM290, IBM297, IBM420, IBM423, IBM424, x-EBCDIC-KoreanExtended, IBM-Thai, IBM871, IBM880, IBM905, IBM00924, cp1025
- Query string remains in original format (URL encoding allowed).
- Body can be sent with/without URL encoding.
- Equal sign and ampersand should NOT be encoded.
"""

def main():
    print(lackoFart)

    parser = ArgumentParser(
        description="Obfuscates a given string with specified encoding.\n" + additional_info,
        formatter_class=RawTextHelpFormatter
    )
    
    # A simple hack to have required arguments and optional arguments separately
    required = parser.add_argument_group('Required Arguments')
    optional = parser.add_argument_group('Optional Arguments')
    
    # Required Options
    required.add_argument('-s', '--str', help='String to obfuscate', dest='str', required=True)
    required.add_argument('-e', '--enc', help='Encoding type (e.g., ibm037, utf-16)', dest='enc', required=True)
    
    # Optional Arguments (main stuff and necessary)
    optional.add_argument('-ueo', help='URL Encode Output', dest='ueo', action='store_true')
    optional.add_argument('-udi', help='URL Decode Input', dest='udi', action='store_true')

    # If no arguments are provided, print help + additional info and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    print('Input: %s' % (args.str))
    print('Output: %s' % (paramEncode(params=args.str, charset=args.enc, urlDecodeInput=args.udi, urlEncodeOutput=args.ueo)))

def paramEncode(params="", charset="", encodeEqualSign=False, encodeAmpersand=False, urlDecodeInput=True, urlEncodeOutput=True):
    result = ""
    equalSign = "="
    ampersand = "&"

    # ✅ Convert charset to lowercase and map it
    original_charset = charset.lower()
    mapped_charset = IBM_ENCODING_MAP.get(original_charset, original_charset)

    if not mapped_charset:
        print(f"❌ Error: Encoding '{original_charset}' is not supported.")
        sys.exit(1)

    try:
        if '&' in params and '=' in params:  # Ensuring params contain both delimiters
            if encodeEqualSign:
                equalSign = equalSign.encode(mapped_charset, errors="replace").decode(mapped_charset, errors="replace")
            if encodeAmpersand:
                ampersand = ampersand.encode(mapped_charset, errors="replace").decode(mapped_charset, errors="replace")

            params_list = params.split("&")
            for param_pair in params_list:
                if "=" in param_pair:
                    param, value = param_pair.split("=", 1)  # Split only at first '='
                else:
                    param, value = param_pair, ""

                if urlDecodeInput:
                    param = urllib.parse.unquote(param)
                    value = urllib.parse.unquote(value)

                # ✅ Handle correct encoding
                param = param.encode(mapped_charset, errors="replace")
                value = value.encode(mapped_charset, errors="replace")

                if urlEncodeOutput:
                    param = urllib.parse.quote_plus(param)
                    value = urllib.parse.quote_plus(value)

                if result:
                    result += ampersand
                result += param + equalSign + value

        else:
            if urlDecodeInput:
                params = urllib.parse.unquote(params)

            # ✅ Encode the whole string properly
            result = params.encode(mapped_charset, errors="replace")

            if urlEncodeOutput:
                result = urllib.parse.quote_plus(result)

    except LookupError:
        print(f"❌ Error: Encoding '{mapped_charset}' is not supported in python and/or isnt a recognized/valid encoding.")
        sys.exit(1)

    return result


if __name__ == '__main__':
    main()
