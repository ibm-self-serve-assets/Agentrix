import './login.scss';
import { Row, Column, Button } from "@carbon/react";
import { Launch } from '@carbon/icons-react';
import { useNavigate } from "react-router-dom";
import Footer from '../Footer/Footer';

const LoginPage = () => {

    const navigate = useNavigate();
    return (
        <div className="login-page" style={{  textAlign: 'center'}}>

            <Row>
                <Column lg={16} style={{ padding: '13rem 5rem 11.5rem 5rem' }}>
                    <div>
                        <h1 style={{fontWeight: 800}}>AI-Powered Wardrobe — Effortless organization, personalized styling, and smart fashion choices.</h1></div>
                    <div>
                        <div style={{ margin: "2rem 0" }}>
                            <h3 style={{fontWeight: 500}}>Craft your signature style with a smart planner that perfects every outfit combo.</h3>
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
            </Row>
   
        <Footer/>
        
        </div>
    );
};

export default LoginPage;

