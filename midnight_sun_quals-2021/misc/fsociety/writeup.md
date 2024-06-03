
## fsociety

Solved by: `fkil`

### Description

The challenge allows us to connect remotely to an ssh-service. After connecting, the server advertises itself as an ssh service based on MySQL and PHP and
we are given a login prompt. The challenge asks us to retrieve the password of the user `elliot`.

### Solution

After trying a simple SQL-Injection payload: `' OR '1' = '1`, we were able to get further in the login process. However,
we were shown a screen telling us, we are not part of fsociety and were not able to continue further. However, as we are able
to discern a "successful" login from a failed one, we can use a Blind SQL-Injection to retrieve the contents of the database.



