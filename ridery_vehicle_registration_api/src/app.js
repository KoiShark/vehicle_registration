import express from "express";
import vehicleRoutes from './routes/vehicleRoutes.js';

const PORT = 3000;

const app = express();
app.use(express.json());

// Routes
app.use('/api/vehicles', vehicleRoutes);

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something broke!' });
});

app.listen(PORT, () => {
    console.log(`Server running at port http://localhost:${PORT}`);
});
