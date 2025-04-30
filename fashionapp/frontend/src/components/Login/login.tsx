import React, { useState } from "react";
import './login.scss';
import { Row, Column, Button } from "@carbon/react";
import { Launch } from '@carbon/icons-react';
import { useNavigate } from "react-router-dom";

const LoginPage = () => {

    const navigate = useNavigate();
    return (
        <div className="login-page" style={{  height: 'calc(100vh - 80px)'}}>

            <Row>
                <Column lg={8} style={{ padding: '11rem 5rem 0 5rem' }}>
                    <div>
                        <h2>Intelligent AI styling—effortlessly curate, organize, and refine your wardrobe with ease.</h2></div>
                    <div>
                        <div style={{ margin: "2rem 0" }}>
                            <h4>Design and personalize your ideal wardrobe using our planner to discover the perfect outfit pairings for any occasion.</h4>
                        </div>
                        <div>
                            <Button
                                kind="primary"
                                renderIcon={Launch}
                                onClick={() => {
                                    navigate('/login');
                                }}
                            >Login</Button>
                        </div>
                        <div style={{ margin: "1rem 0", display: 'flex' }}>
                            <div>
                                {/* <img src="/5-starts.png" style={{marginTop: '-2rem'}}
                                    width={120} height={80}
                                ></img> */}
                            </div>
                            </div>
                    </div>
                </Column>
                <Column lg={8} style={{ padding: '11rem 5rem 0 5rem' }}>
                    <img src="/loginpage.jpg" width={400} height={400}></img>
                </Column>
            </Row>
     <Row>
        <Column>
        <footer>
                <div className="footer" style={{ padding: '2rem' }}>
                    <p style={{ marginBottom: '0.5rem' }}>Powered by <strong>IBM watsonx</strong> © 2025</p>
                    <img src="./ibm-logo-black.png" alt="IBM watsonx Logo" style={{ height: '30px', 'margin': '0 10px' }} />
                </div>
            </footer>
        </Column>
     </Row>
        </div>
    );
};

export default LoginPage;

