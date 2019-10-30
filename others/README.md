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
