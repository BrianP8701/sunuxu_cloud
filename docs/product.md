# sunuxu.com

## 1. Product Overview
- The AI assistant will receive all messages and emails sent to the real estate agent and generate responses on their behalf.
- The AI may also take actions such as scheduling appointments, sending emails with paperwork, requesting documents to be filled out, sharing information, updating and messaging other people based on context, and updating the CRM.
- All actions taken by the AI will require the agent's approval before being executed.

## 2. AI Model and Technology
### 2.1 AI Model
- The product will use a pre-trained language model like GPT-4 or Claude, without any fine-tuning or training of custom models.

### 2.2 Structured Output
- The AI will use the Instructor library, which allows for defining structured data schemas using Pydantic models.
- Instructor forces the LLM to output data in the specified structure, handling retry mechanisms and converting the Pydantic model to the expected format for defining schemas.
- This approach turns the general intelligence of the LLM into a programmable tool by getting structured output that can be used in the application.

## 3. Conversation Management
### 3.1 Conversation Types
- The AI will use a predefined set of conversation types, such as buyer transaction, seller transaction, renter, landlord, and others (to be determined).

### 3.2 Conversation Flow
- The LLM will be provided with relevant context in its prompt, including the conversation history and data models.
- It will choose from a set of predefined actions, such as generating a reply, scheduling an appointment, emailing or texting someone else, or asking the agent a question.
- The LLM can choose multiple actions and will describe its plan for each action.
- After selecting actions, separate LLM calls will be made for each action, providing the plan, action, and context to execute the task.

### 3.3 Handling Deviations from Predefined Conversation Types
- When a conversation deviates significantly from the predefined conversation types or introduces unrelated topics, the AI will mark the conversation as "other".
- Schemas will be created to model conversations of type "other", and the AI will still attempt to generate responses and propose actions, seeking the agent's approval as usual.
- For unanticipated conversation types, a more generic conversation model will be used, storing basic information and previous messages.

### 3.4 Conversation Spanning Multiple Sessions
- Initially, the system will brute-force and include all context in the prompt for each interaction.
- In the future, methods will be implemented to remove unnecessary old information and summarize or compress relevant information to maintain context across multiple sessions or extended periods.

### 3.5 Handling Unexpected Information
- Additional "other" fields will be added to the conversation type, person, and participant models to capture important information that doesn't fit into the predefined schema.

### 3.6 AI System and Conversation Plans
- The core of the system relies on the AI (LLM) receiving context and a set of actions to choose from, and then outputting actions.
- The available actions will vary depending on the situation and context.
- When a message is received (e.g., via Twilio or email), an identify person function will match the sender's contact information with an existing person ID or create a new one if no match is found.
- If a person ID is found, the system will analyze the person's conversation object, including active transactions and relevant details.
- Each conversation will have a list called `conversation_plans`, which contains IDs of `ConversationPlan` objects.
- `ConversationPlan` objects are created for specific situations, such as when a potential seller begins talking to the agent. They contain a list of goals and completed goals.
- Different types of `ConversationPlan` objects will be created, such as `ConvertLeadConversationPlan`, `SellerConversationPlan`, and `BuyerConversationPlan`.
- An additional `CustomPlan` object will be added to each conversation to handle unique real-world situations that may arise.
- Actions within the plans can include gathering information and documents from the person, updating the CRM, and more.
- Contingencies and conditional actions will be dynamically generated and added to the `CustomPlan`.
- When a message is received, the system will identify the person, gather context and plans into the prompt, and provide a set of actions based on the current plans and steps.
- The LLM will make an intelligent decision, and the chosen actions will be sent to the agent for approval before being executed.

## 4. Action Management
### 4.1 Action Proposal and Approval
- The AI will be provided with all relevant context, including readable data from the person, conversation, and transaction models, as well as all previous messages in the conversation.
- Given the most recent message and a numbered list of actions, the AI will output a list of integers representing the indexes of the actions it wants to take, along with a description/plan for each action.
- The AI will then use the context, description, and plan to handle each action, such as writing a response, sending an email, or filling out a CRM form.
- If the context length becomes an issue due to long conversations or frequent interactions with the same person across multiple transactions, methods will be implemented to handle this.

### 4.2 Action Prioritization
- There is no prioritization of actions. The AI will perform all proposed actions after receiving approval from the agent.

