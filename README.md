# Browser MIDI
## A Javascript / Python browser MIDI player

This is a hacky way to play MIDI files in a browser. First list available MIDI files on a server, then make an AJAX call to a Python CGI script that converts the MIDI to OGG, then feed the AJAX call's output to a HTML5 audio object.

## Installation

* Install Apache, configure as usual

```
cd /home/user
git clone git@github.com:SirDifferential/browsermid.git
```

* Create directories for the site, ie:

```
mkdir /home/user/public_html/browsermid
mkdir /home/user/public_html/browsermid/cgi-bin
mkdir /home/user/public_html/browsermid/midis
``` 

* Create VirtualHost configs, enable CGI

```
<VirtualHost *:80>
    ServerName CoolServer.com
    DocumentRoot /home/user/public_html
    <Directory />
            Options FollowSymLinks +Indexes
            AllowOverride All
            Order allow,deny
            Allow from all
    </Directory>

    <Directory /home/user/public_html/browsermid/cgi-bin>
            Options +ExecCGI
            AddHandler cgi-script .cgi .py
            AllowOverride None
            Order allow,deny
            Allow from all
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
```

* Place files in the website folder:

```
cd /home/user/browsermid
cp -r * ./ /home/user/public_html/browsermid/
```

* Place some music in the midis folder:

```
cd /home/user/midi
cp coolmusic.mid /home/user/public_html/browsermid/midis/
```

* Go to coolserver.com/browsermid

## License

The MIT License (MIT)

Copyright (c) 2014 Jesse Kaukonen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


