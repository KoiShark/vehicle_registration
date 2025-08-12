from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    vehicle_image_128 = fields.Image(
        string="Vehicle img", max_width=128, max_height=128, copy=False
    )

    vehicle_sequence = fields.Char(
        string="Vehicle Sequence", copy=False
    )

    @api.depends("model_id.brand_id.name", "model_id.name", "license_plate", "vehicle_sequence")
    def _compute_vehicle_name(self):
        super()._compute_vehicle_name()
        for rec in self:
            rec.name += rec.vehicle_sequence and f"/{rec.vehicle_sequence}" or ""

    @api.constrains("driver_id")
    def _check_driver_id(self):
        if not self.driver_id:
            raise ValidationError(_("It's mandatory to assign a driver to the vehicle."))

    @api.constrains("license_plate")
    def _check_license_plate(self):
        if not self.license_plate:
            raise ValidationError(_("It's mandatory to assign a license plate to the vehicle."))

    @api.model_create_multi
    def create(self, vals_list):
        """Supered create model to create sequence."""
        for vals in vals_list:
            if not vals.get("vehicle_sequence", False) and (vehicle_model_id := vals.get("model_id", False)):
                vals.update({
                    "vehicle_sequence": self._get_vehicle_sequence(vehicle_model=vehicle_model_id)
                })
        return super().create(vals_list)

    def _get_vehicle_sequence(self, vehicle_model):
        """
        Get vehicle model sequence next by code.

        Returns:
        char: vehicle sequence.
        """
        model_id = self.env["fleet.vehicle.model"].browse(vehicle_model)
        sequence_obj = self.env["ir.sequence"]
        vehicle_sequence = sequence_obj.next_by_code(model_id.sequence_code)
        return vehicle_sequence

    def update_vehicle_sequence(self):
        for rec in self:
            rec.vehicle_sequence = rec._get_vehicle_sequence(vehicle_model=rec.model_id.id)
