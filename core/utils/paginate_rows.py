# core/utils/paginate_rows.py
from sqlalchemy import select, func, or_
from sqlalchemy.orm import joinedload

from core.database.azure_postgresql import AzurePostgreSQLDatabase

async def paginate_rows(
    model_class,
    page_number: int,
    page_size: int,
    sort_by: str,
    sort_ascending: bool,
    join=None,
    eagerloads=None,
    **conditions,
):
    db = AzurePostgreSQLDatabase()
    async with db.sessionmaker() as session:
        query = select(model_class)

        # Apply eager loading with specific columns
        if eagerloads:
            for load in eagerloads:
                relationship = getattr(
                    model_class, load["relationship"]
                )  # Ensure this is a direct attribute reference
                if "columns" in load and load["columns"]:
                    # Convert column names to class attributes
                    only_columns = [
                        getattr(relationship.property.mapper.class_, col)
                        for col in load["columns"]
                    ]
                    query = query.options(
                        joinedload(relationship).load_only(*only_columns)
                    )
                else:
                    query = query.options(joinedload(relationship))

        # Apply joins if specified
        if join:
            if isinstance(join, list):
                for j in join:
                    query = query.join(j)
            else:
                query = query.join(join)

        # Apply filters based on conditions
        if conditions:
            for key, value in conditions.items():
                column_attr = getattr(model_class, key)
                if isinstance(value, list):
                    # Check if None is one of the values and needs special handling
                    if None in value:
                        non_null_values = [v for v in value if v is not None]
                        if non_null_values:
                            # Combine 'in_' for non-null values and 'is_(None)' for null
                            condition = or_(
                                column_attr.in_(non_null_values),
                                column_attr.is_(None),
                            )
                        else:
                            # Only null values are specified
                            condition = column_attr.is_(None)
                    else:
                        condition = column_attr.in_(value)
                    query = query.filter(condition)
                else:
                    # Handle single value which might be None
                    if value is None:
                        query = query.filter(column_attr.is_(None))
                    else:
                        query = query.filter(column_attr == value)

        # Count total items matching the conditions
        total_items = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        # Apply sorting
        if sort_by:
            if sort_ascending:
                query = query.order_by(getattr(model_class, sort_by))
            else:
                query = query.order_by(getattr(model_class, sort_by).desc())

        # Apply pagination
        query = query.offset(page_number * page_size).limit(page_size)

        # Execute the query
        result = await session.execute(query)

        # Calculate total pages
        total_pages = (total_items + page_size - 1) // page_size

        return result.scalars().all(), total_items, total_pages
