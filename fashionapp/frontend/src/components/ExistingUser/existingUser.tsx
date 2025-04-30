import React, { useState, useEffect } from "react";

import { Row, Column, Button, ClickableTile, Link } from "@carbon/react";
import { ArrowRight, UserAvatar } from '@carbon/icons-react';
import './existingUser.scss'
import { useNavigate } from "react-router-dom";

interface User {
    user_id: number,
    user_fullname: string,
    user_email: string
    user_username: string,
    user_pwd: string
}


const ExistingUserPage = () => {
    const [users, setUsers] = useState<User[]>([]);

    useEffect(() => {
        fetch("/userdata_complete.json")
            .then((response) => response.json())
            .then((data) => {
                console.log("data", data); // Logs data once
                setUsers(data); // Store all users
            })
            .catch((error) => console.error("Error fetching user data:", error));
    }, []); // Empty dependency array ensures it runs only once

    const handleTileClick = (user: User) => {
        navigate("/homepage", { state: { user } }); // Pass user data to homepage
      };

    const navigate = useNavigate();
    return (
        <div className="login-page" style={{  height: 'calc(100vh - 80px)'}}>
            <Row>
                <Column lg={8} style={{ padding: '11rem 11rem 0 11rem' }}>
                    <div className="spacing">
                        {users.length > 0 ? (
                            users.map((user) => (
                                <ClickableTile 
                                className="spacing"
                                key={user.user_id} id={`clickable-tile-${user.user_id}`} href=""
                                
                                onClick={() => { 
                                    handleTileClick(user)
                                    
                                }}>
                                    <div style={{ display: "flex", justifyContent: "center" }}>
                                        <div style={{ marginRight: "1rem" }}>
                                            <UserAvatar size={48} />
                                        </div>
                                        <div style={{ marginTop: "0.1rem" }}>
                                            <div>{user.user_fullname}</div>
                                            <div>{user.user_email}</div>
                                        </div>
                                    </div>
                                </ClickableTile>
                            ))
                        ) : (
                            <p>Loading users...</p>
                        )}
                    </div>
                    <div className="spacing" style={{ display: 'flex', justifyContent: "flex-end" }}>
                        <Link
                            href="#"
                            renderIcon={ArrowRight}
                            onClick={() => {
                                navigate('/createUser')
                              
                            }}
                        >
                            Create User
                        </Link>
                    </div>
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

export default ExistingUserPage;


