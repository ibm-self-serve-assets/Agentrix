import { useState, useEffect } from "react";

import { Row, Column, ClickableTile, Link } from "@carbon/react";
import { ArrowRight, UserAvatar } from '@carbon/icons-react';
import './existingUser.scss'
import { useNavigate } from "react-router-dom";
import Footer from "../Footer/Footer";

interface User {
    user_id: number,
    user_fullname: string,
    user_email: string
    user_username: string,
    user_pwd: string,
    user_profileImg: string
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
      localStorage.setItem("user", JSON.stringify(user)); // Backup
      navigate("/homepage", { state: { user } });
    };
    

    const navigate = useNavigate();
    return (
        <div className="login-page">
            <Row>
            {users.length > 0 && (
  <>
    {users.map((user) => (
      <Column key={user.user_id} lg={4} style={{ padding: '13rem 5rem 11.5rem ' }}>
        <ClickableTile
          className="spacing"
          id={`clickable-tile-${user.user_id}`}
          href=""
          style={{ textAlign: 'center', height: '210px'}}
          onClick={() => handleTileClick(user)}
        >
          <div 
        //   style={{ display: "flex", justifyContent: "center" }}
          >
            <div style={{ marginRight: "1rem" }}>
              {user.user_profileImg && (
                <img
                  src={`/avatars/${user.user_profileImg}.png`}
                  alt={user.user_fullname}
                  style={{ width: '60%', height: '60%' }}
                />
              )}
            </div>
            <div style={{ marginTop: "0.1rem" }}>
              <div>{user.user_fullname}</div>
              <div>{user.user_email}</div>
            </div>
          </div>
        </ClickableTile>
      </Column>
    ))}
      <Column  lg={4} style={{ padding: '13rem 5rem 11.5rem' }}>
      <ClickableTile
          className="spacing"
          id={`create-user`}
          href=""
          style={{ textAlign: 'center', height: '210px'}}
          onClick={() => navigate('/createUser')}
        >
            <div style={{ marginRight: "1rem" }}>
              <UserAvatar
               style={{ width: '60%', height: '60%' }}/>
            </div>
            <div style={{ marginTop: "0.1rem" }}>
            
            <Link
              href="#"
              renderIcon={ArrowRight}
              onClick={() => navigate('/createUser')}
            >
              Create User
            </Link>
             
            </div>
     
        </ClickableTile>
      </Column>
 
    {/* <div className="spacing" 
    style={{ display: 'flex', justifyContent: "flex-end" }}
    >
    
    </div> */}
  </>
)}

            {/* // ) : (
            //     <p>Loading users...</p>
            // )   } */}
                {/* <Column lg={8} style={{ padding: '11rem 11rem 0 11rem' }}>
                    <img src="/loginpage.jpg"  alt="Login Page" width={400} height={400}/>
                </Column> */}
            </Row>
            <Footer/>
        </div>
    );
};

export default ExistingUserPage;


