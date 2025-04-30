import http from "../config/axios";

export const llmEndpoints = {
  LLM:"/api",
};


export const getRecommendation = async (payload): Promise<{}>=> {
  const getDetails = "/getrecommendations"
  const config = {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  };
  console.log("payload -> ", payload)

  try {
    const response = await http.post(getDetails, payload, config);
    // console.log("response", response);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getMbRecommendation = async (payload): Promise<{}>=> {
  const getDetails = "/getmbrecommendations"
  const config = {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  };
  console.log("payload -> ", payload)

  try {
    const response = await http.post(getDetails, payload, config);
    // console.log("response", response);
    return response.data;
  } catch (error) {
    throw error;
  }
};