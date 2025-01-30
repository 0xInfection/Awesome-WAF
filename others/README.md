## [`obfu.py`](https://github.com/0xinfection/awesome-waf/blob/master/others/obfu.py)
> A small script to encode and obfuscate your payloads easily to your desired encodings.

### Usage:
```
$ python obfu.py -h

        OBFUSCATOR

usage: python3 obfu.py [-h] [-s STR] [-e ENC] [-ueo] [-udi]

Required Arguments:
  -s STR, --str STR  String to obfuscate
  -e ENC, --enc ENC  Encoding type. eg: ibm037, utf16, etc

Optional Arguments:
  -ueo               URL Encode Output
  -udi               URL Decode Input
  -info              Show encoding guidelines

    Encoding Guidelines for Various Environments:

    Nginx, uWSGI-Django-Python3:
    - Supported Encodings: IBM037, IBM500, cp875, IBM1026, IBM273
    - Query string and body need to be encoded.
    - URL-decoded parameters in query string and body.
    - Equal sign and ampersand needed to be encoded as well (no URL encoding).

    Nginx, uWSGI-Django-Python2:
    - Supported Encodings: IBM037, IBM500, cp875, IBM1026, utf-16, utf-32, utf-32BE, IBM424
    - Query string and body need to be encoded.
    - URL-decoded parameters in query string and body afterward.
    - Equal sign and ampersand should not be encoded in any way.

    Apache-TOMCAT8-JVM1.8-JSP:
    - Supported Encodings: IBM037, IBM500, IBM870, cp875, IBM1026, IBM01140-IBM01149, utf-16, utf-32, utf-32BE, IBM273-IBM285, IBM290, IBM297, IBM420, IBM424, IBM-Thai, IBM871, cp1025
    - Query string in its original format (could be URL-encoded as usual).
    - Body could be sent with/without URL encoding.
    - Equal sign and ampersand should not be encoded in any way.

    Apache-TOMCAT7-JVM1.6-JSP:
    - Supported Encodings: Similar to Apache-TOMCAT8.
    - Query string in its original format (could be URL-encoded as usual).
    - Body could be sent with/without URL encoding.
    - Equal sign and ampersand should not be encoded in any way.

    IIS6, 7.5, 8, 10 - ASPX (v4.x):
    - Supported Encodings: IBM037, IBM500, IBM870, cp875, IBM1026, IBM01047, IBM01140-IBM01149, utf-16, unicodeFFFE, utf-32, utf-32BE, IBM273-IBM285, IBM290, IBM297, IBM420, IBM423, IBM424, x-EBCDIC-KoreanExtended, IBM-Thai, IBM871, IBM880, IBM905, IBM00924, cp1025
    - Query string in its original format (could be URL-encoded as usual).
    - Body could be sent with/without URL encoding.
    - Equal sign and ampersand should not be encoded in any way.
```
### Example Usage:
```
$ python3 obfu.py -s 'param=<svg/onload=prompt()//' -e ibm037 -ueo
```
```
        OBFUSCATOR

Input: param=<svg/onload=prompt()//
Output: %97%81%99%81%94~L%A2%A5%87a%96%95%93%96%81%84~%97%99%96%94%97%A3M%5Daa
```

### Sidenote:
This script can encode in all types of formats which are supported by the Python Engine.
