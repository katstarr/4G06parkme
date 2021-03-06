let ParkingLotData = require("../modules/ParkingLotsData")

module.exports = (app) => {
    app.get('/api/parkinglot/:id/parkingspaces/all', (req, res) => {
        res.send({parkingspaces: ParkingLotData.GetAllParkingSpaces(req.params.id)});
    })

    app.get('/api/parkinglot/:id/parkingspaces/best', (req, res) => {
        res.send({id: ParkingLotData.GetBestParkingSpace(req.params.id, req.query.preference, req.query.accessible)});
    })

    app.get('/api/parkinglot/:id/parkingspaces/:parkingspaceid', (req, res) => {
        res.send({parkingspaces: ParkingLotData.GetParkingSpace(req.params.id, req.params.parkingspaceid)});
    })
}