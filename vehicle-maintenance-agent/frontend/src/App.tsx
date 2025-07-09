import './App.scss'
import ChatPage from './pages/ChatPage/ChatPage';
import  { useState } from "react";
import {
  Column,
  Theme,
  // Toggle,
  Header, 
  HeaderGlobalBar,
  // HeaderGlobalAction,
  Row,
  Button,
  HeaderName
} from "@carbon/react";
import {ArrowRight, IbmKnowledgeCatalog} from '@carbon/icons-react';

type AppType = 'Insurance Claim Agent' | 'Supply Chain Agent' | 'Vehicle Maintenance Agent';
function App() {
  const [theme] = useState<"g100" | "g10">("g100"); // ✅ Explicit type

  // const toggleTheme = () => {
  //   setTheme((prevTheme) => (prevTheme === "g100" ? "g10" : "g100"));
  // };


  const appName = import.meta.env.VITE_APP_NAME;
  // Determine background class based on app name
const backgroundClassMap: Record<AppType, string> = {
  'Supply Chain Agent': 'bg-overlay bg-supply',
  'Insurance Claim Agent': 'bg-overlay bg-insurance',
  'Vehicle Maintenance Agent': 'bg-overlay bg-vehicle',
};

const isKnownApp = (name: string): name is AppType =>
  name === 'Supply Chain Agent' || name === 'insurance' || name === 'Vehicle Maintenance Agent';

const backgroundClass = isKnownApp(appName)
  ? backgroundClassMap[appName]
  : 'bg-side';



const renderContent = () => {
  switch (appName) {
    case 'Vehicle Maintenance Agent':
      return (
        <>
          <h1>Your Vehicle.</h1>
          <h1>Your Safety.</h1>
          <h1>Effortlessly Maintained.</h1>
          <h3>
            Predictive diagnostics, service scheduling,<br />
            and real-time insights — tailored for your fleet.<br />
            Experience smarter vehicle maintenance.
          </h3>
        </>
      );
    case 'insurance':
      return (
        <>
          <h1>Your Health.</h1>
          <h1>Your Terms.</h1>
          <h1>Instantly Covered.</h1>
          <h3>
            Smarter recommendations, faster claims,<br />
            and always-on support – tailored just for you.<br />
            Experience health insurance that truly<br />
            understands you.
          </h3>
        </>
      );
    case 'Supply Chain Agent':
      return (
        <>
          <h1>Your Supply Chain.</h1>
          <h1>Your Control.</h1>
          <h1>Instantly Optimized.</h1>
          <h3>
            Smarter planning, real-time insights,<br />
            and end-to-end visibility – customized<br />
            for your operations.<br />
            Experience a supply chain that truly<br />
            understands your business.
          </h3>
        </>
      );
    default:
      return <h1>Welcome to Our App</h1>;
  }
};




  return (
    <>
      <Theme theme={theme}>
         <Header aria-label="Header for Our Skeleton App">
      <HeaderName style={{ color: "white", cursor: "pointer" }} onClick={() => {}}>
        &nbsp;{import.meta.env.VITE_APP_NAME}
      </HeaderName>
      
      <HeaderGlobalBar>
            <div style={{ padding: "0.5rem" }}>
          {/* <Toggle
          id="theme-toggle"
          labelA="Light"
          labelB="Dark"
          toggled={theme === "g100"} // Dark mode is 'g100'
          onToggle={toggleTheme}
        /> */}
        </div>
      </HeaderGlobalBar>
    </Header>
      
      <div>
        <Row>
           <Column sm={4} md={8} lg={8}>
              <div className="bg-column-wrapper" style={{paddingRight: 0}}>
                <div className={backgroundClass}></div>
                <div className="bg-content">
                  {renderContent()}
                  <div style={{marginTop: '2rem'}}>
                    <div className="cds--layout">
                      <div className="cds--btn-set">
                        <Button kind="secondary"
                        renderIcon={IbmKnowledgeCatalog}>Get Your Quote</Button>
                        <Button kind="primary" renderIcon={ArrowRight}>Explore Plans</Button>
                        </div>
                        </div>
                  </div>
                </div>
              </div>
            </Column>
           <Column sm={4} md={8} lg={8} style={{paddingLeft: 0}}>
            <ChatPage /></Column>
        </Row>
     
      </div>
   
      {/* <footer><div className="footer">This app is built using the watsonx.ai SDK and may include systems and methods pending patent with the USPTO, protected under US Patent Laws. © Copyright IBM Corporation</div></footer> */}
      </Theme>
    </>
  )
}

export default App
