# Puppies API
This is the puppies backend. 

## Running tests
I'll admit the tests are not great, and they're quite hacky.

Get postgres:

`brew install postgres`

If it's installed, bring it up:

`brew services start postgres`

Create data model, and start the web server

`cd puppies/src && python3 db/schema.py && python3 main.py`

While the server is up, run:

` cd ../test && python3 integration.py`

to run the integration tests.

You might want to drop the puppies database afterwards

## About
#### Caveats
Lot's of hacks. Here is a list of tech debt in no particular order:
- The design of the code base is not decoupled or granular enough making unit testing difficult.
- As a consequence of the previous point, I only provided integration tests and no unit tests. 
- Not all HTTP responses and corner cases are handled.
- No JWT Auth.

#### Good stuff
- Data model was somewhat thought out, lends itself nice to the resources and methods
- MVP was relatively quick to hack out.
- API node is not stateful, could be scaled easily.
- User Auth required on relevant resources.
- Feed query/resource returns all posts with picture data and each posts' number of likes.