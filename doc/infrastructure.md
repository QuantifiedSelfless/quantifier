# infrastructure

Requests for authentication to the various [services](availible_data.md) comes
in through the [front-end
server](https://github.com/wannabeCitizen/quantifiedSelf).  Tokens per-service
are sent to the `data dispatcher` which saves tokens to a database and starts
requesting data from the corresponding API.  As data is streaming into the data
dispatcher, it forwards bits of data to the relevant data service for
processing.

![](./figures/infrastructure.png?raw=true)

For example, user A goes to the front-end and oauths for gmail.  On successful
oauth, the token with user information is sent to the data dispatcher.  The
disbatcher will save the oauth tokens in it's tokendb and begin scraping e-mail
information.  As an email is retrieved by the dispatcher, it will send metadata
regarding user connections to the user-graph service and send text information
to the text-server.

# considerations

- ONLY HTTPS. No HTTP
- ONLY the front-end server should be publicly accessible.  All the rest should
  require VPN for access.
- We should consider using a public key encryption to keep all information
  private.  The private key should only be available to the user.
    - a public/private key could be generated on the front end and public key
      can be sent around to dispatcher with authentication requests
