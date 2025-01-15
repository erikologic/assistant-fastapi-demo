# Assistant API

## Problem

### Description

The product department wants a system to be notified when a customer requests assistance from a bot. The bot will make an http call (like a webhook) with the following information:

- Topic: a string with values can be sales or pricing
- Description: a string with a description of the problem that needs assistance from.

You need to expose an API endpoint that will receive this call and depending on the selected topic will forward it to a different channel:

```
Topic    | Channel   
----------------------
Sales    | Slack
Pricing  | Email
```

### Notes

- Slack and Email are suggestions. Select one channel that you like the most, the other can be a mock.
- There may be more topics and channels in the future.

### The solution should

- Be written in your favorite language and with the tools with which you feel comfortable.
- Be coded as you do daily (libraries, style, testing...).
- Be easy to grow with new functionality.
- Be a dockerized app.

## Solution

### Stack/Libraries

- Python
- FastAPI
- Auth0
- Docker
- Pytest
- OpenTelemetry
- StructLog

### How to run

- Copy the .env.example file to .env and fill in the environment variables
  
```bash
cp .env.example .env
```

- Install [Poetry](https://python-poetry.org/docs/#installation) and [Poe](https://poethepoet.natn.io/installation.html), e.g.:

```bash
pipx install poetry
poetry self add 'poethepoet[poetry_plugin]'
```

- Install the dependencies:

```bash
poetry install
```

- Run the unit tests:

```bash
poetry poe test
```

- Run the app in dev mode:

```bash
poetry poe dev
```

- Run the app in prod mode:

```bash
poetry poe start
```

## Development

Initially, I created the `/heartbeat` endpoints to explore the FastAPI framework behaviour.  
I can agree if the tests against those endpoints seems to be testing the framework a bit, but I found it a good way to understand how the framework works.

The `/assistance` endpoint is heavily influenced by concepts of Ports & Adapters and TDD.  
There is a "framework" layer (`router.py`) and a "domain" layer (`service.py`).

The tests of the framework layer are more focused on checking authentication and validation is working as expected, and that known errors are translated to the correct HTTP status code.  
The tests of the domain layer are instead focused on the functional requirements.  

The service itself is a thin dispatch/proxy layer, so there isn't much business logic, and this strong division might even be overkill at this stage of the project.  
I wanted to showcase my capability to write code [ready for changes](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749?gi=6607ec8ec0a1).  
I have succesfully developed many systems leveraging the Ports & Adapters design, they always provided innumerable benefits and are usually worth the upfront investment .  
Although, this is a decision that should be made on a case-by-case basis e.g. I def would not suggest for leveraging this pattern on spike/PoC code!

I think it's current shape allows for a great flexibility.  
Adding a new topic/channel should be as easy as creating the Channel class, and adding the topic -> channel configuration.

I also spiked the `CachedChannelConfiguration` to demonstrate the capability of updating the configuration (with a 60 seconds backoff system) while the service is running.  
Depending on the use case there are many variants: pull based (current), push based via webhook or POST call...  

The `POST /assistance` endpoint (and some in `/heartbeat`) is protected by a scoped JWT token, leveraging Auth0 and adding elements of RBAC.  
Only a user with a "request-assistance" scope can call the endpoint.  
To test the endpoint while the service is running, I have created the `test_service.sh` script that will fetch the token from Auth0 and call the endpoint via curl.

The API has a number of middleware installed to make it more production-ready:

- **correlation_id**: creates an ID per request, so e.g. different log entries can be easily traced, accepting an "X-Request-ID" header too for distributed correlation.
- **structured_logging**: to package the logs in a structured way (JSON) e.g.for ingesting in an ELK stack - disabled on local.  
The middleware is also responsible for adding the correlation_id and other useful context to the log entries.  
_Most of the code is a copy & paste from the referenced gist, prob worth a good revisit when building a production-ready application._
- **open_telemetry**: to trace the requests through the system, including to external services (ATM only when using aiohttp)*, and accepting distributed traces. It is configured only to emit spans on the console while in Docker, just for demo purposes.  
_\* Launching the app in Docker, and requesting assistance for the Sales (Slack) channel, will force the service to emit some spans for the received request, but also the outbound POST call to the Slack service._

Finally, Dockerfile and docker-compose to showcase an initial implementation for dockerising the app.

## What I would improve

- This project lacks an infrastructure layer e.g. a WAF to protect from DDOS, Load Balancers and Autoscaling to handle the load, etc.
- This project needs Terraform badly e.g. for Auth0.
- There are no tests that check the integration between the layers.
- Lots of mocking. I normally prefer to create my own stubs, but I am aware this can be controversial.
- All the scripting is managed via Poe. This is neat, but e.g. it would require the building system to have Poe installed.
- There is some spike code in places that I would refactor and/or test better before going to production.
- The OTel SDK is not configured to send traces to a collector, just to the console. Also, we don't use any batching mechanism, which is a performance hit.
- The structured logs are sent to the console. In certain situation this could be fine (e.g. AWS Lambda). Ideally, we would send them to a log aggregator, perhaps in a batched fashion to not block the thread.
