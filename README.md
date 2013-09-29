SublimeVarLogger
=========

This is a plugin for Sublime Text 3 that generates a line of code to log the variable that (a) you have selected, or (b) is under your cursor.

For example, in **Python**, with no selection:
![Screenshot](https://raw.github.com/harveyr/SublimeVarLogger/master/screenshot1.png)

And with a selection:
![Screenshot](https://raw.github.com/harveyr/SublimeVarLogger/master/screenshot2.png)

(If you are using the logging module, it will try to find the name of your logger object and use `<loggername>.debug()` instead.)

Or in **Javascript**:

`console.log('wicked_var:', wicked_var);`

Also works in **Go** (`log.Print()`), **PHP** (`var_dump()`), and **CoffeeScript** (`console.log`).

Comments are welcome!
