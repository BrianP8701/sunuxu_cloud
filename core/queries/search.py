# core/utils/search.py
from sqlalchemy import or_, select
from sqlalchemy.sql.expression import func

from core.database import Database
from core.models import *


async def search(
    table: str,
    query: str,
    user_id: int
):
    db = Database()
    async with db.sessionmaker() as session:
        match table:
            case "people":
                return await search_people(query, user_id)
            case "properties":
                return await search_properties(query, user_id)
            case "transactions":
                return await search_transactions(query, user_id)

async def search_people(query: str, user_id: int):
    db = Database()
    async with db.sessionmaker() as session:
        if any(char.isdigit() for char in query):
            if sum(char.isdigit() for char in query) > 6:
                # Query only the phone column
                stmt = select(PersonRowModel).where(
                    PersonRowModel.user_id == user_id,
                    or_(
                        func.levenshtein(PersonRowModel.phone, query) <= 3,  # Allowing up to 3 typos
                        PersonRowModel.phone.ilike(f"%{query}%")  # Partial match
                    )
                )
            else:
                # Query both email and phone columns
                stmt = select(PersonRowModel).where(
                    PersonRowModel.user_id == user_id,
                    or_(
                        func.levenshtein(PersonRowModel.email, query) <= 3,  # Allowing up to 3 typos
                        PersonRowModel.email.ilike(f"%{query}%"),  # Partial match
                        func.levenshtein(PersonRowModel.phone, query) <= 3,  # Allowing up to 3 typos
                        PersonRowModel.phone.ilike(f"%{query}%")  # Partial match
                    )
                )
        elif "@" in query:
            # Query the email column
            stmt = select(PersonRowModel).where(
                PersonRowModel.user_id == user_id,
                or_(
                    func.levenshtein(PersonRowModel.email, query) <= 3,  # Allowing up to 3 typos
                    PersonRowModel.email.ilike(f"%{query}%")  # Partial match
                )
            )
        else:
            # Query the name column
            stmt = select(PersonRowModel).where(
                PersonRowModel.user_id == user_id,
                or_(
                    func.levenshtein(PersonRowModel.name, query) <= 3,  # Allowing up to 3 typos
                    PersonRowModel.name.ilike(f"%{query}%"),  # Partial match
                    func.levenshtein(PersonRowModel.email, query) <= 3,  # Allowing up to 3 typos
                    PersonRowModel.email.ilike(f"%{query}%")  # Partial match
                )
            )

        result = await session.execute(stmt)
        rows = result.scalars().all()
        return rows

async def search_transactions(query: str, user_id: int):
    db = Database()
    async with db.sessionmaker() as session:
        stmt = select(DealRowModel).where(
            DealRowModel.user_id == user_id,
            or_(
                func.levenshtein(DealRowModel.name, query) <= 3,  # Allowing up to 3 typos
                DealRowModel.name.ilike(f"%{query}%")  # Partial match
            )
        )
        result = await session.execute(stmt)
        rows = result.scalars().all()
        return rows

async def search_properties(query: str, user_id: int):
    db = Database()
    async with db.sessionmaker() as session:
        if any(char.isdigit() for char in query) and sum(char.isdigit() for char in query) > 6:
            # Query the mls_number column
            stmt = select(PropertyRowModel).where(
                PropertyRowModel.user_id == user_id,
                or_(
                    func.levenshtein(PropertyRowModel.mls_number, query) <= 3,  # Allowing up to 3 typos
                    PropertyRowModel.mls_number.ilike(f"%{query}%")  # Partial match
                )
            )
        else:
            # Query the address column
            stmt = select(PropertyRowModel).where(
                PropertyRowModel.user_id == user_id,
                or_(
                    func.levenshtein(PropertyRowModel.address, query) <= 3,  # Allowing up to 3 typos
                    PropertyRowModel.address.ilike(f"%{query}%")  # Partial match
                )
            )
        
        result = await session.execute(stmt)
        rows = result.scalars().all()
        return rows
