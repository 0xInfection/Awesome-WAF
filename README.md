# Awesome WAF ![Awesome](https://camo.githubusercontent.com/13c4e50d88df7178ae1882a203ed57b641674f94/68747470733a2f2f63646e2e7261776769742e636f6d2f73696e647265736f726875732f617765736f6d652f643733303566333864323966656437386661383536353265336136336531353464643865383832392f6d656469612f62616467652e737667 "Awesome")
> A curated list of awesome WAF stuff. 

![Main Logo](images/how-wafs-work.png 'How wafs work')

__A Concise Definition:__ A web application firewall is a form of firewall with a set of configured rules that controls input, output, and/or access from, to, or by an application or service. It operates by monitoring and potentially blocking the input, output, or system service calls that do not meet the configured policy of the firewall. *(Source [Wikipedia](https://en.wikipedia.org/wiki/Application_firewall))*

Feel free to [contribute]().

### Contents:
- [Awesome WAFs List](#awesome-waf-list)
- [Awesome Testing Methodology](#testing-methodology)
- [Awesome WAF Detection](#)
- [Awesome Evasion Techniques]()
- [Awesome Tools](#awesome-tools)
- [Awesome Blogs & Writeups](#blogs-and-writeups)
- [Awesome Presentations & Papers](#presentations--research-papers)

## Awesome WAFs List
<table>
	<tr>
		<td>
			<a href="http://360.cn">360 WangZhanBao WAF</a>
		</td>
		<td>
			A WAF solution from 360 Security Team.
		</td>
	</tr>
	<tr>
		<td>
			<a href="https://www.airlock.com/products/airlock-waf/">Airlock</a>
		</td>
		<td>
			The Airlock Web Application Firewall offers a unique combination of protective mechanisms for web applications. Each access is systematically monitored and filtered at every level. Used in conjunction with an authentication solution such as Airlock Login or IAM, Airlock WAF can force upstream user authentication and authorization.
			- __Brochure:__ https://www.airlock.com/media/medialibrary/2016/09/Airlock-Suite-en_web.pdf
		</td>
	</tr>
</table>

## Testing Methodology
Alright, now lets see the approach of testing WAFs. Wait, before that we need to know how they work right? Here you go.

### How WAFs Work:
- Using a set of rules to distinguish between normal requests and malicious requests.
- Sometimes they use a learning mode to add rules automatically through learning about user behaviour.

### Operation Modes:
- __Negative Model (Blacklist based)__ - 
One that defines what is not allowed. Eg. Block all `<script>*</script>` inputs.
- __Positive Model (Whitelist based)__ - 
One that defines what is allowed and rejects everything else.
- __Mixed/Hybrid Model (Inclusive model)__ -
One that uses a mixed concept of blacklisting and whitelisting stuff.

### Where To Look:
- Always look out for common ports that expose that a WAF `80`, `443`, `8000`, `8008`, `8080`, `8088`.
> __Tip:__ You can use automate this easily by commandline using a screenshot taker like [WebScreenShot](https://github.com/maaaaz/webscreenshot).
- Some WAFs set their own cookies in requests (eg. Citrix Netscaler, Yunsuo WAF).
- Some associate themselves with separate headers (eg. Anquanbao WAF, Amazon AWS WAF). 
- Some often alter headers and jumble characters to confuse attacker (eg. Citrix Netscaler, Big IP WAF).
- Some WAFs expose themselves in the response content (eg. DotDefender, Armor, truShield Sitelock).
- Other WAFs reply with unusual response codes upon malicious requests (eg. WebKnight).

### Detection Techniques:
1. Make a normal GET request from a browser, intercept and test response headers (specifically cookies).
2. Make a request from command line (eg. cURL), and test response content and headers (no user-agent included).
3. If there is a login page somewhere, try some common (easily detectable) payloads like `' or 1 = 1 --`.
4. If there is some search box or input field somewhere, try detecting payloads like `<script>alert()</script>`.
5. Make GET requests with outdated protocols like `HTTP/0.9` (`HTTP/0.9` does not support POST type queries).
6. Drop Action Technique - Send a raw crafted FIN/RST packet to server and identify response.
> __Tip:__ This method could be easily achieved with tools like [HPing3](http://www.hping.org) or [Scapy](https://scapy.net).
7. Side Channel Attacks - Examine the timing behaviour of the request and response content. 

## WAF Detection
Wanna detect WAFs? Lets see how.
> __NOTE__: This section contains manual WAF detection techniques. You might want to switch over to [next section](#awesome-tools). 

## WAF Evasion Techniques
Lets look at some methods of bypassing and evading WAFs.

## Awesome Tools
### WAF Fingerprinting:
__1. Fingerprinting with [NMap](https://nmap.org)__:

__Source:__ [GitHub](https://github.com/nmap/nmap) | [SVN](http://svn.nmap.org)
- Normal WAF Fingerprinting

```
nmap --script=http-waf-fingerprint <target>
```
- Intensive WAF Fingerprinting
```
nmap --script=http-waf-fingerprint  --script-args http-waf-fingerprint.intensive=1 <target>
```
- Generic Detection
```	
nmap --script=http-waf-detect <target>
```

__2. Fingerprinting with [WafW00f](https://github.com/EnableSecurity/wafw00f)__:

__Source:__ [GitHub](https://github.com/enablesecurity/wafw00f) | [Pypi](https://pypi.org/project/wafw00f)
```
wafw00f <target>
```

### WAF Testing:
- [WAFBench](https://github.com/microsoft/wafbench) - A WAF performance testing suite by [Microsoft](https://github.com/microsoft).
- [WAF Testing Framework](https://www.imperva.com/lg/lgw_trial.asp?pid=483) - A free WAF testing tool by [Imperva](https://imperva.com).

### WAF Evading:
__1. Evading WAFs with [SQLMap Tamper Scripts](https://medium.com/@drag0n/sqlmap-tamper-scripts-sql-injection-and-waf-bypass-c5a3f5764cb3)__:
- General Tamper Testing
```
tamper=apostrophemask,apostrophenullencode,base64encode,between,chardoubleencode,charencode,charunicodeencode,equaltolike,greatest,ifnull2ifisnull,multiplespaces,nonrecursivereplacement,percentage,randomcase,securesphere,space2comment,space2plus,space2randomblank,unionalltounion,unmagicquotes
```
- MSSQL Tamper Testing
```
tamper=between,charencode,charunicodeencode,equaltolike,greatest,multiplespaces,nonrecursivereplacement,percentage,randomcase,securesphere,sp_password,space2comment,space2dash,space2mssqlblank,space2mysqldash,space2plus,space2randomblank,unionalltounion,unmagicquotes
```
- MySQL Tamper Testing
```
tamper=between,bluecoat,charencode,charunicodeencode,concat2concatws,equaltolike,greatest,halfversionedmorekeywords,ifnull2ifisnull,modsecurityversioned,modsecurityzeroversioned,multiplespaces,nonrecursivereplacement,percentage,randomcase,securesphere,space2comment,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,unionalltounion,unmagicquotes,versionedkeywords,versionedmorekeywords,xforwardedfor
``` 
- Generic Tamper Testing 
```
sqlmap -u <target> --level=5 --risk=3 -p 'item1' --tamper=apostrophemask,apostrophenullencode,appendnullbyte,base64encode,between,bluecoat,chardoubleencode,charencode,charunicodeencode,concat2concatws,equaltolike,greatest,halfversionedmorekeywords,ifnull2ifisnull,modsecurityversioned,modsecurityzeroversioned,multiplespaces,nonrecursivereplacement,percentage,randomcase,randomcomments,securesphere,space2comment,space2dash,space2hash,space2morehash,space2mssqlblank,space2mssqlhash,space2mysqlblank,space2mysqldash,space2plus,space2randomblank,sp_password,unionalltounion,unmagicquotes,versionedkeywords,versionedmorekeywords
```

__2. Evading WAFs with [WAFNinja](https://waf.ninja/)__

__Source:__ [GitHub](https://github.com/khalilbijjou/wafninja)
- Fuzzing
```
python wafninja.py fuzz -u <target> -t xss
```
- Bypassing
```
python wafninja.py bypass -u <target> -p "name=<payload>&Submit=Submit" -t xss
```
- Insert Fuzzing
```
python wafninja.py insert-fuzz -i select -e select -t sql
```

__3. Evading WAFs with [WhatWaf](https://github.com/ekultek/whatwaf)__:

Source: [GitHub](https://github.com/ekultek/whatwaf)
```
whatwaf -u <target> --ra --throttle 2
```

## Presentations & Research Papers
### Presentations:
- [WAF Profiling & Evasion Techniques](presentations/OWASP%20WAF%20Profiling%20&%20Evasion.pdf) - A WAF testing and evasion guide from [OWASP](https://www.owasp.org).
- [Protocol Level WAF Evasion Techniques](presentations/BlackHat%20US%2012%20-%20Protocol%20Level%20WAF%20Evasion%20(Slides).pdf) - A presentation at about efficiently evading WAFs at protocol level from [BlackHat US 12](https://www.blackhat.com/html/bh-us-12/).
- [Analysing Attacking Detection Logic Mechanisms](presentations/BlackHat%20US%2016%20-%20Analysis%20of%20Attack%20Detection%20Logic.pdf) - A presentation about WAF logic applied to detecting attacks from [BlackHat US 16](https://www.blackhat.com/html/bh-us-16/).
- [WAF Bypasses and PHP Exploits](presentations/WAF%20Bypasses%20and%20PHP%20Exploits%20(Slides).pdf) - A presentation about evading WAFs and developing related PHP exploits.
- [Playing Around with WAFs](presentations/Playing%20Around%20with%20WAFs.pdf) - A small presentation about WAF profiling and playing around with them from [Defcon 16](http://www.defcon.org/html/defcon-16/dc-16-post.html).

### Research Papers:
- [WASC WAF Evaluation Criteria](papers/WASC%20WAF%20Evaluation%20Criteria.pdf) - A guide for WAF Evaluation from [Web Application Security Consortium](http://www.webappsec.org)
- [Protocol Level WAF Evasion](papers/Qualys%20Guide%20-%20Protocol-Level%20WAF%20Evasion.pdf) - A protocol level WAF evasion techniques and analysis by [Qualys](https://www.qualys.com).
- [WAF Evasion Testing](papers/SANS%20Guide%20-%20WAF%20Evasion%20Testing.pdf) - A WAF evasion testing guide from [SANS](https://www.sans.org).
- [Bypassing all WAF XSS Filters](papers/Evading%20All%20Web-Application%20Firewalls%20XSS%20Filters.pdf) - A paper about bypassing all XSS filter rules and evading WAFs for XSS. 
- [Neural Network based WAF for SQLi](papers/Artificial%20Neural%20Network%20based%20WAF%20for%20SQL%20Injection) - A paper about building a neural network based WAF for detecting SQLi attacks.