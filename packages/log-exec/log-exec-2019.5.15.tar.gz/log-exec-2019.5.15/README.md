<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install log-exec
```

#### How it works
stdout and stderr are duplicated in log files:
```bash
$LOG_EXEC/<command>/out.log
$LOG_EXEC/<command>/err.log
```

#### Config
```bash
$ export LOG_EXEC=~/Library/Logs/log-exec # /usr/local/var/log/log-exec by default
```

#### Scripts usage
command|`usage`
-|-
`log-exec` |`usage: log-exec command [args ...]`

#### Examples
```bash
$ log-exec script.sh
```

or use `log-exec` as interpreter:

`script.sh`
```bash
#!/usr/bin/env log-exec bash
...
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>