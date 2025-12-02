this is a user manual for the tool
the tool uses python native regex engine so adjust your pattern accordingly
put your pattern in the input section followed by the test text and you will see color-highlighted matches of your pattern.
you can make the script executable before using: `chmod +x regex-tool.py` or use it with `./regex-tool.py`
example usage: run the script, provide text, then pattern
eg1: 'text is bad' pattern: ; matches the first word 'text'
eg1: "text is bad" pattern: `^\w+?`; matches the first word "text"
test patternn: 8hduhh 73656 htgjgd 533d
pattern  matxhes the 5 digits
pattern \d{5} matxhes the 5 digits
pattern \d$ mathes digits at the end of li e
pattern \d{2} mathes any 2 digits
