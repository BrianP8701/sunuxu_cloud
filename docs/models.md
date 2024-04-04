# models
Each of these are a table in a SQL database

## Person:
   - Represents an individual involved in real estate transactions.
   - Contains personal information such as first name, middle name, last name, email, phone number, and language.
   - Non-transaction specific and can be associated with multiple transactions.

## Transaction:
   - Represents a specific real estate transaction, such as selling, buying, renting, or leasing a property.
   - Contains a reference to the associated Property object.
   - Includes a list of Participant IDs involved in the transaction.
   - Has a transaction type field to differentiate between different types of transactions.
   - Includes a stage field to track the progress of the transaction.
   - Child classes can be defined for different transaction types, with specific stage variables and meanings.

## Property:
   - Represents a real estate property involved in a transaction.
   - Contains attributes typically found on MLS listings.
   - Includes an area for arbitrary notes related to the property.

## Participant:
   - Represents a person's involvement in a specific transaction.
   - Contains a role attribute to define the participant's role, such as seller, buyer, seller's agent, dual agent, seller's attorney, or escrow officer.
   - Includes a relationships attribute, which is a dictionary mapping other Participant IDs to descriptions of their relationships.

## Conversation:
   - Represents the communication history and context between the agent and a person.
   - Associated with a single Person object.
   - Contains references to all active transactions related to the person.
   - Provides context and additional actions to the AI based on the conversation state, transaction stage, and plan.

## BasePlan and its subclasses (ConvertLeadPlan, CategorizePersonPlan, SellerPlan, BuyerPlan, SellerLawyerPlan):
   - Represent predefined sets of objectives and actions for different stages of a transaction or conversation.
   - Help maintain context and control the AI's actions.
   - Subclasses can be defined for specific plans, such as converting leads, categorizing persons, and handling interactions in a transaction.

## Action:
   - Defines the actions that the AI can take based on the conversation and transaction context.
   - Used primarily on the code side to define the logic and available actions for the programmer.

## User:
   - Represents the real estate agent using the system.
   - Contains configuration options and preferences for customizing the AI system.
