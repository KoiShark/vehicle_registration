{
    "name": "Vehicle Registration",
    "version": "16.0.0.0.1",
    "category": "Human Resources/Fleet",
    "author": "Joel Rivas",
    "contributors": ["Joel Rivas <joelrivas39@gmail.com>"],
    "depends": ["contacts", "fleet"],
    "description": """
    Manage vehicle registration and stablish a API connection
    to log the response in the log model.
    """,
    "data": [
        "security/ir.model.access.csv",
        "data/ir_actions_server.xml",
        "views/res_partner_views.xml",
        "views/fleet_vehicle_views.xml",
        "views/fleet_vehicle_model_views.xml",
        "views/vehicle_api_log_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
