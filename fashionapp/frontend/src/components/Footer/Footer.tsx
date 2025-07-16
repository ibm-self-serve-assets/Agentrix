import React from "react";
import "./Footer.scss";

const Footer = () => {
  return (
    <>
    <div style={{marginTop: '0rem', textAlign: 'center'}}>
    <img src="./ibm-logo-black.png" alt="IBM watsonx Logo" style={{ height: '30px', 'margin': '0 10px',  }} />
            <br/>
            <p style={{ fontSize: '12px' }}>All images have been sourced from Creative Commons</p>
        
    </div>
        <div className="footer">
            <p style={{ marginBottom: '0.5rem' }}>Powered by <strong>IBM watsonx</strong> © 2025</p>
      </div>
      </>
  );
};

export default Footer;
