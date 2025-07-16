
import {
    SideNav, SideNavItems, SideNavLink,
  } from "@carbon/react";
  import {

    Watson
  } from "@carbon/icons-react";
  
  function Navigation() {
     return (<>
      <SideNav aria-label="Side navigation" isRail style={{background: '#ccccc', borderRight: '1px solid var(--cds-border-subtle-01, #c6c6c6)'}} isFixedNav expanded={true} isChildOfHeader={false}>
        <SideNavItems>
          <SideNavLink
            renderIcon={Watson}
            href="/">
              Closet Companion
          </SideNavLink>
          
        </SideNavItems>
        <div className="footer">
           <p style={{marginBottom: '0.5rem'}}>Powered by <strong>IBM watsonx</strong> © 2025 </p>           
           <img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/IBM_watsonx_logo.svg" alt="IBM watsonx Logo" style={{height: '15px', 'margin': '0 10px'}}/>
         </div>
      </SideNav>;
    </>
    );
    
  }
  
  export default Navigation;