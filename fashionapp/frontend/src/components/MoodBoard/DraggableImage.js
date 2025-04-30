import React, { useEffect, useState, useCallback , useMemo} from "react";
import { useDrag } from "react-dnd";
import {Maximize } from "@carbon/icons-react";

const DraggableImage = ({ img, moveImage }) => {
  const [{ isDragging }, drag] = useDrag({
    type: "IMAGE",
    item: { id: img.id },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  });

  return (
    <div
      ref={drag}
      className="moodboard-image-wrapper"
      style={{
        width: img.width,
        height: img.height,
        top: img.top,
        left: img.left,
        opacity: isDragging ? 0.5 : 1,
        position: "absolute",
        cursor: "grab",
      }}
    >
      <img src={`/${img.imgfilepath}`} alt={img.description} className="moodboard-img" />
      <button className="expand-icon" onClick={() => moveImage(img)} aria-label="Expand Image">
        <Maximize size={20} />
      </button>
    </div>
  );
};

export default DraggableImage;
