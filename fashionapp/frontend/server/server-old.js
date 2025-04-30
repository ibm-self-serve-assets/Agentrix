const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const cors = require("cors");

const app = express();
app.use(cors());

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
  },
});

let images = []; // Store shared images

io.on("connection", (socket) => {
  console.log("A user connected:", socket.id);

  // Send current images to new user
  socket.emit("init", images);

  // Listen for new image uploads
  socket.on("addImage", (image) => {
    images.push(image); // Update shared state
    io.emit("updateBoard", images); // Broadcast to all users
  });

  // Disconnect event
  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
  });
});

server.listen(5000, () => {
  console.log("Server running on port 5000");
});
