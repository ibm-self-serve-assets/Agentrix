import axios from "axios";
// console.log('process.env.REACT_APP_BASE_URL', process.env.REACT_APP_BASE_URL);
const http = axios.create({
  baseURL: process.env.REACT_APP_BASE_URL
  // withCredentials: true,
});

export default http;
