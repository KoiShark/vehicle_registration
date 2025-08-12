from odoo import api, fields, models


class VehicleAPILog(models.Model):
    _name = "vehicle.api.log"
    _description = "Logs from Vehicle node API"

    name = fields.Char(string="Response Text")
    response_date = fields.Datetime(string="Response Date", default=fields.Datetime.now)
    status = fields.Selection(
        [("success", "Success"),
         ("error", "Error")], string="Status"
    )

    def set_api_log(self, message, status):
        """
        Handles api log creation
        """

        vals_list = [{
            "name": message,
            "status": status,
        }]

        self.env["vehicle.api.log"].create(vals_list)
