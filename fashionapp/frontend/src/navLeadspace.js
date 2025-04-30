import { Dashboard } from '@carbon/icons-react';
import { useNavigate } from "react-router-dom";
import "./css/Header.css";

// import {Header,HeaderMenuButton,HeaderName,HeaderNavigation,HeaderMenuItem,HeaderMenu,HeaderGlobalBar,HeaderGlobalAction} from '@carbon/react';
import {
  Header,
  HeaderContainer,
  HeaderName,
  HeaderMenuButton,
  HeaderGlobalBar,
  HeaderGlobalAction,
  SkipToContent
} from '@carbon/react';

// interface Props {}
const LeadNavigation= (props) => {
  return (

    <HeaderContainer
      render={({ isSideNavExpanded, onClickSideNavExpand }) => (
        <Header className="headercarbon" aria-label="Carbon Tutorial">

          <SkipToContent />
          <HeaderMenuButton
            aria-label="Open menu"
            onClick={onClickSideNavExpand}
            isActive={isSideNavExpanded}
          />
          <HeaderName className="headername" onClick={() => {
                                    // navigate('/dashboard');
                                  }} prefix="">
          <Dashboard className="appicon" size={20}/>
       
          Test
          </HeaderName>
          <HeaderGlobalBar>
        <HeaderGlobalAction
          aria-label="User">
  
        </HeaderGlobalAction>
      </HeaderGlobalBar>
         
         
        </Header>
      )}
    />
  );

};

export default LeadNavigation;



