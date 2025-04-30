import React from "react";
import "./EmptyState.css";
import beeImage from "../../assets/beeImage.png"

import { Tile } from "@carbon/react";

const EmptyState = (props) => {
  return (
    <Tile  className="empty-state pa-8">
      <img
        src={
          beeImage
        }
        alt={"name"}
        style={{ height: "30px" }}
        className="rotate-image"
      />
      <h4>{props.title}</h4>
    </Tile>
  );
};

export default EmptyState;
