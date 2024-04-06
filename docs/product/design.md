# Design

## UX
Best case scenario we'd have our copilot tap into, have access to and control over the agent's existing phone number. This way the agent can see the texts the ai sends as if it's them. However due to IOS restrictions this is not possible. Instead we'll have to create a twilio number and email for the copilot. The copilot uses this number to communicate with the agent and their clients.

The primary annoyances that comes from this is:
    - our copilot won't be able to see any interactions that doesen't happen through it. this means we have to force the agent to perform all their business interactions through our copilot. this is extremely annoying because people feel most comfortable in their native message and phone apps. 
    - the clients are most likely to avoid interacting with the ai assistant and go straight to interacting with the agent given the choice... rendering what we have irrelevant

lets take the constraints for what they are. whats the best we can do?

Primary communication channels:
    text
        - agents personal number (cannot be shared with copilot)
        - copilot number (cannot be shared with agent natively)
    email
        - agents personal email (this can be shared with copilot)
        - copilot email (can be shared with agent natively)
    call
        - agents personal number (cannot be shared with copilot)
        - copilot number (cannot be shared with agent natively)
    our application
        - chatbot for agent and client
        - agent and copilot can send client forms and documents over the application

from the clients pov they can receive communication from:
    - calls, texts from agents personal number. our copilot cant see any of this. but this is what everyone expects and is most comfortable with
    - emails from the agents personal email. this can be shared with copilot. no friction here!
    - messages from the copilots number. agent can view conversations here through the application which is friction for the agent. clients will be wary of the ai copilot and will likely abandon using it once they get a hold of the agents personal number. 
    - forms and documents shared from the agent through the application. this is friction for the client since they need to create an account

from the agents pov they can receive communication from:
    - receive texts or calls from clients on their personal phone number.
    - receive emails from clients on their personal email
    - receive requests for approval from copilot from copilots number and the application

from copilots pov it can receive communication from:
    - it will receive any email the agent receives
    - it will receive any text sent to its number from clients
    - it can receive messages from the agent from the application
    - it can receive filled out forms or messages from the client from the application
