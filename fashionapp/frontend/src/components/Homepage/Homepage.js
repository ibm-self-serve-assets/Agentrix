import { useState, useEffect, useCallback } from "react";
import {
  Column,
  Row,
} from "@carbon/react";
import "./Homepage.scss";
import LeftPanel from "../LeftPanel/leftPanel";
import WelcomeCreateUserPage from "../WelcomeCreateUserPage/WelcomeCreateUserPage";
import UpcomingEvents from "../UpcomingEvents/UpcomingEvents";
import { useLocation } from "react-router-dom";
import { getRecommendation } from "../../services/llm.service";

const Homepage = () => {
  const location = useLocation();
  const user = location.state?.user; // Get passed user data
 
  const [trigger, setTrigger]  = useState(false); //AIReccomend trigger state
  const [isLoading, setIsLoading] = useState(false);
  // const [inlineToastMsg, setInlineToastMsg] = useState(false);
  // const [notificationTitle, setNotificationTitle] = useState(
  //   "Server is not reachable"
  // );
  // const [notificationKind, setNotificationKind] = useState("info");
  const [editForm, setEditForm] = useState(false);

  const [currentClickedEvt, setCurrentClickedEvt] = useState({});

  const [email, setEmail] = useState("");


  // User details  
  const [userDetails, setUserDetails] = useState(() => {
    // Initialize from location or localStorage
    if (user) {
      return user;
    }
    const savedUser = localStorage.getItem("user");
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [showEvents, setShowEvents] = useState(userDetails?.flow === "existing_user" ? true: false);
  
  // Event details  
  const [eventDetails, setEventDetails] = useState(userDetails?.user_events);

  // Function to update editForm state
  const handleEditFormChange = (newValue) => {
    setEditForm(newValue);
  };
  const handleShowEventsChange = useCallback((newValue) => {
    setShowEvents(newValue);
  }, []);
  

  useEffect(() => {
    // Only save to localStorage once (if passedUser exists)
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    }
  }, [user]);

  useEffect(() => {
    setEventDetails(userDetails?.user_events);
  }, [userDetails, eventDetails, showEvents])

  // const validateEmail = (email) => {
  //   const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  //   return emailRegex.test(email);
  // };

  const emailChange = (value) => {
    setEmail(value);
    // Update the userDetails with the new email value
    setUserDetails((prevDetails) => ({
      ...prevDetails,  // Spread the previous user details
      user_email: value,    // Update only the email field
    }));
  };
  const onClickRecommendation = (id) => {
    console.log("userDets -> ", userDetails)
    let selectedEvent = userDetails.user_events.find((evt) => { return evt.event_id === id })

    let payload = {
      query: {
        user_id: userDetails.user_id,
        event_id: selectedEvent.event_id,
        event_name: selectedEvent.event_name,
        event_date: selectedEvent.event_date,
        event_description: selectedEvent.event_description,
        event_location: selectedEvent.event_location,
        age: userDetails.age,
        gender: userDetails.gender,
        wardrobe_items: userDetails.wardrobe_items,
      
    }}
    fetchRecommendation(payload);
  }


  const fetchRecommendation = async (currentData) => {
    setIsLoading(true);

    try {
      console.log("userDetails -> ",userDetails.user_events)
      console.log("currentData -> ", currentData, currentData.query.event_id)
      let response = await getRecommendation(currentData);
      setIsLoading(false);
      // setTrigger(false);
      //update the userdetails
      console.log("Response: ->", response.response )

      let obj = userDetails.user_events.find(item => item.event_id === currentData.query.event_id)

      // setIsLoadingMsg(false);
      if (response) {
        // setLlmResponse(response?.answer);
        //obj.styling_recc = response.response.styling_recc;
        obj.travel_recc = response.response.travel_recc;
        obj.styling_images = response.response.image_ids;
        console.log("obj -> ", obj)
        setEventDetails(userDetails.user_events);
        setCurrentClickedEvt(obj);
        setIsLoading(false);
      }
      console.log("Text successfully");
    } catch (error) {
      console.error("Error sending text", error);
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Row>
        <Column>
          <div className="notification margin-dashboard">
            {/* {inlineToastMsg && (
              <InlineNotification
                title={notificationTitle}
                // subtitle=""
                kind={notificationKind}
              />
            )} */}
          </div>
        </Column>
      </Row>
      <div className="" style={{background: '', paddingTop: '2rem'}}>
        <Row>
          <Column lg={3} className="login-container" 
          >
            <LeftPanel editFormFlag={editForm} selectedEmail={email} 
              userDetails={userDetails}
              setEditFormFlag={handleEditFormChange} 
              />
          </Column>
          <Column lg={13}>
            {!showEvents ? (
              <WelcomeCreateUserPage
                editFormFlag={editForm}
                setEditFormFlag={handleEditFormChange}
                emailChange={emailChange}
                handleShowEventsChange={handleShowEventsChange}
              ></WelcomeCreateUserPage>
            ) :
              <UpcomingEvents
                user={user}
                userDetails={userDetails}
                setUserDetails={setUserDetails}
                handleShowEventsChange={handleShowEventsChange}
                eventDetails={eventDetails}
                currentEvt={currentClickedEvt}
                setEventRecommendationId={onClickRecommendation}
                wardrobeDetails={userDetails.wardrobe_items}
                isLoading={isLoading}
                setIsLoading={setIsLoading}
                setTrigger={setTrigger}
                trigger={trigger}
              ></UpcomingEvents>
            }

          </Column>
        </Row>
      </div>
    </div>
  );
}

export default Homepage;