### 4.3 Action Expiration and Agent Response
- The AI will wait for the agent's response before proceeding with any proposed actions.
- If the agent manually sends a message or email related to a conversation, all pending actions for that conversation will be automatically discarded.
- After the agent's manual intervention, the AI will wait for the person's reply and use the agent's message as new context to determine the next set of actions.

### 4.4 Action Limitations and Legal Considerations
- The AI will not take any actions without the agent's approval, functioning more like an advanced autocomplete feature.
- There will be no specific limitations on the types of actions the AI can propose, as the agent will have the final say in approving or rejecting each action.

## 5. Agent Interaction and Feedback
### 5.1 Agent Approval Process
- The AI will send a text message to the agent explaining the action it wants to take. If multiple actions are queued, it will notify them of the number of pending actions.
- The agent can approve, reject, or provide feedback on the actions via text message or through a web app interface.
- If changes are requested, the AI will ask for approval again after making the necessary adjustments.

### 5.2 Agent Feedback and Action Modification
- If the agent modifies an action, the AI will try again and ask for approval once more.
- If the agent rejects an action, the AI will drop it.
- In cases where the agent directly sends a response or handles an action without approving or denying the AI's proposal, a method will be implemented to automatically discard the related pending actions.

### 5.3 Agent-Specific Communication Style
- Agents will have the ability to provide prompts describing how they want the AI to communicate for specific conversation types.
- These prompts will be prepended to the system prompts in the code, allowing the AI to adapt its communication style accordingly.

### 5.4 AI Requesting Clarification from the Agent
- When deciding on what action to take, one of the AI's allowed actions is to ask the agent questions.
- The AI will be instructed to ask questions when something isn't clear or when it lacks context to make an informed decision.
- This approach can help address edge cases where the agent has interacted with a person offline (e.g., in person or on the phone), and the AI doesn't have the full context of the conversation.
- One of the AI's rules in its prompts is to avoid making decisions without full context, so it will ask the agent for clarification or additional information when needed.

### 5.5 Agent Feedback on AI Performance
- The agent will have the ability to provide feedback on the AI's performance and the quality of its proposed actions.
- If the agent modifies an action, the AI will retry the action and ask for approval again, incorporating the agent's feedback.

### 5.6 Learning from Agent Modifications
- While not a current priority, the system may implement a feature to learn from the agent's modifications to proposed actions over time.
- This could involve building out system prompts in the user profile object, which can be reused in each message.
- Custom system prompts could be defined for different conversations or specific people, and when the agent provides feedback that should be remembered, it will be saved and included in future decision-making and action-taking processes.

## 6. Data Management
### 6.1 Data Gathering
- Throughout the conversation, the AI will use Pydantic models with Instructor to gather structured information, such as email addresses, phone numbers, budgets, and areas of interest.
- The specific information gathered will depend on the type of conversation, which the AI will determine early in the interaction.
- The AI will fill out these "forms" (Pydantic models) as it collects information during the conversation.

### 6.2 Data Security and Privacy
- All data will be encrypted in the future to ensure security and confidentiality.
- During the development and debugging phase, the developer will have access to the conversations and data related to the agent and people who agree to participate.

## 7. Integration and Scalability
### 7.1 Integration with External Systems
- Initially, the product will use its own simple CRM and calendar schema.
- In the future, integrations with Google Calendar and the agent's CRM will be implemented.
- The LLM will interact with these external systems using Instructor and Pydantic models, treating them as forms to be filled out based on the information gathered during the conversation.

### 7.2 Conversation Scalability and Edge Cases
- The system will scale automatically to handle multiple concurrent conversations.
- Each person will have only one conversation object associated with them.
- If a person can have multiple types of conversations simultaneously, this edge case will be addressed later.
- The AI will be able to change the conversation type as an action when needed.
- Determining the conversation type will be a priority when it hasn't been established yet.

### 7.3 Third-Party API Integrations
- In addition to the MLS integration, the system will integrate with various third-party APIs and services, including:
  - Google Calendar and Apple Calendar for scheduling and event management
  - Twilio for text messaging and phone calls
  - Follow Up Boss for customer relationship management
  - Google Sheets and Google Docs for document management and collaboration
  - Facebook Marketplace and Facebook Messenger for property listings and communication
  - Instagram Direct Messages for social media engagement
  - Potentially WhatsApp, if an API is available
  - Lead generation services and tools

