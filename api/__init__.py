# List of blueprint modules as strings
blueprint_modules = [
    "api.base.add_person.main",
    "api.base.add_property.main",
    "api.base.add_transaction.main",
    "api.base.delete_person.main",
    "api.base.delete_property.main",
    "api.base.delete_transaction.main",
    "api.base.get_person.main",
    "api.base.get_property.main",
    "api.base.get_transaction.main",
    "api.base.update_person.main",
    "api.base.update_property.main",
    "api.base.update_transaction.main",
    "api.crm.download_people.main",
    "api.crm.download_properties.main",
    "api.crm.download_transactions.main",
    "api.crm.get_table_data.main",
    "api.authentication.authenticate_token.main",
    "api.authentication.refresh_token.main",
    "api.authentication.signin.main",
    "api.authentication.signup.main",
    "api.admin.delete_user.main",
    "api.google_places.address_autocomplete.main",
    "api.google_places.get_place_details.main",
]


# Function to dynamically import blueprints
def get_blueprints():
    from importlib import import_module

    blueprints = []
    for module_path in blueprint_modules:
        module = import_module(module_path)
        blueprints.append(module.blueprint)
    return blueprints
