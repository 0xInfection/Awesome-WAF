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
