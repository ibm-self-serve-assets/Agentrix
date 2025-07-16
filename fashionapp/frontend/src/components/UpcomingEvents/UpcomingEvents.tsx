import React, { useState, useEffect } from "react";
import {
  Column,
  Button,
  Tile,
  Row,
  SkeletonPlaceholder,
} from "@carbon/react";
import "./UpcomingEvents.scss";
import {
  AiRecommend,
  ShoppingCatalog,
  Add,
  Edit,
  Location,
  Event,
} from "@carbon/icons-react";
import ModalAddEdit from "../ModalAddEdit/ModalAddEdit";
import CustomAILabel from "../CustomAILabel/CustomAILabel";
import { useNavigate } from "react-router-dom";

interface ImageData {
  user: any;
  userDetails: any;
  setUserDetails: any;
  id: string;
  category: string;
  description: string;
  imgfilepath: string;
  isLoading: any;
  setIsLoading: Function;
  setTrigger: Function;
  trigger: any;
}

const UpcomingEvents = ({
  user,
  userDetails,
  setUserDetails,
  handleShowEventsChange,
  eventDetails,
  setEventRecommendationId,
  wardrobeDetails,
  currentEvt,
  isLoading,
  setIsLoading,
  setTrigger,
  trigger,
}) => {
  const facts = [
    "📱 The average fashion lover scrolls through over 2,000 outfits a week! 📱",
    "👗 Virtual try-ons are changing the way we shop—goodbye dressing rooms! 👗",
    "🎯 73% of users say personalized style suggestions make shopping way easier! 🎯",
    "🛍️ Shoppers are 3x more likely to buy when they can visualize the outfit! 🛍️",
    "🤳 Mirror selfies have officially replaced fitting rooms for fashion decisions! 🤳",
    "📦 The top reason for returns? Wrong size. Fit tech is here to fix that! 📦",
    "🔍 Most users decide in just 8 seconds if an outfit is a yes or no! 🔍",
    "🌍 Sustainable fashion searches have doubled in the past year—style meets impact! 🌍",
    "💬 Reviews with photos get 5x more clicks—seeing is believing in fashion! 💬",
    "🎨 AI-generated outfit pairings are helping users discover new looks daily! 🎨",
  ];
  

  const [selectedEventForModal, setSelectedEventForModal] = useState(null);
  const [imageData, setImageData] = useState<ImageData[]>([]);

  const [open, setOpen] = useState(false);
  const [stylingImages, setStylingImages] = useState<ImageData[]>([]);
  const [currentFact, setCurrentFact] = useState(facts[0]);

  useEffect(() => {
    const interval = setInterval(() => {
      const randomIndex = Math.floor(Math.random() * facts.length);
      setCurrentFact(facts[randomIndex]);
    }, 5000); // Changes fact every 5 seconds

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, []);

  useEffect(() => {
    fetch("/json files/imgmap.json") // Fetch JSON from the public folder
      .then((res) => res.json())
      .then((data: ImageData[]) => {
        if (!Array.isArray(data)) {
          console.error("Error: imgmap.json data is not an array!");
          return;
        }
        const filteredImages = data?.filter(
          (img) => wardrobeDetails?.map(String).includes(img.id.trim()) // Trim here!
        );
        // console.log('filteredImages', filteredImages)
        setImageData(filteredImages);
        console.log("Image Data -> ", imageData, currentEvt);
        if (currentEvt && currentEvt?.event_id > 0) {
          // Ensure styling_images is parsed to an array
          let stylingImagesArray = [];
          if (typeof currentEvt.styling_images === "string") {
            try {
              stylingImagesArray = JSON.parse(
                currentEvt.styling_images.replace(/'/g, '"')
              );
            } catch (error) {
              console.error("Error parsing styling_images:", error);
            }
          } else if (Array.isArray(currentEvt.styling_images)) {
            stylingImagesArray = currentEvt.styling_images;
          }

          const filteredStylingImages = data?.filter((img) =>
            stylingImagesArray.map(String).includes(img.id.trim())
          );

          console.log("filteredStylingImages", filteredStylingImages);
          setStylingImages(filteredStylingImages);
        }
      })
      .catch((error) => console.error("Error loading image map:", error));
  }, [eventDetails, currentEvt]);
  useEffect(() => {
    fetch("/json files/imgmap.json")
      .then((res) => res.json())
      .then((data: ImageData[]) => {
        if (!Array.isArray(data)) {
          console.error("Error: imgmap.json data is not an array!");
          return;
        }

        // Filter wardrobe images
        const filteredImages = data.filter((img) =>
          wardrobeDetails?.map(String).includes(img.id.trim())
        );
        setImageData(filteredImages);
        console.log("Image Data ->", filteredImages, currentEvt);

        // Ensure `currentEvt` and `currentEvt.response.image_ids` exist
        if (currentEvt?.response?.image_ids) {
          const stylingImagesArray = currentEvt.response.image_ids.map(String);

          const filteredStylingImages = data.filter((img) =>
            stylingImagesArray.includes(img.id.trim())
          );

          console.log("Filtered Styling Images ->", filteredStylingImages);
          setStylingImages(filteredStylingImages);
        }
      })
      .catch((error) => console.error("Error loading image map:", error));
  }, [wardrobeDetails, currentEvt]);

  const eventDetailsOld = [
    {
      id: "event1",
      name: "Valentine Dinner",
      location: "Pune",
      description:
        "Gain private access to your IBM Cloud Infrastrucure, plus other Exchange provider clo",
      recommendation: "",
      bgColor: "#001d6c",
    },
    {
      id: "event2",
      name: "Valentine Dinner",
      location: "Pune",
      description:
        "Gain private access to your IBM Cloud Infrastrucure, plus other Exchange provider clo",
      recommendation: "",
      bgColor: "#0f62fe",
    },
    {
      id: "event3",
      name: "Valentine Dinner",
      location: "Pune",
      description:
        "Gain private access to your IBM Cloud Infrastrucure, plus other Exchange provider clo",
      recommendation: "",
      bgColor: "#001d6c",
    },
  ];
  const [eventDetailsnew, setEventDetails] = useState(eventDetails);

  const navigate = useNavigate();

  const handleNavigateToMoodboard = (evt) => {
    navigate("/moodboard", { state: { user, event: evt } });
  };

  const handleAddModal = () => {
    setOpen(true);
    setSelectedEventForModal(null);
  };

  const handleEditModal = (event) => {
    // Open the modal with the selected event's data (for editing)
    setOpen(true);
    setSelectedEventForModal(event); // Pass selected event data
  };
  // Step 4: Function to handle adding a new event
  const addEvent = (newEvent) => {
    console.log("Adding or updating event:", newEvent);
    newEvent.showEditIcon = true;

    // If event_id exists and is valid, we update the event
    if (newEvent.event_id) {
      console.log("newEvent -> ", newEvent.event_id);
      setEventDetails((prevEvents) => {
        const existingEventIndex = prevEvents.findIndex(
          (event) => event.event_id === newEvent.event_id
        );

        // If event ID exists, update it, otherwise add the new event
        if (existingEventIndex !== -1) {
          return prevEvents.map((event, index) =>
            index === existingEventIndex ? { ...event, ...newEvent } : event
          );
        } else {
          return [...prevEvents, newEvent];
        }
      });
      console.log("event details after setting -> ", eventDetails);
    }

    setUserDetails((prevUser) => {
      const userEvents = prevUser.user_events || [];

      const existingUserEventIndex = userEvents.findIndex(
        (event) => event.event_id === newEvent.event_id
      );

      let updatedUserEvents;
      if (existingUserEventIndex !== -1) {
        updatedUserEvents = userEvents.map((event, index) =>
          index === existingUserEventIndex ? { ...event, ...newEvent } : event
        );
      } else {
        updatedUserEvents = [
          ...userEvents,
          { ...newEvent, event_id: newEvent.event_id || Date.now() },
        ];
      }

      return {
        ...prevUser,
        user_events: updatedUserEvents,
      };
    });
    console.log("Updated user with event:", userDetails);
  };

  const formatText = (text: any) => {
    if (typeof text !== "string") {
      console.warn("formatText received a non-string value:", text);
      return text; // Return as-is or an empty fragment
    }

    return text.split("\n").map((line, index) => (
      <React.Fragment key={index}>
        {line}
        <br />
      </React.Fragment>
    ));
  };

  // const [wardrobeImages, setWardrobeImages] = useState(wardrobeImagesList);
  return (
    <div className="">
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div>
          <h3 style={{ margin: "1rem 0" }}>Upcoming Events</h3>
        </div>
        <div style={{ marginTop: "1rem" }}>
          <Button
            kind="primary"
            size="md"
            disabled={eventDetailsnew?.length > 4}
            renderIcon={Add}
            onClick={handleAddModal}
          >
            Add Event
          </Button>
        </div>
      </div>

      <Row className="scrollable-row">
        {eventDetailsnew?.length > 0 &&
          eventDetailsnew?.map((evt, key) => {
            return (
              <>
                <Column key={evt.id} sm={4} md={4} lg={5}>
                  <Tile
                    className="event-tiles"
                    id="clickable-tile-1"
                    // renderIcon={Launch}
                    key={evt.event_id}
                  >
                    <div
                      key={evt.id}
                      style={{
                        paddingBottom: "1rem",
                        paddingTop: "0.5rem",
                        display: "flex",
                        justifyContent: "space-between",
                      }}
                    >
                      <div>
                        {" "}
                        <h4 style={{ paddingTop: "0rem" }}>{evt.event_name}</h4>
                      </div>
                      <div style={{ display: "flex", marginRight: "0.5rem" }}>
                        <AiRecommend
                          className="ai-recommend"
                          key={evt.id}
                          onClick={(event) => {
                            console.log("Clicked event -> ", evt);
                            setTrigger(true);
                            setIsLoading(true);
                            setEventRecommendationId(evt.event_id);
                          }}
                          style={{
                            cursor: "pointer",
                            width: "24px",
                            height: "24px",
                          }}
                        />
                        {evt.showEditIcon && (
                          <div
                            style={{ display: "flex", marginLeft: "1rem" }}
                            onClick={() => handleEditModal(evt)}
                          >
                            <Edit
                              style={{
                                cursor: "pointer",
                                width: "24px",
                                height: "24px",
                              }}
                            />
                          </div>
                        )}
                      </div>
                    </div>

                    <div
                      style={{
                        textWrap: "wrap",
                        marginBottom: "1rem",
                        flex: "1",
                        minHeight: "36px",
                      }}
                    >
                      {evt.event_description}
                    </div>
                    <div
                      style={{
                        flexDirection: "row",
                        display: "flex",
                        gap: "25px",
                        marginBottom: "0.5rem",
                      }}
                    >
                      <div
                        style={{
                          flexDirection: "row",
                          display: "flex",
                          gap: "4px",
                        }}
                      >
                        <Location />
                        {evt.event_location}
                      </div>
                      <div
                        style={{
                          flexDirection: "row",
                          display: "flex",
                          gap: "4px",
                        }}
                      >
                        <Event />
                        {evt.event_date}
                      </div>
                    </div>
                    {/* <div
                      style={{
                        marginBottom: "1.5rem",
                        // bottom: "1rem",
                        // position: "absolute",
                      }}
                    >
                      <Tag
                        className="some-class"
                        onClose={() => {}}
                        size="md"
                        title="Date"
                        type="green"
                      >
                        {evt.event_date}
                      </Tag>
                      <Tag
                        className="some-class"
                        onClose={() => {}}
                        size="md"
                        title="Date"
                        type="purple"
                      >
                        {evt.event_location}
                      </Tag>
                    </div> */}

                    <div
                      style={{
                        bottom: "1rem",
                        right: "1rem",
                        justifySelf: "right"
                      }}
                    >
                  
                    </div>
                  </Tile>
                </Column>
              </>
            );
          })}
      </Row>
      <Row style={{ marginTop: "0.5rem" }}>
        <Column>
          <h3 style={{ margin: "1rem 0" }}>Recommendations</h3>
          <Tile className="bg-tile-event">
            {trigger ? (
              isLoading ? (
                <div>
                  <h4 style={{ marginBottom: "1rem", fontStyle: "italic" }}>
                    A touch of luxury takes a moment, in the meantime, did you
                    know...?{" "}
                  </h4>
                  <h5
                    style={{
                      fontFamily: "cursive",
                      fontSize: "x-large",
                      marginBottom: "2rem",
                    }}
                  >
                    {currentFact}
                  </h5>
                  <SkeletonPlaceholder className="skeleton-loader" />
                </div>
              ) : (
                <Row
                  style={{
                    marginTop: "0.5rem",
                    display: "flex",
                    alignItems: "stretch",
                  }}
                >
                  <Column
                    lg={10}
                    style={{ display: "flex", flexDirection: "column" }}
                  >
                    <Tile
                      decorator={
                        <CustomAILabel name="mistralai/mixtral-8x7b-instruct-v01" />
                      }
                      id="tile-1"
                      className="bg-tile-recommendation"
                      style={{
                        flex: 1,
                        display: "flex",
                        flexDirection: "column",
                        maxHeight: "480px",
                        overflow: "hidden",
                      }}
                    >
                      <div className="ai-data">
                        <div className="data-container">
                          <h4> Styling Recommendation</h4>
                        </div>
                      </div>
                      <div
                        style={{
                          display: "flex",
                          padding: "1rem",
                          flexWrap: "wrap",
                          overflowY: "scroll",
                        }}
                      >
                        <Row narrow>
                          {stylingImages.map((img) => (
                            <Column lg={4}>
                              <Tile
                                style={{
                                  height: "330px", // Ensure all tiles have the same height
                                  width: "100%",
                                  padding: 0,
                                  marginBottom: "0.5rem",
                                  overflow: "hidden",
                                  display: "flex",
                                  flexDirection: "column",
                                }}
                              >
                                {/* Image on top, full width */}
                                <div style={{ width: "100%" }}>
                                  <img
                                    src={`/${img.imgfilepath}`}
                                    alt={img.description}
                                    style={{
                                      width: "100%",
                                      height: "240px", // Adjust as needed
                                      objectFit: "cover",
                                      display: "block",
                                    }}
                                  />
                                </div>

                                {/* Description below, left-aligned */}
                                <div
                                  style={{
                                    padding: "1rem",
                                    flex: 1,
                                    display: "flex",
                                    alignItems: "flex-start",
                                    justifyContent: "center",
                                    textAlign: "left",
                                  }}
                                >
                                  <h5
                                    style={{
                                      margin: "0",
                                      fontSize: "1rem",
                                      width: "100%", // Ensures it takes full space
                                    }}
                                  >
                                    {img.description}
                                  </h5>
                                </div>
                              </Tile>
                            </Column>
                          ))}
                        </Row>
                      </div>
                    </Tile>
                  </Column>
                  <Column
                    lg={6}
                    style={{ display: "flex", flexDirection: "column" }}
                  >
                    <Tile
                      decorator={
                        <CustomAILabel name="mistralai/mixtral-8x7b-instruct-v01" />
                      }
                      className=".bg-tile-recommendation"
                      style={{
                        flex: 1,
                        display: "flex",
                        flexDirection: "column",
                        maxHeight: "480px",
                        overflow: "hidden",
                      }}
                    >
                      <h4> Travel Recommendation</h4>
                      <div
                        style={{
                          padding: "1rem",
                        }}
                      >
                        <img
                          src="/bee.svg"
                          alt="beeImg"
                          width={32}
                          height={32}
                        ></img>
                      </div>
                      <div
                        style={{
                          padding: "0rem  0rem",
                          textAlign: "justify",
                          flex: 1,
                          flexWrap: "wrap",
                          overflowY: "scroll",
                        }}
                      >
                        {formatText(currentEvt?.travel_recc)}
                      </div>
                    </Tile>
                  </Column>
                </Row>
              )
            ) : (
              <div>
                <h4>
                  {" "}
                  Plan your look effortlessly—click an event for instant
                  recommendations!{" "}
                </h4>
                <div style={{ padding: "2rem" }}>
                  <ShoppingCatalog size={72} />
                </div>
              </div>
            )}
          </Tile>
        </Column>
      </Row>
      <div>
        <h3 style={{ margin: "1rem 0" }}>My Wardrobe</h3>
        <Row>
          {imageData.map((img) => (
            <Column key={img.id} lg={4}>
              <Tile
                style={{
                  height: "260px", // Ensure all tiles have the same height
                  width: "100%",
                  padding: "0",
                  overflow: "hidden",
                  display: "flex",
                  flexDirection: "column",
                }}
              >
                {/* Image on top, full width */}
                <div style={{ width: "100%" }}>
                  <img
                    src={`/${img.imgfilepath}`}
                    alt={img.description}
                    style={{
                      width: "100%",
                      height: "180px", // Adjust as needed
                      objectFit: "cover",
                      display: "block",
                    }}
                  />
                </div>

                {/* Description below, left-aligned */}
                <div
                  style={{
                    padding: "1rem",
                    flex: 1,
                    display: "flex",
                    alignItems: "flex-start",
                    justifyContent: "center",
                    textAlign: "left",
                  }}
                >
                  <h5
                    style={{
                      margin: "0",
                      fontSize: "1rem",
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      width: "100%", // Ensures it takes full space
                    }}
                  >
                    {img.description}
                  </h5>
                </div>
              </Tile>
            </Column>
          ))}
        </Row>
      </div>

      {open && (
        <>
          <ModalAddEdit
            open={open}
            userDetails={userDetails}
            modalHeading={
              selectedEventForModal
                ? "Edit Event details"
                : "Add New Event details"
            }
            setOpen={() => setOpen(false)}
            modalLabel={""}
            // setUserDetails={(vale)=> setUserDetails(value)}
            action={selectedEventForModal ? "Save Changes" : "Save"} // Adjust button text
            addEvent={addEvent} // Pass addEvent handler
            selectedEventForModal={selectedEventForModal} // Pass selected event if editing
            isEdit={selectedEventForModal ? true : false} // Pass isEdit flag to differentiate Add/Edit
          />
        </>
      )}
    </div>
  );
};

export default UpcomingEvents;
