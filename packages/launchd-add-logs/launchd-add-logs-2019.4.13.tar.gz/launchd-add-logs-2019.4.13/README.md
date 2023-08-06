<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-Unix-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install launchd-add-logs
```

#### How it works
```
~/Library/Logs/LaunchAgents/<Label>/out.log
~/Library/Logs/LaunchAgents/<Label>/err.log
```

`<name>.plist`
```xml
<key>StandardErrorPath</key>
<string>/Users/<username>/Library/Logs/LaunchAgents/<Label>/err.log</string>
<key>StandardOutPath</key>
<string>/Users/<username>/Library/Logs/LaunchAgents/<Label>/out.log</string>
```

#### Scripts usage
command|`usage`
-|-
`launchd-add-logs` |`usage: launchd-add-logs path ...`

#### Examples
```bash
$ find ~/Library/LaunchAgents -name "*.plist" -print0 | xargs -0 launchd-add-logs
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>