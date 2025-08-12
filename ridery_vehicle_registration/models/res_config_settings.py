from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # TODO: add logic to admit webhooks based on parameters
    enable_log_creation_webhook = fields.Boolean(
        string="Enable log creation webhook",
        default=False,
        config_parameter="ridery_vehicle_registration.enable_log_creation_webhook",
    )

    vehicle_registration_endpoint = fields.Char(
        string="Registration Endpoint",
        default="http://localhost:3000/api/vehicles/register",
        config_parameter="ridery_vehicle_registration.vehicle_registration_endpoint",
    )
