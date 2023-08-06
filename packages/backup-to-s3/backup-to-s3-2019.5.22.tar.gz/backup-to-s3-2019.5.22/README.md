<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install backup-to-s3
```

#### How it works
```
<s3-bucket-name>/<slug>/<year>/<year-month>/<year-month-day>/name-<datetime>.tar.gz
```

#### Config
environment variables (optional):

variable|description|default value
-|-|-
`BACKUP_TO_S3_BUCKET`|s3 bucket name| `backup-to-s3-<account-id>`
`BACKUP_TO_S3_EXCLUDE_FROM`|exclude patterns|`$XDG_CONFIG_HOME/backup-to-s3/exclude.txt`, e.g. `~/.config/backup-to-s3/exclude.txt`

#### Scripts usage
```bash
usage: backup-to-s3 path ...
```

#### Examples
```bash
$ cd ~
$ backup-to-s3 git
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>