## 8. Transactions
- A transaction encompasses the entire process of buying, selling, or renting a home from start to finish.

### 8.1 Transaction Workflow and Milestones
- Real estate transactions generally follow a similar workflow and set of milestones, with a finite set of transaction types.
- The typical stages of a transaction may include: information gathering, offers, closing, and post-closing activities.
- The specific names and details of these stages will be determined with further research and input from real estate experts.

### 8.2 Property Object and Transaction Relationship
- Each transaction will correspond to one property, and there will be a related "Property" object for each transaction.

### 8.3 Handling Multiple Active Transactions per Person
- A new object called `participant` will be introduced, representing a person involved in a transaction.
- The `person` object will feature two dictionaries: `active_transactions` and `terminated_transactions`. Each dictionary has transaction IDs serving as keys and participant IDs as values.
- The `participant` object will have a base parent class and child classes for various types of people involved in a transaction, each with their own workflows and plans.
- When a person is involved in multiple transactions simultaneously, the AI will include both transaction and participant information in the prompt, allowing the model to decide on the appropriate actions based on the context.

### 8.4 Handling Transactions with Multiple Participants
- Each transaction object will contain a list of participant IDs, representing the persons involved in that specific transaction.
- Participant objects are distinct from person objects, as they are transaction-specific and include the participant's role and other transaction-related details.
- The participant object will have a `relationships` field, which is a dictionary mapping participant IDs to a string describing their relationship with other participants in the transaction.
- The system will have different workflows and sets of actions based on the type of transaction and the roles of the participants involved.
- Each role (e.g., buyer, seller, buyer's agent, seller's agent, dual agent) depending on the type and state of the transaction, will have its own predefined plan and general workflow, which will be expanded over time.
- The available actions for the AI will depend on the person, their current transactions, their role, and the current state of the transaction.
- The system will track the agent's manual actions to update the state and ask questions if it appears that the agent took actions that were not captured or require additional information.

### 8.5 Handling Transaction-Specific Documents and Files
- For different types of transactions, there is generally a set of reusable paperwork that will be predefined in the system's logic.
- Throughout conversations, the AI will automatically collect information to fill out the CRM.
- The paperwork will be labeled with corresponding fields in the code logic, allowing for autofill functionality.
- For e-signatures, the system will send emails to the relevant parties requesting them to sign the documents electronically.
- The organization of paperwork, labeling fields, and integrating them into the workflow based on the type of transaction, role, and data from the CRM will be part of the coding process.
- The system will manage the documents and adapt to different paperwork requirements based on decisions made during the transaction.

### 8.6 Handling Transaction Cancellations or Fall-Throughs
- The AI will include transaction cancellation or fall-through as a potential action it can choose.
- The web app interface will allow the agent to modify and handle these types of situations.

### 8.7 Handling Post-Closing Activities and Follow-ups
- The agent will have the ability to create drip campaigns and post-transaction flows to handle and automate post-closing tasks and follow-ups.

## 9. Legal and Regulatory Considerations
- Twilio requires obtaining consent from individuals before messaging them.
- The AI must disclose that it is an artificial intelligence when communicating with people.
- Since the agent is approving all actions, the AI is primarily assisting them in saving time while remaining compliant with regulations.
- As the initial focus is on building the product for your mom, handling legal and compliance requirements for different jurisdictions will be considered later.

## 10. Future Features and Expansion
- Develop a comprehensive CRM system.
- Integrate more sources of communication, like Facebook Messages, phone calls, Instagram DMs etc.
- Expand the AI's capabilities to generate and manage leads.
- Allow the AI to handle additional tasks such as marketing campaigns.
- Serve as an overall oracle for the agent, assisting them with various aspects of their real estate business.
- Proactive Insights and Recommendations: At this stage, the system will not focus on proactively providing insights or recommendations to the agent based on patterns or trends identified across conversations and transactions. The focus is primarily on being an advanced autocomplete engine.

