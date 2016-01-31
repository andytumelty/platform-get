# platform-get
Uses National Rail (UK) API to predict which platform your train will depart from

## Usage

### Tokens and Credentials
This is not a shared service (yet). To use you'll need to generate your own
tokens for the [National Rail APIs](http://www.nationalrail.co.uk/46391.aspx).
Specifically, this app uses the [Darwin](http://www.nationalrail.co.uk/46391.aspx)
[Open Live Departure Boards Web Service (OpenLDBWS)](http://lite.realtime.nationalrail.co.uk/openldbws/).
Register for an OpenLDBWS token
[here](http://lite.realtime.nationalrail.co.uk/openldbws/).

Once you get you token, drop it in credentials.yml. Although included in
.gitignore to try and prevent people from inadvertently publicising their
tokens, I'll make sure the structure of the yaml is kept up to date.
