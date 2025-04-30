
import {
    SideNav, SideNavItems, SideNavLink, HeaderName, Header, SkipToContent
  } from "@carbon/react";
  import {
    Fork,
    Chat,
    Watson
  } from "@carbon/icons-react";
// import { background } from "@carbon/themes";
  
  function Navigation() {
     return (<>
         {/* <Header aria-label="IBM Platform Name">
      <SkipToContent />
      <HeaderName href="#" prefix="IBM">
        [Platform]
      </HeaderName>
      </Header> */}
      <SideNav aria-label="Side navigation" isRail style={{background: '#ccccc', borderRight: '1px solid var(--cds-border-subtle-01, #c6c6c6)'}} isFixedNav expanded={true} isChildOfHeader={false}>
        <SideNavItems>
          <SideNavLink
            renderIcon={Watson}
            href="/">
              Wardrobe Planner
          </SideNavLink>
          
        </SideNavItems>
        <div className="footer" style={{padding: '1rem'}}>
           <p style={{marginBottom: '0.5rem'}}>Powered by <strong>IBM watsonx</strong> © 2025 </p>           
           <img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/IBM_watsonx_logo.svg" alt="IBM watsonx Logo" style={{height: '15px', 'margin': '0 10px'}}/>
         </div>
      </SideNav>;
    </>
    );
    
  }
  
  export default Navigation;