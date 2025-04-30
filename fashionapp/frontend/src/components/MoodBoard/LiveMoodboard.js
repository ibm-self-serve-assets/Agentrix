import React, { useEffect, useState } from "react";
import {
  Row,
  Column,
  Tile,
  Dropdown,
  Tag,
  RadioButtonGroup,
  RadioButton,
  Button,
  Link,
  SkeletonPlaceholder,
  DatePicker,
  DatePickerInput,
  Modal,
  InlineNotification
} from "@carbon/react";
import { AddAlt, ShoppingCatalog, Maximize, Add } from "@carbon/icons-react";
import LeftPanel from "../LeftPanel/leftPanel";
import { useLocation } from "react-router-dom";
import CustomAILabel from "../CustomAILabel/CustomAILabel";
import "./LiveMoodboard.scss";
import { getMbRecommendation } from "../../services/llm.service";
import { useNavigate } from "react-router-dom";
// import Draggable from "react-draggable";
import { DraggableCore } from "react-draggable";
import { useMemo } from "react";


const LiveMoodboard = () => {
  const location = useLocation();
  const facts = [
    "👠 Louboutin’s red soles? Inspired by a bottle of nail polish! 👠",
    "👜 A Hermès Birkin bag once sold for $500,000—more than a house! 👜",
    "👗 The ‘Little Black Dress’ was once considered scandalous! 👗",
    "💎 The world’s most expensive shoes are worth $17 million! 💎",
    "🕶️ Sunglasses were first worn by judges in ancient China to hide emotions. 🕶️",
    "🎩 Burberry invented the trench coat, but it wasn’t for fashion—it was military gear! 🎩",
    "⌚ Some luxury watches take years to make—Rolex insists on perfection! ⌚",
    "🏛️ The first high heels were worn by men in the 1600s for horse riding. 🏛️",
    "✨ Marie Antoinette’s custom-made shoes still exist—valued at $50,000! ✨",
    "🎭 Venetian women in the 15th century wore 20-inch platform shoes! 🎭",
  ];

  const { user, event } = location.state || {};


  const [editForm, setEditForm] = useState(false);
  const [email, setEmail] = useState("");
  const [userDetails, setUserDetails] = useState(user || {});
  const [eventDetails, setEventDetails] = useState(user?.user_events || []);
  const [gender, setGender] = useState(user?.gender || "female");
  const [catalogItems, setCatalogItems] = useState([]);
  const [moodboardImages, setMoodboardImages] = useState([]);
  const [moodboardImageIds, setMoodboardImageIds] = useState([]);
  const [mbRecommendations, setMbRecommendations] = useState([]);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [currentFact, setCurrentFact] = useState(facts[0]);
  const [triggerAPI, setTriggerAPI] = useState(false);
  const [category, setCategory] = useState([]);
  const [catalogByCategory, setCatalogByCategory] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [inlineToastMsg, setInlineToastMsg] = useState(false);
  const [notificationTitle, setNotificationTitle] = useState(
    "Server is not reachable"
  );
  const [notificationKind, setNotificationKind] = useState("info");
  

  const navigate = useNavigate();

  useEffect(() => {
    if (userDetails) {
      setEventDetails(userDetails.user_events || []);
      console.log("Updated user details:", userDetails);
    }
  }, [userDetails]);

  // Convert date for display in DatePicker format (mm/dd/yyyy)
  const formatDateToPicker = (date) => {
    const cleanDate = date.replace(/\d+(st|nd|rd|th)/, (match) => match.slice(0, -2));
    const d = new Date(cleanDate);

    if (isNaN(d.getTime())) {
      console.log("Invalid date:", date);
      return "";
    }

    const month = (d.getMonth() + 1).toString().padStart(2, "0");
    const day = d.getDate().toString().padStart(2, "0");
    const year = d.getFullYear();
    return `${month}/${day}/${year}`; // MM/DD/YYYY format
  };

  const [date, setDate] = useState(formatDateToPicker(event.event_date));

  const handleDropdownChange = ({ selectedItem }) => {
    console.log('selectedItem', selectedItem);
    console.log("Current Background:", randomBgImage);

    // const handleDateChange = (date: any) => setDate(date); // DatePicker gives date in specific format


    const filteredItems = catalogItems.filter((item) => {
      return item?.category === selectedItem.appendText + ' ' + selectedItem.category
    }
    );
    setCatalogByCategory(filteredItems);
  };

  useEffect(() => {
    fetch("/json files/imgmap.json")
      .then((response) => response.json())
      .then((data) => {
        // Filter catalog items by selected gender
        const filteredItems = data.filter(
          (item) => item?.gender?.toLowerCase() === gender?.toLowerCase()
        );
        setCatalogItems(filteredItems);

        const uniqueCategories = Array.from(
          new Map(filteredItems.map((item) => {
            const match = item.category.match(/\b(men|women)\b/gi); // Extract "men" or "women"
            const appendText = match ? match[0] : null;  // Store "men" or "women" if found
            const cleanedCategory = item.category.replace(/\b(men|women)\b/gi, "").trim();  // Remove "men" or "women"
            return [cleanedCategory, { id: item.id, category: cleanedCategory, appendText }];
          })).values()
        );
        setCategory(uniqueCategories);
        console.log('uniqueCategories', uniqueCategories);
      })
      .catch((error) => console.error("Error loading catalog:", error));
  }, [gender]);

  useEffect(() => {
    console.log("Updated Moodboard Image IDs:", moodboardImageIds);
  }, [moodboardImageIds]);

  useEffect(() => {
    console.log("Updated Moodboard Images:", moodboardImages);
  }, [moodboardImages]);

  useEffect(() => {
    const interval = setInterval(() => {
      const randomIndex = Math.floor(Math.random() * facts.length);
      setCurrentFact(facts[randomIndex]);
    }, 5000); // Changes fact every 5 seconds

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, []);

  const handleEditFormChange = (newValue) => {
    setEditForm(newValue);
  };

  const handleGenderChange = (value) => {
    setGender(value);
  };
  const handleAddToMoodboard = (item) => {
    setMoodboardImages((prevImages) => {
      if (prevImages.some((img) => img.id === item.id)) return prevImages;

      const containerWidth = 500; // Replace with dynamic size if needed
      const containerHeight = 500;
      const maxAttempts = 100;
      let newItem;
      let attempts = 0;

      do {
        const newWidth = Math.floor(Math.random() * 80) + 100;
        const newHeight = Math.floor(Math.random() * 80) + 100;

        // Generate a more evenly distributed left position
        const sections = Math.floor(containerWidth / newWidth);
        const sectionIndex = Math.floor(Math.random() * sections);
        const newLeft = sectionIndex * (containerWidth / sections);

        // Ensure top is also well-distributed
        const newTop = Math.floor(Math.random() * (containerHeight - newHeight));

        newItem = {
          ...item,
          width: newWidth,
          height: newHeight,
          top: newTop,
          left: newLeft,
        };

        attempts++;

        if (attempts > maxAttempts) {
          console.warn("Couldn't place image without overlap, placing anyway.");
          break;
        }

      } while (prevImages.some(img => isOverlapping(img, newItem)));

      console.log('newItem', newItem);

      return [...prevImages, newItem];
    });

    setMoodboardImageIds((prevIds) => {
      if (prevIds.includes(item.id)) return prevIds;
      return [...prevIds, item.id];
    });
  };

  // Function to check overlap
  const isOverlapping = (img1, img2) => {
    return !(
      img1.left + img1.width < img2.left ||
      img2.left + img2.width < img1.left ||
      img1.top + img1.height < img2.top ||
      img2.top + img2.height < img1.top
    );
  };



  const eventImages = {
    "Business Trip": [
      "/bg-images/business-travel-1.jpg",
      "/bg-images/business-travel-2.jpg",
      "/bg-images/business-travel-3.jpg",
    ],
    "Valentine Dinner": [
      "/bg-images/valentines-dinner-1.jpg",
      "/bg-images/valentines-dinner-2.jpg",
      "/bg-images/valentines-dinner-3.jpg",
      "/bg-images/valentines-dinner-4.jpg",
      "/bg-images/valentines-dinner-5.jpg",

    ],
    "Fashion Event": [
      "/bg-images/fashion-event-1.jpg",
      "/bg-images/fashion-event-2.jpg",
      "/bg-images/fashion-event-3.jpg",
      "/bg-images/fashion-event-4.jpg",
      "/bg-images/fashion-event-5.jpg",
    ],
  };


  // Function to get a random image for the given event
  const getRandomBgImage = (eventName) => {
    const defaultImage = "/bg-images/business-travel-2.jpg"; // Set your default image path
    const images = eventImages[eventName] || [];
    console.log('images', images, eventImages[eventName], eventImages, eventName)
    return images.length > 0 ? images[Math.floor(Math.random() * images.length)] : defaultImage;
  };

  // const MoodboardColumn = ({ event }) => {
  const [randomBgImage, setRandomBgImage] = useState(null);

  useEffect(() => {
    if (event?.event_name) {
      setRandomBgImage(getRandomBgImage(event.event_name));
    }
  }, [event.name]); // Runs when event.name changes

  const handleDragStart = (e, id) => {
    e.dataTransfer.setData("id", id);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const id = e.dataTransfer.getData("id");
    const updatedImages = moodboardImages.map((img) =>
      img.id === id ? { ...img, x: e.clientX, y: e.clientY } : img
    );
    setMoodboardImages(updatedImages);
  };
  const fetchRecommendations = async () => {
    setLoadingRecommendations(true); // Show loading state
    setInlineToastMsg(false);
    setTriggerAPI(true);
    let payload = {
      query: {
        user_id: userDetails.user_id,
        event_id: event.event_id,
        event_name: event.event_name,
        event_date: event.event_date,
        event_description: event.event_description,
        event_location: event.event_location,
        age: userDetails.age,
        gender: userDetails.gender,
        wardrobe_items: userDetails.wardrobe_items,
        moodboard_items: moodboardImageIds.map(Number).filter((n) => !isNaN(n)),
      },
    };
    let attempt = 0;
    let success = false;

    while (attempt < 2 && !success) {
      try {
        attempt++;
        let response = await getMbRecommendation(payload);

        if (!response || !response.response || !response.response.images) {
          throw new Error("Invalid response from API");
        }

        const recommendedImageIds = response.response.images.map(Number);

        // Fetch the image map
        const imgResponse = await fetch("/json files/imgmap.json");
        const imgData = await imgResponse.json();

        // Match the recommended images with imgmap.json
        const matchedImages = imgData.filter((img) =>
          recommendedImageIds.includes(Number(img.id))
        );

        setMbRecommendations(matchedImages);
        success = true;
      } catch (error) {
        console.error(`Attempt ${attempt}: Error fetching recommendations`, error);

        if (attempt === 1 && error.response?.status === 500) {
          console.warn("API is taking longer than expected. Retrying...");
        } else if (attempt === 2) {
          console.error("Failed after retry. Please try again later.");
          setMbRecommendations([]); // Ensure UI updates correctly
          console.error("Error showing recommendations Please try again later.");
          setNotificationKind("error");
          // setInlineToastMsg(true);
          setNotificationTitle("Error showing recommendations Please try again later.")
          setLoadingRecommendations(false);
        }
      }
    }

    setLoadingRecommendations(false);

  };

  const handleSubmit = (e) => {
    let user = userDetails;
    // e.stopPropagation();
    console.log("userDetails", userDetails);
    navigate("/homepage", { state: { user } });
  };

  return (
    <div className="login-page">
         <Row>
        <Column>
          <div className="notification noti">
            {inlineToastMsg && (
              <InlineNotification
                title={notificationTitle}
                // subtitle=""
                kind={notificationKind}
              />
            )}
          </div>
        </Column>
      </Row>
      <Row>
        <Column lg={3} className="login-container">
          <LeftPanel
            editFormFlag={editForm}
            selectedEmail={email}
            userDetails={userDetails}
            setEditFormFlag={handleEditFormChange}
          />
        </Column>
        <Column lg={13} className="moodboard"
        >
          {/* Background layer (only if randomBgImage exists) */}
          {randomBgImage && (
            <div
              style={{
                backgroundImage: `url('${randomBgImage}')`, // Use your image URL
                backgroundSize: "cover",
                backgroundPosition: "center",
                backgroundRepeat: "no-repeat",
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                opacity: 0.5, // Only affects background
                zIndex: 0, // Keeps background behind content
              }}
            />
          )}
          <div style={{ position: "relative", zIndex: 1 }}>
            <div className="title">
              <h3 style={{ fontWeight: 500 }}>Moodboard for {event?.event_name} </h3>
              {/* <Tag type="green">{event?.event_date}</Tag> */}
            </div>

            <div style={{ position: "relative", float: "right", zIndex: 1 }}>
              <Button
                style={{ cursor: "pointer" }}
                kind="ghost"
                onClick={(e) => {
                  handleSubmit(e);
                }}
              >
                {" "}
                Go Back{" "}
              </Button>
            </div>
          </div>
          <div style={{ position: "relative", zIndex: 1 }}>
            Select a category, pick your favorites, and get personalized
            recommendations!
          </div>
          <div style={{ display: 'flex' }}>

            <div style={{ margin: '1rem 0', width: '50%', zIndex: 1 }}>
              <Dropdown id="category" titleText="Select a Category"
                // selectedItem={}
                onChange={(evt) => handleDropdownChange(evt)}
                label="Select a Category"
                // style={{width: '100%', flex: "1 1 auto"}}
                style={{ width: "50%", flex: "0 0 auto" }}
                size="sm"
                items={category}
                itemToString={item => item ? item.category : ''} />
            </div>
            <div style={{ width: '30%', pointerEvents: "none" }}>
              <RadioButtonGroup
                className="gender"
                defaultSelected={gender}
                legendText="Gender"
                name="radio-button-default-group"

                // onChange={handleGenderChange}
                value={gender}
              >
                <RadioButton id="female" labelText="Female" value="female" />
                <RadioButton id="male" labelText="Male" value="male" />
              </RadioButtonGroup>
            </div>
            <div style={{ width: '19%', pointerEvents: "none", margin: "1rem 0px" }}>
              <DatePicker
                datePickerType="single"
                dateFormat="m/d/Y"
              >
                <DatePickerInput
                  placeholder="mm/dd/yyyy"
                  labelText="Date of event"
                  id="date-picker-single"
                  // disabled={true}
                  size="sm"
                  defaultValue={date} // Pass date state to the input field
                />
              </DatePicker>
            </div>
          </div>

          <Row>
            <Column lg={4}>
              <Row className="catalog">
                {catalogByCategory.length > 0 ? (
                  catalogByCategory.map((item) => (
                    <Column className="catalog-col" key={item.id}>
                      <div>
                        <Tile
                          style={{
                            // height: "240px", // Keep consistent height for each tile
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
                              src={`/${item.imgfilepath}`}
                              alt={item.description}
                              style={{
                                width: "100%",
                                height: "180px",
                                objectFit: "cover",
                                display: "block",
                              }}
                            />
                          </div>

                          {/* Description below, left-aligned */}
                          <div style={{ flex: 1, justifyContent: "space-between", textAlign: "left", display: 'flex' }}>
                            <div>
                              <h5 style={{ margin: "0", fontSize: "1rem", overflow: "hidden", textOverflow: "ellipsis" }}>
                                {item.description}
                              </h5>
                            </div>
                            <div
                              className="add-icon"
                              style={{
                                cursor: "pointer",
                                position: "relative",
                              }}
                              onClick={() => handleAddToMoodboard(item)}
                            >
                              <AddAlt size={24} />
                              <span className="tooltip">Add to moodboard</span>
                            </div>
                          </div>
                        </Tile>
                      </div>
                    </Column>
                  ))
                ) : (
                  <>
                    {/* <p>No items found for selected category.</p> */}
                    <Column style={{ paddingRight: 0 }}>
                      <Tile className="bg-tile-event"
                        //  style={{height: '100%'}}
                        style={{ height: mbRecommendations.length > 0 ? '90%' : '100%' }}
                      >
                        <div>
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
                          <h5
                            style={{
                              fontFamily: "cursive",
                              fontSize: "x-large",
                              marginBottom: "1rem",
                              overflowWrap: "break-word", /* Break long words */
                              wordBreak: "break-word", /* Ensure breaking within words */
                              whiteSpace: "normal" /* Allow wrapping */
                            }}
                          >
                            Pick a category to view a catalog
                          </h5>

                        </div>
                      </Tile>
                    </Column>
                  </>
                )}
              </Row>
            </Column>
            <Column lg={12}>
              {/* <h3 style={{ margin: "0 0 1rem 0" }}>Moodboard</h3> */}

              <Tile className="bg-tile-event"
                style={{ height: mbRecommendations.length > 0 ? '100%' : '100%', overflow: 'scroll' }}
              >
                <div className="moodboard-tile" style={{ height: mbRecommendations.length > 0 ? '70%' : '80%' }}>
                  {moodboardImages.length > 0 ? (
                    <>
                      <div className="moodboard-container">
                        {moodboardImages.map((img) => (
                          <div
                            key={img.id}
                            className="moodboard-image-wrapper"
                            style={{
                              width: img.width,
                              height: img.height,
                              top: img.top,
                              left: img.left
                            }}
                          >
                            <img src={`/${img.imgfilepath}`} alt={img.description} className="moodboard-img" />
                            <button className="expand-icon" onClick={() => setSelectedImage(img)} aria-label="Expand Image">
                              <Maximize size={20} />
                            </button>
                          </div>
                        ))}
                      </div>

                    </>
                  ) : (
                    <div className="empty-moodboard">
                      <h4>Mood meets style - design a moodboard that feels like you</h4>
                      <div>
                        <img src={`/moodboardNew1.png`} alt="moodboard icon" style={{
                          width: "50%",
                          height: "50%",
                          objectFit: "cover",
                        }} />
                      </div>
                    </div>
                  )}
                </div>

                {/* Generate Recommendations Button */}
                <div>
                  <Button kind="ghost" className="gen-mb-recommendations" onClick={fetchRecommendations}>
                    {loadingRecommendations ? "Generating..." : "Generate Recommendations"}
                  </Button>
                </div>
                <div>
                  {triggerAPI && !loadingRecommendations && (
                    <>
                      {mbRecommendations.length > 0 ? (
                        <>
                          {/* <h4 style={{ margin: "1rem 0" }}>Recommendations</h4> */}
                          <Tile
                            className="bg-tile-event"
                            decorator={
                              <CustomAILabel name="mistralai/mixtral-8x7b-instruct-v01" />
                            }
                            style={{
                              // maxHeight: "550px", // Limit height to fit two rows
                              overflowY: "auto", // Enable vertical scrolling
                              display: "flex",
                              flexDirection: "column",
                              padding: "1rem",
                            }}
                          >
                            <Row className="moodboard-images">
                              {mbRecommendations.map((img) => (
                                <Column key={img.id} lg={3} md={3} sm={4} style={{ paddingRight: "0rem" }}>
                                  <Tile
                                    style={{
                                      // height: "260px", // Ensure all tiles have the same height
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
                                          height: "160px",
                                          display: "block",
                                          border: "2px solid",
                                          borderImage: "linear-gradient(45deg, #0540c8, #8a3ffc) 1"
                                        }}
                                      />
                                      <button className="add-icon-recomm" onClick={() => handleAddToMoodboard(img)} aria-label="Expand Image">
                                        <Add size={16} />
                                      </button>
                                      <button className="expand-icon" onClick={() => setSelectedImage(img)} aria-label="Expand Image">
                                       
                                        <Maximize size={10} />
                                      </button>
                                    </div>

                                    {/* Description below, left-aligned */}
                                    <div
                                      style={{
                                        flex: 1,
                                        justifyContent: "center",
                                        textAlign: "left",
                                        display: "flex"
                                      }}
                                    >
                                      {/* <h5
                                    style={{
                                      margin: "0rem 0.5rem",
                                      fontSize: "1rem",
                                      whiteSpace: "nowrap",
                                      overflow: "hidden",
                                      textOverflow: "ellipsis",
                                      width: "100%", // Ensures it takes full space
                                    }}
                                  >
                                    {img.description}
                                  </h5> */}
                                    </div>
                                  </Tile>
                                </Column>
                              ))}
                            </Row>
                          </Tile>
                        </>
                      ) : (
                        <Tile
                          className="bg-tile-event"
                          decorator={
                            <CustomAILabel name="mistralai/mixtral-8x7b-instruct-v01" />
                          }
                          style={{
                            // maxHeight: "550px", // Limit height to fit two rows
                            overflowY: "auto", // Enable vertical scrolling
                            display: "flex",
                            flexDirection: "column",
                            padding: "1rem",
                          }}
                        >
                          <p>No recommendations available.</p>
                        </Tile>
                      )}
                    </>
                  )}
                </div>
                {/* Image Expand Modal */}
                {selectedImage && (
                  <Modal
                    open={!!selectedImage}
                    modalHeading={selectedImage.description}
                    passiveModal
                    onRequestClose={() => setSelectedImage(null)}
                  >
                    <img src={`/${selectedImage.imgfilepath}`} alt={selectedImage.description} style={{ width: "100%" }} />
                  </Modal>
                )}
              </Tile>

              {/* <Tile className="bg-tile-event">
                <div className="moodboard-tile">
                  {moodboardImages.length > 0 ? (
                    <Row className="moodboard-images">
                      {moodboardImages.map((img) => (
                        <Column key={img.id} lg={3} md={3} sm={4}>
                          <img
                            src={`/${img.imgfilepath}`}
                            alt={img.description}
                            width="180px"
                            height="200px"
                          />
                        </Column>
                      ))}
                    </Row>
                  ) : (
                    // <p>Add images to get the magic going!</p>
                    <div>
                    <h4 style={{ marginBottom: "1rem", fontStyle: "italic" }}>
                      {" "}
                     Mood meets style- designed a moodboard that feels like you{" "}
                    </h4>
                    <div style={{ padding: "2rem" }}>
                    <img
                            src={`/moodboardNew.png`}
                            alt={'moodboard icon'}
                            width="100"
                            height="100"
                          />
                    </div>
                  </div>
                  )}
                </div>
                <div>
                  <Button
                    kind="ghost"
                    className="gen-mb-recommendations"
                    onClick={fetchRecommendations}
                  >
                    {loadingRecommendations
                      ? "Generating..."
                      : "Generate Recommendations"}
                  </Button>
                </div>
              </Tile> */}

            </Column>
          </Row>
        </Column>
      </Row>
      {loadingRecommendations && (
        <div className="loading-overlay">
          <img src="/agentflow-dark.gif" alt="Loading..." style={{
            width: "80%",
            height: "80%",
            objectFit: "cover",
          }} />

        </div>
      )}
    </div>
  );
};

export default LiveMoodboard;
