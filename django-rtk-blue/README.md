# django-rtk-blue

This package is the combination of the following django-rtk packages:

- django-rtk-upfront
- django-rtk-password
- django-rtk-magic-link

It has:

- a Backend class that inherits from all the Backends in these packages.
- a Validator that inherits from all the Validators in these packages.
- a Mutation class that inherits from all the Mutation classes in these packages.
- a Query class that inherits from all the Query classes in these packages.

## Management commands

### The delete-stale-activation-tokens

This command deletes all activation tokens older than some date.
