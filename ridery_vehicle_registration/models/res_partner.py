import requests
import logging
import json

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    vehicle_ids = fields.One2many("fleet.vehicle", "driver_id", string="Vehicles")
    vehicle_count = fields.Integer(
        compute="_compute_vehicle_count", string="Vehicle Count"
    )

    def _compute_vehicle_count(self):
        """
        Compute the number of vehicles assigned to a contact.

        Assing:
        int -> vehicle_count: number of vehicles.
        """

        for rec in self:
            rec.vehicle_count = len(rec.vehicle_ids)

    def action_open_vehicles(self):
        """
        Open a list view with the vehicles assigned to the contact

        Returns:
        ir.actions.act_window
        """
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Vehicles"),
            "view_mode": "tree,form",
            "res_model": "fleet.vehicle",
            "domain": [("id", "in", self.vehicle_ids.ids)]
        }

    def action_send_vehicle_api(self):
        """
        Action to send vehicles by driver.
        """
        self.ensure_one()

        vehicle_data = self.vehicle_ids.mapped(lambda vehicle: {
            "id": vehicle.id,
            "name": vehicle.name,
            "modelId": vehicle.model_id.id,
            "model": vehicle.model_id.display_name,
            "driverId": vehicle.driver_id.id,
            "driver": vehicle.driver_id.display_name,
            "brand": vehicle.brand_id.display_name,
            "license_plate": vehicle.license_plate,
            "odometer": vehicle.odometer_count,
            "odometer_unit": vehicle.odometer_unit,
            "color": vehicle.color,
            "modelYear": vehicle.model_year,
            "transmission": vehicle.transmission,
        })

        payload = {
            "driverId": self.id,
            "vehicles": vehicle_data,
        }

        endpoint = self.env['ir.config_parameter'].sudo().get_param("ridery_vehicle_registration.vehicle_registration_endpoint", default="http://localhost:3000/api/vehicles/register")

        try:
            response = requests.post(
                url="http://localhost:3000/api/vehicles/register",
                data=json.dumps(payload),
                headers={
                    "Content-Type": "application/json",
                },
                timeout=30,
            )

            # create log with
            response_data = response.json()

            type = response.status_code == 200 and "success" or "warning"

            message = f"Code {response.status_code}. {response_data.get('message', 'error')}"
            status = response_data.get("status", "error")

            self.env["vehicle.api.log"].set_api_log(message, status)

        except requests.exceptions.RequestException as e:
            type = "warning"
            message = e
            status = "error"
            self.env["vehicle.api.log"].set_api_log(message, status)

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Vehicle API status"),
                "type": type,
                "message": message,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
