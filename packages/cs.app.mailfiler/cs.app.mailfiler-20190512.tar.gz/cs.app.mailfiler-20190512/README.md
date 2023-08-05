email message filing system which monitors multiple inbound Maildir folders


Mailfiler is my email message filing system.

It monitors multiple Maildir folders for new messages
and files them according to various easy to write rules.
Its use is described fully in the mailfiler(1cs) manual entry.

The rules files are broadly quite simple and described fully
in the mailfiler(5cs) manual entry.
The rules are normally single line rules of the form:

    target,... label condition

If the rule should always fire
then the condition may be omitted.

The targets may be
mail folders (file the message in the named folder),
assignment statements (set an environment variable),
email addresses (send the message to the specified address)
or some other special purpose actions.

The conditions are usually tests of the header email addresses
including whether an address is a member of some group/alias
but may also test various other things about the message headers.

## Class `Condition_AddressMatch`

MRO: `_Condition`, `cs.obj.O`  
A condition testing for the presence of an address.

## Class `Condition_HeaderFunction`

MRO: `_Condition`, `cs.obj.O`  
A condition testing the contents of a header.

## Class `Condition_InGroups`

MRO: `_Condition`, `cs.obj.O`  
A condition testing messages addresses against address groups.

## Class `Condition_Regexp`

MRO: `_Condition`, `cs.obj.O`  
A condition testing headers against a regular expression.

## Function `current_value(envvar, cfg, cfg_key, default, environ)`

Compute a configurable path value on the fly.

## Function `FilterReport(rule, matched, saved_to, ok_actions, failed_actions)`

Create a FilterReport object.

Parameters:
* `rule`: the `Rule` on which to report
* `matched`: whether the rule was matched
* `saved_to`: where messages were filed
* `ok_actions`: actions which succeeded
* `failed_actions`: actions which failed

## Function `get_target(s, offset, quoted=False)`

Parse a single target specification from a string; return Target and new offset.

Parameters:
* `s`: the string to parse
* `offset`: the starting offset of the parse
* `quoted`: if true then the parser is already inside quotes:
  do not expect comma or whitespace to end the target specification.
  Default: `False`

## Function `get_targets(s, offset)`

Parse list of targets from the string `s` starting at `offset`.
Return the list of Targets strings and the new offset.

## Function `maildir_from_name(mdirname, maildir_root, maildir_cache)`

Return the Maildir derived from mdirpath.

## Class `MailFiler`

MRO: `cs.obj.O`  
A mail filer.

## Function `main(argv=None, stdin=None)`

Mailfiler main programme.

## Class `MessageFiler`

MRO: `cs.obj.O`  
A message filing object, filtering state information used during rule evaluation.

Attributes:
* `.maildb`: Current MailDB.
* `.environ`: Storage for variable settings.
* `.addresses(header)`: Caching list of addresses from specified header.

## Function `parserules(fp)`

Read rules from `fp`, yield Rules.

## Function `resolve_mail_path(mdirpath, maildir_root)`

Return the full path to the requested mail folder.

## Class `Rule`

MRO: `cs.obj.O`  
A filing rule.

## Class `Rules`

MRO: `builtins.list`  
Simple subclass of list storing rules, with methods to load
rules and filter a message using the rules.

## Function `save_to_folderpath(folderpath, M, message_path, flags)`

Save the Message `M` to the resolved `folderpath`.

Parameters:
* `folderpath`: the path to the target mail folder.
* `M`: the message to save.
* `message_path`: pathname of existing message file, allowing
  hardlinking to new maildir if not `None`.
* `flags`: save flags as from MessageFiler.flags

## Function `scrub_header(value)`

"Scrub" a header value.
Presently this means to undo RFC2047 encoding where possible.

## Class `Target_Assign`

MRO: `cs.obj.O`  
A filing target to set a filing state environment variable.

## Class `Target_EnvSub`

MRO: `cs.obj.O`  
A filing target to delivery to a string
which is subject to environment subject to environment variable expansion
where the environment variables are derived from the filing state.

## Class `Target_Function`

MRO: `cs.obj.O`  
A filing target to run a Python function against a message.

## Class `Target_MailAddress`

MRO: `cs.obj.O`  
A filing target for an email address.

## Class `Target_MailFolder`

MRO: `cs.obj.O`  
A filing target for a mail folder.

## Class `Target_PipeLine`

MRO: `cs.obj.O`  
A filing target to pipe the message contents to a shell command.

## Class `Target_SetFlag`

MRO: `cs.obj.O`  
A filing target to apply a flag to a message.

## Class `Target_Substitution`

MRO: `cs.obj.O`  
A filing target to apply a regular expression string substitution
to message headers.

## Class `WatchedMaildir`

MRO: `cs.obj.O`  
A class to monitor a Maildir and filter messages.
