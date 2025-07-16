import { useState, useEffect } from "react";
import {
  Column,
  Button,
  Tile,
  Row,
  TextInput,
  IconButton
} from "@carbon/react";
import "./WelcomeCreateUserPage.scss";
import { SendFilled } from '@carbon/icons-react';

const WelcomeCreateUserPage = ({  setEditFormFlag, handleShowEventsChange , emailChange}) => {


  // const [isLoading, setIsLoading] = useState(false);
  // const [inlineToastMsg, setInlineToastMsg] = useState(false);
  // const [notificationTitle, setNotificationTitle] = useState(
  //   "Server is not reachable"
  // );
  // const [notificationKind, setNotificationKind] = useState("info");
  const [clickedStartStyling, setClickedStartStyling] = useState(false);
  // const [editForm, setEditform] = useState(false);
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const imgData = [{
    gender: 'men',

    data: [{ id: 1, src: "/imagerepo/image16.png", name: "Footwear" },
    { id: 2, src: "/imagerepo/image3.png", name: "Apparel" },
    { id: 3, src: "/imagerepo/image29.png", name: "Fragrance & Beauty" },
    { id: 4, src: "/imagerepo/image45.png", name: "Accessories" },]
  }, {
    gender: 'female',
    data: [{ id: 1, src: "/imagerepo/image18.png", name: "Footwear" }, //need to change
    { id: 2, src: "/imagerepo/image11.png", name: "Apparel" },
    { id: 3, src: "/imagerepo/image26.png", name: "Fragrance & Beauty" },
    { id: 4, src: "/imagerepo/image42.png", name: "Accessories" },]
  }

  ]
  const [images] = useState(imgData[1].data)
  
  
  useEffect(() => {
    // Example: Change editFormFlag when some condition is met
    setEditFormFlag(true);
  }, [handleShowEventsChange]); // Runs on mount, modify as per requirement

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };
  

  const handleEmailChange = (event) => {
    const value = event.target.value;
    setEmail(value);

    if (value && !validateEmail(value)) {
      setError("Invalid email format");
    } else {
      setError("");
    }
  };

  return (
    <div style={{marginTop: '1rem'}}>
      {clickedStartStyling ? (
        <>
          <Tile className="bg-tile">
            <h4>Always be ready for any event! Link your calendar by entering your email, and we'll curate your wardrobe to match.</h4>
            <h6 style={{ margin: '1rem 0' }}>📅 No events found—connect now to unlock effortless styling!</h6>
            <div style={{ display: "flex", justifyContent: "center", padding: '0rem', margin: '0 3rem' }}>

              <div>
                <TextInput
                  style={{ width: '400px' }}
                  labelText=""
                  id="email"
                  value={email}
                  onChange={handleEmailChange}
                  placeholder="Enter Email"
                  invalid={!!error}
                  invalidText={error}
                />
              </div>
              <div>
                <IconButton
                  kind="ghost"
                  size="sm"
                  disabled={!email}
                  onClick={() => { 
                    setClickedStartStyling(true); 
                    setEditFormFlag(false); // Update parent state
                    handleShowEventsChange(true) // as soon as revceived email show events
                    emailChange(email);
                   }}
                  className="icon-btn"
                  label="Enter"
                >
                  <SendFilled size={24} />
                </IconButton>
              </div>

            </div>
          </Tile>

        </>
      ) : (
        <Tile className="bg-tile">
          <h2>Wearing the same outfits on repeat and still not feeling your best?</h2>
          <h6 style={{ margin: '1rem 0' }}>Let us get to know your body better—share a few details and we’ll tailor looks that truly fit you. Ready? Click 'Start Styling'</h6>
          <Button kind="secondary" onClick={() => {
            setClickedStartStyling(true);
          }}>Start Styling</Button>
        </Tile>

      )}

      <div style={{marginTop: '1rem'}}>
        <h3 >Trending Now by Category</h3>
        <Row>
          {images.map((image) => (
            <Column key={image.id} lg={8} style={{ margin: '1rem 0 0 0 ' }}>
              <Tile style={{ height: '100%' }}>
                <h3 style={{ textAlign: 'center' }}>{image.name}</h3>
                <div key={image.id} className="text-center">
                  <img src={image.src} alt={image.name}
                    height={190} width={300}
                    // style={{ width: "100%", height: "auto", objectFit: "contain" }} 
                    className="w-32 h-32 border-2 border-gray-300 rounded" />

                </div>
              </Tile>
            </Column>
          ))}

        </Row>
      </div>
    </div>
  );
}

export default WelcomeCreateUserPage;