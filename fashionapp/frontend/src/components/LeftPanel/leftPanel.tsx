import { useState, useEffect } from "react";
import { FormGroup, Form, TextInput, Link, Dropdown

} from "@carbon/react";
import { ArrowRight, UserAvatar } from '@carbon/icons-react';
import "./leftPanel.scss";
import { CircleLoader } from "react-spinners";
import Footer from "../Footer/Footer";

interface Props {
    editFormFlag: boolean;
    selectedEmail: string;
}

const LeftPanel = ({ editFormFlag, selectedEmail, setEditFormFlag, userDetails }) => {

    const [loading, setLoading] = useState(false);

    useEffect(()=>{
    },[userDetails, setEditFormFlag,])

    const items = [{ id: '1', text: 'Pear' },
    { id: '2', text: 'Oval' },
    { id: '3', text: 'Hourglass' },
    { id: '4', text: 'Petite' }
    ]

    const [formData, setFormData] = useState(userDetails);

    // Filter items based on userDetails.bodyShape
    const filteredBodyShape = Array.isArray(items) ? items.find(item => item.text === formData?.bodyshape) || null : null;



    // Handle TextInput Change
    const handleInputChange = (e) => {
        const { id, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [id]: value
        }));
    };
    // Handle Dropdown Change
    const handleDropdownChange = ({ selectedItem }) => {
        setFormData(prevState => ({
            ...prevState,
            bodyshape: selectedItem.text
        }));
    };


    // Handle Form Submission
    const handleSubmit = (e) => {
        if (userDetails?.flow  === "exiting_user") {
           
          }
          e.preventDefault();
       e?.stopPropagation();
        // navigate('/events')
        setEditFormFlag(true);
    };
    return (

        <div style={{ padding: '2rem', }}>
            <div style={{ textAlign: 'center' }}>
                {userDetails?.user_profileImg ? (
                    <>
                    <img
                    src={`/avatars/${userDetails?.user_profileImg}.png`}
                    alt={userDetails?.user_fullname}
                    style={{ width: '50%', height: '50%' }}
                    />
                    </>
                ) : (
                    <>
                <UserAvatar size={100} /></>
                )}
              
                <div>
                    <h3>{userDetails?.user_username}</h3>
                </div>
                <div style={{ marginTop: '2rem' }}>
                    {/* {!editFormFlag && ( */}
                    <> 
                    <h4> {userDetails?.user_id < 3 ? userDetails?.user_email : selectedEmail}</h4>

                    </>

                     {/* )} */}
                </div>
            </div>
            <div>
                <Form aria-label="user form" onSubmit={handleSubmit} >

                    <FormGroup className="user-form-formatting" legendText="" disabled={(editFormFlag && userDetails?.flow  === "new_user")  || selectedEmail === ""}>

                        <TextInput className="user-form-formatting" id="age" labelText="Age" placeholder="Enter Age" value={formData?.age}
                            onChange={handleInputChange} />
                        <TextInput className="user-form-formatting" id="weight" labelText="Weight (in Kgs)" placeholder="Enter Weight" value={formData?.weight}
                            onChange={handleInputChange} />
                        <TextInput className="user-form-formatting" id="height" labelText="Height (in inches)" placeholder="Enter Height" value={formData?.height}
                            onChange={handleInputChange} />
                        <Dropdown id="bodyShape" titleText="Body Shape"
                           disabled={(editFormFlag && userDetails?.flow  === "new_user")  || selectedEmail === ""}

                            selectedItem={filteredBodyShape}
                            onChange={handleDropdownChange}
                            label="Choose an Body Shape"
                            items={items}
                            itemToString={item => item ? item.text : ''} />

                    </FormGroup>
                    {/* <Button renderIcon={ArrowRight} kind="ghost" iconDescription="Icon Description" hasIconOnly onClick={()=>{}}> Let's Style your life</Button> */}
                    <Link type="submit" className="user-form-formatting" 
                        // disabled={userDetails?.flow  === "exiting_user"}
                        onClick={handleSubmit}
                        style={{ marginLeft: '0.5rem',
                            cursor: userDetails?.flow  === "existing_user" ? "not-allowed" : "pointer",
                            opacity: userDetails?.flow  === "existing_user" ? 0.5 : 1,
                          }}
                        >
                        Elevate Your Everyday Style
                        
                        <span style={{ marginLeft: '0.5rem',
                      
                          }}
                        ><ArrowRight />
                        </span>
                    </Link>
                </Form>
            </div>
            <footer>
                <div >
                    <p style={{ marginBottom: '0.5rem' }}>Powered by <strong>IBM watsonx</strong> © 2025</p>
                    <img src="./ibm-logo-black.png" alt="IBM watsonx Logo" style={{ height: '30px' }} />
                    <br/>
                    <br/>
                    <p style={{ fontSize: '12px' }}>All images have been sourced from Creative Commons</p>
                </div>
            </footer>

            {loading &&
                // <Loading withOverlay={true}></Loading>
                <div className="loading-overlay">
                    <div className="loading-content">
                        <CircleLoader
                            color={'blue'}
                            loading={true}
                            size={50}
                            aria-label="Loading Spinner"
                            data-testid="loader"
                        />
                        <span>Please wait, invoking watsonx.ai…</span>
                    </div>
                </div>
            }
        </div>

    )
}
export default LeftPanel;