Hippodamia observe the state of all registered microservices (aka watch
dog).

.. figure:: img/Microservice%20Overview.png
   :alt: Pelops Overview

   Pelops Overview

``Hippodamia`` is part of the collection of mqtt based microservices
`pelops <https://gitlab.com/pelops>`__. An overview on the microservice
architecture and examples can be found at
(http://gitlab.com/pelops/pelops).

for Developers
==============

States of a Microservice
------------------------

.. figure:: img/microservice_states.png
   :alt: AState Diagram

   AState Diagram

-  *initialize phase* - an onboarding request has been received by the
   system. if the source has been identified as a known microservice,
   the existing state will be used, a new one will be initialized.
-  *onboarding* - a microserivce has been identified/initialized and the
   system waits for it to react to the onboarding request response.
-  *active* - the observed microservice has been successfully onboarded
   and sends state updates regularly.
-  *inactive* - the microservice has not sent any update for a
   predefined period.
-  *terminated* - the microservice has either send a good-by-message or
   been inactive for to long.
-  *end state* - the system has terminated observation of this
   microservice.

States of the Corresponding Agent
---------------------------------

|AgentState\_Diagram| \* *uninitialized* - agent has just started or a
restart has been forced. on entry of this state a new uuid will be
generated. \* *initizalized* - agent is ready to start onboarding
procedure. \* *onboading* - agent has sent an onboarding request and is
waiting for an reply \* *active* - agent is constantly sending ping,
runtime, and config messages \* *terminating* - agent sends an
termination message to the service before shutdown

Topics
------

see `AsyncAPI <docs/index.html>`__.

Incoming
~~~~~~~~

-  *contact* - for onboarding/offboarding requests
-  *state.ping* - listens for new ping messages
-  *state.runtime* - listens for new runtime messages
-  *state.config* - listens for new config messages
-  *state.end* - listens for termination messages ### Outgoing
-  *uuid* - individual topic opened by each microservice for the
   onboarding process
-  *command.ping* - request ping messages
-  *command.runtime* - request runtime messages
-  *command.config* - request config messages
-  *command.onboarding* - request re-onboarding

Messages
--------

see `AsyncAPI <docs/index.html>`__.

Incoming
~~~~~~~~

-  *onboarding request* - onboarding request from a microservice
-  *ping* - minimum "sign of life" of a microservice
-  *runtime info* - ping plus additional runtime information
-  *config state* - ping plus service configuration
-  *termination info* - end service signal. sent either upon stop of
   service or as last will via mqtt server.

Outgoing
~~~~~~~~

-  *onboarding response* - onboarding response sent by hippodamia to the
   microservice via the provide onboarding topic from the microservice
-  *re-onboard request* - request plus optionally gid
-  *request ping* - request plus optionally gid
-  *request runtime info* - request plus optionally gid
-  *request full state* - request plus optionally gid

Onboarding Sequence
~~~~~~~~~~~~~~~~~~~

.. figure:: img/onboarding.png
   :alt: Sequence

   Sequence

First, the microservice subscribes to a unique topic. This topic is sent
together with additional information to identify the microservice
(especially to look if this microservices has been onboarded previously)
to hippodamias onboarding channel. Hippodamia answers with the
onboarding response message which primarily contains the gid - the
identifier of this particular microservice instance that ideally should
be the same even after the n-th onboarding cycle. The repsonse message
is published to the unique topic from the microservice. Once the
microservice has received its gid, the uniqued topic can be unsubscribed
and the reqular topics will be used for further communication.

Ping Sequence
~~~~~~~~~~~~~

.. figure:: img/ping.png
   :alt: Ping

   Ping

Ping messages are normally sent by the microservice at arbitrary times.
Usually a sent interval of e.g. 60 seconds is implemented. The other
possibility is that hippodamia requests a ping message from all
onboarded microservices. The same sequence applies to runtime, config
and onboarding.

Database
--------

Hippodamia stores all info immediately into the database. \*
Microservice state \* Received messages

.. |AgentState\_Diagram| image:: ../hippodamia-agent/img/agent_states.png


