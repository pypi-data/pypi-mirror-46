do-update-fqdn
===

Update or create a dns record through the DigitalOcean API.

# Caveats

This script makes the assumption that there is only one FQDN that matches a given combination of name and
record type.
So if you have two A records for foo.example.com, this script might fail or delete one of them, depending on what I 
have implemented at that moment.

Right now it simply sets all records that the DO API returned for the given combination to the given `--data`.
I might even try to fix this shortcoming in the future. 

Multiple `--type` arguments with their own address each for updating A and AAAA in one go would also be nice.

It also exposes your DO API token in the process list while running. You have to trust your local machine.