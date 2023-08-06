# console-retry

This utility is designed to run any shell command and retry if no new line was written to 
stdout within a specified timeout

The default timeout applies to lines written to stdout of the shell command. 

Retry is triggered when:
* No new line was written to stdout after specified timeout

Retry is not triggered when:
* The command as a whole takes longer than specified timeout
* The command returns a non-zero (error) return code

To be a good bash-citizen the return code is mirrors the return code of the subcommand or 1 if the command never 
finished in the specified timeout. 