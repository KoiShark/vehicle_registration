import express from "express";
import {
  getAllVehicles,
  getVehicleById,
  registerVehicles
} from '../controllers/vehicleController.js';

const router = express.Router();

router.get('/', getAllVehicles);
router.get('/:id', getVehicleById);
router.post('/register', registerVehicles);

export default router;
