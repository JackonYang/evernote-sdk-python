env_file='../../.private-data/evernote2.env'
cmd_str='python -m evernote2.tools.export_notes --china --token=$evernote_token'

if [ -f "$env_file" ]; then
    env $(cat $env_file | xargs) bash -c "$cmd_str"
else
    bash -c "$cmd_str"
fi
