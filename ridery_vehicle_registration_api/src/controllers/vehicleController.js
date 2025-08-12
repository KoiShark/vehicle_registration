import { readData, writeData } from '../utils/db.js';

export const getAllVehicles = async (req, res) => {
  try {
    const data = await readData();
    res.json(data.vehicles || []);
  } catch (error) {
    console.error("Error getting vehicles:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

export const getVehicleById = async (req, res) => {
  try {
    const data = await readData();
    const id = parseInt(req.params.id);
    const vehicle = (data.vehicles || []).find(v => v.id === id);
    
    if (!vehicle) {
      return res.status(404).json({ error: "Vehicle not found" });
    }
    
    res.json(vehicle);
  } catch (error) {
    console.error("Error getting vehicle:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

export const registerVehicles = async (req, res) => {
  try {
    const { vehicles } = req.body;
    
    if (!vehicles || !Array.isArray(vehicles)) {
      return res.status(400).json({
        status: "error",
        message: "Invalid vehicles data"
      });
    }

    // Process vehicles (example: save to DB)
    console.log("Iterating vehicles:")
    for (const [index, vehicle] of vehicles.entries()) {
        console.log(`Vehicle ${index + 1}:`);
        console.log(vehicle);
    }

    // Read existing data
    const dbData = await readData();
    const existingVehicles = dbData.vehicles || [];

    // Process each new vehicle
    const updatedVehicles = [...existingVehicles]; // Start with existing vehicles

    for (const newVehicle of vehicles) {
        if (!newVehicle.id) {
            return res.status(400).json({
                status: "error",
                message: `Vehicle missing required field: id`
        });
    }

        const existingIndex = existingVehicles.findIndex(v => v.id === newVehicle.id);

        if (existingIndex >= 0) {
            // Update existing vehicle
            updatedVehicles[existingIndex] = { 
            ...updatedVehicles[existingIndex], 
            ...newVehicle 
            };
        } else {
            // Add new vehicle
            updatedVehicles.push(newVehicle);
        }
    }

    // Write updated data back to file
    await writeData({ vehicles: updatedVehicles });

    res.status(200).json({
      status: "success",
      message: `${vehicles.length} vehicles processed`
    });
  } catch (error) {
    console.error("Error registering vehicles:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};
