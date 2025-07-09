

export const startChatSession = async () => {
    const url = `${import.meta.env.VITE_BACKEND_URL}/api/v1/session/create`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
};

export const askDocument = async (query: string) => {
    const url = `${import.meta.env.VITE_BACKEND_URL}/api/v1/chat/generate`;
    const payload = {
        input_data: query
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
};

export const downloadPdf = async () => {
    const url = `${import.meta.env.VITE_BACKEND_URL}/download/report`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/pdf'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.blob();
    } catch (error) {
        throw error;
    }
};

export const chatOrchestrateChatStream= async (
  query: string,
  threadId: string,
  onChunk: (text: string) => void
): Promise<string> => {
  const payload = {
    model: "watsonx/ibm/granite-3-8b-instruct",
    messages: [
      {
        role: "user",
        content: query
      }
    ],
    stream: false,
  };

  const url = `${import.meta.env.VITE_BACKEND_URL}/get_wx_orch_chat`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "*",
        "X-IBM-THREAD-ID": threadId
      },
      body: JSON.stringify(payload)
    });
    if (!response.ok || !response.body) {
      throw new Error(`HTTP error! Status: ${response?.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let resultText = "";

    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      let lines = buffer.split("\n\n"); // SSE messages are separated by double newlines
      buffer = lines.pop() || ""; // Keep unfinished chunk

      for (const line of lines) {
        const clean = line.trim();

        if (clean === "data: [DONE]") {
          break;
        }

        if (clean.startsWith("data: ")) {
          const jsonStr = clean.replace("data: ", "").trim();
          try {
            const data = JSON.parse(jsonStr);
            const delta = data?.choices?.[0]
            // ?.delta?.content;
            if (data) {
              resultText += delta;
              onChunk(data); // 👈 Your callback for each streamed chunk
            }
          } catch (err) {
            console.error("Invalid JSON in SSE:", jsonStr);
          }
        }
      }
    }

    return resultText;
  } catch (error) {
    console.error("chatOrchestrate error:", error);
    throw error;
  }
};

export const chatOrchestrate = async (
  query: string,
  threadId: string,
  onChunk?: (text: string) => void
): Promise<string> => {

  const payload = {
    model: "watsonx/meta-llama/llama-3-2-90b-vision-instruct",
    messages: [
      {
        role: "user",
        content: query
      }
    ],
    stream: false,
  };

  const url = `${import.meta.env.VITE_BACKEND_URL}/get_wx_orch_chat_stream`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-IBM-THREAD-ID": threadId
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (!response.ok) {
      const errorMessage =
        result?.message || `HTTP error! Status: ${response.status}`;
      
      // Optional: pass it to UI
      if (onChunk) {
        onChunk(`[Error]: ${errorMessage}`);
      }

      // Also throw for upstream handlers
      throw new Error(errorMessage);
    }

    // On success
    if (onChunk) {
      onChunk(result);
    }

    return result;
  } catch (error: any) {
    console.error("chatOrchestrateJSON error:", error);

    // Pass structured error to UI
    if (onChunk) {
      onChunk(`[Error]: ${error?.message}`);
    }

    throw error;
  }
};

export const getThreadMessages = async (threadId: string) => {
    const url = `${import.meta.env.VITE_BACKEND_URL}/get_thread_messages/${threadId}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error fetching thread messages:", error);
        throw error;
    }
};

type StreamCallbacks = {
  onChunk?: (chunk: any) => void;
  onError?: (error: any) => void;
};
export const chatOrchestrateStream= async (
  query: string,
  threadId: string,
  { onChunk, onError }: StreamCallbacks
): Promise<string> => {
  const payload = {
    "message": {
      "role": "user", "content": query

    },
    "additional_properties": {},
    "context": {},
  }

  const url = `${import.meta.env.VITE_BACKEND_URL}/get_wx_orch_stream`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "*",
        "X-IBM-THREAD-ID": threadId
      },
      body: JSON.stringify(payload)
    });

     if (!response.ok || !response.body) {
      const errorText = `HTTP error! Status: ${response.status}`;
      if (onError) onError(errorText);
      throw new Error(errorText);
    }


    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let resultText = "";

    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      let lines = buffer.split("\n\n"); // SSE messages are separated by double newlines
      buffer = lines.pop() || ""; // Keep unfinished chunk

      for (const line of lines) {
        const clean = line.trim();

        if (clean === "data: [DONE]") {
          break;
        }

        if (clean.startsWith("data: ")) {
          const jsonStr = clean.replace("data: ", "").trim();
          try {
            const data = JSON.parse(jsonStr);
            const delta = data?.choices?.[0]
            // ?.delta?.content;
            if (data) {
              resultText += delta;
              // onChunk(data); // 👈 Your callback for each streamed chunk
              onChunk?.(data); // ✅ safe and clean

            }
          } catch (err) {
            console.error("Invalid JSON in SSE:", jsonStr);
          }
        }
      }
    }

    return resultText;
  } catch (error) {
    console.error("chatOrchestrate error:", error);
    throw error;
  }
  
};








