# Data Model

We have an abstract singleton class for the SQL database. We currently use Azure Postgresql.
We use Sqlalchemy to define tables. Every table has a corresponding Pydantic model. In our application logic we don't directly use the database or data models, we use the Pydantic models.

## Users and Teams
Users can create teams. Users can have the following roles on a team:
- Broker
- Agent

Only brokers can add/remove people from the team. Users can be a part of multiple teams.
Users in a team can share people, properties and transactions to teammates.

## People
MLS
property
people/participant
users(agents, brokers)
transactions, listing


Skyslope:
    Transactions:
        Transaction types:
            commercial lease
            commercial sale
            LIBOR - Residential Rental - Leased
            LIBOR - Residential, Condo Co-op Sale
            Lot/Land Sale
            Referral/BPO
            Retainer Fee
            Sales
        Representation:
            Purchase
            listing
            Both Purchase & Listing
            Lease Tenant
            Lease Landlord
            Bothe Lease Tenant & Landlord
            Referral
            BPO
            Other
        People:
            Seller/Landlord
            Purchaser/Tenant
            Title/Escrow/Attorney
            Agent Representing Other Side
            Lender
            Home Warranty
            Misc. Contact
        Deal Source:
            Sign
            Advertisement
            Open House
            Personal Referral
            Corporate Referral
            Prospecting
            Previous Customer
            REO Account
            New Home Account
            Farming
            Duty Desk
            MLS
            Office Lead
            SOI
            Expired/Withdrawn
            Social Marketing
            Direct Mail
            Floor Time
            Door Knocking
            Relocation Department
            Drip Marketing
            Call Capture
            Website
            Other
            Home Partners of America


    Listing:
        Listing Parameters:
            MLS#
            Street number
            Street name
            Unit
            Zip code
            State
            City
            County
            Area
            List Price
            Year Built
            Source
            Listing commission
            Sale Commision
            Listing Date
            Expiration Date
            Additional commision breakdown information
            Referring Agent
            Company
            Referral Amount
            Amount
            Transaction Coordinator Fee
            Office Gross Commission
            Listing Types:
                commercial lease
                commercial listing
                LIBOR - Rental Listing
                LIBOR - Residential, Condo Co-op Sale
                Lot/Land Listing
                Express Offers
            Deal Source: (Same as transaction)
        Contact parameters:
            Seller/Landlord:
                First name, last name, company name, email, phone, address, notes
            Home Warranty:
                Representative name, phone number, confirmation number, company name, notes
            Misc. Contact:




MLS
    Add Listing:
        Class:
            Residential
            Rental
            Land
            Commercial/Industrial
            Condo/Co-op/HOA:
                Condo/HOA
                Co-op
        County:
            Nassau
            Suffolk
            Queens
            Kings/Brooklyn
            Bronx
            Columbia
            Delaware
            Dutchess
            Green
            Manhattan
            Orange
            Putnam
            Rockland
            Sullivan
            ulster
            Westchester
            other
        Property Attributes:
            Town/City
            Zip
            Owner Last
            Owner First
            Street Name
            Street Sufx
            Unit
            Block
            Lot
            Property Description
            Acres
            Lot Sqft
            Non Owner Occupied
