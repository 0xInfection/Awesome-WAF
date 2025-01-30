## [`obfu.py`](https://github.com/0xinfection/awesome-waf/blob/master/others/obfu.py)
> A small script to encode and obfuscate your payloads easily to your desired encodings.

### Usage:
```
$ python obfu.py -h

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


usage: obfu.py [-h] -s STR -e ENC [-ueo] [-udi]

Obfuscates a given string with specified encoding.

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

options:
  -h, --help         show this help message and exit

Required Arguments:
  -s STR, --str STR  String to obfuscate
  -e ENC, --enc ENC  Encoding type (e.g., ibm037, utf-16)

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
