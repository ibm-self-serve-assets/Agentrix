import {
  Content,
  Header,
  HeaderName,
  HeaderGlobalAction,
  HeaderGlobalBar,
  Theme,
  Row, Column, SkipToContent,
} from "@carbon/react";
import "./App.scss";
import Homepage from "./components/Homepage/Homepage.js";
import { Provider } from "react-redux";
import { store } from "./store/Store";
import { Search, Notification, Switcher } from "@carbon/icons-react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import ImageGallery from "./components/MoodBoard/imagegallery"
import LiveMoodboard from "./components/MoodBoard/LiveMoodboard";
import LoginPage from "./components/Login/login";
import ExistingUserPage from "./components/ExistingUser/existingUser";
import CreateUserForm from "./components/CreateUserForm/createUserForm";
import UpcomingEvents from "./components/UpcomingEvents/UpcomingEvents";
// import { Column } from "carbon-components-react";
import { useNavigate } from "react-router-dom";
import { UserProfile} from '@carbon/icons-react';

const AppHeader = () => {
  const navigate = useNavigate(); // ✅ Now inside a Router

  return (
    <>
    <Header aria-label="Header for Our Skeleton App">
      <HeaderName style={{cursor: "pointer"}} onClick={() => navigate("/")}>
        &nbsp; Closet Companion
      </HeaderName>
    
    <HeaderGlobalBar >
    <HeaderGlobalAction
      aria-label="Logout"
      onClick={() => navigate("/login")}
    >
      <UserProfile />
    </HeaderGlobalAction>
  </HeaderGlobalBar>
  </Header>
  </>
  );
};

function App() {
  return (
    <BrowserRouter>
      <Theme theme="g100">
        <Provider store={store}>
          <Content>
          <AppHeader /> {/* ✅ Use the new component */}

            <SkipToContent />

            <Routes>
              <Route path="/" element={<LoginPage />} />
              <Route path="/image1" element={<ImageGallery />} />
              {/* <Route path="/moodboard" element={<LiveMoodboard />} /> */}
              <Route path="/login" element={<ExistingUserPage />} />
              <Route path="/createUser" element={<CreateUserForm />} />
              <Route path="/homepage" element={<Homepage />} />
            </Routes>
          </Content>
        </Provider>
      </Theme>
    </BrowserRouter>
  );
}

export default App;
