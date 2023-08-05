# To run 
```bash
ltest -d <file to monitor> -c <command to run>
```

## Example
This will run `make html` whenever ltest notices a change in the current folder
```bash
ltest -d ./ -c make html
```
