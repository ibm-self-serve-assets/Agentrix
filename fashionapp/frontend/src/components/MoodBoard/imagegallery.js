import React, { useState } from "react";

const ImageBoard = () => {
  const [boardImages, setBoardImages] = useState([]);
// console.log('image1', image1)
  // Images from the public folder
  const images = [
    { id: 1, src: "/image1.jpg", name: "Image 1" },
    { id: 2, src: "/image2.jpg", name: "Image 2" },
  ];

  // Function to add image to board
  const addToBoard = (src) => {
    setBoardImages([...boardImages, src]);
  };

  return (
    <div className="p-4">
      {/* Image Selection */}
      <div className="flex gap-4">
        {images.map((image) => (
          <div key={image.id} className="text-center">
            <img src={image.src} alt={image.name} width={100} height={100} className="w-32 h-32 border-2 border-gray-300 rounded" />
            <button
              onClick={() => addToBoard(image.src)}
              className="mt-2 px-3 py-1 bg-blue-500 text-white rounded"
            >
              Add to Board
            </button>
          </div>
        ))}
      </div>

      {/* Image Board */}
      <div className="mt-6 border-2 border-dashed border-gray-500 p-4">
        <h2 className="text-lg font-semibold mb-2" style={{padding: '2rem'}}>Mood Board</h2>
        <div className="flex gap-4" style={{padding: '2rem', border: '1px solid black'}}>
          {boardImages.length === 0 ? (
            <p>No images added yet.</p>
          ) : (
            boardImages.map((src, index) => (
              <img key={index} src={src} 
              width={100} height={100}
              alt={`Board Image ${index + 1}`} className="w-32 h-32 border-2 border-gray-300 rounded" />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageBoard;