## 11. Personalized Content Generation
- Generating personalized content, such as property descriptions or marketing materials, can be included as part of the AI's actions.
- When the conversation type is determined, the conversation object will include the current state of the conversation and the next desired steps.
- In real estate, there are typical processes for sellers and buyers. After gathering initial information and updating the CRM, the AI can trigger actions like posting the property on MLS and other sites or filling out paperwork at appropriate stages.

## 12. Handling Inconsistent Agent Feedback
- The AI will need to handle situations where the agent provides conflicting or inconsistent feedback on similar actions across different conversations.
- Clear methods will be implemented to circle back and ask the agent questions when inconsistencies are detected, allowing the AI to update its internal system based on the agent's responses.
- The AI will not only ask the agent to approve actions but also ask questions to clarify and resolve any conflicting information.

## 13. Handling Multiple Agents and Teams
- The system will follow the same architecture as for individual agents, treating other agents and team members as additional "people" in the system.
- New types of conversation plans will be created to accommodate the interactions and workflows specific to multiple agents and teams.
- The AI should be able to classify conversations as non-business related and not try too hard to categorize them further.

## 14. Integration with Multiple Listing Services (MLS)
- Agents use MLS when posting listings for sellers and generating Comparative Market Analyses (CMAs) for properties.
- Automating the process of filling out and posting MLS listings would be a significant benefit, which can be incorporated into the seller conversation plan at the appropriate stage when sufficient information has been gathered.
- The AI can also assist with searching for property details and gathering information from MLS as needed.
- In addition to the autocomplete functionality, there will be an "oracle" aspect of the application where agents can directly request information or actions from the AI, as well as ask questions about the system if they need clarification or assistance.

## 15. Handling Property-Specific Information and Data
- Gathering property-specific information is a crucial part of the seller conversation plan.
- The web app interface will allow agents to fill in additional property details, which don't necessarily have to be structured.


# Extra
I'll merge these into the docs above later

1. Handling multiple languages within a single conversation:
   - The AI should be capable of detecting the language used in each message and respond accordingly, even if the person switches languages within a single conversation.

2. Dealing with spam, scams, or fraudulent inquiries:
   - The AI will attempt to detect obvious fraud and scams, but ultimately, it will be the agent's responsibility to identify and flag such instances.
   - An action will be added to allow the agent to block a person if they are identified as a scammer.
   - This should definitely become a concern as we scale.

3. Handling attachments and multimedia content:
   - For now, the AI core engine will not handle attachments and multimedia content. This feature will be considered for future development.

4. Dealing with urgent or emergency situations:
   - There will be no special handling for urgent or emergency situations. The AI will execute actions and ask for approval as usual.

5. Handling multiple time zones and international transactions:
   - The system will not handle multiple time zones or international transactions at this stage. This aspect will be ignored for now.

6. Integration with virtual tour and 3D modeling tools:
   - Integration with virtual tour and 3D modeling tools will not be included in the current scope of the product. If required in the future, the system may integrate with external products or services for these features.

7. Handling client reviews and testimonials:
   - The AI will autonomously suggest and run actions to request client reviews and testimonials post-closing, after asking for the agent's referral links and information.
   - The agent will have the option to approve these actions or permanently disable this feature.

# Further thinking
## Workflows & Forms
We can design a general form object. There's lots of different kinds of forms that agents might send out to various people to fill out. We shouldn't constrain the LLM to have to obtain information purely through text and email. That's unnecessary burden and complexity. We can simply design the concept of Workflows & Forms. 

Let's not worry about making customizable forms and workflows that users can create. I just want to create a form that I make that works.

We want to create a general Form and Workflow object that we can easily create many of, and these should be flexible. Let's just design one right now.

Initial form:
- First name
   required, string
- Middle name
   optional, string
- Last name
   required, string
- Email
   required, string
- Phone number
   required, int
- Type
   multiple choice, [seller, buyer, landlord, renter]
- Disclosure Agreement 
   pdf

Okay so whats the flow? We want to send somebody a link they can just click on that will take them to the form. They come to the form and what? We have 2 options:
   - We can have people sign in and make account
   - We can on our side just create custom links for each person, and the person just has to fill out the form. 
Nah. I think we definitely have to make them sign up. For security, so they can keep their stuff private. If its like a public link that if anyone can get hold of and view that's bad.
So here's the user experience. We'll send them the link. They'll copy the code to connect to their agent. Once they connect to their agent, their agent can assign them forms and paperwork through the site.
