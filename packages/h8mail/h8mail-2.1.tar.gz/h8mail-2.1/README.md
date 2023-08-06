<p align="center">
  <img src="https://i.postimg.cc/LXR6Jq8Y/logo-transparent.png" width="420" title="h8maillogo">
</p>



![PyPI - Python Version](https://img.shields.io/pypi/pyversions/h8mail.svg) [![travis](https://img.shields.io/travis/khast3x/h8mail.svg)](https://travis-ci.org/khast3x/h8mail)
> Email OSINT and password finder.  
> Use h8mail to find passwords through [different breach and reconnaissance services](#apis), local breaches such as Troy Hunt's "Collection1" or the infamous "Breach Compilation" torrent.  
> First Anniversary update, feedback and pull requests are welcomed :heart: :birthday:

##  :tangerine: Features

* :mag_right: Email pattern matching (reg exp), useful for reading from other tool outputs
* :dizzy: :new: Loosey patterns for local searchs ("john.smith", "evilcorp") 
* :package: :new: Painless install. Available through `pip`, only requires `requests`
* :whale: Small and fast Alpine Dockerfile available
* :white_check_mark: :new: CLI or Bulk file-reading for targeting
* :memo: Output to CSV file
* :muscle: Compatible with the "Breach Compilation" torrent scripts
* :house: :new: Search .txt and .gz files locally using multiprocessing
  * :cyclone: Compatible with "Collection#1"
* :fire: Get related emails
* :dragon_face: :new: Chase and target related emails in ongoing search
* :crown: Supports premium lookup services for advanced users
* :books: Regroup breach results for all targets and methods
* :rainbow: Delicious colors

#### Demos

######  :unlock: Out of the box

![1](/doc/h8mail1.gif)

###### :rocket: With API services

![2](/doc/h8mail2.gif)

###### :minidisc: With the BreachedCompilation torrent
![3](/doc/h8mail3.gif)

####  APIs

| Service                                               	|                     Functions                     	|       Status       	|
|-------------------------------------------------------	|:-------------------------------------------------:	|:------------------:	|
| [HaveIBeenPwned](https://haveibeenpwned.com/)         	|              Number of email breaches              	|    :white_check_mark:    	|
| [Hunter.io](https://hunter.io/) - Public              	|              Number of related emails             	| :white_check_mark: 	|
| [Hunter.io](https://hunter.io/) - Service (free tier) 	|              Cleartext related emails             	| :white_check_mark: 	|
| [WeLeakInfo](https://weleakinfo.com/) - Public        	|        Number of search-able breach results       	|      :customs:     	|
| [WeLeakInfo](https://weleakinfo.com/) - Service       	|        Cleartext passwords, hashs and salts       	|       :soon:       	|
| [Snusbase](https://snusbase.com/) - Service           	| Cleartext passwords, hashs and salts - Fast :zap: 	| :white_check_mark: 	|
| [Leak-Lookup](https://leak-lookup.com/) - Public :new:     	| Number of search-able breach results              	| :white_check_mark: 	|
| [Leak-Lookup](https://leak-lookup.com/) - Service :new:     	| Cleartext passwords, hashs and salts              	| :white_check_mark: 	|


## :tangerine: Requirements

h8mail 2.0 only requires `requests` to run.

## :tangerine: Install

### Stable release (best)

To install h8mail, run this command in your terminal:

```bash
$ pip3 install --user h8mail
```

**And that's basically it**.  
This is the preferred method to install h8mail, as it will always install the most recent stable release.

If you don't have [`pip`](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide
you through the process.

### From sources

The sources for h8mail can be downloaded from the [Github repo](https://github.com/khast3x/h8mail).

You can either clone the public repository:

```bash
$ git clone git://github.com/khast3x/h8mail
```
Or download the [tarball](https://github.com/khast3x/h8mail/tarball/master):

```bash
$ curl  -OL https://github.com/khast3x/h8mail/tarball/master
```

Once you have a copy of the source, you can install it with:

```bash
$ python setup.py install
```

#### Docker

```bash
$ docker run -ti khast3x/h8mail -h
```

##  :tangerine: Usage

```
usage: h8mail [-h] -t TARGET_EMAILS [TARGET_EMAILS ...] [--loose]
              [-c CONFIG_FILE [CONFIG_FILE ...]] [-o OUTPUT_FILE]
              [-bc BC_PATH] [-sk] [-k CLI_APIKEYS [CLI_APIKEYS ...]]
              [-lb LOCAL_BREACH_SRC [LOCAL_BREACH_SRC ...]]
              [-gz LOCAL_GZIP_SRC [LOCAL_GZIP_SRC ...]] [-sf]
              [-ch [CHASE_LIMIT]]

Email information and password lookup tool

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET_EMAILS [TARGET_EMAILS ...], --targets TARGET_EMAILS [TARGET_EMAILS ...]
                        Either string inputs or files. Supports email pattern
                        matching from input or file, filepath globing and
                        multiple arguments
  --loose               Allow loose search by disabling email pattern
                        recognition. Use spaces as pattern seperators
  -c CONFIG_FILE [CONFIG_FILE ...], --config CONFIG_FILE [CONFIG_FILE ...]
                        Configuration file for API keys. Accepts keys from
                        Snusbase, (WeLeakInfo, Citadel.pw), hunterio
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        File to write CSV output
  -bc BC_PATH, --breachcomp BC_PATH
                        Path to the breachcompilation torrent folder. Uses the
                        query.sh script included in the torrent.
                        https://ghostbin.com/paste/2cbdn
  -sk, --skip-defaults  Skips HaveIBeenPwned and HunterIO check. Ideal for
                        local scans
  -k CLI_APIKEYS [CLI_APIKEYS ...], --apikey CLI_APIKEYS [CLI_APIKEYS ...]
                        Pass config options. Supported format: "K=V,K=V"
  -lb LOCAL_BREACH_SRC [LOCAL_BREACH_SRC ...], --local-breach LOCAL_BREACH_SRC [LOCAL_BREACH_SRC ...]
                        Local cleartext breaches to scan for targets. Uses
                        multiprocesses, one separate process per file, on
                        separate worker pool by arguments. Supports file or
                        folder as input, and filepath globing
  -gz LOCAL_GZIP_SRC [LOCAL_GZIP_SRC ...], --gzip LOCAL_GZIP_SRC [LOCAL_GZIP_SRC ...]
                        Local tar.gz (gzip) compressed breaches to scans for
                        targets. Uses multiprocesses, one separate process per
                        file. Supports file or folder as input, and filepath
                        globing. Looks for 'gz' in filename
  -sf, --single-file    If breach contains big cleartext or tar.gz files, set
                        this flag to view the progress bar. Disables
                        concurrent file searching for stability
  -ch [CHASE_LIMIT], --chase [CHASE_LIMIT]
                        Add related emails from HunterIO to ongoing target
                        list. Define number of emails per target to chase.
                        Requires hunter.io private API key

```

## :tangerine: Usage examples

###### Query for a single target

```bash
$ h8mail -t target@example.com
```

###### Query for list of targets, indicate config file for API keys, output to `pwned_targets.csv`
```bash
$ h8mail -t targets.txt -c config.ini -o pwned_targets.csv
```

###### Query a list of targets against local copy of the Breach Compilation, pass API keys for [Snusbase](https://snusbase.com/) from the command line
```bash
$ h8mail -t targets.txt -bc ../Downloads/BreachCompilation/ -k "snusbase_url=$snusbase_url,snusbase_token=$snusbase_token"
```

###### Query without making API calls against local copy of the Breach Compilation
```bash
$ h8mail -t targets.txt -bc ../Downloads/BreachCompilation/ -sk
```

###### Search every .gz file for targets found in targets.txt locally

```bash
$ h8mail -t targets.txt -gz /tmp/Collection1/
```

###### Check a cleartext dump for target. Add the next 10 related emails to targets to check. Read keys from cli

```bash
$ h8mail -t admin@evilcorp.com -lb /tmp/4k_Combo.txt -ch 10 -k "hunterio=ABCDE123"
```

## :tangerine: Configuration file & keys

h8mail can read keys by using a `config.ini` file with `-c`, or by passing keys from the command line directly with `-k`.

The configuration file format is as follows:
```ini
[h8mail]
shodan =
hunterio =
snusbase_url =
snusbase_token =
; leak-lookup_pub = 1bf94ff907f68d511de9a610a6ff9263
leak-lookup_priv =
```

In the above example, you'll notice a Leak-lookup public key, graciously generated for h8mail users. To activate, uncomment the line and make sure to pass to config file. The API can sometimes timeout. If that's the case, simply relaunch. 



Keys and their respective values can also be passed from the command line, with the `-k` option. Format is like so:  
```
$ h8mail -t john.smith@evilcorp.com -k "K=V, K=V" "K=V"
```



## :tangerine: Troubleshooting

### Python version & Kali

The above instructions assume you are running **python3 as default**. If unsure, type:
```bash
$ python --version
``` 

in your terminal. It should be either `Python 3.*` or `Python 2.*`.  

If you are running python2 as default :  
Make sure you have python3.6+ installed, then replace python commands with explicit python3 calls.



## :tangerine: Thanks & Credits

* [Snusbase](https://snusbase.com/) for being developer friendly
* [kodykinzie](https://twitter.com/kodykinzie) for making a nice [introduction and walktrough article](https://null-byte.wonderhowto.com/how-to/exploit-recycled-credentials-with-h8mail-break-into-user-accounts-0188600/) and [video](https://www.youtube.com/watch?v=z8G_vBBHtfA) on installing and using h8mail
* [Leak-Lookup](https://leak-lookup.com/) for being *infosec research* friendly
* [WeLeakInfo](https://weleakinfo.com/) for being developer friendly. They are currently migrating API service. I'll update h8mail when available :thumbsup:
* h8mail's Pypi integration is strongly based on the work of audreyr's [CookieCutter PyPackage](https://github.com/audreyr/cookiecutter-pypackage)
* Logo generated using Hatchful by Shopify


## :tangerine: Related open source projects
* [WhatBreach](https://github.com/Ekultek/WhatBreach) by Ekultek
* [BaseQuery](https://github.com/g666gle/BaseQuery) by g666gle
* [LeakLooker](https://github.com/woj-ciech/LeakLooker) by woj-ciech
* [HashBuster](https://github.com/s0md3v/Hash-Buster) by s0md3v


## :tangerine: Notes

* Service providers that wish being integrated can send me an email at `k at khast3x dot club` (Protonmail encryption friendly)