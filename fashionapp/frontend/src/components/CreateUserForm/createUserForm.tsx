import React, { useState } from "react";

import { Row, Column, Button, ClickableTile, Link , FormGroup, TextInput,
    RadioButtonGroup,
    RadioButton,
    Stack
} from "@carbon/react";
import { ArrowRight, UserAvatar } from '@carbon/icons-react';
import './createUserForm.scss'
import { useNavigate } from "react-router-dom";

const CreateUserForm = () => {

// Handle change for TextInput
const onChangeCred = (value: string, key: string) => {
    setUser((prev) => ({
      ...prev,
      [key]: value, // Update the key dynamically
    }));
  };
 let newUserObj = {
    user_id: Math.random(),
    user_fullname: '',
    user_email: '',
    user_username: '',
    user_pwd: '',
    gender: 'female',
    age: '',
    weight: '',
    height: '',
    bodyshape: '',
    user_events:[ {
            "event_id": 21,
            "event_name": "Work Trip",
            "event_description": "very detailed description from user",
            "event_location": "Paris",
            "event_date": "12 March 2025",
             "bgColor": "#001d6c"
        }],
     wardrobe_items: [51, 47, 22, 11],
     flow: "new_user"
  }
 const onSubmit = () =>{
   console.log('on createuser', user)
        navigate("/homepage", { state: { user } }); // Pass user data to homepage
 }

 const [user, setUser] = useState(newUserObj);

  // Set initial selected value based on credentials
  const [selectedGender, setSelectedGender] = useState(user.gender === "male" ? "male" : "female" );
  // Handle change event
  const handleGenderChange = (newValue: string) => {
    console.log('newValue', newValue)
    setSelectedGender(newValue);

    // Update credentials based on selected value
    setUser((prev) => ({
      ...prev,
      gender: newValue === "male" ? "male" : "female",
      wardrobe_items: newValue === "male"? [1, 4,29, 42] : [51, 47, 22, 11]
    }));
  };

 const navigate = useNavigate();
    return (
        <div className="login-page" style={{  height: 'calc(100vh - 80px)'}}>

            <Row>
                <Column lg={8} style={{ padding: '11rem 11rem 0 11rem' }}>
                    <FormGroup
                        legendId="form-group-1"
                        className="create-form"
                        legendText="Create User Form"
                    >
                        <Stack gap={7}>
                            <TextInput
                                id="one"
                                value={user.user_username}
                                onChange={(event)=>onChangeCred(event?.target.value, 'user_username')}
                                labelText="UserName"
                            />
                            <TextInput
                                id="two"
                                value={user.user_pwd}
                                onChange={(event)=>onChangeCred(event?.target.value, 'user_pwd')}
                                type="password" required pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}"
                                labelText="Password"
                            />
                            <RadioButtonGroup
                                defaultSelected={selectedGender}
                                legendText="Gender"
                                name="formgroup-default-radio-button-group"
                                onChange={(value) => handleGenderChange(String(value))} // Ensure
                            >
                                <RadioButton
                                    id="male"
                                    labelText="Male"
                                    value="male"
                                    onChange={(eve)=>handleGenderChange('male')}
                                />
                                <RadioButton
                                    id="female"
                                    labelText="Female"
                                    value="female"
                                     onChange={()=>handleGenderChange('female')}
                                />
                             
                            </RadioButtonGroup>
                            <div style={{display: 'flex', justifyContent: 'flex-end'}}>
                            <Button kind="tertiary"
                            size="md"
                            style={{marginRight: '1rem'}}
                            onClick={()=>{
                                navigate('/login')
                            }}
                            >
                                Cancel
                            </Button>
                            <Button size="md"
                             onClick={()=>{
                                onSubmit()
                            }}
                            >
                                Submit
                            </Button>
                            </div>
                        </Stack>
                    </FormGroup>

                </Column>
                <Column lg={8} style={{ padding: '11rem 11rem 0 11rem' }}>
                    <img src="/loginpage.jpg" width={400} height={400}></img>
                </Column>
            </Row>
            <footer>
                <div className="footer" style={{ padding: '1rem' }}>
                    <p style={{ marginBottom: '0.5rem' }}>Powered by <strong>IBM watsonx</strong> © 2025</p>
                    <img src="./ibm-logo-black.png" alt="IBM watsonx Logo" style={{ height: '30px', 'margin': '0 10px' }} />
                </div>
            </footer>
        </div>
    );
};

export default CreateUserForm;


