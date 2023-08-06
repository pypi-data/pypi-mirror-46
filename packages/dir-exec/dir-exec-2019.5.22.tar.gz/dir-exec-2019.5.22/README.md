<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install dir-exec
```

#### Scripts usage
command|`usage`
-|-
`dir-exec` |`usage: dir-exec command path ...`

#### Examples
```bash
$ find ~/git/gists -type d -mindepth 1 -maxdepth 1 -print0 | xargs -0 dir-exec command
```

execute function
```bash
func() {
    ...
}
export -f func
find ~/git/gists -type d -mindepth 1 -maxdepth 1 -print0 | xargs -0 dir-exec func
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>