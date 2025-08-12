from odoo import api, fields, models


class FleetVehicleModel(models.Model):
    _inherit = "fleet.vehicle.model"

    short_code = fields.Char(string="Short Code", copy=False)
    sequence_code = fields.Char(
        string="Sequence Code", compute="_compute_sequence_code", copy=False, store=True, precompute=True
    )

    _sql_constraints = [
        ("short_code_unique", "unique(short_code/sequence_code)", "Short_code must be unique.")
    ]

    @api.depends("short_code")
    def _compute_sequence_code(self):
        """
        Compute individual sequence code for vehicle model
        """
        for rec in self:
            if (sequence_code := rec.sequence_code) and not rec.vehicle_count:
                # unlink existing sequence only when there's no vehicle associated
                print(f"\n\n{sequence_code=}\n\n")
                self.env["ir.sequence"].search([("code", "=", sequence_code)]).unlink()

            rec.sequence_code = rec.short_code and f"{rec.short_code}.vehicle.model" or False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            print(f"\n\n{vals=}\n\n")
            if (model := vals.get("name", False)) and (prefix := vals.get("short_code", False)):
                self._set_vehicle_model_sequence(model, prefix).id
        return super().create(vals_list)

    def write(self, vals):
        """
        Supered write
        """
        if code := vals.get("short_code", False):
            self._set_vehicle_model_sequence(model=self.name, prefix=code).id
        return super().write(vals)

    def _set_vehicle_model_sequence(self, model, prefix):
        """
        Set a unique sequence for each vehicle model
        """
        vals = {
            "name": f"{model} Vehicle",
            "code": f"{prefix}.vehicle.model",
            "prefix": f"{prefix}",
            "padding": 5,
            "company_id": False,
        }
        return self.env["ir.sequence"].create(vals)
